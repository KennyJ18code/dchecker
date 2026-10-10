# The calculated readings, explained

Everything the D-Checker log contains is one of two things: a **sensor** (a thermistor, a pressure transducer, a current transformer, a pulse count the board sent to a valve) or a **board value** (a target the control is aiming at, a mode, a flag). The app adds a third kind: **calculated** readings, derived from the sensors with physics. They are labelled "Calc" or "Calculated" wherever they appear. This document explains each one: what it is, how it is worked out, what it looks like on a healthy unit, and what moves it.

Units: °F, psig, rps (compressor revolutions per second), BTU/h. Enthalpy is in kJ/kg internally (CoolProp 8 tables for R-410A and R-32); you never see it, but it is the currency most of the capacity math is done in.

---

## Part 1 · The refrigerant state readings

These are the ones a tech would normally work out from gauges and a PT chart. The app does them from the unit's own transducers and thermistors on every row.

### Saturation temperatures: Te and Tc
The board logs its own `Evap temp` (Te) and `Cond temp` (Tc). Te and Tc are the board's figures. Te comes from the outdoor suction-side sensor. Tc is the coil thermistor Tm in FIT and Goodman cooling, and the indoor (FIT) or outdoor (DH9VS, Goodman) high-side sensor in heating (SiUS612209EA p.49). The DH9VS has no Tm; its high-side sensor serves in both modes (DH9VS install manual p.30, p.43). On the Goodman \*VZC20 the cooling Tc from Tm is inferred (RS6215002r10 p.95), and the heating Te is the board's estimate, because its one outdoor transducer then reads the discharge side (RS6215002r10 p.15, p.96). Most readings below use the board's Te and Tc. The indoor-coil readings use saturation at the indoor pressure sensor. The energy math in Part 3 converts `Low pressure` and `High pressure` itself, with the refrigerant in use (R-410A dew point, or R-32); on the FIT in cooling the logged high pressure is itself the board's figure from Tm, so there it is not independent of the board.

*Refrigerant check:* when the log does not state its refrigerant, the app compares the board's Te with sat(LP), and Tc with sat(HP), in both tables and takes the table that fits better; failing that, the model name decides. R-32 runs 1–17 psi higher than R-410A at the same temperature. This is not a sensor check: on the FIT in cooling the logged HP is the board's own figure from Tm, so Tc − sat(HP) only shows which table the board used (SiUS612209EA p.49).

### Suction superheat (SH) = suction temp − Te
How far the gas returning to the compressor is above its boiling point. It is the proof that the evaporator finished boiling the liquid and that no liquid reaches the compressor. Suction superheat is not what either valve controls. In cooling the indoor EEV holds the indoor coil's outlet superheat to **Target SH** (9 °F, 14 °F below 70 °F outdoor, SiUS612412E p.7). In heating the outdoor EEV holds suction − outdoor coil middle (Ts − Tm) at 7 °F on the R-32 FIT (SiUS612412E p.7). Low or zero = flooding (overfeed, too much charge, low airflow); high = starving (undercharge, restriction, a valve that cannot open far enough).

### Indoor coil ΔT (gas − liquid) = indoor gas temp − indoor liquid temp
Measured at the indoor coil's own two pipe thermistors. Not the coil superheat: in cooling the liquid thermistor reads two-phase refrigerant entering the coil (SiUS612412E p.9), so this reads lower than the coil's outlet superheat by the coil's pressure drop. The indoor coil superheat is indoor gas − saturation at the indoor pressure sensor. In heating the roles flip: the gas pipe is the hot inlet and the liquid pipe the cooled outlet, so the number is the temperature drop across the condenser.

### Subcooling (SC) = Tc − liquid pipe temp
How far the liquid leaving the condenser is below its condensing temperature. It is the proof there is a solid column of liquid at the metering device. The board logs a "Target SC"; no service manual says what it controls. **SC vs target** is the plain difference, not a control error. Low SC = low charge or a condenser that cannot reject heat; high SC = overcharge or a restriction downstream backing liquid up. The manuals' subcooling numbers are charge targets valid only in their test modes, measured with a gauge at the liquid stop valve: 7–10 ± 1 °F by size on the R-32 FIT in the charge verification test (DC6VS/DH6VS install manual p.31), 11 ± 1 °F on the DH9VS (DH9VS install manual p.26), 8 ± 1 °F on the Goodman \*VZC20 in charge mode (RS6215002r10 p.23–24). No DZ6VS charging table is on file.

