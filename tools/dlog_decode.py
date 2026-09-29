#!/usr/bin/env python3
"""Decode a Daikin D-Checker phone recording (.tgz / folder with datalabel.txt + .log) into the
same CSV the PC D-Checker app exports. Mirrors the decoder inside the web app (template.html).

Verified byte-for-byte against PC exports of two recordings:
  * FIT DZ6VS (INV_Unitary_*.txt label file)      — types 105/107/151/152/161/164/211/217/313/203/215/30x/310/311/314/801
  * 3-head mini split (Multi_Split.txt label file) — types 151/152/155/161/162/163/165/200-210
Known PC-app quirks that this decoder does NOT copy: a whole-degree Celsius reading prints as e.g. "60"
instead of "60.8" °F; the PC drops an occasional record; timestamps lose their seconds.

usage: python dlog_decode.py <recording.tgz | folder> [out.csv]
"""
import sys, os, io, csv, struct, tarfile, gzip

PSI_PER_KGF = 14.223           # the PC app's kgf/cm² → psi factor (verified: 0 of 404 cells differ)
OPMODE = {0: 'Stop', 1: 'Heating', 2: 'Cooling', 3: 'Fan', 4: 'Dry'}   # 1 confirmed (FIT heating), 2 confirmed (multi cooling)
OPMODE_FW = {0: 'Cooling', 1: 'Heating'}

