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
| Cabinet | 320 × 380 × 1180 mm, 22 mm birch plywood |
| Front edges | R19 vertical roundovers |
| Bass volume | ~75 L net sealed (below divider plate) |
| Mid chamber | ~13 L net sealed (top section; datasheet rec. 13 L) |
| Bass / mid crossover | 200 Hz BW4 |
| Mid / tweeter crossover | 1100 Hz LR4 |
| Mid / tweeter c-c | 164 mm (physical minimum; verify from physical parts) |
| DSP gains | Woofer 0 dB (unity), Mid -4.0 dB, Tweeter -9.0 dB |
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

All simulations use real datasheet frequency response curves, baffle step modeling, and waveguide loading estimates. The anechoic plot shows pre-DSP response; the in-room plot adds room gain modeling, level correction, and DSP EQ toward a Harman in-room target.

### Anechoic per-driver crossover sum

![Anechoic crossover sum](simulations/plots/system_response_anechoic.png)

Individual driver curves with DSP level adjustments and coherent sum through LR4 crossovers. No room gain, no EQ — raw anechoic only.

| Driver | DSP gain | Filter |
|---|---|---|
| 2× GRS 12SW-4HE (woofer) | 0.0 dB (unity) | LP 200 Hz BW4, HP 18 Hz subsonic |
| ScanSpeak 18W/4424G00 (mid) | −4.0 dB | HP 200 BW4 / LP 1100 Hz LR4 |
| SB26STAC-C000-4 (tweeter) | −9.0 dB | HP 1100 Hz LR4, WG +2.5 dB |

| Metric | Value |
|---|---|
| Midband ripple (500-10k) | 2.8 dB |
| Sum @ 500 Hz | 0 dB (reference) |
| Sum @ 2 kHz | −2.3 dB |
| Sum @ 10 kHz | −1.8 dB |

**Script:** [system_response_anechoic.py](simulations/system_response_anechoic.py)

### In-room, level-corrected, and post-DSP

![In-room response progression](simulations/plots/system_response_inroom.png)

Four-stage progression from anechoic to post-DSP, modeling an average living room (4.5×4×2.4 m, 43 m³, RT60 0.4s).

**Optimized gains (in-room vs Harman target):**

| Driver | DSP gain |
|---|---|
| 2× GRS 12SW-4HE (woofer) | 0.0 dB (unity) || ScanSpeak 18W/4424G00 (mid) | −4.0 dB |
| SB26STAC-C000-4 (tweeter) | −9.0 dB |

| Stage | Ripple 500-10k | @100 Hz | @500 Hz | @10 kHz |
|---|---|---|---|---|
| Anechoic (pre-DSP) | 2.8 dB | 82.9 | 86.9 | 85.1 |
| In-room | 3.7 dB | 88.6 | 86.9 | 83.6 |
| Level-corrected | 3.7 dB | 1.7 | 0.0 | −3.3 |
| Post-DSP | 3.5 dB* | 1.7 | 0.1 | −3.3 |

*Post-DSP ripple includes intentional Harman bass shelf + HF tilt. Residual deviation from target: ±0.3 dB (500-10k). DSP correction range: ±1.3 dB.

**Script:** [system_response_inroom.py](simulations/system_response_inroom.py)

### In-room gain optimization

![Gain optimization](simulations/plots/inroom_gain_optimization.png)

Three-stage progression showing why gain correction is needed and what it achieves:

| Stage | @100 Hz | @2 kHz | @10 kHz | RMS deviation |
|---|---|---|---|---|
| All gains = 0 dB | −2.1 | +2.0 | +1.7 | 3.59 dB |
| Optimized (W0/M−4/T−9) | +1.7 | −2.3 | −3.3 | 0.59 dB |
| Post-DSP (±1.3 dB PEQ) | +1.7 | −1.0 | −3.3 | 0.06 dB |

