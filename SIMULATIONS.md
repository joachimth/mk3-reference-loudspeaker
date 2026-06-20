# Simulations

This file tracks simulation work and assumptions for Mk2 Reference Loudspeaker.

---

# Important Note

The simulations so far are simplified design-direction estimates, not final measured data. They are intended to guide design choices before CAD, prototyping and measurements.

Final crossover and DSP decisions must be based on real measurements in the finished cabinet.

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

- WG212
- WG220
- WG230
- WG240
- 1250-1600 Hz mid/tweeter crossover region
- 140-157 mm c-c spacing

## Current conclusion

The strongest improvement comes from:

- Lower mid/tweeter crossover
- Shorter c-c spacing
- Smooth baffle/waveguide integration

WG212 with approx. 1250 Hz LR4 and 140 mm c-c is the current best simplified candidate.

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

- [ ] Recreate all current Python simulations in version-controlled scripts
- [ ] Add assumptions at top of each script
- [ ] Export plots to `simulations/plots/`
- [ ] Export CSV data to `simulations/csv/`
- [ ] Create a comparison table for all design versions
- [ ] Validate against actual measurements later
