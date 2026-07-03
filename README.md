# Mk3 Reference Loudspeaker

A DIY active 3-way reference loudspeaker project, inspired by Genelec 8361, Dutch & Dutch 8C, and Revel Salon2.

> **mk3 branch:** SB26STAC-C000-4 tweeter, 1100 Hz crossover. The `main` branch retains the original mk2 H2606/920000 design at 1250 Hz. See `docs/SB26STAC-C000-4_analysis.md` for the full comparison.

## Current Design - v7 (mk3)

| Parameter | Value | mk2 (main branch) |
|---|---|---|
| Woofers | 2 × GRS 8SW-4HE-8 (push-push, side-mounted) | same |
| Midrange | ScanSpeak 15W/4434G00 | same |
| Tweeter | **SB Acoustics SB26STAC-C000-4** in WG212 waveguide | ScanSpeak H2606/920000 |
| Cabinet | 300 × 370 × 1080 mm, 22 mm birch plywood | same |
| Front edges | R50 vertical roundovers | same |
| Bass volume | ~69 L sealed | same |
| Mid chamber | ~5.7 L sealed | same |
| Bass/mid xover | 150 Hz LR4 | same |
| Mid/tweeter xover | **1100 Hz LR4** | 1250 Hz LR4 |
| Mid/tweeter c-c | 140 mm | same |
| Bass alignment | Fc ~34.5 Hz, Qtc ~0.62 | same |
| System type | Active, DSP-controlled | same |

### Why mk3 — the SB26STAC advantage

| Metric | mk2 (H2606) | mk3 (SB26STAC) | Improvement |
|---|---|---|---|
| Fs | 1030 Hz | 750 Hz | 280 Hz lower |
| Crossover margin | 220 Hz (1250-1030) | 350 Hz (1100-750) | +130 Hz |
| Xmax | 0.2 mm | 0.6 mm | 3× more |
| Excursion headroom | 0 dB (ref) | +8.1 dB | +8.1 dB |
| DI mismatch at crossover | 5.3 dB | 4.6 dB | -0.7 dB better |
| Sensitivity vs 15W | +5.5 dB (needs -5.5 dB pad) | +1.8 dB (needs -1.8 dB pad) | Better match |
| Broadside null (150mm c-c) | 1147 Hz (above 1250 xover) | 1147 Hz (above 1100 xover, LR4 suppresses) | Null fully outside band |

## CAD Renders

Auto-generated on every CAD change. [Full documentation →](cad/)

### Waveguide (WG212 for SB26STAC-C000-4)

| | |
|:---:|:---:|
| ![Mouth](assets/renders/waveguide_mouth.png) | ![Rear](assets/renders/waveguide_rear.png) |
| Mouth (front) | Rear / back plate |
| ![Side](assets/renders/waveguide_side.png) | ![Top](assets/renders/waveguide_top.png) |
| Side profile (OS bore) | Top (throat view) |
| ![Iso](assets/renders/waveguide_iso.png) | ![Cutaway](assets/renders/waveguide_cutaway.png) |
| Isometric | Half-section cutaway |

> **CAD:** `cad/mk2_waveguide_sb26stac.scad` (SB26STAC version, mk3 primary)
> **STL:** `cad/exports/sb26stac/waveguide_sb26stac.stl`
> The H2606 version (`cad/mk2_waveguide_os.scad`) remains on the `main` branch.

### Cabinet (v6b)

| | |
|:---:|:---:|
| ![Front](assets/renders/cabinet_front.png) | ![Rear](assets/renders/cabinet_rear.png) |
| Front (baffle with drivers) | Rear panel |
| ![Left](assets/renders/cabinet_left.png) | ![Right](assets/renders/cabinet_right.png) |
| Left side (woofer) | Right side (woofer) |
| ![Top](assets/renders/cabinet_top.png) | ![Bottom](assets/renders/cabinet_bottom.png) |
| Top | Bottom |
| ![Exterior](assets/renders/cabinet_exterior.png) | ![Cutaway](assets/renders/cabinet_cutaway.png) |
| 3/4 exterior | Half-section cutaway |
| ![Assembly](assets/renders/cabinet_assembly.png) | ![Full](assets/renders/cabinet_full_cutaway.png) |
| With waveguide mounted | Full assembly cutaway |