Driver sensitivities explain the needed pads: woofer pair 87.5 dB, mid 92.0 dB (+4.5 dB), tweeter+WG 93.5 dB (+6.0 dB). The extra tweeter pad beyond sensitivity matching (−9 vs −6) accounts for the Harman HF tilt target.

The optimizer confirms W0/M−4.0/T−9.0 as optimal at 0.1 dB resolution. Spreads: W−M = 4.0 dB, M−T = 5.0 dB. Woofer at 0 dB unity avoids wasting DAC headroom.

**Script:** [inroom_gain_optimization.py](simulations/inroom_gain_optimization.py)

### Target comparison: Harman vs BBC-style

![Target comparison](simulations/plots/target_comparison.png)

Two in-room target philosophies with their optimal per-driver gains:

| Target | Woofer | Mid | Tweeter | W-M spread | M-T spread | Character |
|---|---|---|---|---|---|---|
| **Harman** | 0.0 dB | −4.0 dB | −9.0 dB | 4.0 dB | 5.0 dB | Flat, modern, slightly bright |
| **BBC-style** | 0.0 dB | −3.0 dB | −8.0 dB | 3.0 dB | 5.0 dB | Warm, vocal-forward, less fatiguing |

Both share M-T = 5.0 dB spread. BBC needs 1 dB less woofer-to-mid because the −2 dB presence dip at 2 kHz naturally lowers the mid in the critical vocal region. Post-DSP residual: ±0.3 dB for both. DSP correction: Harman ±1.3 dB, BBC ±1.7 dB.

**Harman target:** +3.5 dB bass shelf below 100 Hz, −1 dB/octave HF tilt above 1 kHz (Olive et al. research).
**BBC target:** −2 dB presence dip at 2 kHz, +2 dB bass shelf below 120 Hz, −0.8 dB/octave HF tilt above 3 kHz (LS3/5a school).

**Script:** [target_comparison.py](simulations/target_comparison.py)

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

Baffle step is modeled with separate effective radii for side-mounted woofers vs front-mounted mid/tweeter, parsed from [cabinet.scad](cad/cabinet.scad) via [cabinet_params.py](simulations/cabinet_params.py):

| Driver | Mount | Baffle dimension | Effective radius | f_bs |
|---|---|---|---|---|
| 2× GRS 12SW-4HE | Side panel | D = 380 mm | 190 mm | 287 Hz |
| 18W/4424G00 | Front baffle | W = 320 mm | 160 mm | 341 Hz |
| SB26STAC-C000-4 | Front baffle | W = 320 mm | 160 mm | 341 Hz |

All simulation scripts import from `cabinet_params.py` which parses `cad/cabinet.scad` at runtime. CI validates consistency on every push.

**Scripts:** [baffle_step.py](simulations/baffle_step.py), [cabinet_params.py](simulations/cabinet_params.py)

### Waveguide profile

![Waveguide profile](simulations/plots/waveguide_termination.png)

**Script:** [waveguide_profile.py](simulations/waveguide_profile.py)

### All simulation scripts

| Script | What it computes | Output |
|---|---|---|
| `bass_alignment_maxspl.py` | Sealed alignment + excursion-limited max-SPL + Linkwitz Transform | `bass_alignment_maxspl.png` |
| `bass_volume_compare.py` | Sealed alignment sensitivity to box volume (64-72 L) | `bass_volume_compare.png` |
| `baffle_step.py` | Baffle step diffraction model (standalone visualization) | `baffle_step.png` |
| `cabinet_params.py` | Parses cabinet.scad for dimensions; provides side/front baffle step functions | — (module) |
| `waveguide_profile.py` | Waveguide mouth-to-baffle termination cross-section | `waveguide_termination.png` |
| `directivity_estimate.py` | Directivity index across crossover | `directivity_estimate.png` |
| `vertical_lobing.py` | Vertical interference-null angle vs frequency | `vertical_lobing.png` |
| `vertical_polar_map.py` | Vertical 2D heat-map vs frequency | `vertical_polar_map.png` |
| `polar_response.py` | 2D polar map + spinorama curves + horizontal polar cuts | `polar_response.png` |
| `system_response_realistic.py` | Full system response with real datasheet curves | `system_response_realistic.png` |
| `system_response_anechoic.py` | Per-driver crossover sum, anechoic, pre-EQ, pre-room | `system_response_anechoic.png` |
| `system_response_inroom.py` | 4-stage: anechoic → in-room → level-corrected → post-DSP | `system_response_inroom.png` |
| `target_comparison.py` | Harman vs BBC-style in-room targets with optimal gains | `target_comparison.png` |
| `inroom_gain_optimization.py` | In-room response: all-zero vs optimized gains vs post-DSP, with sensitivity analysis | `inroom_gain_optimization.png` |
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

