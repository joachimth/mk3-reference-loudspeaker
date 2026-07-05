# Mk3 Reference Loudspeaker

A DIY active 3-way reference loudspeaker, inspired by Genelec 8361, Dutch & Dutch 8C, and Revel Salon2.

[![Build and deploy](https://github.com/joachimth/mk3-reference-loudspeaker/actions/workflows/build-and-deploy.yml/badge.svg)](https://github.com/joachimth/mk3-reference-loudspeaker/actions/workflows/build-and-deploy.yml)

---

## Design Summary

| Parameter | Value |
|---|---|
| Woofers | 2 × GRS 12SW-4HE (push-push, side-mounted) |
| Midrange | ScanSpeak 18W/4424G00 (top of baffle, `cad/midrange.scad`) |
| Tweeter | SB Acoustics SB26STAC-C000-4 in custom waveguide (below the midrange) |
| Cabinet | 320 × 370 × 1080 mm, 22 mm birch plywood |
| Front edges | R19 vertical roundovers |
| Bass volume | ~65 L net sealed (below divider plate; target 75 L) |
| Mid chamber | ~11 L net sealed (top section; datasheet rec. 13 L) |
| Bass / mid crossover | 150 Hz LR4 |
| Mid / tweeter crossover | 1100 Hz LR4 (re-validate for the 18 cm cone) |
| Mid / tweeter c-c | 165 mm (physical minimum; verify from physical parts) |
| Bass alignment | Fc ~41 Hz sealed (→28 Hz, Q 0.707 via Linkwitz Transform) |
| DSP | MiniDSP 4×10 HD |
| System type | Active, DSP-controlled |

### Why SB26STAC-C000-4

| Property | Value |
|---|---|
| Fs | 750 Hz (350 Hz margin at 1100 Hz crossover) |
| Xmax | 0.6 mm (3× more than typical horn tweeters) |
| Sensitivity | 91.5 dB / 2.83V / 1m |
| Impedance | 4 Ω |
| Type | Conventional soft dome, not horn-loaded |

The SB26STAC has a low Fs and generous excursion headroom. At 1100 Hz crossover, it operates 350 Hz above resonance with +8.1 dB excursion margin. Sensitivity matches the 18W/4424G00 midrange within 0.5 dB, requiring only minimal DSP padding. See [tweeter selection analysis](docs/SB26STAC-C000-4_analysis.md) for the full rationale.

---

## Simulation Results

All simulations use real datasheet frequency response curves, baffle step modeling, and waveguide loading estimates. Pre-DSP, anechoic.

### System frequency response

![System response](simulations/plots/system_response_realistic.png)

| Metric | Value |
|---|---|
| ±3 dB bandwidth | 623 - 9710 Hz |
| Midband ripple (500-10k) | 4.2 dB |
| DSP correction needed (midband) | ±4.0 dB |
| Sum @ 1100 Hz (crossover) | 89.9 dB |

**Script:** [system_response_realistic.py](simulations/system_response_realistic.py)

### Crossover optimization

![Crossover optimization](simulations/plots/crossover_optimization.png)

Sweep confirms 1100 Hz as optimal crossover frequency for the SB26STAC.

**Script:** [crossover_optimization.py](simulations/crossover_optimization.py)

### Optimal response vs baseline

![Optimal response](simulations/plots/optimal_response.png)

**Script:** [crossover_optimization.py](simulations/crossover_optimization.py)

### Spinorama estimate

![Spinorama](simulations/plots/spinorama_estimate.png)

**Script:** [spinorama_estimate.py](simulations/spinorama_estimate.py)

### System response comparison

![System response comparison](simulations/plots/system_response_comparison.png)

### Tweeter selection analysis

![Tweeter comparison](simulations/plots/tweeter_comparison.png)

Historical analysis of why SB26STAC-C000-4 was selected. The H2606/920000 is shown as the evaluated baseline, not a current option.

**Script:** [tweeter_comparison.py](simulations/tweeter_comparison.py)

### Directivity

![Directivity](simulations/plots/directivity_estimate.png)

**Script:** [directivity_estimate.py](simulations/directivity_estimate.py)

### Vertical polar map

![Vertical polar map](simulations/plots/vertical_polar_map.png)

**Script:** [vertical_polar_map.py](simulations/vertical_polar_map.py)

### Vertical lobing

![Vertical lobing](simulations/plots/vertical_lobing.png)

**Script:** [vertical_lobing.py](simulations/vertical_lobing.py)

### Polar response

![Polar response](simulations/plots/polar_response.png)

**Script:** [polar_response.py](simulations/polar_response.py)

### Bass alignment

![Bass alignment](simulations/plots/bass_alignment_maxspl.png)

**Script:** [bass_alignment_maxspl.py](simulations/bass_alignment_maxspl.py)

### Bass volume comparison

![Bass volume](simulations/plots/bass_volume_compare.png)

**Script:** [bass_volume_compare.py](simulations/bass_volume_compare.py)

### Baffle step

![Baffle step](simulations/plots/baffle_step.png)

**Script:** [baffle_step.py](simulations/baffle_step.py)

### Waveguide profile

![Waveguide profile](simulations/plots/waveguide_termination.png)

**Script:** [waveguide_profile.py](simulations/waveguide_profile.py)

### All simulation scripts

| Script | What it computes | Output |
|---|---|---|
| `bass_alignment_maxspl.py` | Sealed alignment + excursion-limited max-SPL + Linkwitz Transform | `bass_alignment_maxspl.png` |
| `bass_volume_compare.py` | Sealed alignment sensitivity to box volume (64-72 L) | `bass_volume_compare.png` |
| `baffle_step.py` | Baffle step diffraction for 300 mm cabinet | `baffle_step.png` |
| `waveguide_profile.py` | Waveguide mouth-to-baffle termination cross-section | `waveguide_termination.png` |
| `directivity_estimate.py` | Directivity index across crossover | `directivity_estimate.png` |
| `vertical_lobing.py` | Vertical interference-null angle vs frequency | `vertical_lobing.png` |
| `vertical_polar_map.py` | Vertical 2D heat-map vs frequency | `vertical_polar_map.png` |
| `polar_response.py` | 2D polar map + spinorama curves + horizontal polar cuts | `polar_response.png` |
| `system_response_realistic.py` | Full system response with real datasheet curves | `system_response_realistic.png` |
| `spinorama_estimate.py` | Spinorama estimate (on-axis, LW, ER, SP, DI) | `spinorama_estimate.png` |
| `crossover_optimization.py` | Crossover frequency sweep (800-1600 Hz) | `crossover_optimization.png` |
| `tweeter_comparison.py` | SB26STAC selection analysis (excursion, sensitivity, directivity) | `tweeter_comparison.png` |

See [SIMULATIONS.md](SIMULATIONS.md) for assumptions and methodology. See [simulations/README.md](simulations/README.md) for running instructions.

---

## CAD

### Waveguide (SB26STAC-C000-4)

| | |
|:---:|:---:|
| ![Mouth](assets/renders/waveguide_mouth.png) | ![Rear](assets/renders/waveguide_rear.png) |
| Mouth (front) | Rear / back plate |
| ![Side](assets/renders/waveguide_side.png) | ![Top](assets/renders/waveguide_top.png) |
| Side profile | Top (throat view) |
| ![Iso](assets/renders/waveguide_iso.png) | ![Cutaway](assets/renders/waveguide_cutaway.png) |
| Isometric | Half-section cutaway |

**CAD:** `cad/waveguide.scad` | **STL:** `cad/exports/waveguide.stl`

Key dimensions (verify with calipers before printing):

| Dimension | Value |
|---|---|
| Throat diameter | 28 mm (dome + surround) |
| BCD (screw circle) | 88.5 mm |
| Faceplate OD | ~100 mm |
| Waveguide type | Oblate spheroid, non-horn-loaded |

### Cabinet

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

**CAD:** `cad/cabinet.scad` | **STL:** `cad/exports/cabinet.stl`

Renders auto-generated by CI on every CAD change. See [cad/README.md](cad/README.md) for details.

### Driver Models

Parametric OpenSCAD models for each driver, plus manufacturer/reference 3D geometry.

| Driver | SCAD model | 3D reference |
|---|---|---|
| GRS 12SW-4HE (woofer) | `cad/GRS-12SW-4HE.scad` | — (datasheet only) |
| ScanSpeak 18W/4424G00 (mid) | `cad/midrange.scad` | [STEP](assets/cad/18W-4424G00.STEP) · [STL](assets/cad/18W-4424G00_ref.stl) |
| SB26STAC-C000-4 (tweeter) | `cad/SB26STAC-C000-4.scad` | [STEP](assets/cad/SB26STAC-C000-4.stp) · [STL](assets/cad/SB26STAC-C000-4_ref.stl) |

See [assets/cad/README.md](assets/cad/README.md) for file provenance and notes.

---

## DSP

MiniDSP 4×10 HD with pre-built XML config.

| Driver path | Filters |
|---|---|
| Woofer (×2) | Subsonic HP ~18 Hz LR4, Linkwitz Transform (39.0→28 Hz, Q 0.76→0.707), LP 150 Hz LR4 |
| Midrange | HP 150 Hz LR4, LP 1100 Hz LR4 |
| Tweeter | HP 1100 Hz LR4, level trim -1.8 dB |

**Pre-built config:** [dsp-configs/](dsp-configs/) — import `mk3-sb26stac-1100hz.xml` via File → Import in MiniDSP plugin. See [dsp-configs/README.md](dsp-configs/README.md) for the full filter specification and biquad coefficients.

---

## Documentation

The full design bible lives in the `docs/` folder:

| Chapter | File |
|---|---|
| Master index | [00_design_bible.md](docs/00_design_bible.md) |
| 1. Project goals | [01_project_goals.md](docs/01_project_goals.md) |
| 2. Theory | [02_theory.md](docs/02_theory.md) |
| 3. Woofer selection | [03_woofer_selection.md](docs/03_woofer_selection.md) |
| 4. Midrange selection | [04_midrange_selection.md](docs/04_midrange_selection.md) |
| 5. Tweeter selection | [05_tweeter_selection.md](docs/05_tweeter_selection.md) |
| 6. Waveguide development | [06_waveguide_development.md](docs/06_waveguide_development.md) |
| 7. Cabinet development | [07_cabinet_development.md](docs/07_cabinet_development.md) |
| 8. Push-push bass | [08_push_push_bass.md](docs/08_push_push_bass.md) |
| 9. Volume calculations | [09_volume_calculations.md](docs/09_volume_calculations.md) |
| 10. Bracing | [10_bracing.md](docs/10_bracing.md) |
| 11. Crossovers | [11_crossovers.md](docs/11_crossovers.md) |
| 12. Directivity | [12_directivity.md](docs/12_directivity.md) |
| 13. Spinorama | [13_spinorama.md](docs/13_spinorama.md) |
| 14. DSP | [14_dsp.md](docs/14_dsp.md) |
| 15. Measurements | [15_measurements.md](docs/15_measurements.md) |
| 16. Build guide | [16_build_guide.md](docs/16_build_guide.md) |
| 17. Future versions | [17_future_versions.md](docs/17_future_versions.md) |
| Tweeter analysis | [SB26STAC-C000-4_analysis.md](docs/SB26STAC-C000-4_analysis.md) |

### Reference files

| File | Contents |
|---|---|
| [DESIGN_REQUIREMENTS.md](DESIGN_REQUIREMENTS.md) | Acoustic and mechanical targets |
| [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) | Rationale for all key design decisions |
| [PARTS.md](PARTS.md) | Driver and materials list with pricing |
| [PROJECT_TODO.md](PROJECT_TODO.md) | Task list and dependency graph |
| [PROTOTYPE_CHECKLIST.md](PROTOTYPE_CHECKLIST.md) | 3-step pre-build verification guide |
| [SIMULATIONS.md](SIMULATIONS.md) | Simulation assumptions and methodology |
| [MEASUREMENTS.md](MEASUREMENTS.md) | Post-build measurement plan |
| [BUILD_LOG.md](BUILD_LOG.md) | Physical build log |
| [ROADMAP.md](ROADMAP.md) | Version history and future plans |
| [CHANGELOG.md](CHANGELOG.md) | Design change log |
| [REFERENCES.md](REFERENCES.md) | Books, papers, tools |
| [CLAUDE.md](CLAUDE.md) | AI assistant context (design spec, edit rules) |

### Datasheets

| Driver | Datasheet | Extracted data |
|---|---|---|
| GRS 12SW-4HE (woofer) | [PDF](assets/datasheets/GRS-12SW-4HE.pdf) | [Full reference](assets/datasheets/GRS-12SW-4HE.md) — Fs 22 Hz, Qts 0.43, Vas 80.4 L, Xmax 12.5 mm (Klippel), Sd 504 cm², Bl 16.2 Tm, 250 W, 84.5 dB |
| GRS 8SW-4HE-8 (woofer, historical — superseded) | [PDF](assets/datasheets/GRS-8SW-4HE-8-spec-sheet.pdf) | [freq response](assets/datasheets/GRS-8SW-4HE-8_freq_response.csv), [impedance](assets/datasheets/GRS-8SW-4HE-8_impedance.csv), [T/S params](assets/datasheets/GRS-8SW-4HE-8_params.csv) |
| ScanSpeak 18W/4424G00 (mid) | [PDF](assets/datasheets/18W-4424G00.pdf) | [Full reference](assets/datasheets/18W-4424G00.md) — Fs 49 Hz, Qts 0.38, Vas 24.1 L, Sd 137 cm², 91 dB; parametric model `cad/midrange.scad` |
| ScanSpeak 15W/4434G00 (mid, historical — superseded in v9) | [PDF](assets/datasheets/15W-4434G00.pdf) | [freq response](assets/datasheets/15W-4434G00_freq_response.csv), [impedance](assets/datasheets/15W-4434G00_impedance.csv), [T/S params](assets/datasheets/15W-4434G00_params.csv) |
| SB Acoustics SB26STAC-C000-4 (tweeter) | [PDF](assets/datasheets/SB26STAC-C000-4.pdf) | [freq response](assets/datasheets/SB26STAC-C000-4_freq_response.csv), [T/S params](assets/datasheets/SB26STAC-C000-4_params.csv) |

See [assets/datasheets/README.md](assets/datasheets/README.md) for extraction details.

---

## Project Status

**Current gate:** Purchase SB26STAC-C000-4 → caliper verify dimensions → print waveguide → measure distortion at 1100 Hz → build prototype.

See [PROJECT_TODO.md](PROJECT_TODO.md) for the full task list and dependency graph. See [PROTOTYPE_CHECKLIST.md](PROTOTYPE_CHECKLIST.md) for the 3-step pre-build guide.

---

## License

MIT
