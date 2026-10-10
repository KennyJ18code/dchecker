# Daikin Inverter Refrigeration Rules

Diagnostic rules for Daikin residential inverter equipment: FIT split systems (DX6VS, DZ6VS, R-32 DC6VS/DH6VS) and mini splits (Aurora cold-climate, standard wall mounts, ducted and multi-zone). Each rule turns sensor readings from the Daikin service app and technician probes into a diagnosis before the question gets asked.

## Rule sources in the app (v100)

This file is the original rules spec. Since v100 (2026-10-09) the app follows the owner's rule: **every rule matches the platform's service manual, always**. Where a manual gives a line, the app uses that line and the card names the manual and page; where this file's numbers differ from the manual, the manual wins. A rule with no manual page behind it is a **field rule**: it is kept, but the app shows it only with Settings → Field rules and provisional patterns on, labels the card "Field rule, not from a service manual", and never shows it above a warning. **Law** means refrigerant physics (for example water freezing at 32 °F).

Manuals: SiUS612209EA and installation manual 3P731493-1 (FIT R-410A), SiUS612412E (FIT R-32), SiUS612415E and the DH9VS / DH7VS / DC9VS installation manual (double-fan DH9VS family), RS6215002r10 (Goodman / Amana *VZC20 = DZ20VC / DZ9VC / *SZV9), DX9VC installation and service reference, SiUS121736EA (MXS), SiUS121632EA (MXL), SiUS121827E (5MXS48T / 4MXL36T), SiUS122410EC (MXM / MXT), IOD-4054B (DFVE air handler), the CAPEA / CAPE installation manual (cased coils), RSD6620001r1 (Daikin communicating furnace, for its E7). Page numbers are PDF pages.

### Rules from this file