### Cabinet Drawings & Cut List

Dimensioned 2D drawings auto-generated from `cabinet.scad` + driver SCAD files. Updated by CI on every push.

**[→ Open interactive drawing viewer](assets/drawings/index.html)** — all 12 drawings with navigation, per-drawing download, and combined PDF.

**[→ Download all drawings (PDF, 13 pages)](assets/drawings/mk3-cabinet-drawings.pdf)**

Overview drawings:

| Drawing | SVG | PDF | Description |
|---|---|---|---|
| Assembly dims | [SVG](assets/drawings/assembly_dims.svg) | [PDF](assets/drawings/assembly_dims.pdf) | Front + side elevation, driver heights, internal dims |
| Cut list | [SVG](assets/drawings/cut_list.svg) | [PDF](assets/drawings/cut_list.pdf) | All panels with dimensions, quantities, notes |
| Front baffle | [SVG](assets/drawings/front_baffle.svg) | [PDF](assets/drawings/front_baffle.pdf) | Midrange + waveguide cutouts, rebates, pilot holes |
| Side panel | [SVG](assets/drawings/side_panel.svg) | [PDF](assets/drawings/side_panel.pdf) | Woofer cutout, 8 pilot holes on BCD, shelf positions |

Per-panel cut drawings:

| Panel | SVG | PDF |
|---|---|---|
| Front baffle | [SVG](assets/drawings/panel_front_baffle.svg) | [PDF](assets/drawings/panel_front_baffle.pdf) |
| Back panel | [SVG](assets/drawings/panel_back.svg) | [PDF](assets/drawings/panel_back.pdf) |
| Side panel L | [SVG](assets/drawings/panel_side_left.svg) | [PDF](assets/drawings/panel_side_left.pdf) |
| Side panel R | [SVG](assets/drawings/panel_side_right.svg) | [PDF](assets/drawings/panel_side_right.pdf) |
| Top panel | [SVG](assets/drawings/panel_top.svg) | [PDF](assets/drawings/panel_top.pdf) |
| Bottom panel | [SVG](assets/drawings/panel_bottom.svg) | [PDF](assets/drawings/panel_bottom.pdf) |
| Divider plate | [SVG](assets/drawings/panel_divider.svg) | [PDF](assets/drawings/panel_divider.pdf) |
| Shelf brace ×3 | [SVG](assets/drawings/panel_shelf_brace.svg) | [PDF](assets/drawings/panel_shelf_brace.pdf) |

Alternative material cut plan:

| Drawing | SVG | PDF | Description |
|---|---|---|---|
| Pine board cut plan | [SVG](assets/drawings/pine_cutplan.svg) | [PDF](assets/drawings/pine_cutplan.pdf) | 3× 25×620×2420 mm massiv fyr (Jem & Fix) — rip + crosscut layout |

Generator: `scripts/generate_drawings.py` (parses SCAD source files, no hardcoded dimensions).

### Cabinet v2 (baffel_insert variant)

Alternative cabinet design with a 3D-printed baffel insert. Same enclosure,
bracing, and woofer placement, but the front baffle has a single pocket for
a precision-printed insert instead of individual driver cutouts in plywood.
The insert provides flush rebate for the midrange, pocket + elliptical hole
for the waveguide, and precise screw patterns.

