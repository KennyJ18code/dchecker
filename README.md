# D-Checker Cycle Viewer

Daikin D-Checker logs on a live refrigerant-circuit diagram, with playback, trend pinning, targets and diagnostic signatures. Runs entirely in the browser; no data leaves the device.

- `index.html` - the app (built from `template.html` + `sample.csv`)
- `template.html` - source; `__SAMPLE_CSV__` is replaced by the demo log at build
- `sw.js`, `manifest.webmanifest`, `icons/` - installable web app (Add to Home Screen)
- `tools/dlog_decode.py` - PC-side decoder for phone recordings (same logic as the app)
- `samples/shop-fit-test.tgz` - a recording straight from the D-Checker phone app

Build: replace `__SAMPLE_CSV__` in `template.html` with the contents of `sample.csv` and write `index.html`.

## 3D view

The Cycle tab opens on the 2D drawing; the **3D | 2D** switch beside it shows a rotatable 3D model of the same circuit, and the app remembers each tech's choice. Developed in the `dchecker-3d` copy and merged here at v53.

- **What is drawn.** The outdoor unit as a glass cabinet with its L-shaped coil, black batwing propeller fan modelled on Daikin part 2026774 (three broad sickle blades, each with a hooked leading tip and a V-notch in the trailing edge), 4-way valve, and an inverter rotary compressor (domed shell on rubber-mounted feet, discharge out the top of the dome, terminal cover on the upper shell) with its suction accumulator strapped to the shell side, suction into the accumulator top and a J-tube from its bottom into the lower shell; on heat pumps whose log carries the Hot gas SV channel, the hot-gas bypass (tee off the discharge line, strainer, solenoid valve, into the suction line), coloured and with a green coil while the log shows it open (it opens mostly in restart standby to equalize pressures); pipes are drawn close to real tube size; the line set; and either an upflow air handler with an A-coil and blower (FIT), piped as installed: the line set comes around to the front of the cabinet and enters through the panel at the bottom-left of the coil section, suction stub above liquid stub; inside, liquid runs through the indoor EEV to a distributor with feeder tubes into both slabs, and suction collects in a header on each slab's front edge joined by a crossover that runs out the suction stub or wall-mounted heads (mini split). On a mini split every head has its own gas and liquid line down the wall to its own port, port EEV and junction on the gas and liquid headers inside the outdoor unit. Heat pump or AC, and the visible heads, follow the Equipment selector and the Heads buttons.
- **What moves.** Pipes take the same thermal colours, hi/lo sides, flow direction and idle rules as the 2D drawing (same pipe ids, `segTemp()`, port EEV at 0 pulses = idle head). Bands travel along live pipes while playing, a cone on each pipe's longest run points with the flow even when paused, the outdoor fan spins, coils take their coil temperature.
- **Readings.** Built as a teaching view, so no reading ever hides. Each chip is projected from its sensor's 3D anchor (a dot on the model) and sits beside it when there is room; when there is not, it moves to a side column (outdoor readings on the outdoor unit's side, indoor and head readings on the other), kept in the sensors' top-to-bottom order and tied to its dot by a leader line. Columns hug the model, and a sensor turned off screen keeps its chip with the leader pointing to the edge. Tapping a chip pins its trend to the bottom bar like a 2D tag. Rule states colour the chip border and its leader.
- **Learning tools.** *Tabled in 3d-12: the tap-to-learn part cards and the X-ray view are switched off (`FEAT3` in `template.html`; the code is kept). Phase and P-h remain.* Tap any part (compressor, accumulator, reversing valve, coils, fans, expansion valves, distributor, headers, line set, service valves, hot-gas valve, or a cabinet with Covers on) for a card: what it does in the current mode, its live readings and what they mean, where it sits on the P-h chart, and the rulebook checks that watch it (highlighted while firing). **Phase** colours every pipe and coil by refrigerant state (vapour, liquid + vapour, liquid; strong = high side, pale = low side), from the role of each pipe checked against the measured temperature and the saturation temperatures, so liquid that is flashing or vapour that is wet shows up. **X-ray** turns the shells to glass and shows the compressor's stator, rotor and shaft, and its swing pump moving as the real one does (the eccentric carries the piston round the bore without letting it spin, and the piston's blade slides through a bushing that rocks in the cylinder wall), with oil in the sump; the compressor card adds an animated cross-section of the pump from above, filling the suction pocket blue and the shrinking compression pocket red, the accumulator's J-tube and pooled liquid, the reversing valve's slide (it shifts with the mode) and pilot solenoid, and each expansion valve's needle rising with its logged opening. **P-h** draws the live cycle on a pressure-enthalpy chart (R-410A and R-32 property tables from CoolProp 8, ASHRAE reference) with Tc, Te, superheat, subcooling, flash gas, refrigeration effect, compressor work and a rough COP; the selected part's step is highlighted. Mini-split boards log no pressures, so for them saturation comes from coil temperatures and the chart says so.
- **Touch.** One finger orbits, two fingers pinch-zoom and pan, double tap or Reset returns to the starting view; Front / Side / Top are presets; Readings hides the chips; Covers puts the units together as installed (outdoor cabinet with top, base pan, service panel, fan grille and coil guards; air handler side, back and top panels, supply plenum, blower and coil doors with the line set through the coil door; mini-split head shells with vane and a line-hide over each run down the wall) and takes them off again. Both choices are remembered. The 3D | 2D switch brings back the flat schematic.
- **How.** `V3` in `template.html` is a small WebGL 1 renderer with no libraries: tubes with rounded elbows built by parallel transport, boxes, cylinders, cones, one shader (Lambert plus a travelling band along the pipe-length attribute). It renders on demand; the only continuous work is the flow while playing, throttled to about 22 frames a second. No extra files to download or cache.
- **Checking it.** `tools/shot.html` drives the app inside headless Chrome (WebGL works there): params `file=none`, `at=`, `v3=front|side|top`, `drag=dx,dy` (synthetic touch drag), `eqsel=ac-multi`, `dim=2d`, `off=` scroll offset.

