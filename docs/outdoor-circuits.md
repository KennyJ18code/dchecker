# Daikin outdoor-unit refrigerant circuits (templates for the viewer)

Scope: outdoor units only. Every unit the D-Checker 3 model list supports, grouped by the
service manual whose piping diagram applies. Images live in `docs/manuals/`.
Source PDFs are kept locally but not committed (see `.gitignore`).

| Family (Daikin / Goodman-Amana twins) | Refrigerant | Platform | Service manual | Piping diagram |
|---|---|---|---|---|
| DX6VS / DZ6VS (2021 R-410A FIT, no Goodman twin) | R-410A | Daikin FIT side-discharge | SM-SiUS612209EA (`fit-dx6vs-dz6vs-service.pdf`) | `fit-service-p8.png` (AC), `fit-service-p9.png` (HP) |
| DC6VS / DH6VS / DC9VSA / DH7VSA = GXV6S / GZV6SA / GXV9SA / GZV7SA | R-32 | Daikin FIT side-discharge (2024) | SiUS612414E (Goodman-badged, ManualsLib 3967244) | `r32-fit-sius612414e-p8-ac.jpg`, `-p9-hp.jpg`, `-p10-cooling-flow.jpg`, `-p11-heating-flow.jpg` |
| DC9VS / DH7VS / DH9VS (2025 R-32 FIT "Aurora") | R-32 | Daikin FIT side-discharge | not public yet; install manual only (`dh9vs-dh7vs-dc9vs-install.pdf`, 7-seg tables `dh9vs-dh7vs-dc9vs-p43.png`) | use the SiUS612414E drawings |
| DX17VSS / DZ17VSA | R-410A | Daikin side-discharge (pre-FIT) | SiUS612102E (ManualsLib 2150969) | `dx17vss-dz17vsa-service-p9-ac.jpg`, `-p10-hp.jpg` |
| DX20VC / DZ20VC = GVXC20 / GVZC20 | R-410A | Goodman top-discharge inverter | RS6115001 / RS6215001 (ManualsLib 2525889 DX20VC, 2341281 DZ20VC) | `dx20vc-service-p15-cooling-txv.jpg`, `-p16-cooling-comm.jpg`, `dz20vc-service-p15-cooling-txv.png`, `-p16-cooling-comm.jpg` |
| DX9VC / DZ9VC = GSXV9 / GSZV9 | R-410A | Goodman top-discharge inverter (2022) | not public (install manual only, `dx9vc-install.pdf`) | use the DX20VC / DZ20VC drawings |

## 1. Daikin FIT side-discharge (DX6VS/DZ6VS, DC6VS/DH6VS/DC9VSA/DH7VSA, DC9VS/DH7VS/DH9VS)

The R-32 drawings in SiUS612414E are the same circuit, component for component, as the
R-410A FIT drawings in SM-SiUS612209EA. Only the refrigerant and the PT table change.
The app's current portrait and landscape drawings were built from these, so they already
fit every FIT unit.

Heat pump (DZ6VS, DH6VS, DH7VSA, DH7VS, DH9VS):

- Discharge: compressor → check valve → Td thermistor → HPS → PS (pressure sensor tee) → 4-way.
- Hot-gas bypass: tee after the check valve → strainer → solenoid valve (SV) → into the
  accumulator inlet line (suction). Drawn as a branch off the discharge riser.
- Gas line: 4-way → muffler (1.5–3 ton only) → fusible plug + 7/16" service port → gas stop valve.
- Suction: 4-way → Ts thermistor → accumulator → compressor accumulator → compressor.
- Outdoor coil: Tm (heat-exchanger thermistor, mid coil) and Tb (defrost thermistor, coil
  outlet in heating). Ta ambient on the coil face.
- Liquid side: coil → strainer → outdoor EEV with check-valve bypass (check valve lets
  cooling flow skip the EEV) → strainer → Tl liquid-pipe thermistor → liquid stop valve.
- 3.5–5 ton adds a PCB-cooling heatsink in the liquid line between Tl and the strainer.
- Indoor side (for reference only): PS on the gas pipe, Tgi, coil, Tli, filter, indoor EEV,
  filter, filter drier.

