# Mk3 Reference Loudspeaker - Design Bible

## About this document

This is the master documentation index for the Mk3 Reference Loudspeaker project. Each chapter covers one aspect of the design process, from initial goals through theory, driver selection, cabinet development, simulation, measurement, and build.

The design bible is a living document. It will be updated as the project progresses from simulation to physical prototype to final tuning.

---

## Current design summary - v9 (in progress)

- Active 3-way loudspeaker with DSP crossovers
- 2 × GRS 12SW-4HE woofers (side-mounted push-push, 12" high excursion)
- ScanSpeak 18W/4424G00 midrange at the TOP of the baffle (`cad/midrange.scad`)
- SB Acoustics SB26STAC-C000-4 tweeter in a custom non-horn-loaded waveguide (`cad/waveguide.scad`), mounted BELOW the midrange
- Full-width tilted divider plate between midrange and waveguide: mid chamber above (~11 L net), bass volume below (~65 L net)
- Cabinet: 320 × 370 × 1080 mm, 22 mm birch plywood, R19 front roundovers
- Bass: ~65 L net sealed, Fc ~41 Hz → 28 Hz via LT, Qtc target 0.707 after LT
- Mid chamber: predicted Qtc ~0.68, Fc ~88 Hz (18W datasheet closed-box rec.: 13 L)
- Crossovers: 150 Hz LR4 (bass/mid), 1100 Hz LR4 (mid/tweeter, re-validate for 18 cm cone)
- Mid/tweeter c-c: 165 mm (physical minimum with these flanges; DD-016)

---

## Chapters

| # | Title | File | Status |
|---|---|---|---|
| 1 | Project goals and philosophy | [01_project_goals.md](01_project_goals.md) | Complete |
| 2 | Loudspeaker theory | [02_theory.md](02_theory.md) | Complete |
| 3 | Woofer investigations | [03_woofer_selection.md](03_woofer_selection.md) | Complete |
| 4 | Midrange investigations | [04_midrange_selection.md](04_midrange_selection.md) | Complete |
| 5 | Tweeter investigations | [05_tweeter_selection.md](05_tweeter_selection.md) | Complete |
| 6 | Waveguide development | [06_waveguide_development.md](06_waveguide_development.md) | Complete (CAD done; print + measure pending) |
| 7 | Cabinet development | [07_cabinet_development.md](07_cabinet_development.md) | Complete (CAD done; build pending) |
| 8 | Push-push bass | [08_push_push_bass.md](08_push_push_bass.md) | Complete |
| 9 | Volume calculations | [09_volume_calculations.md](09_volume_calculations.md) | Complete |
| 10 | Bracing | [10_bracing.md](10_bracing.md) | Complete (representational CAD; detail pending build) |
| 11 | Crossovers | [11_crossovers.md](11_crossovers.md) | Complete (frequency pending distortion measurement) |
| 12 | Directivity | [12_directivity.md](12_directivity.md) | Complete |
| 13 | Spinorama | [13_spinorama.md](13_spinorama.md) | Complete (estimated; true spinorama pending build) |
| 14 | DSP | [14_dsp.md](14_dsp.md) | Complete (platform selected: MiniDSP 4×10 HD) |
| 15 | Measurements | [15_measurements.md](15_measurements.md) | Plan written; execution pending prototype |
| 16 | Build guide | [16_build_guide.md](16_build_guide.md) | Plan written; execution not started |
| 17 | Future versions | [17_future_versions.md](17_future_versions.md) | Complete |
