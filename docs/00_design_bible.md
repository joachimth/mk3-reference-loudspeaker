# Mk2 Reference Loudspeaker - Design Bible

## About this document

This is the master documentation index for the Mk2 Reference Loudspeaker project. Each chapter covers one aspect of the design process, from initial goals through theory, driver selection, cabinet development, simulation, measurement, and build.

The design bible is a living document. It will be updated as the project progresses from simulation to physical prototype to final tuning.

---

## Current design summary - v6b

- Active 3-way loudspeaker with DSP crossovers
- 2 × GRS 8SW-4HE-8 woofers (side-mounted push-push)
- ScanSpeak 15W/4434G00 midrange
- ScanSpeak H2606/920000 tweeter in WG212 waveguide
- Cabinet: 300 × 370 × 1080 mm, 22 mm birch plywood, R50 front roundovers
- Bass: ~69 L sealed, Fc ~34.5 Hz, Qtc ~0.62
- Crossovers: 150 Hz LR4 (bass/mid), 1250 Hz LR4 (mid/tweeter)
- Mid/tweeter c-c: 140 mm

> **mk3 branch note:** The above is the mk2 main-line design (H2606, 1250 Hz).
> On the `mk3-sb26stac` branch, the tweeter is **SB Acoustics SB26STAC-C000-4**
> with a **1100 Hz LR4** crossover and a non-horn-loaded waveguide
> (`cad/mk2_waveguide_sb26stac.scad`). The woofer, midrange, cabinet and
> bass/mid crossover are unchanged. See `ROADMAP.md` (v7/mk3 entry),
> `CHANGELOG.md`, and `PROJECT_TODO.md` for the mk3 design.

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
| 14 | DSP | [14_dsp.md](14_dsp.md) | Complete (platform not yet selected) |
| 15 | Measurements | [15_measurements.md](15_measurements.md) | Plan written; execution pending prototype |
| 16 | Build guide | [16_build_guide.md](16_build_guide.md) | Plan written; execution not started |
| 17 | Future versions | [17_future_versions.md](17_future_versions.md) | Complete |