Air conditioner (DX6VS, DC6VS, DC9VSA, DC9VS):

- No reversing valve, no hot-gas solenoid, no muffler, no discharge check valve, no outdoor
  EEV, no liquid-line check valve, no Tb defrost thermistor.
- Outdoor PS sits on the gas (suction) line next to the fusible plug, so it reads LOW side.
- Circuit: gas stop valve → PS → Ts → accumulator → compressor accumulator → compressor →
  Td → HPS → coil (Tm, Ta) → Tl → liquid stop valve. 3.5–5 ton adds the heatsink after Tl.

Op-mode codes for the R-32 units (7-seg monitor): 0 Stop, 1 Cooling start-up,
2 Heating start-up, 3 Oil return, 4 Heating, 5 Defrost, 6 Cooling
(`dh9vs-monitor-mode-codes.txt`).

## 2. DX17VSS / DZ17VSA (older Daikin side-discharge)

Same circuit as the FIT family with two differences worth drawing:

- HP 1.5–3 ton has a **pressure regulating valve** in series with the outdoor EEV on the
  liquid line (between the EEV and the strainer on the coil side). 3.5–5 ton does not.
- Muffler is not shown on the gas line; otherwise identical (SV hot-gas bypass, check
  valve, HPS, PS on discharge for HP, PS on suction for AC, heatsink on 3.5–5 ton).

## 3. DX20VC / DZ20VC (Goodman top-discharge inverter, ComfortNet)

A different physical layout. Sensors: Ta, Td, Tm, Tl only (no Ts, no Tb), one outdoor
HP/LP pressure sensor at the gas ball valve, HPS on the discharge. Communicating indoor
units add ID HP/LP sensor, Tgi, Tli.

Heat pump (DZ20VC):

- Compressor → check valve → HPS / Td → oil separator → 4-way (reversing valve).
  Oil separator drain returns through a capillary tube to the suction side.
- Gas line: 4-way → HP/LP sensor → gas ball valve.
- Suction: 4-way → accumulator → compressor. No Ts thermistor.
- Liquid: coil → filter → outdoor EEV with check-valve bypass → "Ref cooling" loop
  (PCB cooling U-tube on the liquid line) → Tl → liquid stop valve → filter drier.
- 5 ton adds a crankcase heater; the 2–4 ton and 5 ton drawings otherwise match.

Air conditioner (DX20VC): the manual re-uses the HP drawing (still shows a 4-way symbol);
there is no outdoor EEV and no check-valve bypass, the liquid line runs coil → filter →
Ref cooling → Tl → stop valve. Treat the 4-way on that drawing as an artifact.

## 4. DX9VC / DZ9VC (2022 Goodman-platform inverter, R-410A)

No public service manual. Install manual has charge tables and 7-seg codes but no piping
diagram. They are the same ComfortNet top-discharge platform as DX20VC/DZ20VC (same sensor
names Ta/Td/Tm/Tl + one HP/LP sensor), so use the DX20VC/DZ20VC drawing until Daikin
publishes the manual. Model files in D-Checker: INV_Unitary_DX9VC(_5ton), DZ9VC.

## What this changes for the app

1. Two outdoor drawing families are enough: **side-discharge (FIT-style)** and
   **top-discharge (VC-style)**. Each has an AC and an HP variant, and a 3.5–5 ton
   sub-variant (heatsink on the liquid line; VC units always have the Ref-cooling loop).
2. AC variant of the FIT drawing: drop the 4-way, SV/strainer bypass, muffler, discharge
   check valve, outdoor EEV + check valve, Tb; move the outdoor PS to the suction line.
3. VC family needs its own sensor map: no Ts, no Tb, single HP/LP sensor, oil separator +
   capillary, accumulator directly on the 4-way, Ref-cooling loop on every size.
4. DX17VSS/DZ17VSA: FIT HP drawing plus a pressure regulating valve on 1.5–3 ton.
5. Model detection from header.txt (INV_Unitary_<model>.txt) picks the family; the 4-way
   column picks AC vs HP when the model name is missing.

## 5. Multi-zone mini splits (2MXS/3MXS/4MXS/5MXS, MXL) — R-410A

