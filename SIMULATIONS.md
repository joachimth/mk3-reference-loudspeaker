# Simulations

This file tracks simulation work and assumptions for the Mk3 Reference Loudspeaker.

---

# Important Note

The simulations so far are simplified design-direction estimates, not final measured data. They are intended to guide design choices before CAD, prototyping and measurements.

Final crossover and DSP decisions must be based on real measurements in the finished cabinet.

Version-controlled, assumption-headed scripts and their plots now live in
[`simulations/`](simulations/) (`bass_alignment_maxspl.py`, `bass_volume_compare.py`,
`vertical_lobing.py`, `directivity_estimate.py`, `crossover_simulation.py`,
`system_response.py`, `polar_response.py`, `vertical_polar_map.py`,
`system_response_realistic.py`, `spinorama_estimate.py`,
`crossover_optimization.py`, `tweeter_comparison.py`); parametric
OpenSCAD geometry lives in [`cad/`](cad/) (waveguide + cabinet).

### Current design scripts

The following scripts document the current SB26STAC / 1100 Hz design and the
tweeter selection analysis:

- `system_response_realistic.py` — realistic system response using actual
  digitized datasheet frequency-response curves, baffle step, waveguide loading
  and LR4 crossovers.
- `spinorama_estimate.py` — spinorama estimate (on-axis, listening window,
  early reflections, sound power, DI, PIR) using real datasheet curves.
- `crossover_optimization.py` — systematic crossover-frequency sweep for
  the SB26STAC scoring Fs margin, excursion headroom, directivity match,
  vertical lobing ripple and system-sum flatness. Confirms 1100 Hz as optimal.
- `tweeter_comparison.py` — tweeter selection analysis (excursion,
  distortion, sensitivity) documenting why the SB26STAC was chosen.
- `system_response_inroom.py` — four-stage progression: anechoic (pre-DSP)
  → in-room (average living room 4.5×4×2.4m, room gain + HF absorption)
  → level-corrected (normalized @500 Hz) → post-DSP (EQ toward Harman
  in-room target, 1/3 octave PEQ simulation). Uses v9 drivers: 2× GRS
  12SW-4HE, ScanSpeak 18W/4424G00, SB26STAC-C000-4. Output:
  `plots/system_response_inroom.png`, `csv/system_response_inroom.csv`.

---

# In-Room Response Simulation

## Model (added July 6, 2026)

The in-room simulation (`system_response_inroom.py`) extends the anechoic
system response with a room acoustics model and DSP correction simulation.

### Room model — average living room

- Dimensions: 4.5 × 4.0 × 2.4 m (V = 43.2 m³) — typical Danish stue
- RT60 ≈ 0.4 s (furnished room with carpet, curtains, sofa)
- Schroeder frequency: ~192 Hz
- Room gain: +6 dB/octave below f_schroeder, capped at +9 dB
  (3 boundary surfaces + modal density boost)
- HF absorption: −1.5 dB/octave above 5 kHz, capped at −3 dB
  (furnishings, carpet, curtains)

### Harman in-room target curve

- Flat 100 Hz – 1 kHz (0 dB reference)
- Bass shelf: +3.5 dB below 100 Hz (second-order transition)
- HF tilt: −1 dB/octave above 1 kHz

### DSP simulation

- Uses optimized DSP gains (woofer +1.5 dB, mid −4.0 dB, tweeter −9.0 dB)
- Optimized for in-room response vs Harman target curve
- Simulates ~10 PEQ bands at 1/3 octave resolution
- DSP correction range: ±2.0 dB (smoothed, 1/3 octave)
- Residual deviation from target: ±0.3 dB (500 Hz – 10 kHz)

### Results