## Project Status

[![Run simulations](https://github.com/joachimth/mk2-reference-loudspeaker/actions/workflows/simulations.yml/badge.svg)](https://github.com/joachimth/mk2-reference-loudspeaker/actions/workflows/simulations.yml)
[![Render CAD models](https://github.com/joachimth/mk2-reference-loudspeaker/actions/workflows/cad-render.yml/badge.svg)](https://github.com/joachimth/mk2-reference-loudspeaker/actions/workflows/cad-render.yml)

Design candidate **v7 (mk3)** is selected. CAD models and simulations are complete for the SB26STAC-C000-4 tweeter.

**Current gate:** Purchase SB26STAC-C000-4 → caliper verify dimensions → print WG212 (SB26STAC version) → measure distortion at 1100 Hz → build prototype.

> The H2606/920000 design (v6b, mk2) remains on the `main` branch as the fallback path.

See [`PROJECT_TODO.md`](PROJECT_TODO.md) for the full task list and dependency graph.

## Documentation

The full Design Bible lives in the `docs/` folder:

| Chapter | File |
|---|---|
| Master index | [docs/00_design_bible.md](docs/00_design_bible.md) |
| 1. Project goals | [docs/01_project_goals.md](docs/01_project_goals.md) |
| 2. Theory | [docs/02_theory.md](docs/02_theory.md) |
| 3. Woofer selection | [docs/03_woofer_selection.md](docs/03_woofer_selection.md) |
| 4. Midrange selection | [docs/04_midrange_selection.md](docs/04_midrange_selection.md) |
| 5. Tweeter selection | [docs/05_tweeter_selection.md](docs/05_tweeter_selection.md) |
| 6. Waveguide development | [docs/06_waveguide_development.md](docs/06_waveguide_development.md) |
| 7. Cabinet development | [docs/07_cabinet_development.md](docs/07_cabinet_development.md) |
| 8. Push-push bass | [docs/08_push_push_bass.md](docs/08_push_push_bass.md) |
| 9. Volume calculations | [docs/09_volume_calculations.md](docs/09_volume_calculations.md) |
| 10. Bracing | [docs/10_bracing.md](docs/10_bracing.md) |
| 11. Crossovers | [docs/11_crossovers.md](docs/11_crossovers.md) |
| 12. Directivity | [docs/12_directivity.md](docs/12_directivity.md) |
| 13. Spinorama | [docs/13_spinorama.md](docs/13_spinorama.md) |
| 14. DSP | [docs/14_dsp.md](docs/14_dsp.md) |
| 15. Measurements | [docs/15_measurements.md](docs/15_measurements.md) |
| 16. Build guide | [docs/16_build_guide.md](docs/16_build_guide.md) |
| 17. Future versions | [docs/17_future_versions.md](docs/17_future_versions.md) |

## Reference Files

- [DESIGN_REQUIREMENTS.md](DESIGN_REQUIREMENTS.md) - Acoustic and mechanical targets
- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) - Rationale for all key decisions
- [PARTS.md](PARTS.md) - Driver and materials list
- [SIMULATIONS.md](SIMULATIONS.md) - Simulation work and assumptions
- [MEASUREMENTS.md](MEASUREMENTS.md) - Measurement plan
- [BUILD_LOG.md](BUILD_LOG.md) - Physical build log
- [ROADMAP.md](ROADMAP.md) - Version history and future plans
- [CHANGELOG.md](CHANGELOG.md) - Design change log
- [REFERENCES.md](REFERENCES.md) - Books, papers, tools
- [TODO.md](TODO.md) - Outstanding tasks
- [REVIEW.md](REVIEW.md) - External technical review of the docs/simulations (flags physics-doc errors and revisits the 1250 Hz / 140 mm targets)
- [simulations/](simulations/) - Version-controlled simulation scripts + generated plots (bass alignment / max-SPL, vertical lobing)
- [cad/](cad/) - Parametric CAD (OpenSCAD OS waveguide for the H2606)
- [assets/](assets/) - Drawings, response plot, DSP table, and the SB23 study's design bible (reference material; see [assets/README.md](assets/README.md) — note the SB23 material diverges from the v6b spec)

## License

MIT
