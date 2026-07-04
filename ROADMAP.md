# Mk3 Reference Loudspeaker Roadmap

## v8 — GRS 12SW-4HE woofer upgrade (current)

Current design:

- 300 x 370 x 1080 mm cabinet
- 22 mm birch plywood
- R50 front roundovers
- 2 x GRS 12SW-4HE side-mounted push-push woofers (12" high excursion)
- ScanSpeak 15W/4434G00 midrange
- SB Acoustics SB26STAC-C000-4 tweeter
- Custom non-horn-loaded waveguide (`cad/waveguide.scad`)
- Approx. 75 L sealed bass volume (under divider plate)
- Approx. 5.7 L sealed mid chamber
- 150 Hz LR4 bass/mid crossover
- 1100 Hz LR4 mid/tweeter crossover
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

## v9 — Measurement-validated design

- Build first physical prototype
- Measure all drivers in cabinet
- Import measurements into VituixCAD
- Validate or revise 1100 Hz crossover
- Validate vertical listening window

## v10 — CAD/package refinement

- Final cabinet drawings
- Final waveguide model
- STEP/STL export
- CNC/fræse-ready drawings

## v11 — DSP implementation

- Initial MiniDSP/FusionAmp presets
- Delay optimization
- EQ and target curves
- House curve versions

## v12 — Advanced variants

- FIR filters
- Alternative midranges
- Cardioid/controlled bass experiments

## v13 — Integrated active version

- Integrated amplifier module
- Internal DSP
- Full wiring plan
- Finalized build guide
