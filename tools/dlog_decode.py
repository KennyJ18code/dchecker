"""Decode a D-Checker mobile recording (.tgz or the .log + datalabel.txt inside it) to the same CSV the PC app exports.

Record format (reverse-engineered from a Daikin FIT log, 2026-09-25):
  file header : start 'YYYYMMDDHHMMSS' + end 'YYYYMMDDHHMMSS' + 20 bytes
  record      : 'YYYYMMDDHHMMSS' then TLV groups [group id][0x00][length] data..., terminated by 0xFF 0xFF
  groups      : 0x00 config, 0x10 status, 0x20 temps/pressures, 0x21 currents, 0x30 actuators, 0x50 indoor unit (repeats per IDU)
  datalabel   : group, offset, size, type, format, unit class, visible, ..., label, ..., kind (index 16: 1 temp, 2 pressure, 3 delta-T)
  types       : 105/107 int16 LE x0.1 (0x8000 = no data) | 151 uint16 | 152/220 uint8 | 161 uint8/2 (%) | 164 uint8x5 (rpm)
                211 fan step | 217 op mode enum | 313 IDU mode enum | 203 error type | 215 error code hex | 30x bit x | 310/311 nibbles
"""
import sys, io, tarfile, struct, csv

OPMODE = {0: 'Stop', 1: 'Heating', 2: 'Cooling', 3: 'Fan', 4: 'Dry'}          # 1 confirmed; others provisional
# IDU byte 2: upper nibble = mode (same enum as op mode), bit3 = thermo on, bit2 = freeze protection
PSI_PER_KGF = 14.2233

def parse_labels(text):
    rows = []
    for i, line in enumerate(text.lstrip('﻿').splitlines()):
        f = line.split(',')
        if line.startswith('#') or len(f) < 17:
            rows.append(None); continue
        rows.append({'n': i + 1, 'grp': int(f[0], 16), 'off': int(f[1]), 'size': int(f[2]), 'type': int(f[3]),
                     'fmt': f[4], 'ucls': f[5], 'vis': f[6] == '1', 'label': f[9], 'kind': int(f[16]), 'plot': int(f[18]) if len(f) > 18 and f[18] not in ('', ) else 0})
    return rows

def split_records(raw):
    hdr = 28 + 20
    pos = hdr; recs = []
    while pos + 14 <= len(raw):
        ts = raw[pos:pos + 14].decode('ascii', 'replace'); pos += 14
        groups = {}
        while pos + 2 <= len(raw):
            if raw[pos] == 0xFF and raw[pos + 1] == 0xFF:
                pos += 2; break
            gid, ln = raw[pos], raw[pos + 2]; pos += 3
            groups[gid] = raw[pos:pos + ln]; pos += ln
        recs.append((ts, groups))
    return recs

def unit_suffix(l):
    k = l['kind']
    return '(F)' if k == 1 or (k == 3 and l['plot']) else '(psi)' if k == 2 else ''

def decode_value(lbl, g):
    o, t = lbl['off'], lbl['type']
    if g is None: return '---'
    if t in (105, 107):
        v = struct.unpack_from('<h', g, o)[0]
        if v == -32768: return '---'
        v /= 10.0
        k = lbl['kind']
        if k == 1: v = v * 1.8 + 32
        elif k == 3: v = v * 1.8
        elif k == 2: v = v * PSI_PER_KGF
        s = f'{v:.1f}'
        return s[:-2] if s.endswith('.0') else s
    if t == 151: return str(struct.unpack_from('<H', g, o)[0])
    if t in (152, 220): return str(g[o])
    if t == 211: return 'OFF' if g[o] == 0 else str(g[o])
    if t == 161: return str(g[o] / 2).rstrip('0').rstrip('.')
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
    return '?'

def to_csv(labels, recs):
    cols = [l for l in labels if l and l['vis'] and l['type'] not in (995, 998)]
    head = ['DateTime'] + [f"{l['n']}:{l['label']}{unit_suffix(l)}" for l in cols]
    out = [head]
    for ts, groups in recs:
        stamp = f"{int(ts[4:6])}/{int(ts[6:8])}/{ts[0:4]} {int(ts[8:10])}:{ts[10:12]}:{ts[12:14]}"
        out.append([stamp] + [decode_value(l, groups.get(l['grp'])) for l in cols])
    return out

def load_any(path):
    if path.endswith(('.tgz', '.tar.gz')):
        tf = tarfile.open(path, 'r:gz'); labels = log = None
        for m in tf.getmembers():
            if m.name.endswith('datalabel.txt'): labels = tf.extractfile(m).read().decode('utf-8')
            elif m.name.endswith('.log'): log = tf.extractfile(m).read()
        return labels, log
    import os
    d = os.path.dirname(path)
    return open(os.path.join(d, 'datalabel.txt'), encoding='utf-8-sig').read(), open(path, 'rb').read()

if __name__ == '__main__':
    labels, log = load_any(sys.argv[1])
    rows = to_csv(parse_labels(labels), split_records(log))
    w = csv.writer(sys.stdout, lineterminator='\n'); w.writerows(rows)