### Subcooling at indoor coil (heating only) = saturation at the indoor pressure sensor (the board's Tc if none) − indoor liquid temp
In heating the indoor coil is the condenser, so its subcooling is measured at its outlet. The DH9VS also logs an "IDU Target SC"; no manual on file describes it. On the FIT the indoor EEV is fully open in heating (SiUS612412E p.7).

### Liquid line ΔT (heating only) = indoor liquid − outdoor liquid pipe
Temperature lost along the liquid line from the indoor coil to the outdoor unit. A few degrees is normal (a rule of thumb, not from the manuals). A large value means the line is flashing (pressure drop, undercharge, long or undersized line) or absorbing heat in an attic.

### Discharge superheat (DSH) = discharge temp − Tc
How much hotter the gas leaving the compressor is than its condensing temperature. It is the compressor's health line. The manuals' analysis charts flag discharge superheat under 20 °F, and over 70 °F (cooling) or 80 °F (heating) (SiUS612209EA p.12–13); the Goodman \*VZC20 charts use 20–70 °F (RS6215002r10 p.95–96). Low DSH = liquid reaching the compressor; in cooling the analysis charts mark low indoor airflow, a dirty indoor coil, indoor recirculation and overcharge for it. Very high DSH = the compressor is starving or worn: the charts mark low charge, a restriction or a stop valve not fully open, and also a failed reversing valve or outdoor solenoid valve, because hot gas leaking to the suction raises discharge superheat (SiUS612209EA p.12–13; RS6215002r10 p.95–96). On the DH9VS a blocked liquid injection circuit is a listed cause of high discharge temperature (DH9VS install manual p.32, p.34).

### Compression ratio = (HP + 14.7) / (LP + 14.7)
Absolute discharge pressure over absolute suction pressure. It is the mechanical workload on the compressor: 2–3 is easy, 4–5 is hard (cold heating) as a rule of thumb, and volumetric efficiency falls as it rises. The app uses it in the mass-flow model (Part 3).

### Lift = Tc − Te
The same workload in temperature terms: how far the heat pump has to lift heat. Small lift in mild weather, large lift in extremes. Many of the "calculated" numbers are most reliable when lift is large, and the app grades its confidence on it.

### Outdoor coil approach
- Cooling: **Tc − outdoor air**. How much hotter the condenser has to run than the air cooling it. 10–20 °F at full speed is a common rule of thumb (engineering figure, not from the manuals); it shrinks at low speed. A rising approach at the same speed means the coil is not rejecting heat: dirty, fan slow, recirculating.
- Heating: **outdoor air − Te**. The evaporator has to run colder than the outdoor air to absorb heat. Larger values mean a frosted or dirty coil, or a starving evaporator.

### Outdoor coil vs saturation
- Heating only: **OD coil temp − Te** (the mid-coil Tm where the log has it, else Tb). The outdoor coil thermistor should sit near saturation in the two-phase part of the coil; a big difference says the thermistor is in a region that has already finished its phase change, or has frost on it. There is no cooling version: in FIT cooling the board's Tc is the coil thermistor Tm itself (SiUS612209EA p.49), so it would compare Tm with itself.

### Outdoor EV % open and Indoor EV % open
Pulses ÷ the valve's ceiling. Outdoor valve: 480 where the manual gives it (SiUS612412E p.7); otherwise the highest count the log holds, labelled as from the recording. The app shows pulses only where the recording contradicts the manual (the R-32 FIT logs on file hold 327 in cooling, from the recordings) and on the Goodman \*VZC20, whose manual gives no pulse counts and whose outdoor valve is bypassed by a check valve in cooling (RS6215002r10 p.12–13). Indoor valve: 480, fully open (SiUS612412E p.7); pulses only on the Goodman. Multi ports: 480 full travel (SiUS612209EA p.134), with MXS/MXL limiting a running port to 450 (SiUS121736EA p.119) and MXM/MXT to 480 (SiUS122410EC p.162); the app scales each port by that running ceiling. The valve that is not controlling sits fully open by design: the outdoor EEV in cooling, the indoor EEV in heating (SiUS612412E p.7). A controlling valve pinned at its ceiling for long means the control wants more flow than it can get: low charge, a restriction upstream, or a valve not moving. One held near its minimum means the opposite.

### Compressor vs target = rps − target rps
The board logs the speed it is asking for. A sustained shortfall means something is capping speed: a current, discharge-temperature, or pressure drop control (the drop-control chips name which).

### INV current per rps = INV current ÷ compressor speed
Amps per unit of speed. For one unit at similar pressures it is nearly a constant; it climbs with compression ratio. A rise at the same speed and lift means the compressor is working harder for the same output: mechanical wear, or a motor/drive problem.