| | | |
|:---:|:---:|:---:|
| ![Front](assets/renders/cabinet_v2_front.png) | ![Iso](assets/renders/cabinet_v2_iso.png) | ![Cutaway](assets/renders/cabinet_v2_cutaway.png) |
| Front (with insert + drivers) | Isometric | Half-section cutaway |

**CAD:** `cad/cabinet_v2.scad` | **STL:** `cad/exports/cabinet_v2.stl` | **Insert:** `cad/baffel_insert_1.scad`

#### Baffel insert (3D-print)

| | | |
|:---:|:---:|:---:|
| ![Front](assets/renders/baffel_insert_front.png) | ![Fit front](assets/renders/baffel_insert_fit_front.png) | ![Fit iso](assets/renders/baffel_insert_fit_iso.png) |
| Print-ready (front) | With all drivers fitted | Fitted isometric |
| ![Fit rear](assets/renders/baffel_insert_fit_rear.png) | ![Section](assets/renders/baffel_insert_section.png) | |
| Fitted rear view | Half-section | |

The insert is 285 x 380 x 15 mm with backside ribbing for stiffness. Print
flat (backside down). `vis="fit"` shows the insert with the 18W/4424G00
midrange and SB26STAC tweeter in place for visual verification.

Parametric OpenSCAD models for each driver, plus manufacturer/reference 3D geometry.

#### GRS 12SW-4HE (woofer)

| | | |
|:---:|:---:|:---:|
| ![Front](assets/renders/driver_woofer_front.png) | ![Iso](assets/renders/driver_woofer_iso.png) | ![Section](assets/renders/driver_woofer_section.png) |
| Front | Isometric | Half-section |

**SCAD:** `cad/GRS-12SW-4HE.scad` | **3D:** — (datasheet only) | **Template:** `vis="skabelon"` for drill template

#### ScanSpeak 18W/4424G00 (midrange)

| | | |
|:---:|:---:|:---:|
| ![Front](assets/renders/driver_midrange_front.png) | ![Iso](assets/renders/driver_midrange_iso.png) | ![Section](assets/renders/driver_midrange_section.png) |
| Front | Isometric | Half-section |

**SCAD:** `cad/midrange.scad` | **STEP:** [18W-4424G00.STEP](assets/cad/18W-4424G00.STEP) | **STL:** [reference](assets/cad/18W-4424G00_ref.stl)

#### SB26STAC-C000-4 (tweeter)

| | | |
|:---:|:---:|:---:|
| ![Front](assets/renders/driver_tweeter_front.png) | ![Iso](assets/renders/driver_tweeter_iso.png) | ![Section](assets/renders/driver_tweeter_section.png) |
| Front | Isometric | Half-section |

**SCAD:** `cad/SB26STAC-C000-4.scad` | **STEP:** [SB26STAC-C000-4.stp](assets/cad/SB26STAC-C000-4.stp) | **STL:** [reference](assets/cad/SB26STAC-C000-4_ref.stl)

See [assets/cad/README.md](assets/cad/README.md) for file provenance and notes.

---

## DSP

MiniDSP 4×10 HD with pre-built XML config.

| Driver path | Filters |
|---|---|
| Woofer (×2) | Subsonic HP ~18 Hz LR2, Linkwitz Transform (39.0→28 Hz, Q 0.76→0.707), LP 200 Hz BW4, gain 0 dB |
| Midrange | HP 200 Hz BW4, LP 1100 Hz LR4, gain -4.0 dB |
| Tweeter | HP 1100 Hz LR4, gain -9.0 dB |

**Pre-built config:** [dsp-configs/](dsp-configs/) — import `mk3-v9-200-1100-bw4-lr4.xml` via File → Import in MiniDSP plugin. See [dsp-configs/README.md](dsp-configs/README.md) for the full filter specification and biquad coefficients.

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
| Drawings guide | [DRAWINGS_GUIDE.md](docs/DRAWINGS_GUIDE.md) |

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
