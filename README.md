# Mk2 Reference Loudspeaker

A DIY active 3-way reference loudspeaker project, inspired by Genelec 8361, Dutch & Dutch 8C, and Revel Salon2.

## Current Design - v6b

| Parameter | Value |
|---|---|
| Woofers | 2 × GRS 8SW-4HE-8 (push-push, side-mounted) |
| Midrange | ScanSpeak 15W/4434G00 |
| Tweeter | ScanSpeak H2606/920000 in WG212 waveguide |
| Cabinet | 300 × 370 × 1080 mm, 22 mm birch plywood |
| Front edges | R50 vertical roundovers |
| Bass volume | ~69 L sealed |
| Mid chamber | ~5.7 L sealed |
| Bass/mid xover | 150 Hz LR4 |
| Mid/tweeter xover | 1250 Hz LR4 |
| Mid/tweeter c-c | 140 mm |
| Bass alignment | Fc ~34.5 Hz, Qtc ~0.62 |
| System type | Active, DSP-controlled |

## Project Status

Design candidate v6b is selected. Physical prototype not yet started.

Next steps: waveguide CAD, cabinet CAD, prototype build, measurements.

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
