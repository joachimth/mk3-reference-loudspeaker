# Mk3 Reference Loudspeaker — Project TODO

**Branch:** `mk3-sb26stac` | **Design version:** v7 | **Updated:** July 4, 2026

This branch uses the SB Acoustics SB26STAC-C000-4 tweeter with a 1100 Hz LR4 crossover.
The `main` branch retains the original mk2 design (H2606/920000, 1250 Hz).

Grouped by area. The critical path to prototype is marked 🔴.

---

## 🔴 Critical path — must complete before prototype build

### WG212 waveguide (SB26STAC version)

- [ ] **Caliper-verify SB26STAC-C000-4 dimensions** — throat/dome diameter, faceplate OD, mounting screw BCD, recess depth. The SCAD model (`cad/mk2_waveguide_sb26stac.scad`) uses datasheet values but none have been physically verified yet.
- [ ] **Print WG212-SB26STAC prototype** (PETG recommended, print flat, slow cool). STL at `cad/exports/sb26stac/waveguide_sb26stac.stl`.
- [ ] **Test-fit SB26STAC in printed waveguide** — verify faceplate seating, throat alignment, screw positions.
- [ ] **Measure SB26STAC distortion at 1100 Hz in WG212** — this is the gate. Target: ≤2% THD at 1100 Hz / 96 dB SPL. If >3%, raise crossover to 1300-1400 Hz and update all simulation scripts. See `H2606_DISTORTION_TEST.md` (protocol applies to SB26STAC with 1100 Hz target frequency).
- [ ] **Confirm realistic c-c spacing** from printed waveguide flange + 15W frame. Expected ~150-155 mm, not 140 mm nominal. Update `cc_mid_tw_mm` in simulation scripts and DESIGN_DECISIONS.md.

### Cabinet CAD

- [ ] **Verify mid chamber net volume** from `cabinet.scad` solid model — target 5.7 L.
- [ ] **Verify woofer mounting depth** fits 22 mm wall — check GRS 8SW-4HE-8 spec.
- [ ] **Confirm driver cutout diameters** — woofer 185 mm and midrange 124 mm are estimates. Get exact values from datasheets / physical measurement.
- [ ] **Add vertical braces** to `cabinet.scad`.
- [ ] **Export STEP file** from cabinet + waveguide models.

### DSP platform

- [x] **MiniDSP 4×10 HD selected** as DSP platform.
- [x] **MiniDSP XML config generated** — `dsp-configs/mk3-sb26stac-1100hz.xml` (on `main` branch, import via File → Import in MiniDSP plugin). Note: this file exists on `main` but is NOT on the `mk3-sb26stac` branch yet. See todo below.
- [ ] **Copy dsp-configs/ to mk3 branch** — the XML generator and pre-built configs currently live only on `main`.
- [ ] **Verify DSP config with measurement** — import XML, measure, adjust delays and EQ.

---

## Simulation status

### Completed scripts (mk3-specific)

| Script | What it does | Status |
|---|---|---|
| `mk2_vs_mk3_realistic_response.py` | Real datasheet curves + baffle step + WG loading. **Fixed July 4:** wg_loading transition formula corrected (parenthesization bug caused smeared gain). 15W datasheet extraction artifact at 400 Hz identified and fixed. | ✅ Verified |
| `mk2_vs_mk3_spinorna.py` | Spinorama estimate (on-axis, listening window, early reflections, sound power, DI) using simplified driver models. | ✅ |
| `mk3_crossover_optimization.py` | Systematic crossover frequency sweep for SB26STAC (800-1600 Hz). Confirms 1100 Hz as optimal. | ✅ |
| `h2606_vs_sb26stac_comparison.py` | Head-to-head driver comparison (excursion, sensitivity, directivity, Fs margin). | ✅ |
| `directivity_estimate.py` | DI mismatch across crossover. Updated for SB26STAC. | ✅ |
| `vertical_polar_map.py` | Vertical lobing heat-map. Updated for 1100 Hz crossover. | ✅ |

### Simulation issues found and fixed (July 4, 2026)