### Pressure sensor check
The indoor pressure sensor sits on the gas pipe at the indoor coil. In cooling that pipe is suction, so **LP − indoor pressure** should be a few psi (line pressure drop). In heating it is discharge, and the check only means something where HP is a separate sensor (DH9VS, Goodman): there **HP − indoor pressure** should be a few psi. On the FIT the heating HP is the indoor sensor itself (SiUS612412E p.48). A large or negative value says one of the transducers is off.

### Discharge vs isentropic
The app estimates what the discharge temperature *would* be for an ideal (isentropic) compression from the suction state to the discharge pressure, with k = 1.2, and reports **actual − ideal**. A real compressor is always hotter than ideal by a roughly steady amount for that lift. Growing = compressor heat and wear; negative = wet suction or hot gas bypassing.

### Slopes (5 min)
Discharge temperature, low pressure, outdoor EV and compressor speed each get a 5-minute linear trend in °F/min, psi/min, pulses/min, rps/min. They answer "is it moving, and which way" without staring at a trail, and they drive the steady-state detection below.

### Multi-zone only
- **Discharge vs target**: a multi's port EEVs steer discharge temperature to a target (Daikin's "indirect superheat control", SiUS121736EA p.121); this is that control's error.
- **Port X gas − liquid** (both measured in the outdoor unit, not across the coil, SiUS121736EA p.103) and **Port X EV %** per head: the per-port gas − liquid difference and EV position. A head with EV open and no gas − liquid difference is not doing anything; a head with EV closed and the fan on is re-evaporating liquid left in the coil.

---

## Part 2 · The analysis states (not readings, but they gate everything)

- **Running**: compressor speed > 0 and the compressor command not OFF (the DH9 reports a 10 rps standby that is not a run).
- **Steady**: for the last few minutes, speed, both pressures and the EV have all stayed within narrow bands. Refrigerant numbers are only judged steady-state; everything moves while the compressor ramps.
- **Locked speed**: speed held within a few percent for 10 min or more. Charge judgements need this.
- **Dropout**: a row where a pressure reads near zero or Tc is absurd; skipped by the ranges and baselines.
- **Baseline / range**: each reading's median and spread over the steady rows, and its min/max over the log.

---

## Part 3 · The energy readings (new)

These are the ones that answer "how much is the unit actually doing", and they deserve the deepest understanding because they stack several estimates.

### Outdoor unit input power (kW) = V × system current × 0.97
`Sys. Op. Current` is the outdoor unit's total draw (on every row checked it equals INV current + fan current). FIT logs have no voltage column, so V comes from Settings (240 V default; read it at the disconnect if you can). 0.97 is an assumed power factor; no service manual gives one. Error here is mostly the voltage you assume: a 230 V unit entered as 240 is 4 % high on everything downstream.

### Mass flow — the one number everything else hangs on

Capacity is mass flow × enthalpy change. The log has no flow meter, so mass flow has to be inferred. There are two independent ways, and the app uses both.

