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
