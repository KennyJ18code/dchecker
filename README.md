# D-Checker Cycle Viewer

Daikin D-Checker logs on a live refrigerant-circuit diagram, with playback, trend pinning, targets and diagnostic signatures. Runs entirely in the browser; no data leaves the device.

- `index.html` - the app (built from `template.html` + `sample.csv`)
- `template.html` - source; `__SAMPLE_CSV__` is replaced by the demo log at build
- `sw.js`, `manifest.webmanifest`, `icons/` - installable web app (Add to Home Screen)
- `tools/dlog_decode.py` - PC-side decoder for phone recordings (same logic as the app)
- `samples/shop-fit-test.tgz` - a recording straight from the D-Checker phone app

Build: replace `__SAMPLE_CSV__` in `template.html` with the contents of `sample.csv` and write `index.html`.

## Opening a recording straight from the D-Checker phone app

The mobile D-Checker app saves each recording as a `.tgz` (a folder with a binary `.log`, `datalabel.txt`, `header.txt`, `mapping.txt`, `graph.txt`, `customer.txt`). The PC "Dchecker3" program normally converts that to CSV. This app decodes the `.tgz` itself: **Open log...** and pick the archive (or the `.log` together with its `datalabel.txt`). **Save CSV** then writes the same CSV the PC app would.

Record format (worked out from a Daikin FIT heat-pump log): each record is a 14-digit timestamp followed by tagged binary blocks `[group][0][length] data...` ending in `FF FF`; `datalabel.txt` gives every field's group, byte offset, size, type and label. Types: 105/107 int16 x0.1 (C or kgf/cm2, `0x8000` = no data), 151 uint16, 152/220 uint8, 161 uint8/2 (%), 164 uint8x5 (rpm), 211 fan step, 217 op mode, 313 indoor mode (upper nibble), 203 error type, 215 error code, 30x bit x, 310/311 nibbles.

Known differences from the PC export: the phone recording keeps seconds on every timestamp; one valid record the PC app dropped is kept; the PC app truncates whole-degree-C temperatures to integer F (16.0 C -> "60"), this app converts exactly (60.8).

## Multi-zone mini splits

Logs from 2–5 port MXS/MXL outdoor units (columns `Rm_A gas temp`, `Port A EV`…) are detected automatically and drawn as one zone per port with a shared outdoor unit. Each head's gas and liquid line drops on its own into the outdoor unit and lands on its own junction of a header block (gas bar and liquid bar in one manifold); nothing is shared between heads (that is a VRV trunk, not a mini split). A liquid line that has to pass the gas bar is drawn with a break. The port EEV splits each liquid line into a header-side segment (coloured by the outdoor coil) and a line-set segment (coloured by the port thermistor), so the letdown across the valve is visible in thermal mode. See `docs/outdoor-circuits.md` §5. `tools/shot.html` is a headless-Chrome screenshot harness for checking the drawing.

## Refrigerant and PT chart

The app carries R-410A (dew point) and R-32 saturation tables from CoolProp 8, 5 °F steps from −40 to 160 °F, in `PT410` / `PT32`. The refrigerant in use is auto-detected: on a FIT log the board's logged Te/Tc at the logged LP/HP are compared with both tables and the closer one wins; otherwise the model name decides (DC/DH = R-32, DX/DZ = R-410A); a Multi_Split log names no model so it is assumed R-410A (MXS) unless the Refrigerant selector is set to R-32 (MXL). The selection feeds the Te/Tc PT checks, the discharge-limit rule and the PT chart in the Data tab, which also shows the live saturation temperatures for the current row.

## Rulebook

`docs/rulebook.md` is the Daikin inverter rules spec (laws L1–L6, FIT rules S1–S15, mini-split rules M1–M18). The app evaluates the rules it has data for on every row (gated on a speed-locked compressor, L1) and shows them as chips with their ids, in the narration line, and as synopsis cards with Why and Fix steps. Thresholds live in `RT` in the source and are field starting points, not Daikin limits.
