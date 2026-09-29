# How the app decodes a phone recording (.tgz), and how it compares to the PC app's CSV

Worked on the shop recording `samples/shop-fit-test.tgz` (Daikin FIT DZ6VS, 11/26/2025) against the
PC app's export of the same recording, `sample.csv`. The phone app does not encrypt anything; the
archive is plain gzip + tar with a binary log inside. The app reads it in the browser, no PC step.

## 1. Unpack

```
shop-fit-test.tgz  (gzip)  →  tar
  customer.txt                       (REC only),Shop FIT test,,Andy Burch,,,,Kenny J,Brackett Heating and Air,,2025-11-26 11:42:16,
  20251126090117/header.txt          20251126090117,(REC only),INV_Unitary_DZ6VS.txt,@,30,1,1,4,…
  20251126090117/datalabel.txt       129 lines — one per data item (group, offset, size, type, label…)
  20251126090117/20251126090335.log  18 778 bytes — the recording
  20251126090117/graph.txt, mapping.txt   (display settings, ignored)
```

`header.txt` field 3 names the model file, which is where the app gets the unit type
(`INV_Unitary_DZ6VS` → DZ = heat pump). Field 5 is the sample interval, 30 s.

## 2. The label file tells the app where every value lives

Each line of `datalabel.txt`: `group, offset, size, type, format, …, visible, …, label, …, kind, …`.
The column number in the CSV is simply the line number. Examples:

```
L12:  0x10, 0, 1, 217, … Op mode                 → group 0x10, byte 0, enum
L13:  0x10, 1, 1, 307, … Therm. on/off           → group 0x10, byte 1, bit 7
L38:  0x10, 5, 1, 215, … Error code              → group 0x10, byte 5, hex
L61:  0x20, 12, 2, 105, … High pressure (kind 2) → group 0x20, bytes 12–13, int16 ×0.1 kgf/cm²
L80:  0x30, 4, 1, 307, … 4way vlv                → group 0x30, byte 4, bit 7
L113: 0x50, 2, 1, 313, … Indoor operation mode   → group 0x50, byte 2, upper nibble
```

Lines whose visible flag is 0, and types 995/998, are not exported. That leaves 62 columns plus DateTime,
the same 63 the PC app writes.

## 3. The log: a 48-byte header, then one record per sample

```
header: "20251126090335" "20251126113305" + 20 bytes   (start / end timestamps)
record: 14-char timestamp, then groups of  [id][00][len][data…], ended by FF FF
```

First record, raw:

```
ts 20251126102435
  group 0x00 len 10: 09 01 00 01 01 01 00 01 04 01          config
  group 0x10 len 16: 01 a0 00 00 00 00 00 80 00 00 00 00 00 00 c8 00   status / controls
  group 0x20 len 23: c8 00 ba 00 ff 01 e6 00 ad 00 18 01 ad 00 64 00 18 01 63 00 32 00 01   temps / pressures
  group 0x21 len 17: 18 00 17 00 1d 01 00 00 00 00 1e 00 06 00 00 00 00   currents
  group 0x30 len 12: 1c 08 25 00 80 00 00 c0 1c 9e 3f 00    actuators
  group 0x50 len 25: 80 00 18 00 00 00 00 00 00 00 00 13 01 d9 01 e0 01 00 00 00 00 ad 00 00 80   indoor unit
  FF FF
```

## 4. Decoding rules, by type

| type | bytes | rule | example from record 1 |
|---|---|---|---|
| 105 / 107 | int16 LE | ×0.1; 0x8000 = `---`. kind 1: °C→°F; kind 3: Δ°C→Δ°F; kind 2: kgf/cm² × **14.223** → psi | `c8 00` = 200 → 20.0 °C → **68** °F (Outdoor air) |
| 151 | uint16 LE | as is | `25 00` → **37** pls (EV) |
| 152 / 220 | uint8 | as is | `1c` → **28** rps (Comp) |
| 161 | uint8 | ÷2 | `c8` → **100** % (Demand) |
| 164 | uint8 | ×5 | `3f` → **315** rpm (OU fan) |
| 211 | uint8 | 0 → `OFF`, else the step | `08` → **8** (Fan step) |
| 217 | uint8 | 0 Stop, 1 Heating, 2 Cooling, 3 Fan, 4 Dry | `01` → **Heating** (Op mode) |
| 313 | uint8 | upper nibble, same enum | `18` → 1 → **Heating** (Indoor mode) |
| 203 | uint8 | 0 → `Normal`, else `Error n` | `00` → **Normal** (Error type) |
| 215 | uint8 | two hex digits | `00` → **00** (Error code) |
| 300–307 | bit (type − 300) | `ON` / `OFF` | `a0` = 1010 0000: bit7 Therm **ON**, bit6 Restart standby **OFF**, bit5 Startup ctrl **ON**, bit4 Defrost **OFF** … |
| 310 / 311 | nibble | upper / lower | retry counters |
| 314 | uint16 | four hex digits | IDU model code |
| 801 | – | constant `R410A` | Refrigerant type |

