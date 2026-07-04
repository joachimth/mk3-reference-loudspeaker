# Chapter 12 - Directivity

---

## What is directivity?

Directivity describes how a loudspeaker radiates sound in different directions. A loudspeaker with ideal directivity control radiates smoothly controlled patterns at all frequencies, with the pattern narrowing gradually with frequency as expected from the geometry.

Poor directivity produces:
- Sudden changes in the off-axis pattern at crossover frequencies ("directivity step")
- Narrow vertical lobes from c-c spacing at crossover
- Diffraction artifacts from cabinet edges
- Irregular reflections in the listening room

---

## Directivity Index (DI)

The Directivity Index is the difference in dB between the on-axis response and the sound power response (the integrated energy radiated in all directions).

A smooth, monotonically rising DI is a sign of well-controlled directivity. It indicates:
- The loudspeaker becomes gradually more directional at higher frequencies (as expected from increasing source size relative to wavelength)
- There are no abrupt directivity transitions

Irregularities in the DI (dips, steps, irregularities) indicate directivity problems at those frequencies.

---

## Sources of directivity problems

### Crossover directivity mismatch

At the crossover frequency, two drivers of different sizes transition between each other. If their off-axis responses do not match at the crossover frequency, the combined off-axis response will show a step or dip.

For the mid/tweeter crossover at 1100 Hz:
- The ScanSpeak 15W midrange at 1100 Hz radiates over a moderate angle (the ~120 mm cone diameter is beginning to narrow the pattern)
- The SB Acoustics SB26STAC-C000-4 is a conventional dome with no built-in horn, so the custom waveguide provides all of the directivity control
- Without the waveguide, a directivity step would be present at the crossover frequency

The custom SB26STAC waveguide (`cad/mk2_waveguide_sb26stac.scad`) is designed to provide directivity control matching the 15W midrange at the crossover frequency. Unlike the WG212 (which horn-loads the H2606 on the mk2 main branch), this is a non-horn-loaded waveguide.

### Vertical lobing

Two vertically separated drivers produce an interference pattern in the vertical plane at frequencies where their separation is comparable to the wavelength. This appears as a lobe structure in the vertical polar plot.

The 140 mm c-c spacing and 1100 Hz crossover were selected together to minimize the lobing impact within the ±15° listening window. See Chapter 11 for quantitative analysis.

### Cabinet diffraction

The edges of the cabinet cause sound waves to diffract, adding a second source of radiation at the edge. This produces ripple in both the on-axis and off-axis responses, particularly in the 500-5000 Hz range depending on cabinet dimensions.

The R50 front edge roundovers minimize diffraction by presenting a smooth curve rather than a sharp edge to the propagating wavefront. Larger roundovers produce smoother diffraction.

### Driver beaming

At high frequencies, individual drivers become increasingly directional because their radiating diameter becomes large relative to the wavelength. This is called beaming.

The ScanSpeak 15W begins to beam above approximately 1500-2000 Hz in free-field. The 1100 Hz crossover is designed to transition to the tweeter/waveguide before significant beaming occurs.

---

## Design response

| Problem | Solution | Status |
|---|---|---|
| Mid/tweeter directivity mismatch | WG212 waveguide | In development |
| Vertical lobing | 140 mm c-c + 1100 Hz crossover | Simulated |
| Cabinet diffraction | R50 front roundovers | Selected |
| Midrange beaming | Cross at 1100 Hz | Simulated |

---

## Simulation results summary

The simplified simulations explored multiple combinations of:
- Waveguide size (WG212 to WG240)
- Crossover frequency (1250 to 1600 Hz)
- C-c spacing (140 to 157 mm)

Key finding: **lower crossover frequency and shorter c-c spacing produced more consistent benefit than larger waveguide mouth diameter.**

SB26STAC waveguide with 1100 Hz and 140 mm c-c is the current best candidate. This must be verified with real measurements of the physical prototype.

---

## Target directivity behavior

| Frequency range | Expected pattern |
|---|---|
| Below 150 Hz | Omnidirectional (woofers, long wavelengths) |
| 150 Hz - 1 kHz | Gradually narrowing (midrange, baffle loading) |
| 1 kHz - 3 kHz | Controlled by WG212 waveguide |
| 3 kHz - 20 kHz | Gradually narrowing (tweeter in waveguide) |

The horizontal polar pattern should be smooth and symmetrical. The vertical polar pattern should be usable over at least ±15° without major lobing artifacts in the crossover region.

---

## Measurement requirements

To fully characterize the directivity:

- Horizontal: 0°, 10°, 20°, 30°, 40°, 50°, 60° minimum (70°, 80°, 90° extended)
- Vertical: ±10°, ±15°, ±20°, ±30°

These measurements feed into VituixCAD to compute the full spinorama and DI curve.

See Chapter 15 (Measurements) for the full measurement plan.
