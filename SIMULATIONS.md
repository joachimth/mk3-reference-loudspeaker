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

- 2 x GRS 8SW-4HE-8
- Sealed cabinet
- Approx. 68-70 L net bass volume
- Fs approx. 24.9 Hz
- Vas approx. 31.7 L per driver
- Qts approx. 0.45

## Current estimate

- Fc approx. 34-35 Hz
- Qtc approx. 0.62

## Interpretation

This is a low-Q sealed alignment that should respond well to moderate DSP bass extension.

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