Whole-degree values print without a decimal (`68`, not `68.0`), exactly as the PC app prints them.
A group that is missing from a record (communication dropout) makes every column in it `---`.

## 5. The record becomes a CSV row, identical to the PC app's row

```
app: 11/26/2025 10:24:35,R410A,Heating,ON,OFF,ON,OFF,OFF,OFF,OFF,OFF,Normal,00,OFF,0,OFF,0,OFF,0,OFF,0,OFF,0,OFF,0,100,68,65.5,124,…
PC : 11/26/2025 10:24   ,R410A,Heating,ON,OFF,ON,OFF,OFF,OFF,OFF,OFF,Normal,00,OFF,0,OFF,0,OFF,0,OFF,0,OFF,0,OFF,0,100,68,65.5,124,…
```

From here on a phone recording and an uploaded PC CSV are the same thing: the app hands the CSV text
to the same parser, so every status, control and error column is read, evaluated and drawn by one
code path. The only difference is that the app keeps the seconds in the timestamp; the PC app drops them.

## 6. Full comparison, all 137 rows × 62 columns (2026-09-28, app v37)

Method: decode the .tgz in the app, pair each row with the PC CSV row for the same minute, compare
every cell as text.

| columns | result |
|---|---|
| 25 status / control / error columns (Op mode, Therm, Restart standby, Startup ctrl, Defrost, Oil return, Demand signal, Low noise, Freeze protection, Error type, Error code ×2, the drop-control and retry counters, Retry code, Fan step, 4-way, SV, Comp/Fan op command, Indoor mode, Refrigerant) | **identical in every row** |
| 3 pressure columns | identical after switching the psi factor to 14.223, the value the PC app uses (0 of 404 cells differ; 14.2233 differed in 22 by 0.1 psi) |
| temperatures | identical, except the PC app's known bug: a whole-°C reading such as 16.0 °C prints as `60` instead of `60.8` °F (8 cells in Suction temp). The app prints the correct value. |
| OU fan rpm | one cell: 10:44:05 the log holds 158 → 790 rpm, the PC row says 785 (a partial record; the PC app appears to have re-read that byte). |
| row count | the PC app dropped the 11:00:05 record; the app keeps it (138 rows vs 137). |

Eight records are missing one or more groups (10:28:35, 10:37:35 … 10:44:05); both the app and the PC
app print `---` for those cells.

To re-run the check: open the app with the test server, load the .tgz through `window.dchkOpen`, read
`window.dchkCsv()` and diff against `sample.csv`. The Python twin of the decoder is `tools/dlog_decode.py`.

## 7. Multi-split recordings use a different type set (verified 2026-09-28, app v44)

`header.txt` names `Multi_Split.txt` instead of `INV_Unitary_<model>.txt`, the label file has 292 lines, and the
record carries **one copy of groups 0x41/0x42 per indoor head** (three copies on a 3-head system). The label file
repeats the indoor block once per head on the same group id, so repeat k reads copy k. Column numbering matches the
PC export (outdoor 1–95, head k at 97 + 28·k).

| type | bytes | rule | example |
|---|---|---|---|
| 151 | uint16 | as is | port EV pulses, fan rpm |
| 152 | uint8 | as is; kind 3 (ΔD) = °C steps → `round(v × 1.8)` °F | `04` → **7** |
| 155 | uint16 | ÷10 | `df07` → **201.5** V |
| 161 | uint8 | ÷2 = °C → °F (kind 1) | `2c` → **71.6** (setpoint) |
| 162 | uint8 | 0 = `---`; (v − 64) ÷ 2 = °C → °F | `54` → **50** (coil) |
| 163 | uint8 | × 0.25 A | `09` → **2.25** |
| 165 | uint16 | timers; 0x8000 → `0` | |
| 200 | uint8 | `ON` / `OFF` | |
| 201 / 202 | enum | 0 Stop, 1 Heating, 2 Cooling, 3 Fan, 4 Dry (2 confirmed) | |
| 204 | uint8 | error code, decimal | `00` → **0** |
| 205 | enum | 4-way mode: 0 Cooling, 1 Heating | |
| 206 / 207 / 208 / 209 / 210 | enum | fan tap, flap `P<n>`, flap setting, airflow (0 Auto), transmission (1 Normal) | |

Comparison of the phone recording `samples/minisplit-20260920.tgz` against the PC export of the same recording
(`samples/minisplit-3head.csv`): 1248 paired rows, 73 common columns, header identical, **every status, control and
error cell identical**; the only differing cells are the PC app's whole-degree truncation (`60` for 60.8 °F, 369 cells
across nine temperature columns). The phone log holds 1258 records; the PC dropped 10.

The PC export ("REC only") writes only 73 of the 289 visible columns: it skips items that never held a value in the
recording (Hz limits, timers, ODU monitors, humidity, per-head pipe temps, second fan) and a few enums it does not
decode (fan tap). The app exports every visible column; the extra columns are empty or constant here, and the app
maps channels by column number so they do no harm. Unconnected ports still log EV = 0, so the zone count comes from
gas/liquid thermistors, a non-zero EV, or an indoor address, not from the EV column alone.