**Way 1: the compressor's energy balance.** A hermetic compressor is a sealed can with a motor inside it. Essentially all the electrical power that goes in comes out as energy in the gas: the shaft work compresses it, and the motor's heat is carried away by the suction gas flowing over the windings. Only a little escapes through the shell to the air (less with Daikin's sound blanket) or is lost in the drive electronics outside the can; the app allows 7 % for both. So:

```
ṁ = P_comp × (1 − 0.07) ÷ (h2 − h1)

P_comp = V × INV current × 0.97          watts into the compressor drive
h1     = enthalpy of the suction gas     from Te and suction superheat
h2     = enthalpy of the discharge gas   from Tc and discharge superheat
```

The denominator is where the risk is. h2 − h1 is the enthalpy rise *per pound* of gas. When the lift is small (a mild day, low speed) the compressor adds very little energy per pound, so the rise is small, so a few degrees of error on the discharge thermistor is a large fraction of it. The app measures this directly for every row: it recomputes h2 with the discharge 10 °F hotter and reports how much ṁ would change.

- **good**: ≤ 12 % change — large lift, trust it to about ±10–15 %
- **fair**: ≤ 20 %
- **poor**: more — small lift, trust it to about ±25 %

Both logs recorded so far were mild-weather logs: every DZ6 row was fair, every DH9 row poor. That is honest, not a defect; the winter and summer logs will be good.

There is also a built-in sanity check. From the same two enthalpies the app can compute the compressor's *apparent isentropic efficiency* (ideal enthalpy rise ÷ actual). On the DZ6 rows it is 0.72, which is where a rotary compressor typically sits (engineering figure, not from the manual). If the discharge thermistor were lying badly this would come out at 0.9 or 0.5.

**Way 2: displacement.** This is the formula the compressor manufacturer would use:

```
ṁ = displacement × rps × ρ_suction × η_v

displacement : cc swept per revolution, fixed for a given compressor
rps          : logged compressor speed
ρ_suction    : density of the suction gas, from Te and suction superheat (kg/m³)
η_v          : volumetric efficiency = 0.97 − 0.035 × (compression ratio − 2), held between 0.72 and 0.97
```

Volumetric efficiency is the fraction of the swept volume that actually gets filled with fresh gas each revolution; gas re-expanding from the clearance space and leakage past the vane take the rest, and both get worse as the pressure ratio climbs. The model above is a generic rotary-compressor curve (engineering assumption, not from the manuals).

Way 2 is robust at any lift (speed is exact, density is well measured) **but needs the displacement**, and Daikin does not publish it for the FIT compressors. So the app learns it: on every *good, steady* row ≥ 5 minutes into a run it solves Way 1 for ṁ and then Way 2 backwards for displacement. Once it has 12 such rows it takes the median, stores it per model and size (that is why the unit-size picker matters), and from then on uses Way 2 for every row of every log of that unit. The Data-tab card tells you which way is in use and how many good rows it has. On the DH9 at 32 rps the implied displacement came out around 50 cc/rev, plausible for a 3-ton compressor (engineering judgement; no manual on file names the DH9VS compressor type); it will firm up on a cold-day log.

*A subtlety on the DH9VS:* its install manual names a liquid injection circuit (DH9VS install manual p.32, p.34) but does not say when it runs. The app assumes that in heating the injection EEV sends some liquid into the compressor mid-stroke. That flow is part of what the compressor discharges, so Way 1's ṁ is the **condenser** flow, which is the right one for heating capacity. In cooling the injection EEV stayed closed through the one recording on file (from the recording, not the manual); if it is open, a small share of the flow bypasses the evaporator and the cooling capacity is slightly overstated (assumption).

### Calculated capacity (BTU/h) = ṁ × Δh across the indoor coil × 3412

```
Cooling:  Δh = h_vapor(Te, indoor gas temp − Te) − h_liquid(liquid pipe temp)
Heating:  Δh = h2 − h_liquid(indoor liquid temp)
```

Cooling: the energy the refrigerant picked up between entering the indoor coil as liquid (at the outdoor liquid-pipe temperature; the EV only drops its pressure, not its enthalpy) and leaving as superheated gas at the indoor gas thermistor. Heating: the energy it gave up between the compressor discharge and leaving the indoor coil as subcooled liquid.

What it includes: everything the coil exchanged with the air. What it leaves out: heat lost from the discharge line to the attic before the gas reaches the coil (heating), and the suction line's heat pickup after the coil (cooling: the app uses the indoor gas thermistor, which is at the coil, precisely to exclude that). What it cannot see: duct losses between the coil and the grilles, electric heat strips, and duct leakage. Compare with the air-side check for those.

Reading it: a 3-ton unit at full speed on a 95 °F day should show near its 34,000–36,000 nameplate; at 40 rps on a 70 °F day it should show much less, because the control asked for less. Capacity falling at *constant* speed and conditions is the finding: frost, dirty coil, low charge, airflow.

### COP = capacity (kW) ÷ outdoor unit input (kW)
Heat moved per unit of electricity bought, for the outdoor unit (compressor + fan; the indoor blower is not in the log's current). As rules of thumb (not from the manuals), a heat pump at 47 °F runs around 3.5–4.5, at 17 °F around 2–2.5, and in mild cooling 4–6. It inherits capacity's confidence grade, plus the voltage assumption. Very high values in mild weather are usually a "poor"-grade capacity, not a miracle.

### Calculated air ΔT — the expected grille reading
The same capacity carried by the air the blower says it is moving:

- **Heating**: `ΔT = BTU/h ÷ (1.08 × CFM)`. Heating adds no moisture, so this is exact for that airflow. 1.08 is the heat capacity of a cubic foot of standard air per minute per °F.
- **Cooling**: a bracket, because part of the capacity goes into condensing water (latent) and the log cannot see humidity.
  - *dry coil*: `BTU/h ÷ (1.08 × CFM)` — the drop if no latent work happens (upper bound).
  - *wet coil*: a coil bypass model. Start from the return air (typed in the Data tab, or 75 °F / 50 % RH assumed), take its enthalpy, subtract `BTU/h ÷ (4.5 × CFM)` to get the supply enthalpy, assume the coil surface sits 2 °F above Te and the air touching it leaves saturated, and the supply temperature lands on the line between return and coil surface in proportion to the enthalpy. 4.5 converts CFM to pounds of air per hour.
  - The tag shows the midpoint; the card shows the bracket and places a typed supply reading in it. Where it lands says how much of the capacity is latent: near the dry number means the coil is running almost dry (high cfm/ton, dry return); near the wet number means a lot of dehumidification.

This reading is only as good as the CFM. `Present CFM` is the air handler's own airflow estimate, not a measurement (SiUS612412E p.47); the CFM shown on the thermostat or board may differ from measured airflow (IOD-4054B p.15). That is why a measured supply-air reading that misses the bracket points first at the airflow figure.

---

## Part 4 · How the estimates combine, and what to trust when

| If you want to know… | Trust… | Because… |
|---|---|---|
| Is the charge right | SH, SC, EV % — on steady, locked-speed rows (not SC vs the logged Target SC: no manual says what that target controls) | these are direct sensor arithmetic |
| Is the compressor healthy | DSH, discharge vs isentropic, amps per rps | each isolates the compressor from the rest |
| Is the coil rejecting/absorbing heat | approach, coil vs saturation | direct |
| How much is it delivering | Calc capacity, with its confidence grade | one inferred quantity (ṁ) times direct ones |
| Is the duct/airflow the problem | Calc air ΔT vs a probe at the grille | the only place the log and the house meet |
| Efficiency | COP | capacity's grade plus the voltage assumption |

Rules of thumb for the energy readings: believe the trend before the absolute; believe a good-grade row before a poor one; believe the number more once the card says "from displacement"; and when the air-side and refrigerant-side disagree by more than about 15 % (a rule of thumb), suspect the CFM first, then the grille temperatures, then the capacity estimate.

---

## Part 5 · Corrections the app applies from the log itself (v68)

These need nothing from the tech. The Data-tab card lists which of them were possible for the log in hand.

- **At-rest thermistor offsets.** After the compressor has been off 30 minutes or more, every outdoor thermistor should read outdoor air. The app takes the median difference of discharge, suction, liquid-pipe and both coil thermistors against outdoor air over those rows and subtracts it from the running rows in the energy math (offsets over 6 °F are treated as sun or a real fault, reported, and not applied). The logged high and low pressures should also agree at rest; the card says by how much they do. On the FIT only the low one is an outdoor transducer: the high one is the board's figure from Tm in cooling or the indoor sensor in heating (SiUS612209EA p.49). The diagram keeps showing what the board sees, because the board controls on that.
- **Coil-outlet enthalpy at the coil's own pressure.** In cooling the gas leaving the indoor coil is evaluated at the indoor pressure sensor, not the outdoor LP, so the suction-line pressure drop no longer leaks into the capacity.
- **Oil.** 2 % of what the compressor pumps is assumed to be oil carrying no useful enthalpy.
- **5-minute trailing average.** Capacity, input power and the expected air ΔT are averaged over the last five minutes of the same run and mode (about ten rows at 30 s), which cuts sensor noise by roughly 3×. Early rows of a run average what is there.
- **Learned volumetric-efficiency slope.** The good rows record effective displacement (swept volume × η_v) against pressure ratio. When one log spans more than one unit of pressure ratio, the slope is fitted from the data; otherwise the generic rotary curve is used. The learned value is stored per model and size as `e0 + e1 × (PR − 2.5)` and merged across logs.

What this buys: poor-lift rows move from about ±25 % to roughly ±12 %, good rows from ±9 % to about ±7 %. The three assumed constants (voltage, power factor, shell loss) remain, and only a calibration against a real system removes them; see the plan in the README.

### Calculated input power (kW) and energy (kWh) — v69
Input power = line volts (Settings) × `Sys. Op. Current` × 0.97, the outdoor unit's draw (compressor drive + fan). Energy is that power
summed over each row's elapsed time, run by run, as a running total; a recording gap is capped at two sample intervals so the unit's
unknown draw during it is not invented. The Data-tab card and synopsis card L7 give total kWh, hours running, average and peak kW, and the
cost at the electric rate in Settings ($/kWh, default 0.15). The indoor blower is not in the log, so this is the outdoor unit's bill only;
the voltage assumption carries straight through (a 230 V unit entered as 240 reads 4 % high).
