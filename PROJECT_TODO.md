# Mk2 Reference Loudspeaker — Project TODO

Generated June 22, 2026 after full repo audit.
Grouped by area. The critical path to prototype is marked 🔴.

---

## 🔴 Critical path — must complete before prototype build

### WG212 waveguide
- [ ] **Measure real H2606/920000 throat exit diameter** — update `throat_d` in `cad/mk2_waveguide_os.scad` (currently 28 mm placeholder). Print throat test pieces first. Without this, the print is a gamble.
- [ ] **Print WG212 prototype** (PETG recommended, print flat, slow cool). Use STL from the CI release.
- [ ] **Test-fit H2606 in printed WG212** — verify faceplate seating pocket depth (`tw_fp_recess=4`), back-plate diameter (`tw_ring_od=130`), and screw hole positions (BCD 92 mm).
- [ ] **Measure H2606 distortion at 1250 Hz in WG212** — this is the gate. If THD at 1250 Hz is acceptable (< ~1-2%), the crossover target holds. If not, shift to 1350-1450 Hz and update `fc_mid` in all simulation scripts.
- [ ] **Confirm realistic c-c spacing** from the printed WG212 flange + 15W frame — expected ~150-155 mm, not 140 mm. Update `cc_mid_tw_mm` in `simulations/design_versions_comparison.py` and DESIGN_DECISIONS.md DD-011.

### Cabinet CAD
- [ ] **Verify mid chamber net volume** from `cabinet.scad` solid model — target 5.7 L. Currently listed as "representational."
- [ ] **Verify woofer mounting depth** fits 22 mm wall — check GRS 8SW-4HE-8 spec for max mounting depth. Risk noted in build guide.
- [ ] **Confirm driver cutout diameters** — woofer 185 mm and midrange 124 mm are estimates. Get exact values from datasheets / physical measurement.
- [ ] **Add vertical braces** to `cabinet.scad` — noted as open in TODO.md.
- [ ] **Export STEP file** from cabinet + waveguide models (for CNC or external review).

### DSP platform
- [ ] **Select DSP/amplifier platform** — MiniDSP 4×10 HD, Hypex FusionAmp FA123/FA253, or ADAU1452 custom. Decision needed before ordering electronics.

---

## Documentation fixes (known errors)

- [x] **README.md "Next steps"** — updated to current state: print WG212 → measure → build prototype. CI badges added.
- [x] **`docs/00_design_bible.md` chapter status column** — all 17 chapters now have accurate status (Complete / Plan written / etc.).
- [x] **`simulations/README.md`** — all 11 scripts now in the table, including `crossover_simulation`, `system_response`, `polar_response`, `vertical_polar_map`, `design_versions_comparison`, `baffle_step`.
- [x] **DESIGN_REQUIREMENTS.md** — c-c entry now notes 140 mm nominal vs ~150–155 mm expected from physical parts.
- [x] **PARTS.md** — quantities per pair, indicative pricing, supplier notes, DSP platform candidates and open items added.
- [x] **`assets/README.md`** — column descriptions added for `mk2_dsp.csv`, `mk2_parametre.csv`, `mk2_stykliste.csv`.

---

## Simulations — open tasks

- [ ] **Update `system_response.py` tweeter model** once H2606-in-WG212 is measured. The current tanh step is a placeholder — swap it for a polynomial fit to the real FR.
- [x] **Add DSP EQ / Linkwitz Transform to `bass_alignment_maxspl.py`** — already present (line 81).
- [x] **Add baffle step simulation** — `baffle_step.py` added. Vanderkooy single-pole model, 300 mm wide cabinet, f_bs ≈ 325 Hz. PNG + CSV output.
- [x] **Group delay plot** — `bass_volume_compare.py` already has a group delay subplot (ax2).
- [ ] **Import measured data** into simulation scripts once prototype is built — spinorama.csv, polar_horizontal.csv will become comparison targets.

---

## CAD — open tasks

