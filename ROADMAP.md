# Mk2 Reference Loudspeaker Roadmap

## v1 - Initial concept

- Active 3-way reference loudspeaker concept
- Initial cabinet and driver layout
- SB23 woofer-based starting point

## v2 - Cabinet development

- 300 mm wide cabinet concept
- Side-mounted push-push woofers
- Dedicated midrange chamber
- H2606 in waveguide

## v3 - GRS woofer investigation

- Introduced GRS 8SW-4HE-8 as alternative woofer
- Evaluated sealed-box alignments
- Found strong fit for 64-70 L sealed bass volume

## v4 - 280 mm cabinet exploration

- Explored narrower 280 mm front baffle
- Compared edge roundovers
- Found R40 useful but mechanically constrained

## v5 - 300 mm / R50 cabinet

- Selected 300 mm front width
- Selected R50 vertical front roundovers
- Targeted 64-70 L sealed bass volume
- Refined woofer placement and mid chamber

## v6 - Directivity optimization

- Compared WG212, WG220, WG230 and WG240 concepts
- Compared 1300-1600 Hz mid/tweeter crossover region
- Found c-c spacing more important than larger waveguide mouth

## v6b - Current reference candidate

Current main design:

- 300 x 370 x 1080 mm cabinet
- 22 mm birch plywood
- R50 front roundovers
- 2 x GRS 8SW-4HE-8 side-mounted push-push woofers
- ScanSpeak 15W/4434G00 midrange
- ScanSpeak H2606/920000 tweeter
- WG212 waveguide
- Approx. 69 L sealed bass volume
- Approx. 5.7 L sealed mid chamber
- 150 Hz LR4 bass/mid crossover
- 1250 Hz LR4 mid/tweeter crossover
- Target 140 mm mid/tweeter c-c spacing

## v7 - Measurement-validated design

- Build first physical prototype
- Measure all drivers in cabinet
- Import measurements into VituixCAD
- Validate or revise 1250 Hz crossover
- Validate vertical listening window

## v8 - CAD/package refinement

- Final cabinet drawings
- Final waveguide model
- STEP/STL export
- CNC/fræse-ready drawings

## v9 - DSP implementation

- Initial MiniDSP/FusionAmp presets
- Delay optimization
- EQ and target curves
- House curve versions

## v10 - Advanced variants

- FIR filters
- Alternative tweeters
- Alternative midranges
- Cardioid/controlled bass experiments

## v11 - Integrated active version

- Integrated amplifier module
- Internal DSP
- Full wiring plan
- Finalized build guide

---

## Alternative variant - SB23 line (parallel study)

A separate, self-contained study explores a **SB23-based** version of the Mk2
rather than the GRS bass of the main v6b line. It shares the H2606 tweeter, 15W
midrange and waveguide direction but differs on the bass and several cabinet
numbers:

- 2 × SB Acoustics SB23NRXS45-8 (push-push), sealed ~64 L, Qtc ≈ 0.75 / Fc ≈ 54 Hz
- OS (oblate-spheroid) waveguide, ~1600 Hz LR4 mid/tweeter, c-c ~157-160 mm
- Cabinet ~1050 mm tall, 180 Hz LR4 bass/mid

This is **not** the reference design — v6b (GRS) remains the main line. The full
write-up, drawings, parameters and parts list live in
[`assets/`](assets/) (see [`assets/mk2_design_bible_sb23.md`](assets/mk2_design_bible_sb23.md)
and [`assets/README.md`](assets/README.md)). Several of its directivity arguments
(higher crossover near the waveguide control limit, ~157-160 mm c-c) align with
the review caveats now recorded against DD-010 / DD-011.

## v7 / mk3 — SB26STAC tweeter (mk3-sb26stac branch)

A parallel design variant created July 3 2026 on the `mk3-sb26stac` branch:

- **Tweeter:** SB Acoustics SB26STAC-C000-4 conventional dome tweeter selected
  (replaces ScanSpeak H2606/920000 from the mk2 main line). Fs 750 Hz, 0.6 mm
  Xmax, 91.5 dB, 4 Ω. Not horn-loaded — requires a different waveguide than
  WG212.
- **Crossover:** 1100 Hz LR4 mid/tweeter crossover (lower than mk2's 1250 Hz),
  giving the tweeter more excursion headroom (+8.1 dB vs H2606 at the crossover
  frequency).
- **Waveguide:** Custom non-horn-loaded waveguide (`cad/mk2_waveguide_sb26stac.scad`).
- **Branch:** `mk3-sb26stac` created July 3 2026. See `PROJECT_TODO.md` for the
  mk3 task list and `CHANGELOG.md` for the v7/mk3 entry.