Not yet in 3D: the top-discharge cabinets (DX20VC / DZ20VC / DX9VC / DZ9VC), service parts (strainers, check valves, muffler), air-flow streams, and tap-a-pipe picking.

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

## Trends

Each strip in the Trends tab draws the reading's logged target on the same scale as an orange dashed line when the log has one (discharge target, target comp speed, target OU fan, target SH/SC, requested airflow); the picker marks those readings "+target". The Overlay button puts up to five ticked readings on one chart, each on its own scale in its own colour with its target dashed in that colour, and a legend showing the value at the cursor and the range of each line. On phones the reading picker folds to one line so the chart is on screen. Tapping a reading on the Cycle screen pins it to the bottom bar (up to five); with two or more pinned, the bar overlays them on one chart with the same legend (each entry has its own unpin ×), or shows a strip each with the Separate switch.

## Models

Unitary logs are read by column **label**, because models number their columns differently (a DH9VS shifts everything from column 76 on). Verified layouts: DZ6VS (R-410A FIT) and DH9VS (R-32 with vapour injection, two fans, drain pan valve); the DH9's extra readings (injection EV, fan 2, fan driver fin temperatures, indoor target SC, drain pan valve) are in Trends and Data. A reading this model never reports is hidden on the diagram. See `docs/decode-walkthrough.md` §8. The DH9VS is drawn as its own variant of the 2D diagram (injection EEV into the compressor, drain pan heater circuit with its solenoid, PCB heatsink, mufflers on the discharge, service port on the suction), per its service piping diagram; see `docs/outdoor-circuits.md` §6. The 3D model follows: the DH9VS is the tall two-fan cabinet with a full-height coil, each fan turning on its own rpm, plus the injection valve and line, the heatsink, both mufflers and the drain pan heater loop.

## Error codes

An error byte in the log is decoded to the code the unit shows (U4, F3, A5 …) and shown with its meaning as a header chip, in the narration line, and as a synopsis card with how long it was present, the raw byte, the readings that bear on it and the first checks. The Data tab has the full searchable table. The byte-to-code reading follows Daikin's bus convention and is still to be confirmed on a real fault recording; see `docs/decode-walkthrough.md` §9.

## Refrigerant and PT chart

The app carries R-410A (dew point) and R-32 saturation tables from CoolProp 8, 5 °F steps from −40 to 160 °F, in `PT410` / `PT32`. The refrigerant in use is auto-detected: a unitary log states it in its first column (R410A or R32) and that wins; failing that, the board's logged Te/Tc at the logged LP/HP are compared with both tables and the closer one wins; otherwise the model name decides (DC/DH = R-32, DX/DZ = R-410A); a Multi_Split log names no model so it is assumed R-410A (MXS) unless the Refrigerant selector is set to R-32 (MXL). The selection feeds the Te/Tc PT checks, the discharge-limit rule and the PT chart in the Data tab, which also shows the live saturation temperatures for the current row.

## Rulebook

`docs/rulebook.md` is the Daikin inverter rules spec (laws L1–L6, FIT rules S1–S15, mini-split rules M1–M18). The app evaluates the rules it has data for on every row (gated on a speed-locked compressor, L1) and shows them as chips with their ids, in the narration line, and as synopsis cards with Why and Fix steps. Thresholds live in `RT` in the source and are field starting points, not Daikin limits.
