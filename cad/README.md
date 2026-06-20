# CAD

Parametric CAD models for the Mk2 Reference Loudspeaker.

## `mk2_waveguide_os.scad`

A fully parametric **OpenSCAD** model of the tweeter waveguide for the
ScanSpeak **H2606/920000** — an oblate-spheroid (OS) constant-directivity bore
with a tangent rolled mouth that ends flush with the baffle.

- Mouth ≈ **211.7 × 121.0 mm**, total depth **75 mm** (the WG212 family).
- Asymmetric coverage ≈ **100° horizontal / 64° vertical**.
- Horizontal pattern control down to ≈ **1620 Hz**, i.e. designed to support a
  clean LR4 crossover to the 15W/4434G00 **near the waveguide's control limit**
  rather than well below it (this relates to the crossover discussion in
  [../REVIEW.md](../REVIEW.md) §C2 — the repo's current target is 1250 Hz LR4).

### Critical tunables (verify before printing)

- `throat_d` (28 mm placeholder) **must be matched to the real H2606 dome /
  faceplate exit** — this sets whether you get a throat resonance. Print throat
  test pieces against the physical tweeter first.
- The mouth roundover must blend smoothly into the cabinet's baffle roundover;
  a step there re-introduces diffraction.

### Building

Open in OpenSCAD, render with F6, export STL. `$fn` is high for export — drop to
64 while iterating. The model echoes the computed mouth size and depth on render.

A rendered profile of this waveguide is in
[../assets/mk2_waveguide_profil.png](../assets/mk2_waveguide_profil.png).

These are **design-direction geometry, not validated by measurement.** Mouth
size, throat and coverage must be confirmed against H2606-in-waveguide
measurements.