Service manual SiUS121502E (`docs/manuals/mxs-service.pdf`, 227 pp); outdoor piping diagrams rendered as
`mxs-service-p204-2-3mxs-outdoor-piping.png` and `mxs-service-p205-4mxs-outdoor-piping.png`.

Circuit (3MXS24): compressor → muffler → discharge thermistor → 4-way → outdoor coil (distributor + capillaries,
coil thermistor) → liquid stop valve → muffler with filter → liquid header → one EEV per port (EVa/EVb/EVc) →
liquid-pipe thermistor per port → filter → room. Gas side: room → gas-pipe thermistor per port → muffler per
port → gas header → gas stop valve → accumulator → 4-way → accumulator → compressor.

D-Checker log layout (`samples/minisplit-3head.csv`): no pressure sensors at all. Outdoor columns 1–13 and 45–86
(op mode, defrost, error, target discharge, max-Hz limiters 5–8 with 255 = no limit, rps cap 10, OAT 45, coil 46,
discharge 47, port gas 48–52, port liquid 55–59, fin 62, current 64, volts 65, comp on 73, rps 74/75, fan 76/77,
4-way 82/83, port EV 84–88). Each indoor head is a 28-column block starting at 97 + 28·k (address, mode, error,
ΔD, return air, coil temp, fan, flap/louver, setpoint, airflow, transmission). EEV full open = 450 pulses (p.86).

The app draws this as one row (phone) or column (desktop) per port with the head and its port EV, and a shared
outdoor unit. Diagnostics are temperature based: port gas − liquid (coil ΔT / superheat proxy), return air − coil,
discharge vs target discharge, comp vs target and vs the rps cap, and the four max-Hz limiters as chips.

## 6. DH9VS (R-32, vapour injection) — verified against the service piping diagram, 2026-10-02

The app draws this variant when the log carries an injection EV or a drain pan valve column (`uniVar() === 'dh9'`).
It is the FIT heat pump circuit plus:

- **Injection.** A tee on the liquid line, after the PCB heatsink, feeds an injection EEV whose outlet goes straight into the
  compressor's injection port. Logged as `EV (injection)(pls)`; 0 pulses = closed (it stayed closed for the whole 68 °F cooling
  recording we have). Pipe id `inj`, coloured by the liquid pipe temperature while the valve is open.
- **Drain pan heater.** Discharge gas is taken off above the compressor, through a strainer and the drain pan solenoid
  (`SV (drain pan)`), through a loop in the base pan, then a check valve and a capillary tube into the coil's liquid end (between the
  coil and the liquid-side strainer). Pipe id `pan`, live only while the compressor runs and the solenoid is ON.
- **PCB heatsink** on the liquid line between the liquid stop valve and the injection tee; the liquid pipe thermistor sits on the stop
  valve side of it.
- **Discharge:** discharge thermistor, HPS, two mufflers, HP sensor, hot-gas bypass tee (strainer + solenoid to the suction), check
  valve, reversing valve. The gas line itself has no muffler.
- **Suction:** reversing valve → service port (7/16" flare) and fusible plug → suction thermistor → accumulator → LP sensor →
  compressor accumulator → compressor.
- **Outdoor EEV** has a check valve in parallel (bypassed in cooling), with a strainer on the coil side. Two outdoor fans. One coil
  thermistor (defrost) and no mid-coil thermistor.
- **Indoor:** as the FIT — EEV with a filter each side, liquid and gas thermistors, pressure sensor on the gas pipe; a filter drier in the
  field liquid line.

In 3D the DH9VS is the tall two-fan cabinet (1.33 m against 0.99 m, full-height coil, each propeller turning on its own fan's rpm), with the
injection EEV and its line into the compressor shell, the PCB heatsink on the liquid line by the stop valve, two mufflers on the discharge
riser, and the drain pan heater: riser with strainer and solenoid behind the valves, a loop round the base pan under the coil, check valve
and capillary into the coil's liquid outlet. The solenoid coil turns green when open.

Not drawn in 2D: the second fan, the second muffler (one symbol stands for both), the compressor accumulator. Not drawn in 3D: service
port and fusible plug.
