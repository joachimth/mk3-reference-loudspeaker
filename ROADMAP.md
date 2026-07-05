# Mk3 Reference Loudspeaker Roadmap

## v9 — 18W/4424G00 midrange, mid-over-waveguide layout (current, in progress)

Current design candidate:

- 320 x 370 x 1080 mm cabinet (width driven by the opposed 12" woofers)
- 22 mm birch plywood
- R19 front roundovers (R50 leaves no flat for the waveguide flange)
- 2 x GRS 12SW-4HE side-mounted push-push woofers (12" high excursion)
- ScanSpeak 18W/4424G00 midrange at the TOP of the baffle (`cad/midrange.scad`)
- SB Acoustics SB26STAC-C000-4 tweeter in the waveguide BELOW the midrange
- Custom non-horn-loaded waveguide (`cad/waveguide.scad`)
- Full-width tilted divider plate between midrange and waveguide
- Approx. 65 L net sealed bass volume (below divider; target remains 75 L)
- Approx. 11 L net sealed mid chamber (18W datasheet closed-box rec.: 13 L)
- 150 Hz LR4 bass/mid crossover
- 1100 Hz LR4 mid/tweeter crossover (re-validate for the 18 cm cone)
- 165 mm mid/tweeter c-c spacing (physical minimum with these flanges)
- See CHANGELOG v9 and DD-016

## v8 — GRS 12SW-4HE woofer upgrade

- 300 x 370 x 1080 mm cabinet (superseded: width -> 320 mm in v9)
- 2 x GRS 12SW-4HE side-mounted push-push woofers (12" high excursion)
- ScanSpeak 15W/4434G00 midrange (superseded by 18W/4424G00 in v9)
- Approx. 75 L sealed bass volume target (under divider plate)
- Approx. 5.7 L sealed mid chamber
- Target 140 mm mid/tweeter c-c spacing

Woofer upgrade details:

- Woofer upgraded from GRS 8SW-4HE-8 (8") to GRS 12SW-4HE (12" high excursion)
- Bass volume increased to ~75 L under divider plate
- Linkwitz Transform: Fc 39→28 Hz, Qtc 0.76→0.707
- Max SPL @ 30 Hz: +16 dB over previous design
- See DD-015, CHANGELOG v8

## v7 — SB26STAC tweeter, 1100 Hz crossover

- SB Acoustics SB26STAC-C000-4 tweeter selected (Fs 750 Hz, 0.6 mm Xmax)
- 1100 Hz LR4 mid/tweeter crossover
- Custom non-horn-loaded waveguide
- GRS 8SW-4HE-8 woofers (superseded in v8 by 12SW)

## v10 — Measurement-validated design

- Build first physical prototype
- Measure all drivers in cabinet
- Import measurements into VituixCAD
- Validate or revise 1100 Hz crossover
- Validate vertical listening window

## v11 — CAD/package refinement

- Final cabinet drawings
- Final waveguide model
- STEP/STL export
- CNC/fræse-ready drawings

## v12 — DSP implementation

- Initial MiniDSP/FusionAmp presets
- Delay optimization
- EQ and target curves
- House curve versions

## v13 — Advanced variants

- FIR filters
- Alternative midranges
- Cardioid/controlled bass experiments

## v14 — Integrated active version

- Integrated amplifier module
- Internal DSP
- Full wiring plan
- Finalized build guide