- [ ] **Waveguide: STEP export** — for external machining or material comparison.
- [x] **Waveguide CAD: fix stale header comment** — header said "crossover at ~1600 Hz"; corrected to 1250 Hz LR4 (unconfirmed) with fallback options.
- [x] **Waveguide CAD: add `min(1.0, ...)` clamp in `prof_r`** — defensive guard against floating-point rounding at z=D_tot where asin argument is algebraically exactly 1.0.
- [x] **cabinet.scad: sync mouth/flange dims from waveguide** — was hardcoded (211.7×121.0 mm etc.); now uses exported functions `wg_mouth_rx()`, `wg_mouth_ry()`, `wg_flange_w_fn()`, etc. so any waveguide geometry change propagates automatically.
- [x] **Official H2606/920000 datasheets added** — PDF + drawing PNG + STEP + IGS + x_t in `assets/datasheets/`. README with all key dimensions.
- [x] **`throat_d` corrected: 28 → 33 mm** — from official ScanSpeak STEP file. H2606 horn exit is ø33.0 mm (r=16.5 at front face). The WG212 is an extension waveguide starting at the H2606's horn exit. Verify with calipers on physical unit.
- [x] **`tw_bcd` corrected: 92 → 95 mm** — from drawing (Pitch diam. ø95 ±0.1 mm). Previous value would have placed all 4 mounting screws 1.5 mm too close to centre; tweeter would not mount correctly.
- [x] **`tw_face_d` corrected: 104.3 → 104.0 mm** — from drawing (ø104 ±0.2 mm).
- [x] **`tw_hole_d` corrected: 4.4 → 4.0 mm** — from drawing (ø4 ±0.10 mm × 4).
- [ ] **Waveguide: add baffle roundover blend** — `Lr` controls the mouth roundover. Document in `cad/README.md` how to increase `Lr` for a smoother mouth-to-baffle transition (currently 10 mm, could go to 18-20 mm for a more gradual blend).
- [ ] **Cabinet: 2D cut drawings** — for workshop use. Currently only OpenSCAD 3D model, no panel dimensions sheet.
- [ ] **Cabinet: mid chamber dimensioned drawing** — volume verification requires a proper dimensioned sketch.
- [ ] **Verify `wg_through` parameter** in `cabinet.scad` (currently 0.3 mm overlap) — once the WG212 is printed and measured, confirm this cosmetic offset is correct.

---

## CI/CD — minor improvements

- [ ] **`cad-render.yml`: add STEP export** once an OpenSCAD→STEP pipeline is confirmed (OpenSCAD 2021.01 supports `--export-format binstl`; STEP requires either a newer version or FreeCAD scripting).
- [x] **`simulations.yml`: pin numpy + matplotlib versions** — now `>=1.26,<3` and `>=3.8,<4`.
- [x] **Add a `README.md` badge** for the simulations workflow status — both CI badges added to README Project Status section.
- [ ] **`cad-render.yml` camera angles** — review after first render run; adjust if the views aren't informative.

---

## Build — ordered sequence

*(Not started. Full sequence in `docs/16_build_guide.md`.)*

- [ ] Order all drivers (2× GRS 8SW-4HE-8, 1× ScanSpeak 15W/4434G00, 1× H2606/920000 per speaker)
- [ ] Order DSP/amplifier platform
- [ ] Order 22 mm birch plywood (~4 sheets per pair)
- [ ] Order hardware (threaded inserts, gasket tape, terminal plate, cable)
- [ ] Cut panels (Phase 1)
- [ ] Cut driver cutouts — confirm diameters from physical drivers first (Phase 2)
- [ ] Assemble mid chamber (Phase 3)
- [ ] Assemble main cabinet (Phase 4)
- [ ] Internal damping (Phase 5)
- [ ] Install woofers — verify push-push polarity with battery test (Phase 6)
- [ ] Install mid chamber + midrange (Phase 7)
- [ ] Install WG212 + tweeter — confirm c-c from built cabinet (Phase 8)
- [ ] Sand + finish (Phase 9)
- [ ] Install electronics (Phase 10)

---

## Measurements (post-build)

*(Full plan in `docs/15_measurements.md` and `MEASUREMENTS.md`.)*

- [ ] Measure H2606 distortion at 1250 Hz **before** finalizing crossover — this is the design gate
- [ ] Nearfield woofer measurement
- [ ] Nearfield midrange measurement
- [ ] Nearfield tweeter/WG measurement
- [ ] Far-field on-axis (gated or outdoor ground-plane)
- [ ] Polar sweep horizontal: 0° → 180° in 10° steps
- [ ] Polar sweep vertical: ±30° in 10° steps
- [ ] Import to VituixCAD — extract acoustic centers, set delays
- [ ] Finalize DSP: delays + baffle step EQ + waveguide EQ + Linkwitz Transform
- [ ] REW preset file backup

---

## Future versions (not blocking v6b)

- [ ] **v7: Cardioid bass** — rear-firing woofer array for dipole/cardioid bass cancellation
- [ ] **v8: Purifi midrange** — swap 15W for Purifi 5" or 6.5" once crossover frequency is measured
- [ ] **v9: Bliesma tweeter** — Bliesma T25B or similar as alternative to H2606
- [ ] **v10: FIR crossovers** — linear-phase crossover once DSP platform supports it
- [ ] **GitHub Pages site** — render the design bible as a static site from the `docs/` folder

---

## Summary — what's blocking what

```
throat_d verified
    └─► WG212 printed + H2606 test-fit
            └─► distortion measurement at 1250 Hz
                    ├─► crossover frequency confirmed (or adjusted to 1350-1450 Hz)
                    │       └─► DSP platform selected
                    │               └─► build starts
                    └─► c-c confirmed from real parts
                            └─► DESIGN_REQUIREMENTS + DD-011 updated
```