- [x] **wg_loading_db() parenthesization bug** — `np.log10(f_low) * 0.3` should have been `(np.log10(f_high) - np.log10(f_low)) * 0.3`. This caused the waveguide loading gain to smear across 500-5000 Hz instead of transitioning sharply at the control frequency. Fixed in `mk2_vs_mk3_realistic_response.py`.
- [x] **15W datasheet extraction artifact** — The npz data file had a 27 dB V-shaped dip at 400 Hz (62.5 dB floor) caused by PDF grid-line misread. The clean CSV source (`assets/datasheets/15W-4434G00_freq_response.csv`) shows flat 90.8 dB at 400 Hz. Fixed by regenerating npz from CSV.
- [x] **Datasheet CSVs added to mk3 branch** — The freq_response CSV files were only on `main`, not on `mk3-sb26stac`. Copied over so simulations are reproducible without switching branches.

### Simulation results (mk3, pre-DSP, anechoic)

| Metric | Value |
|---|---|
| ±3 dB bandwidth | 623-9710 Hz |
| Midband ripple (500-10k) | 4.2 dB |
| Passband ripple (200-15k) | 7.5 dB |
| Sum @ 1100 Hz (crossover) | 89.9 dB |
| Sum @ 100 Hz | 83.0 dB |
| Sum @ 10 kHz | 92.3 dB |
| DSP correction needed (midband) | ±4.0 dB |

### Open simulation tasks

- [ ] **Update `system_response.py`** to use real SB26STAC datasheet curve instead of tanh placeholder. Currently still uses the mk2 placeholder model.
- [ ] **Import measured data** once prototype is built — spinorama.csv, polar data will become comparison targets.
- [ ] **Port `real_datasheet_response.py` to mk3 branch** — the main branch has a more sophisticated simulation script (758 lines) with coherent summing, off-axis curves, and proper sealed cabinet blending. The mk3 branch only has the comparison script. Consider consolidating.
- [ ] **Regenerate all plots** after any crossover frequency change — the plots in `simulations/plots/` are committed but can go stale if scripts are edited without re-running.

---

## CAD — open tasks

- [x] **SB26STAC waveguide CAD** — `cad/mk2_waveguide_sb26stac.scad` created. BCD 88.5 mm, throat 28 mm (dome + surround, no horn). STL rendered, manifold.
- [ ] **Waveguide: STEP export** — for external machining.
- [ ] **Waveguide: add baffle roundover blend** — `Lr` controls mouth roundover. Document in `cad/README.md`.
- [ ] **Cabinet: 2D cut drawings** — for workshop use.
- [ ] **Cabinet: mid chamber dimensioned drawing** — volume verification.
- [ ] **Verify `wg_through` parameter** in `cabinet.scad` once waveguide is printed.

---

## Documentation — needs updating for mk3

These files still contain mk2-primary content and should be reviewed/updated:

- [ ] **TODO.md** — still describes mk2 v6b tasks. Should be removed or merged into this file to avoid confusion.
- [ ] **ROADMAP.md** — no v7/mk3 entry. Should document the branch from mk2 to mk3.
- [ ] **REVIEW.md** — written for mk2 (questions 1250 Hz / 140 mm c-c). On mk3, crossover is 1100 Hz. Should note which review items are resolved by the mk3 design.
- [ ] **DESIGN_DECISIONS.md** — needs DD entries for SB26STAC selection, 1100 Hz crossover, and SB26STAC waveguide design.
- [ ] **DESIGN_REQUIREMENTS.md** — crossover should read 1100 Hz, not 1250 Hz.
- [ ] **PARTS.md** — should list SB26STAC-C000-4 as primary tweeter, H2606 as fallback.
- [ ] **PROTOTYPE_CHECKLIST.md** — references H2606/WG212 at 1250 Hz. Should reference SB26STAC at 1100 Hz.
- [ ] **SIMULATIONS.md** — should list the new mk3 simulation scripts.
- [ ] **simulations/README.md** — script table is missing mk3-specific scripts.
- [ ] **CHANGELOG.md** — needs v7/mk3 entry.
- [ ] **docs/11_crossovers.md** — should document 1100 Hz LR4 as primary.
- [ ] **docs/06_waveguide_development.md** — should cover SB26STAC waveguide design.
- [ ] **docs/14_dsp.md** — should reference mk3 MiniDSP config (1100 Hz).
- [ ] **MEASUREMENTS.md** — distortion test target should be 1100 Hz.
- [ ] **CLAUDE.md** — should reflect mk3 design parameters.
- [ ] **assets/mk2_design_bible_sb23.md** — stale reference from SB23 era. Should be clearly marked as historical only, or moved to an archive folder.