def f1(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s

def parse_labels(text):
    """One entry per datalabel.txt line (None for comments / short lines). Multi-split files repeat the
    indoor-unit block once per head on the same group id; repeat k reads copy k of that group."""
    rows, seen = [], {}
    for i, line in enumerate(text.lstrip('﻿').splitlines()):
        f = line.split(',')
        if line.startswith('#') or len(f) < 17:
            rows.append(None); continue
        key = (f[0], f[1], f[2], f[3], f[9]); inst = seen.get(key, 0); seen[key] = inst + 1
        rows.append({'n': i + 1, 'grp': int(f[0], 16), 'off': int(f[1]), 'size': int(f[2]), 'type': int(f[3]),
                     'fmt': f[4], 'ucls': f[5], 'vis': f[6] == '1', 'label': f[9], 'kind': int(f[16]),
                     'plot': int(f[18]) if len(f) > 18 and f[18] != '' else 0, 'inst': inst})
    return rows

def split_records(raw):
    """48-byte header, then records: 14-char timestamp + groups [id][00][len][data…] ended by FF FF.
    Groups that repeat within a record (one per indoor head) are kept as a list in order."""
    pos, recs = 48, []
    while pos + 14 <= len(raw):
        ts = raw[pos:pos + 14].decode('ascii', 'replace'); pos += 14
        groups = {}
        while pos + 2 <= len(raw):
            if raw[pos] == 0xFF and raw[pos + 1] == 0xFF:
                pos += 2; break
            gid, ln = raw[pos], raw[pos + 2]; pos += 3
            groups.setdefault(gid, []).append(raw[pos:pos + ln]); pos += ln
        recs.append((ts, groups))
    return recs

def unit_suffix(l):
    k = l['kind']
    return '(F)' if k == 1 or (k == 3 and (l['plot'] or 'Delta-D' in l['label'])) else '(psi)' if k == 2 else ''

def decode_value(lbl, gl):
    o, t = lbl['off'], lbl['type']
    g = gl[lbl.get('inst', 0)] if gl and lbl.get('inst', 0) < len(gl) else None
    if g is None or len(g) < o + lbl['size']: return '---'
    if t in (105, 107):                                   # int16 ×0.1 (°C / kgf/cm² / Δ°C); 0x8000 = no value
        v = struct.unpack_from('<h', g, o)[0]
        if v == -32768: return '---'
        v /= 10.0
        k = lbl['kind']
        if k == 1: v = v * 1.8 + 32
        elif k == 3: v = v * 1.8
        elif k == 2: v = v * PSI_PER_KGF
        return f1(v)
    if t == 151: return str(struct.unpack_from('<H', g, o)[0])
    if t == 152 and lbl['kind'] == 3: return str(round(g[o] * 1.8))      # multi ΔD: °C steps → °F
    if t in (152, 220): return str(g[o])
    if t == 211: return 'OFF' if g[o] == 0 else str(g[o])
    if t == 161:                                          # FIT demand % (÷2); multi half-degree °C setpoint / discharge / fin
        c = g[o] / 2
        return f1(c * 1.8 + 32 if lbl['kind'] == 1 else c)
    if t == 164: return str(g[o] * 5)
    if t == 217: return OPMODE.get(g[o], f'Mode {g[o]}')
    if t == 313: return OPMODE.get(g[o] >> 4, f'Mode {g[o] >> 4}')
    if t == 203: return 'Normal' if g[o] == 0 else f'Error {g[o]}'
    if t == 215: return f'{g[o]:02X}'
    if 300 <= t <= 307: return 'ON' if (g[o] >> (t - 300)) & 1 else 'OFF'
    if t == 310: return str(g[o] >> 4)
    if t == 311: return str(g[o] & 0x0F)
    if t == 314: return f'{struct.unpack_from("<H", g, o)[0]:04X}'
    if t == 801: return 'R410A'
    # ---- multi-split (Multi_Split.txt) types ----
    if t == 155: return f1(struct.unpack_from('<H', g, o)[0] / 10)          # volts ×0.1
    if t == 162:                                                            # half-degree °C, offset 64; 0 = no value
        if g[o] == 0: return '---'
        c = (g[o] - 64) / 2
        return f1(c * 1.8 + 32 if lbl['kind'] == 1 else c)
    if t == 163:                                                            # amps in quarter steps
        v = g[o] * 0.25
        return str(int(v)) if v == int(v) else str(v)
    if t == 165:
        v = struct.unpack_from('<H', g, o)[0]; return '0' if v == 0x8000 else str(v)
    if t == 200: return 'ON' if g[o] else 'OFF'
    if t in (201, 202): return OPMODE.get(g[o], f'Mode {g[o]}')
    if t == 204: return str(g[o])
    if t == 205: return OPMODE_FW.get(g[o], f'Mode {g[o]}')
    if t == 206: return ('Auto ' if g[o] & 0x80 else '') + f'tap {g[o] & 0x7f}'
    if t == 207: return f'P{g[o]}'
    if t == 208: return str(g[o])
    if t == 209: return 'Auto' if g[o] == 0 else f'Level {g[o]}'
    if t == 210: return 'Normal' if g[o] == 1 else f'Error {g[o]}'
    return '?'

def to_csv(labels, recs):
    cols = [l for l in labels if l and l['vis'] and l['type'] not in (995, 998)]
    out = io.StringIO(); w = csv.writer(out, lineterminator='\n')
    w.writerow(['DateTime'] + [f"{l['n']}:{l['label']}{unit_suffix(l)}" for l in cols])
    for ts, groups in recs:
        stamp = f"{int(ts[4:6])}/{int(ts[6:8])}/{ts[:4]} {int(ts[8:10])}:{ts[10:12]}:{ts[12:14]}"
        w.writerow([stamp] + [decode_value(l, groups.get(l['grp'])) for l in cols])
    return out.getvalue()

def load_any(path):
    """Return (labels_text, log_bytes) from a .tgz/.tar/.gz or a folder."""
    if os.path.isdir(path):
        lab = open(os.path.join(path, 'datalabel.txt'), 'rb').read()
        logs = [f for f in os.listdir(path) if f.lower().endswith('.log')]
        return lab.decode('utf-8', 'replace'), open(os.path.join(path, logs[0]), 'rb').read()
    data = open(path, 'rb').read()
    if data[:2] == b'\x1f\x8b': data = gzip.decompress(data)
    t = tarfile.open(fileobj=io.BytesIO(data)); names = t.getnames()
    lab = [t.extractfile(n).read() for n in names if n.lower().endswith('datalabel.txt')][0]
    log = [t.extractfile(n).read() for n in names if n.lower().endswith('.log')][0]
    return lab.decode('utf-8', 'replace'), log

if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    lab, log = load_any(sys.argv[1])
    text = to_csv(parse_labels(lab), split_records(log))
    if len(sys.argv) > 2: open(sys.argv[2], 'w', encoding='utf-8-sig', newline='').write(text); print('wrote', sys.argv[2])
    else: sys.stdout.write(text)
