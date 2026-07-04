# Chapter 13 - Spinorama

> **Note:** All spinorama and directivity-index curves discussed in
> this repository are **simplified power-response estimates from simulation, not
> CEA-2034 data measured on a turntable.** They indicate design direction only;
> the true spinorama can only come from gated anechoic/quasi-anechoic
> measurements of the finished speaker (see [Chapter 15](15_measurements.md)).

---

## What is a spinorama?

The spinorama is a standardized set of frequency response measurements defined in the CEA-2034 / CTA-2034-A standard. It provides a complete description of a loudspeaker's directional behavior using a set of derived curves, each averaged from multiple measurement angles.

The term "spinorama" refers to the process of rotating the loudspeaker on a turntable (spinning it) and taking measurements at many angles to build a full polar dataset.

---

## CEA-2034 curves

| Curve | Definition |
|---|---|
| On-axis (SP) | Measured directly in front at 0° horizontal, 0° vertical |
| Listening Window (LW) | Average of on-axis + ±10° H + ±10° V (5 measurements) |
| Early Reflections (ER) | Average of selected floor/ceiling/side wall reflection angles |
| Sound Power (SP) | Energy average across all measured directions |
| Directivity Index (DI) | On-axis minus Sound Power (dB) |
| Early Reflections DI (ERDI) | Listening Window minus Early Reflections (dB) |
| Predicted In-Room Response (PIR) | Weighted sum: 12% LW + 44% ER + 44% Sound Power |

---

## Why spinorama?

The spinorama captures the full directional behavior of a loudspeaker in a standardized way. Floyd Toole and Sean Olive demonstrated at Harman that listener preference ratings correlate strongly with spinorama results, particularly:

- Flat and smooth Listening Window
- Smooth Sound Power (generally declining with frequency)
- Narrow difference between Listening Window and Early Reflections
- Smoothly rising Directivity Index

A loudspeaker optimized for spinorama quality tends to perform well across a wide range of listening rooms and positions.

---

## Spinorama targets for this project

### On-axis / Listening Window
Target: ≤ ±1.5 dB in the main listening range (200 Hz to 10 kHz) after DSP.

A flat listening window is the foundation. Significant deviations will be audible regardless of room conditions.

### Sound Power
Target: smoothly and gradually declining from bass to treble. No major peaks or dips.

A loudspeaker that radiates cleanly in all directions will have smooth sound power. Diffraction artifacts, directivity steps, and driver resonances all appear in the sound power curve.

### Early Reflections
Target: smooth curve, close to the Listening Window shape. The difference (ERDI) should be small and smooth.

A large gap between the Listening Window and Early Reflections at a specific frequency indicates an abrupt directivity change at that frequency.

### Directivity Index
Target: monotonically rising with frequency. No sudden steps or dips.

A smooth DI indicates consistent directivity control across the full frequency range. Steps in the DI correspond to crossover directivity mismatches, diffraction artifacts, or driver beaming transitions.

### Predicted In-Room Response
Target: smooth downward slope from bass to treble (Harman target). Approximately -1 to -2 dB per octave from 1 kHz to 10 kHz.

---

## Spinorama targets summary

| Curve | Target |
|---|---|
| On-axis | Flat ±1.5 dB after DSP |
| Listening Window | Smooth, close to on-axis |
| Early Reflections | Smooth, small gap from LW |
| Sound Power | Smooth decline, no steps |
| Directivity Index | Monotonically rising |
| Predicted In-Room | Smooth downward slope |

---

## Simulation workflow

Simplified spinorama curves were generated during the design optimization phase using Python scripts (to be version-controlled and committed to the repository). These simulations used idealized driver radiation assumptions and are not substitutes for real measurements.

The simulation results were used to:
- Compare cabinet width and roundover options
- Compare waveguide sizes (~212 to ~240 mm mouth)
- Compare crossover frequencies and c-c spacings
- Identify the most impactful design variables

**Important note:** The simulations are design direction estimates. All crossover and DSP decisions will be finalized from real measurements of the physical prototype.

---

## Measurement workflow

After the prototype is built:

1. Measure all required horizontal and vertical angles in REW
2. Import measurements into VituixCAD
3. Apply acoustic offsets (physical positions)
4. Compute CEA-2034 derived curves
5. Evaluate spinorama quality
6. Optimize crossover and DSP if required
7. Re-measure and iterate

See Chapter 15 (Measurements) for the full measurement procedure.

---

## Simulation tasks (open)

- Recreate all current Python simulations in version-controlled scripts
- Export simulation plots to `simulations/plots/`
- Export simulation data to `simulations/csv/`
- Document assumptions at the top of each simulation script