---

## CI/CD

- [x] **simulations.yml** — pins numpy + matplotlib versions.
- [x] **cad-render.yml** — auto-renders STL + views on CAD changes.
- [ ] **cad-render.yml: STEP export** — once OpenSCAD→STEP pipeline confirmed.
- [ ] **simulations.yml: run mk3 scripts** — verify CI runs the new mk3 simulation scripts and they pass.

---

## Build — ordered sequence

*(Not started. Full sequence in `docs/16_build_guide.md`.)*

- [ ] Order all drivers (2× GRS 8SW-4HE-8, 1× ScanSpeak 15W/4434G00, 1× SB26STAC-C000-4 per speaker)
- [ ] Order MiniDSP 4×10 HD
- [ ] Order 22 mm birch plywood (~4 sheets per pair)
- [ ] Order hardware (threaded inserts, gasket tape, terminal plate, cable)
- [ ] Cut panels (Phase 1)
- [ ] Cut driver cutouts — confirm diameters from physical drivers first (Phase 2)
- [ ] Assemble mid chamber (Phase 3)
- [ ] Assemble main cabinet (Phase 4)
- [ ] Internal damping (Phase 5)
- [ ] Install woofers — verify push-push polarity with battery test (Phase 6)
- [ ] Install mid chamber + midrange (Phase 7)
- [ ] Install waveguide + SB26STAC tweeter — confirm c-c from built cabinet (Phase 8)
- [ ] Sand + finish (Phase 9)
- [ ] Install electronics (Phase 10)

---

## Measurements (post-build)

*(Full plan in `docs/15_measurements.md` and `MEASUREMENTS.md`.)*

- [ ] Measure SB26STAC distortion at 1100 Hz **before** finalizing crossover — this is the design gate
- [ ] Nearfield woofer measurement
- [ ] Nearfield midrange measurement
- [ ] Nearfield tweeter/waveguide measurement
- [ ] Far-field on-axis (gated or outdoor ground-plane)
- [ ] Polar sweep horizontal: 0° → 180° in 10° steps
- [ ] Polar sweep vertical: ±30° in 10° steps
- [ ] Import to VituixCAD — extract acoustic centers, set delays
- [ ] Finalize DSP: delays + baffle step EQ + waveguide EQ + Linkwitz Transform
- [ ] REW preset file backup

---

## Summary — what's blocking what

```
SB26STAC purchased + caliper verified
    └─► WG212-SB26STAC printed + test-fit
            └─► distortion measurement at 1100 Hz
                    ├─► crossover frequency confirmed (or adjusted to 1300-1400 Hz)
                    │       └─► DSP config imported + verified
                    │               └─► build starts
                    └─► c-c confirmed from real parts
                            └─► DESIGN_REQUIREMENTS + DD updated
```

## Relationship to mk2 (main branch)

The `main` branch is the **fallback path**. If the SB26STAC distortion test at 1100 Hz fails and the crossover cannot be raised enough, the mk2 design (H2606 at 1250 Hz) remains viable. Key differences:

| Parameter | mk3 (this branch) | mk2 (main) |
|---|---|---|
| Tweeter | SB26STAC-C000-4 | H2606/920000 |
| Crossover | 1100 Hz LR4 | 1250 Hz LR4 |
| Waveguide | SB26STAC custom (no horn) | WG212 (horn-loaded) |
| Tweeter Fs | 750 Hz | 1030 Hz |
| Excursion headroom | +8.1 dB | 0 dB (ref) |
| Sensitivity match | -1.8 dB pad | -5.5 dB pad |

See `docs/SB26STAC-C000-4_analysis.md` for the full driver comparison.