| Rule | What the app does | Source |
|---|---|---|
| L1 Lock the speed | Gates the refrigerant rules on a locked speed (within ±5 % for 10 min); data-quality cards for locked time and recording gaps | field numbers (gate only) |
| L2 Prove the sensors | Thermistors vs outdoor air after 30 min off (3 °F) | field |
| L2 (X1–X3) | Stuck, implausible and noisy sensors, the column check | the app's own wide margins on impossible readings; the thermistor error codes come from each manual |
| L3 Discharge temperature | S2t and S2h below | manual |
| L4 Pinned at max speed | L4 (needs the rated maximum in `RPS_MAX`), L4h hunting | field |
| L5 Protection control | L5: a limiter or drop flag holding the speed for 10 min | field number; the flags are the board's own. The multi limiter cards use each family's zones (manual) |
| L6 Coil must beat the dew point | Calculated capacity and COP card (information) | law (calculation) |
| S1 Liquid returning | Discharge SH under the analysis chart's 20 °F line inside the chart's outdoor range (SiUS612209EA p.12–13; RS6215002r10 p.95–96; DX9VC p.21), and on the R-410A FIT in cooling suction SH under 4 °F (SiUS612209EA p.12). R-32 FIT (no chart): the E21 condition, discharge SH under 9 °F with the indoor EEV at its 50-pulse minimum (SiUS612412E p.50) | manual |
| S2 Starved compressor, high discharge | S2t: discharge past the board's trip line, 248 °F (E22; SiUS612209EA p.52, SiUS612412E p.51). S2h: discharge above the analysis chart's 200 °F line inside its outdoor range (SiUS612209EA p.12–13; RS6215002r10 p.95–96; DX9VC p.21) | manual |
| S3 Power quality | Not a rule; the voltage and current error codes come from the manuals | — |
| S4 Indoor coil freezing | Indoor coil saturation under 32 °F for 10 min in cooling | law (32 °F); the 10 min is a field number |
| S5 Suction transducer vs gauge | Not in the app (needs a gauge) | — |
| S6 Pinned at max speed | Folded into L4 | field |
| S7 High head | Condensing more than 25 °F over outdoor air at speed | field; the manual's test is the analysis-chart card |
| S8 Airflow | Present airflow under 90 % of requested | field; the board's own fault is b9 / Eb9. Present CFM is the blower's estimate (IOD-4054B p.15) |
| S9 Heating outdoor coil split | S9w wider than 28 °F; S9n narrower than 5 °F at speed | field |
| S10 Defrost behaviour | More than 2 defrosts an hour | field. The manuals' defrost maximum (120 min on the FIT, SiUS612209EA p.44; 30 min factory setting on the *VZC20, RS6215002r10 p.64) is used by pattern A9 |
| S11 Shoulder-season humidity | 65–80 °F outdoors near the lowest speed | field |
| S12 Continuous fan | Blower running with the compressor off, after the 120 s Cool Airflow OFF Delay (SiUS612209EA p.43) | field |
| S13 Return leak, S14 Settings | Not in the app | — |
| S15 Fault history | A code repeated 3+ times | field |
| M1 Low charge | A port valve at the most the board gives an operating room (450 pulses on the MXS / MXL, 480 on the MXM / MXT) with discharge over its target, after the starting control (SiUS121736EA PDF 119–121; SiUS121632EA PDF 105–107; SiUS122410EC PDF 162–163) | manual |
| M2 Cross-piped | Not a rule in the app | — |
| M3 Flooding | M3o / M3s: discharge SH under 20 °F with the port valves mostly closed / one mostly open | field |
| M4 Drive stress | Input-current limiter holding the speed (SiUS121736EA PDF 110), or the fin above the temperature its L4 trip clears at (SiUS121736EA PDF 219; SiUS121632EA PDF 199; SiUS122410EC PDF 318) | manual |
| M5 Freeze-up | Freeze-up limiter holding the speed, or the coldest operating head coil under the family's drop line (SiUS121736EA PDF 111; SiUS121632EA PDF 99; SiUS122410EC PDF 149) | manual |
| M6 Peak-cut | Hottest head coil at or above the family's "up" line with the peak-cut limiter holding (SiUS121736EA PDF 113; SiUS121632EA PDF 99; SiUS122410EC PDF 150) | manual |
| M7 Cold-weather capacity | M7e, M7c | field |
| M8 Base pan ice | Outdoor fan under 70 % of its target below 32 °F | field |
| M9 Cooling in cold weather | Head coil under the freeze-up "up" line with outdoor air under 60 °F | field (the line is the manual's, the 60 °F gate is not) |
| M10 Thermistor codes | Error reference per family; the multi discharge-thermistor disconnection test (discharge 10.8 °F below the coil after the starting control; SiUS121736EA PDF 120, SiUS122410EC PDF 163) | manual |
| M11 Communication errors | Error reference per family | manual |
| M12 Short cycles | A head that satisfies in under 10 min on average | field |
| M13 Fan on high, humid | Fan at maximum with a coil at or above 52 °F | field |
| M14 Fan after the compressor stops | Port closed, fan on, coil at room temperature. The factory fan behaviour is cited (SiUS121736EA PDF 249; SiUS122410EC PDF 364) | field |
| M15 Head reads the ceiling | Keeps calling (ΔD signal 5 or more) with return air below setpoint | field |
| M16–M18 | Advice; not rules in the app | — |

### Rules from the manuals that this file did not have

| Rule | Line | Source |
|---|---|---|
| Analysis chart | Every reading outside the chart's lines inside its outdoor range (cooling 67–115 °F, heating 17–62 °F), and the causes whose X marks cover all of them, with the chart's remedy | SiUS612209EA p.12–13; RS6215002r10 p.95–96; DX9VC p.21 |
| E13 high pressure | 605 psig | SiUS612209EA p.49; SiUS612412E p.48; RS6215002r10 p.15 (HPS); SiUS612415E p.15, p.50 (HPS opens 605, cuts in 465) |
| E15 low pressure | 17 psig for 5 min (FIT); **11 psig** for 5 min (DH9VS family) | SiUS612209EA p.50; SiUS612412E p.49; SiUS612415E p.51 |
| E21 low discharge SH | under 9 °F with the EEV at its minimum (R-32 FIT, DH9VS family) | SiUS612412E p.50; SiUS612415E p.52 |
| E22 discharge | 248 °F | SiUS612209EA p.52; SiUS612412E p.51; SiUS612415E p.53 |
| E32 inverter fin | 203 °F (R-410A) / 214 °F (R-32) on 1.5–3 ton, 230 °F on 3.5–5 ton; about 226 °F on the DH9VS family | SiUS612209EA p.53–54; SiUS612412E p.52–53; SiUS612415E p.54 |
| E41 refrigerant shortage, heating | discharge SH over 117 °F (R-410A FIT) / 135 °F (R-32 FIT) / 153 °F (DH9VS family); liquid pipe more than 3.6 °F below outdoor air (FIT: 3.5–5 ton; DH9VS family: all sizes) | SiUS612209EA p.55; SiUS612412E p.54; SiUS612415E p.55 |
| Charge figure (information only) | R-410A FIT by size (1.5 t 10, 2 t 12, 2.5 t 14, 3 t 15 [DX6VSA 13], 3.5 t 8, 4 t 9, 5 t 9; Enhanced 2 t 14, 3 t 8, 3.5 t 9, 4 t 9 °F, ±1 °F, CHARGE MODE); 11 ±1 °F (DH9VS family, CVT); 8 ±1 °F (*VZC20 and DX9VC charge mode; the 5-ton *VZC20's Daikin twin and successor manuals say 10 °F); applies only in the manual's own charge test | installation manual 3P731493-1 p.29–30; DH9VS installation manual p.26; RS6215002r10 p.23–24; RSD6215002r9 p.32; DX9VC p.10–12 |
| Multi limiter zones | Freeze-up, peak-cut, discharge drop and stop, input current, and the fin's L4 line: each family's own values | SiUS121736EA PDF 106–113, 219; SiUS121632EA PDF 97–99, 199; SiUS122410EC PDF 147–150, 318 |
| Error codes | One table per family, from its manual | each manual's error-code pages |

### Signatures, patterns and the colour bands

- **Signatures** (the per-row flags): low discharge SH at speed uses the manual's line above; "held" uses the board's own drop flags. EV pinned or closed, discharge climbing, LP falling, outdoor vs indoor pressure, outdoor coil, current, thermistor order, short cycles and "SC never reached" are field rules. The outdoor EEV is judged only in heating: in cooling it is bypassed by its check valve (SiUS612209EA p.9; SiUS612412E p.7, p.9; RS6215002r10 p.12–13).
- **Fault library and EEV-response checks (V1 / V2)**: field rules. V1 follows what the outdoor EEV controls in heating (suction − outdoor coil middle on the R-32 FIT, SiUS612412E p.7); V2 only in cooling (the indoor EEV is fully open in heating, p.7).
- **Cause → effect patterns** (A–H): shown only when confirmed on a real repair, or with the switch on. Where a manual gives a line the pattern uses it (defrost maximum, the board's discharge drop flag, the R-32 FIT outdoor superheat, the high-pressure line).
- **Colour bands**: the Rules tab's "From the service manual" list is built from the lines above for the loaded platform; bands a user adds are listed apart as "Your own bands (not from a manual)".
- **Logged targets**: Target SH is the indoor EEV's cooling target (SiUS612412E p.7; SiUS612415E p.9, 5.4–18 °F). On the DH9VS family the IDU Target SC is the outdoor EEV's heating target for the indoor subcooling (SiUS612415E p.9, 1.8–9 °F). No manual describes the outdoor "Target SC" column, so it is shown for reference only and the rules that compare subcooling with it are field rules.
- **Defrost runs**: the compressor stops just before and just after a defrost (SiUS612209EA / SiUS612412E p.11); those stops are part of the defrost, not new runs. Newer R-32 heat pumps defrost on 2, 6, 12 or 24 h intervals (SiUS612417EA p.9, p.45), so no fixed maximum interval is assumed for them.
- **Airflow (S8)**: judged only after 2 min running and 2 min of an unchanged request, outside defrost: the request ramps by design (cooling profile D) and is 0 in defrost.

## How to use this file

This is a spec for building a rules engine and a technician-facing reference. Each rule has:

- `id`: stable identifier (L = law, S = split system, M = mini split)
- `category`: `law`, `split`, or `mini`
- `severity`: `law`, `critical`, `major`, `moderate`, `minor`
- `rule`: the statement a tech reads
- `why`: the reasoning
- `readings`: what to pull from the app (App) and from probes (Probe)
- `fix`: ordered corrective actions
- `logic`: pseudo-code for the rules engine, using the derived variables defined below

### Severity definitions

| Severity | Meaning |
|---|---|
| law | Foundational principle; every other rule depends on it |
| critical | Risk of compressor or inverter drive damage |
| major | System can't hold setpoint |
| moderate | Humidity or comfort drift |
| minor | Efficiency loss or nuisance |

### Implementation notes

- **Gate every refrigerant rule on `speed_locked` (Law L1).** Readings taken while the compressor is ramping are invalid.
- **Gate every calculation on sensor validity (Law L2).** If a sensor fails the at-rest check, suppress rules that use it and raise `sensor_drift` instead.
- **Source mapping changes by equipment and mode.** See the derived variables table. On a mini split, `t_evap_sat` is the indoor coil thermistor in cooling but the outdoor coil thermistor in heating.
- **Thresholds are field starting points, not Daikin published limits.** (In the app, superseded by the service manuals where they give a line: see Rule sources above.) Store them as configurable parameters per model and refrigerant, not constants. R-32 runs hotter discharge temperatures than R-410A; its discharge limit must come from the model's service manual.
- **Fault codes** (U0, F3, A5, E7, J3, etc.) match most Daikin mini split families. Verify per model before hard-coding.

### To verify before production

1. The exact procedure to lock the FIT in fixed-speed charge mode (copy from the installation manual into L1).
2. Discharge temperature limits per refrigerant and model.
3. Mini split fault code lists for the models installed.

## Derived variables

| Variable | Formula | FIT split source | Mini split source |
|---|---|---|---|
| `t_evap_sat` | Evaporating saturation | Suction transducer (app) via PT chart; verify with gauge | Cooling: indoor coil thermistor. Heating: outdoor coil thermistor |
| `t_cond_sat` | Condensing saturation | High-side gauge via PT chart | Cooling: outdoor coil (mid) thermistor. Heating: indoor coil thermistor |
| `dsh` | `t_discharge - t_cond_sat` | App discharge temp if shown, else clamp 6" from compressor | App discharge pipe thermistor |
| `ssh` | `t_suction_line - t_evap_sat` | Probe at suction service valve | Probe at gas valve (cooling only) |
| `sc` | `t_cond_sat - t_liquid_line` | Probe at liquid service valve; target from nameplate/IM | Rarely used; charge by weight |
| `approach` | `t_outdoor_coil - t_ambient` (cooling) | App coil + ambient, ambient verified by probe | App outdoor coil + outdoor air |
| `split_heat` | `t_ambient - t_outdoor_coil` (heating) | App | App |
| `dew_margin` | `dp_room - t_evap_sat` | Probe room dew point, app suction sat | Probe room dew point, app indoor coil |
| `speed_locked` | Fixed speed, stable >= 10 min | Charge/test mode | Forced cooling or test run |

## Outdoor conditions context

| Outdoor air | Normal | Watch for | Rules |
|---|---|---|---|
| Above 95°F, cooling | High head, higher discharge, board may cap speed on high-pressure control | Recirculation (FIT side discharge), dirty coils, derate mistaken for low charge | L5, S7, M4 |
| 80–95°F, cooling | Best window to verify charge at locked speed | Anything outside SH/SC/discharge bands is real | L1, L3, S1, S2, M1 |
| 65–80°F, high outdoor dew point | Low sensible load, compressor near minimum or cycling | Humidity danger zone | L6, S11, S12, M12–M14 |
| Below ~60°F, cooling | Low head, cold coil, charge readings unreliable | Indoor coil freezing; low-ambient setup; weigh in charge | S4, M5, M9 |
| 40–60°F, heating | Light load, low speed; supply air in the 90s°F is normal | "Blowing cold air" calls that aren't failures | S9, M17 |
| 28–40°F, heating, humid | Heaviest frosting, most frequent defrost | Base pan ice, missed or false defrosts | S10, M8 |
| 5–28°F, heating | Long runtimes, high speeds, fewer defrosts (drier air) | Outdoor coil split widening without defrost; capacity vs heat loss | S9, M7 |
| Below model's rated capacity point | Capacity drops; missing setpoint can be normal (Aurora runs to -13°F) | Backup heat sequencing, not refrigeration faults | M7 |


## Laws (apply to both equipment types)

### L1: Lock the speed before you judge the charge

- **id:** `L1`
- **category:** `law`
- **severity:** `law`

**Rule:** No pressure, superheat or subcooling reading on an inverter means anything until the compressor is held at a known, fixed speed and stable for 10–15 minutes.

**Why:** Every refrigerant number moves with compressor speed. A suction pressure that's perfect at high speed is a problem at low speed, and the board is moving the EEV and outdoor fan at the same time it ramps.

**Readings:**

- App: compressor speed (Hz or rps) holding steady; EEV position and outdoor fan speed steady.
- Probe: return and supply temps stable within 1°F for 5 minutes.

**Fix:**

1. FIT: use the charge or test mode described in the installation manual so the compressor holds a fixed speed.
2. Mini split: forced cooling or test run from the remote or the outdoor unit's button.
3. Record the speed next to every reading you log.

**Logic:**

```
valid_reading = speed_locked
  AND abs(delta_speed_10min) < 5%
  AND stable_minutes >= 10
```

### L2: Prove the sensors before you trust the math

- **id:** `L2`
- **category:** `law`
- **severity:** `law`

**Rule:** With the system off 30+ minutes, every outdoor thermistor should read within about 3°F of true outdoor air, and the FIT suction transducer should match your gauge within about 3 psi. A sensor that fails this disqualifies every calculation that uses it.

**Why:** Inverters control off their own sensors. An open or shorted thermistor throws a code. A drifted one doesn't; it quietly makes the board chase the wrong target and the system acts sick for no visible reason.

**Readings:**

- App: every thermistor value at rest; suction pressure at rest.
- Probe: shaded outdoor air near the coil; gauge pressure at the service port.

**Fix:**

1. Resistance-check the suspect thermistor against the service manual's table at a measured temperature.
2. Check connector seating, pinched leads and sensor clip contact before blaming the board.

**Logic:**

```
FOR s IN thermistors:
  IF system_off_min >= 30
   AND abs(t[s] - t_ambient_probe) > 3
  THEN flag sensor_drift(s)
```

### L3: Discharge temperature is the truth serum

- **id:** `L3`
- **category:** `law`
- **severity:** `law`

**Rule:** Discharge superheat (discharge line temp minus condensing saturation) around 25–60°F is healthy. Above ~80°F the compressor is starving. Below ~20°F it's flooding.

**Why:** Discharge temperature sums up charge, metering, airflow and compression in one number that's hard to fake. Daikin mini split boards steer the EEV by it, so it's the first place a problem shows.

**Readings:**

- App: discharge thermistor.
- Condensing sat: high-side gauge, or on a mini split in cooling, the outdoor coil thermistor.
- Probe: clamp 6" from the compressor to verify the app.

**Fix:**

1. High: go to S2 or M1.
2. Low: go to S1 or M3.
3. On R-32, use the model's protection threshold rather than R-410A habits.

**Logic:**

```
dsh = t_discharge - t_cond_sat
IF dsh > 80 -> starving
IF dsh < 20 -> flooding
```

### L4: Speed tells you load versus capacity

- **id:** `L4`
- **category:** `law`
- **severity:** `law`

**Rule:** A compressor pinned at max speed for 30+ minutes without satisfying is a capacity problem. A compressor hunting up and down every few minutes is a control, sensor, airflow or oversizing problem.

**Why:** An inverter should find a steady speed that matches load. Where it settles, or fails to, separates a weak machine from a confused one.

**Readings:**

- App: speed trend, target vs actual temperature, runtime.

**Fix:**

1. Pinned high: run the triage in S6 or M7.
2. Hunting: sensor placement, thermostat location, airflow, then sizing.

**Logic:**

```
IF speed >= 0.95*max FOR 30 min
   AND setpoint_unmet -> capacity_deficit
IF speed_reversals > 4 per 15 min -> hunting
```

### L5: Protection control looks weak before it looks broken

- **id:** `L5`
- **category:** `law`
- **severity:** `law`

**Rule:** Before a Daikin inverter throws a code, it derates, pulling speed down for high discharge temp, high pressure, freeze-up, current or heat-sink temperature. Runs but can't keep up, with no code, means find what the board is protecting.

**Why:** Techs chase charge or sizing while the board quietly caps speed to protect itself.

**Readings:**

- App: actual vs target speed; discharge, outdoor coil, indoor coil, current and heat-sink temps; stored fault and retry history.

**Fix:**

1. Find which limit is close to its threshold and fix the cause: dirty coil, recirculation, airflow, charge, power.

**Logic:**

```
IF speed < target_speed FOR 10 min
   AND any(limit_margin < 10%)
THEN protection_derate(limit)
```

### L6: The coil must beat the dew point

- **id:** `L6`
- **category:** `law`
- **severity:** `law`

**Rule:** The indoor coil must run about 10°F or more below the room's dew point to remove meaningful moisture. At or above the dew point it removes none, no matter how long it runs. Target room dew point is 55°F or lower (about 50% RH at 75°F).

**Why:** Inverters love slow, warm coils. Great for efficiency, bad for moisture. Nearly every inverter humidity complaint ends here.

**Readings:**

- Probe: room dry bulb and RH, converted to dew point.
- App: suction saturation (FIT) or indoor coil thermistor (mini split).

**Fix:**

1. Lower the coil temperature: less airflow per ton, dehumidification settings, fan auto instead of on, Dry mode on mini splits, and check sizing.

**Logic:**

```
dew_margin = dp_room - t_evap_sat
IF dew_margin < 5  -> no_latent
IF dew_margin < 10 -> weak_latent
```


## Split systems: Daikin FIT

### S1: Liquid returning to the compressor

- **id:** `S1`
- **category:** `split`
- **severity:** `critical`

**Rule:** At a locked speed, suction superheat at the outdoor unit under ~5°F or discharge superheat under ~20°F means liquid floodback. Stop and find it.

**Why:** The FIT's swing compressor doesn't tolerate oil dilution. Floodback washes oil off the bearings and kills compressors slowly without throwing a code first.

**Readings:**

- App: suction pressure (to saturation), discharge temp, speed.
- Probe: suction line temp at the service valve; sweating or frost on the suction line at the unit.

**Fix:**

1. Cooling: indoor airflow first (filter, blower setting, closed registers), then TXV bulb contact and insulation, then overcharge against nameplate subcooling.
2. Heating: outdoor EEV operation and overcharge.
3. A short low-superheat spike right after defrost is normal; judge after recovery.

**Logic:**

```
IF speed_locked
   AND (ssh < 5 OR dsh < 20)
   AND minutes_since_defrost > 5
THEN CRITICAL floodback
```

### S2: Starved compressor, high discharge

- **id:** `S2`
- **category:** `split`
- **severity:** `critical`

**Rule:** At a locked speed, discharge superheat above ~80°F, or a discharge line above ~225°F on R-410A, means a starved compressor.

**Why:** Hot discharge breaks down POE oil and cooks windings. The board derates first, so this usually shows up as low capacity before it shows up as a code.

**Readings:**

- App: discharge temp (or clamp probe), suction pressure, speed.
- Probe: subcooling at the liquid valve; temperature drop across the field-installed bi-flow drier.

**Fix:**

1. High superheat with low subcooling: undercharge. Leak search, repair, evacuate to 500 microns with a decay test, weigh in.
2. High superheat with normal or high subcooling: restriction. Drier, kinked line set, starving TXV.
3. More than 3°F drop across the drier: replace the drier.

**Logic:**

```
IF dsh > 80 AND sc < sc_target - 3 -> undercharge
IF dsh > 80 AND sc >= sc_target  -> restriction
IF drier_delta_t > 3              -> drier_restricted
```

### S3: Power quality at the drive

- **id:** `S3`
- **category:** `split`
- **severity:** `critical`

**Rule:** Supply voltage must stay inside the nameplate range at full compressor speed and drop no more than ~3% from idle to max speed.

**Why:** The inverter drive is rectifiers and capacitors. Low or sagging voltage drives current up and heats the power module. Loose lugs show up here first, and they end in drive faults or a dead board.

**Readings:**

- Probe: voltage at the disconnect and at the unit terminals, idle vs max speed; amps vs speed.
- App: compressor current if shown; fault history for voltage or current trips.

**Fix:**

1. Torque lugs; check disconnect, whip, conductor size and utility supply.
2. Don't replace a board that tripped on bad power until the power is fixed.

**Logic:**

```
IF v_load < nameplate_min
   OR (v_idle - v_load)/v_idle > 0.03
THEN CRITICAL power
```

### S4: Indoor coil freezing in cooling

- **id:** `S4`
- **category:** `split`
- **severity:** `major`

**Rule:** Evaporating saturation below 32°F sustained in cooling means the coil is freezing. Ice that reaches the suction line at the outdoor unit turns into floodback (S1).

**Why:** Ice chokes airflow, which drops pressure further. When it thaws, it sends liquid back to the compressor.

**Readings:**

- App: suction pressure to saturation, speed.
- Probe: supply air temp; visual ice on the coil or suction line.

**Fix:**

1. Airflow first (filter, blower setting, static, closed dampers), then charge, then low-ambient cooling operation, then metering.

**Logic:**

```
IF mode = cool
   AND t_evap_sat < 32 FOR 10 min
THEN freeze
```

### S5: Suction transducer disagrees with your gauge

- **id:** `S5`
- **category:** `split`
- **severity:** `major`

**Rule:** The FIT's suction pressure transducer should match a known-good gauge within about 3 psi at any operating point.

**Why:** The board uses that transducer for control and protection. When it lies, a healthy system acts sick and a sick system looks fine in the app.

**Readings:**

- App: suction pressure.
- Probe: gauge at the suction service port, same moment.

**Fix:**

1. Verify your gauge, then the transducer connector and harness, then replace the transducer.

**Logic:**

```
IF abs(p_suction_app - p_suction_gauge) > 3
THEN transducer_suspect
```

### S6: Pinned at max speed and not satisfying

- **id:** `S6`
- **category:** `split`
- **severity:** `major`

**Rule:** Classify the capacity deficit by which numbers are off: charge, airflow, protection, or load.

**Why:** Every one of these looks like "not cooling" to the homeowner. The readings separate them in one visit.

**Readings:**

- App: speed vs max and vs target; suction pressure; discharge temp.
- Probe: superheat, subcooling, return-to-supply ΔT, total external static.

**Fix:**

1. High superheat, low subcooling: charge (S2).
2. Normal refrigeration, low ΔT: airflow or ducts (S8).
3. Normal refrigeration and ΔT: load exceeds capacity; check sizing and duct leakage.
4. Speed below max with no code: protection derate (L5).

**Logic:**

```
IF ssh high AND sc low           -> charge
ELIF refrig_ok AND delta_t < 14   -> airflow
ELIF refrig_ok AND delta_t ok     -> load_gt_capacity
ELIF speed < max AND no_code      -> derate
```

### S7: High head from recirculation or a dirty coil

- **id:** `S7`
- **category:** `split`
- **severity:** `major`

**Rule:** Condenser approach above ~25°F at high speed, or the unit's ambient sensor reading more than ~5°F above your probe 3 feet out, means hot air is recirculating or the coil is dirty.

**Why:** The FIT blows horizontally. A fence, wall or shrub inside the clearance throws that air straight back into the intake. The board sees hotter ambient, head climbs, and it derates.

**Readings:**

- App: outdoor coil temp and ambient temp.
- Probe: shaded outdoor air 3 feet from the intake.

**Fix:**

1. Restore the clearances in the installation manual.
2. Clean the coil inside out; check fan speed against command; rule out overcharge.

**Logic:**

```
approach = t_outdoor_coil - t_ambient_probe
IF approach > 25 AND speed >= 0.8*max -> high_head
IF t_ambient_app - t_ambient_probe > 5 -> recirculation
```

### S8: Airflow outside the window

- **id:** `S8`
- **category:** `split`
- **severity:** `major`

**Rule:** Cooling airflow should be about 350–400 CFM per ton, lower when dehumidifying, with total external static at or under the blower table's limit (typically 0.5" w.c.). Return-to-supply ΔT at high speed runs about 16–22°F.

**Why:** Too much air makes a warm coil and a humid house. Too little makes a cold coil, freezing and floodback.

**Readings:**

- Probe: total external static; return and supply dry bulb and wet bulb.
- App or thermostat: blower CFM demand on communicating equipment.

**Fix:**

1. Filter, duct restrictions, blower configuration in the Daikin One+ installer settings.

**Logic:**

```
IF tesp > 0.5        -> restricted
IF delta_t < 14      -> airflow_high
IF delta_t > 24      -> airflow_low
```

### S9: Heating: outdoor coil split

- **id:** `S9`
- **category:** `split`
- **severity:** `major`

**Rule:** In heating at speed, the outdoor coil should run about 10–20°F colder than outdoor air. More than ~25–30°F colder means frost or lost airflow. Less than ~5°F colder means the unit isn't picking up heat: low charge or metering.

**Why:** The outdoor coil is the evaporator in heating. Its split from ambient is the heating-mode version of evaporator ΔT.

**Readings:**

- App: outdoor coil and ambient temps, speed.
- Probe: supply air temperature rise indoors.

**Fix:**

1. Too wide: look for ice, check the fan, defrost initiation and coil sensor position.
2. Too narrow: confirm charge. Verify in cooling when weather allows; in heating, weigh in or use the manufacturer's heating data.

**Logic:**

```
split_heat = t_ambient - t_outdoor_coil
IF split_heat > 28                     -> frost_or_airflow
IF split_heat < 5 AND speed >= 0.6*max -> low_heat_pickup
```

### S10: Defrost behavior

- **id:** `S10`
- **category:** `split`
- **severity:** `major`

**Rule:** Intelligent Defrost should start on frost, not a clock. Defrosting a clean coil is a sensor or logic problem. A heavily iced coil with no defrost is a coil sensor or board problem.

**Why:** Frost is heaviest at 28–40°F in humid air. Missed defrosts build ice from the base pan up; false defrosts waste energy and cause cold-air complaints.

**Readings:**

- App: defrost count or log; outdoor coil temp at start and end of defrost.
- Visual: frost pattern and base pan.

**Fix:**

1. Check coil thermistor mounting and clip; clear base pan drainage; raise unit above snow line; review fault history.

**Logic:**

```
IF defrosts_per_hr > expected(t_ambient) AND coil_clean -> false_defrost
IF ice_visible AND no_defrost_90min -> defrost_failure
```

### S11: Mild, muggy days are the humidity danger zone

- **id:** `S11`
- **category:** `split`
- **severity:** `moderate`

**Rule:** Expect humidity complaints when it's about 65–80°F outside with a high outdoor dew point. Sensible load is small, the compressor sits near minimum, and the coil never gets cold enough.

**Why:** The FIT can satisfy the thermostat long before it satisfies the moisture. Hot days self-correct because the system runs hard; shoulder days don't.

**Readings:**

- Probe: outdoor temp and dew point; room dew point.
- App: speed near minimum; suction saturation against room dew point (L6).

**Fix:**

1. Enable dehumidification in the Daikin One+ (reduced dehum airflow, overcool within a set limit).
2. Confirm the system isn't grossly oversized.
3. If airflow and settings can't fix it, add whole-house dehumidification.

**Logic:**

```
IF 65 <= t_out <= 80 AND dp_out >= 60
   AND dp_room > 55
   AND speed <= min_speed * 1.1
THEN shoulder_humidity
```

### S12: Continuous fan puts the water back

- **id:** `S12`
- **category:** `split`
- **severity:** `moderate`

**Rule:** With the blower on continuous in cooling, the moisture the coil just pulled out gets blown back into the house between compressor cycles.

**Why:** The wet coil becomes a humidifier. Homeowners do this for air circulation and never connect it to the sticky feeling.

**Readings:**

- Probe: room RH climbing while the compressor is off; supply dew point higher than return during the off cycle.

**Fix:**

1. Fan on auto during cooling season. If circulation is wanted, use the thermostat's dehumidification settings instead.

**Logic:**

```
IF fan_mode = on AND compressor = off
   AND dp_supply > dp_return + 1
THEN reevaporation
```

### S13: Return leak pulling humid air

- **id:** `S13`
- **category:** `split`
- **severity:** `moderate`

**Rule:** If the return air dew point at the unit is more than ~2°F higher than the room's dew point, the return is pulling attic, garage or crawlspace air.

**Why:** It hands the coil a moisture load it was never sized for, and it looks exactly like "the system can't dehumidify."

**Readings:**

- Probe: dew point in the room and in the return at the unit, same visit.

**Fix:**

1. Seal the return plenum, filter rack, panned joists and platform returns.

**Logic:**

```
IF dp_return_at_unit - dp_room > 2
THEN return_leak
```

### S14: Check the settings before the refrigeration

- **id:** `S14`
- **category:** `split`
- **severity:** `minor`

**Rule:** Quiet mode, boost mode, capacity limits, airflow trims and dehum settings all change speed and capacity. Confirm them before you chase a capacity complaint.

**Why:** A quiet-mode limit looks exactly like a weak system.

**Readings:**

- Thermostat: Daikin One+ installer settings.
- Outdoor board: field settings.

**Fix:**

1. Document the settings on the work order so the next tech doesn't chase it again.

**Logic:**

```
IF (quiet_mode OR capacity_limit) AND capacity_complaint
THEN check_config
```

### S15: Read the fault history first

- **id:** `S15`
- **category:** `split`
- **severity:** `minor`

**Rule:** Pull stored fault codes and their counts before touching anything. A code that clears itself and repeats is a pattern, not a fluke.

**Why:** The seven-segment display and stored history tell you what happened while nobody was watching.

**Readings:**

- Outdoor board: seven-segment display and stored faults.
- App: fault history.

**Fix:**

1. Log codes, counts and outdoor temp at time of fault when available.

**Logic:**

```
IF count(fault_code, 30 days) >= 3
THEN recurring(fault_code)
```


## Mini splits: Aurora, standard and multi-zone

### M1: Low charge: EEV wide open, discharge still hot

- **id:** `M1`
- **category:** `mini`
- **severity:** `critical`

**Rule:** EEV near fully open and discharge temp still high (discharge superheat above ~80°F, figured as discharge thermistor minus outdoor coil thermistor in cooling) means low charge until proven otherwise.

**Why:** Daikin mini split boards steer the EEV to a target discharge temperature. When the EEV runs out of travel and still can't bring discharge down, there isn't enough refrigerant. U0 (insufficient gas) and F3 (discharge temp control) are the board reaching the same conclusion.

**Readings:**

- App: discharge, outdoor coil, indoor coil, EEV pulses or % open, frequency; U0 or F3 in history.
- Probe: suction line temp at the gas valve in cooling.

**Fix:**

1. Leak search the flares first; they're the most common leak on these. Then brazes, then the indoor coil.
2. Recover, repair, pull to 500 microns with a decay test, weigh in nameplate charge plus the line-length adder.
3. Don't top off by feel.

**Logic:**

```
dsh = t_discharge - t_outdoor_coil   # cooling
IF eev_open >= 90% AND dsh > 80 -> CRITICAL undercharge
IF code IN [U0, F3]           -> confirm_undercharge
```

### M2: Multi-zone cross-piped or cross-wired

- **id:** `M2`
- **category:** `mini`
- **severity:** `critical`

**Rule:** Run one head at a time. That head's coil thermistor must move (drop in cooling, rise in heating) within a few minutes while the others stay near room temp. If a different head moves, piping and wiring don't match.

**Why:** The outdoor board opens room A's EEV for room A's call. If room A's wires land on room B's piping, one head floods and one starves. That damages the compressor and neither room ever makes setpoint.

**Readings:**

- App: each indoor coil thermistor, each zone EEV, room temps.

**Fix:**

1. Use the outdoor unit's wiring-error check function where equipped.
2. Fix the wiring (easier than re-piping) and re-test every zone.

**Logic:**

```
FOR z IN zones:
  run_only(z)
  IF delta_t_coil(z) < 5
     AND any(delta_t_coil(other) >= 5)
  THEN crossed(z, other)
```

### M3: Flooding: overcharge or EEV stuck open

- **id:** `M3`
- **category:** `mini`
- **severity:** `critical`

**Rule:** Discharge superheat under ~20°F at steady operation means liquid is getting back. EEV mostly closed points to overcharge; EEV mostly open points to a stuck valve.

**Why:** Common after the line-length adder gets applied twice, charge gets added for a line set shorter than the precharge length, or someone topped off with gauges on.

**Readings:**

- App: discharge, outdoor coil, EEV pulses; F6 or high-pressure codes on some models.

**Fix:**

1. Recover and weigh in the exact charge.
2. Check EEV coil resistance and that the pulse count actually changes the refrigerant temps.

**Logic:**

```
IF dsh < 20 AND eev_open < 30%  -> overcharge
IF dsh < 20 AND eev_open >= 70% -> eev_stuck_open
```

### M4: Drive stress: current, voltage and heat-sink trips

- **id:** `M4`
- **category:** `mini`
- **severity:** `critical`

**Rule:** Overcurrent, low-voltage and heat-sink temperature trips (the L5, E8, U2 and L4 family on most Daikin mini splits; confirm against the model's code list) mean the drive is being stressed. Find the stress; don't reset and leave.

**Why:** The power module is the most expensive part of the outdoor unit after the compressor, and repeat trips shorten its life.

**Readings:**

- App: current, heat-sink or fin temp, outdoor fan speed.
- Probe: voltage under load at the unit.

**Fix:**

1. Voltage and connections first; clear the heat-sink airflow path and outdoor coil; verify the fan.
2. If overcurrent repeats, check compressor windings and insulation before replacing the board.

**Logic:**

```
IF code IN drive_trip_codes
   OR (t_fin > fin_limit - 10 AND speed_derated)
THEN CRITICAL drive_stress
```

### M5: Freeze-up protection in cooling

- **id:** `M5`
- **category:** `mini`
- **severity:** `major`

**Rule:** The indoor coil thermistor sustained below ~32°F triggers freeze-up protection (A5 on many heads). It's a symptom: airflow first, then charge, then low ambient.

**Why:** Caked blower wheels are the number one airflow killer on wall mounts, and they look fine from the front.

**Readings:**

- App: indoor coil temp, indoor fan speed, frequency, outdoor air temp.

**Fix:**

1. Filter, coil face, blower wheel, fan setting.
2. Charge per M1.
3. Low ambient per M9.

**Logic:**

```
IF mode = cool
   AND t_indoor_coil < 32 FOR 10 min
THEN freeze_protect
```

### M6: Heating peak-cut from high head

- **id:** `M6`
- **category:** `mini`
- **severity:** `major`

**Rule:** In heating, the indoor coil thermistor sits close to condensing temperature. At max speed it normally runs roughly 95–120°F. When it climbs past that with weak airflow, the board cuts speed.

**Why:** A dirty filter in heating doesn't just cut comfort. It drives head pressure into the board's limit and the whole system derates.

**Readings:**

- App: indoor coil temp, frequency, indoor fan speed.
- Probe: supply air temp.

**Fix:**

1. Filter, coil, blower wheel; fan not stuck on quiet or low; rule out overcharge.

**Logic:**

```
IF mode = heat
   AND t_indoor_coil > 125
   AND speed < target_speed
THEN peak_cut
```

### M7: Cold-weather heating capacity

- **id:** `M7`
- **category:** `mini`
- **severity:** `major`

**Rule:** Aurora models hold full rated heating capacity only down to their rated point (5°F on older R-410A models, 0°F on newer R-32 models) and keep running to -13°F. Below the rated point, long runtimes at max speed are normal and missing setpoint may be too.

**Why:** Capacity complaints in a cold snap are often the heat loss outrunning the unit, not a refrigeration fault.

**Readings:**

- App: frequency at max, outdoor air temp, indoor coil temp.
- Probe: supply air temperature rise.

**Fix:**

1. Compare the model's capacity at design temperature to the room's heat loss; plan backup heat below the balance point.
2. If the unit is at max speed with indoor coil under ~90°F in moderate weather, suspect charge (M1).

**Logic:**

```
IF speed >= 0.95*max AND t_ambient < rated_cap_point
   -> expected_shortfall
IF speed >= 0.95*max AND t_ambient > 30
   AND t_indoor_coil < 90 -> low_charge_suspect
```

### M8: Base pan ice and outdoor fan lock

- **id:** `M8`
- **category:** `mini`
- **severity:** `major`

**Rule:** In freezing weather, ice that builds up from the base pan will eventually stop the outdoor fan (E7) and crush fins.

**Why:** Defrost water that can't drain refreezes each cycle and grows upward into the fan.

**Readings:**

- App: outdoor fan speed vs command; E7 in history.
- Visual: base pan and lower coil.

**Fix:**

1. Mount on a stand above the snow line, clear the drain path, keep it out from under roof drip lines.
2. Use the base pan heater where the model calls for it.

**Logic:**

```
IF mode = heat AND t_ambient < 32
   AND fan_rpm < 0.7 * fan_cmd
THEN ice_or_fan_fault
```

### M9: Cooling when it's cold outside

- **id:** `M9`
- **category:** `mini`
- **severity:** `major`

**Rule:** Cooling in cold weather (sunrooms, server closets) drops head pressure. Without the model's low-ambient setup, such as a wind baffle, the indoor coil freezes.

**Why:** Low head means low evaporator pressure. The board protects on freeze-up, the room never cools, and the tech chases charge.

**Readings:**

- App: outdoor air, outdoor coil, indoor coil, frequency.

**Fix:**

1. Confirm the model's cooling range and install the low-ambient accessories it requires.

**Logic:**

```
IF mode = cool
   AND t_ambient < model_cool_min + 10
   AND t_indoor_coil < 35
THEN low_ambient_freeze
```

### M10: Thermistor codes and silent drift

- **id:** `M10`
- **category:** `mini`
- **severity:** `major`

**Rule:** An open or shorted thermistor throws a code (on most Daikin mini splits: J3 discharge, J6 outdoor coil, H9 outdoor air, C4 indoor coil, C9 room). A drifted one throws nothing; use Law 2.

**Why:** Drift is worse than failure because every rule that uses that sensor gives a wrong answer with confidence.

**Readings:**

- App: thermistor values at rest and in operation.
- Probe: surface temp at the sensor location.

**Fix:**

1. Resistance-check against the service manual table at a measured temperature; replace the sensor before the board.

**Logic:**

```
IF code IN thermistor_codes -> replace_or_repair(sensor)
IF sensor_drift(s) (L2)      -> replace(s)
```

### M11: Communication errors aren't refrigeration

- **id:** `M11`
- **category:** `mini`
- **severity:** `major`

**Rule:** U4 means the indoor and outdoor units can't talk. UA means they don't accept each other as a valid pair. Neither is a refrigerant problem.

**Why:** Techs lose hours checking charge on a unit that's simply not being told to run.

**Readings:**

- Probe: interconnect wiring and terminal voltages.
- App: model IDs of each unit.

**Fix:**

1. Continuous interconnect with correct conductor count, no splices in the wall, correct terminal order and ground.
2. For UA, confirm the indoor and outdoor models are an approved combination.

**Logic:**

```
IF code = U4 -> check_interconnect
IF code = UA -> check_pairing
```

### M12: Oversized head, short cycles, sticky room

- **id:** `M12`
- **category:** `mini`
- **severity:** `moderate`

**Rule:** If a head satisfies the room in under ~10 minutes of compressor run and shuts off, it can't dehumidify. The coil barely gets below dew point before it stops.

**Why:** A big head in a small bedroom, or a room smaller than the head's minimum output, cycles instead of running slow.

**Readings:**

- App: frequency and on/off times; indoor coil vs room dew point across the cycle.

**Fix:**

1. Dry mode, fan on auto or low, avoid Powerful mode.
2. Long term: right-size the head, or use a smaller head on a multi.

**Logic:**

```
IF avg_on_minutes < 10 AND rh_room > 55
THEN oversized_cycling
```

### M13: Fan on high in humid weather

- **id:** `M13`
- **category:** `mini`
- **severity:** `moderate`

**Rule:** A wall mount locked on high fan in humid weather raises the coil temperature. The room reaches setpoint at 60%+ RH.

**Why:** More air across the coil means a warmer coil. It's Law 6 in its most common form.

**Readings:**

- App: indoor coil temp.
- Probe: room dew point.
- Remote: fan setting.

**Fix:**

1. Fan on auto or low, or Dry mode. Show the homeowner why.

**Logic:**

```
IF fan_setting = high AND dew_margin < 10
THEN fan_humidity
```

### M14: Indoor fan running after the compressor stops

- **id:** `M14`
- **category:** `mini`
- **severity:** `moderate`

**Rule:** If the head's fan keeps blowing after the compressor stops in cooling, the water on the coil goes back into the room.

**Why:** Same physics as S12. It's the fixed fan speed setting doing it, not a failure.

**Readings:**

- Probe: room RH trend during compressor-off time.
- App: indoor coil warming while the fan runs.

**Fix:**

1. Fan on auto, or Dry mode for humid spells.

**Logic:**

```
IF compressor = off AND indoor_fan = on
   AND rh_room rising
THEN reevaporation
```

### M15: The head reads the ceiling, not the room

- **id:** `M15`
- **category:** `mini`
- **severity:** `moderate`

**Rule:** If the head's room thermistor reads more than ~4°F off from your probe at 5 feet, the head is controlling on stratified air.

**Why:** In heating it satisfies on warm ceiling air and leaves the floor cold. In cooling, a head tucked in an alcove can short-cycle on its own discharge.

**Readings:**

- App: room thermistor.
- Probe: air temp at 5 feet in the middle of the room.

**Fix:**

1. Use a remote or wired controller with its own sensor where supported; adjust louver direction; set expectations on setpoint.

**Logic:**

```
IF abs(t_room_app - t_room_probe_5ft) > 4
THEN stratification
```

### M16: Gauges cost charge: diagnose from thermistors first

- **id:** `M16`
- **category:** `mini`
- **severity:** `moderate`

**Rule:** Connect gauges only when the thermistors give you a reason. Most wall-mount outdoor units have one service port on the gas valve: low side in cooling, high side in heating.

**Why:** On a system holding a couple of pounds, every hookup and every hose removed on the high side costs a measurable share of the charge.

**Readings:**

- App: discharge, outdoor coil, indoor coil and EEV tell the charge story without a gauge.

**Fix:**

1. Use low-loss fittings; connect and disconnect in cooling when the port is on the low side.

**Logic:**

```
IF thermistor_rules_inconclusive
THEN gauges_ok
ELSE skip_gauges
```

### M17: Normal behavior that generates callbacks

- **id:** `M17`
- **category:** `mini`
- **severity:** `minor`

**Rule:** Defrost (fan stops, steam, whoosh, reversing valve click), hot start (no indoor air until the coil warms), oil return cycles, and idle heads on a multi warming slightly or ticking as EEVs bleed are all normal.

**Why:** Knowing normal saves a truck roll and keeps the customer's trust.

**Readings:**

- App: operating mode and defrost flag at the time of the complaint.

**Fix:**

1. Explain it to the homeowner; leave a one-page "what's normal" sheet.

**Logic:**

```
IF complaint IN normal_behaviors
   AND mode_matches
THEN educate_no_repair
```

### M18: Filters and blower wheel, before they become M5 or M6

- **id:** `M18`
- **category:** `mini`
- **severity:** `minor`

**Rule:** Dirty filters and blower wheels quietly cost efficiency long before they cause freeze-up in cooling or peak-cut in heating.

**Why:** This is the maintenance-visit rule. Catch it here and M5 and M6 never happen.

**Readings:**

- App: indoor coil temp trending colder in cooling or hotter in heating at the same speed and conditions, visit over visit.

**Fix:**

1. Clean filters, coil and wheel on every maintenance visit; log the indoor coil temp at a locked speed as a baseline.

**Logic:**

```
IF trend(t_indoor_coil at locked speed) drifting > 4F from baseline
THEN clean_airpath
```

## Appendix: rules added by the app (not in the original spec)

### X1: Stuck sensor (under L2 / M10)

- **severity:** `major`
- **Rule:** A thermistor or transducer that holds one exact value for 20+ minutes (60 for outdoor air, 15 for pressures) while the compressor speed moves 5+ rps or a neighbouring sensor of the same kind moves 3+ °F is stuck.
- **Why:** A live sensor never sits on one exact value that long while the system changes. Open or shorted sensors throw codes; stuck or bridged ones do not.
- **Fix:** Clamp a probe at the sensor; resistance-check against the service manual; connector, pinched leads, clip contact.
- **Logic:** `same_value_minutes >= 20 AND (rps_range >= 5 OR any(other_sensor_range >= 3))`

### X2: Implausible reading against neighbours (under L2 / M10)

- **severity:** `major`
- **Rule:** For 10+ minutes while settled: an outdoor coil or pipe sensor more than 90 °F from outdoor air; discharge colder than the outdoor coil; high pressure at or below low pressure; indoor gas vs liquid more than 60 °F apart; a head coil more than 45 °F from its return air while its fan runs; a port's gas and liquid more than 45 °F apart while the port is open.
- **Why:** The refrigerant cannot be in that state, so one of the two sensors is wrong, misplaced or on the wrong pipe.
- **Fix:** Probe next to each sensor to find which one disagrees with reality; check placement and clip; resistance-check.

### X3: Noisy sensor

- **severity:** `major`
- **Rule:** Three or more single-row jumps of more than 30 °F (100 psi) that vanish on the next row.
- **Fix:** Wiggle-test the connector and harness; look for chafe at sheet-metal pass-throughs.

### V1 / V2: EEV not responding (under S2 / M3)

- **severity:** `major`
- **Rule:** After a pulse move of 40+ pulses (60 on the FIT indoor EV) at steady compressor speed, the temperature that valve meters must change by at least 1 °F in the expected direction within 8 minutes. FIT outdoor EV in heating: suction superheat falls when it opens. FIT indoor EV: coil gas − liquid falls (cooling), subcooling falls (heating). Mini-split port EV: that head's coil temperature falls when it opens in cooling, rises in heating. Four or more moves with 70 %+ unanswered = not responding.
- **Why:** The board is commanding the valve and the refrigerant is not following — a stuck body, a coil slipping steps, or a starved circuit that mutes the valve.
- **Fix:** EEV coil resistance and connector; watch pulses and the metered temperature together; replace coil, then body; rule out a starved circuit.
- **Logic:**
```
FOR each move WHERE |Δpulses| >= thr AND |Δrps| <= 5%:
  response = mean(metric, t+3..t+8) - mean(metric, t-3..t)
  answered = response * expected_sign >= 1.0
IF moves >= 4 AND unanswered/moves >= 0.7 -> eev_not_responding
```