| Stage | Ripple 200–15k | Ripple 500–10k | @100 Hz | @500 Hz | @2 kHz | @10 kHz |
|---|---|---|---|---|---|---|
| Anechoic (pre-DSP) | 2.7 dB | 2.7 dB | 83.5 | 86.7 | 84.5 | 85.1 |
| In-room | 3.6 dB | 3.6 dB | 89.2 | 86.7 | 84.5 | 83.6 |
| Level-corrected | 3.6 dB | 3.6 dB | 2.5 | 0.0 | −2.1 | −3.1 |
| Post-DSP | 4.8 dB | 3.5 dB | 1.7 | 0.1 | −1.0 | −3.3 |

Post-DSP deviation from Harman target: ±0.3 dB (500 Hz – 10 kHz).
The 4.8 dB ripple 200–15k is the intentional bass shelf + HF tilt, not ripple.

### Target comparison: Harman vs BBC-style

A second target curve (BBC-style) was optimized with its own gain set:

| Target | Woofer | Mid | Tweeter | W-M | M-T | Pre-EQ RMS | Post-DSP residual |
|---|---|---|---|---|---|---|---|
| Harman | +1.5 dB | −4.0 dB | −9.0 dB | 5.5 dB | 5.0 dB | 0.89 dB | ±0.3 dB |
| BBC-style | +1.0 dB | −3.5 dB | −8.5 dB | 4.5 dB | 5.0 dB | 0.88 dB | ±0.3 dB |

BBC target: −2 dB presence dip at 2 kHz, +2 dB bass shelf below 120 Hz,
−0.8 dB/octave HF tilt above 3 kHz. Both targets achievable with ±2.0 dB
DSP correction. M-T spread is 5.0 dB for both; only W-M differs (BBC
needs 1 dB less due to the presence dip lowering the mid region).

---

# Bass Simulations

## Current assumption

- 2 x GRS 12SW-4HE
- Sealed cabinet, ~75 L net (volume under divider plate)
- Fs 22 Hz
- Vas 80.4 L per driver (160.8 L combined)
- Qts 0.43
- Xmax 12.5 mm (Klippel verified), Sd 504 cm²

## Current estimate

- Sealed Fc ~39 Hz, Qtc ~0.76
- Linkwitz Transform target: Fc 39.0 → 28 Hz, Qtc 0.76 → 0.707
- Max SPL @ 30 Hz: +16 dB over the previous 8SW design
- Displacement: 12.6 cm³ (was 2.0 cm³ with the 8SW)

## Interpretation

This is a low-Q sealed alignment with a Linkwitz Transform to 28 Hz / 0.707. The
12SW's large Sd and high Xmax give substantially more low-frequency headroom than
the previous 8SW.

---

# Cabinet Width and Roundover Simulations

Variants explored:

- 270 mm front
- 280 mm front
- 300 mm front
- 320 mm front
- 340 mm front
- R20-R70 roundovers

## Current conclusion

300 mm front width with R50 vertical front roundovers is the best practical compromise.

---

# Waveguide and Crossover Simulations

Variants explored:

- ~212 to ~240 mm waveguide mouths
- 1100-1600 Hz mid/tweeter crossover region
- 140-157 mm c-c spacing

## Current conclusion

The strongest improvement comes from:

- Lower mid/tweeter crossover
- Shorter c-c spacing
- Smooth baffle/waveguide integration

The custom SB26STAC waveguide with approx. 1100 Hz LR4 and 140 mm c-c is the current best simplified candidate.

---

# Spinorama-style Curves

Curves to maintain:

- On-axis
- Listening window
- Early reflections estimate
- Sound power estimate
- Predicted in-room estimate
- Directivity Index

---

# Simulation Tasks

- [x] Recreate all current Python simulations in version-controlled scripts
- [x] Add assumptions at top of each script
- [x] Export plots to `simulations/plots/` (CI auto-commits on every push)
- [x] Export CSV data to `simulations/csv/` (crossover, system, spinorama, polar, vertical)
- [x] Create a comparison table for all design versions (`design_versions_comparison.py` → `design_versions.md` + `csv/design_versions.csv`)
- [ ] Validate against actual measurements (blocked: prototype not yet built)
