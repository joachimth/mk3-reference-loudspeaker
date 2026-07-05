# Mk3 Reference Loudspeaker — Project TODO

**Design version:** v8 | **Updated:** July 5, 2026

The design uses the SB Acoustics SB26STAC-C000-4 tweeter with a 1100 Hz LR4 crossover.

Grouped by area. The critical path to prototype is marked 🔴.

---

## 🔴 Critical path — must complete before prototype build

### SB26STAC waveguide

- [ ] **Caliper-verify SB26STAC-C000-4 dimensions** — throat/dome diameter, faceplate OD, mounting screw BCD, recess depth. The SCAD model (`cad/waveguide.scad`) uses datasheet values but none have been physically verified yet.
- [ ] **Print SB26STAC waveguide prototype** (PETG recommended, print flat, slow cool). STL at `cad/exports/waveguide.stl`.
- [ ] **Test-fit SB26STAC in printed waveguide** — verify faceplate seating, throat alignment, screw positions.
- [ ] **Measure SB26STAC distortion at 1100 Hz in waveguide** — this is the gate. Target: ≤2% THD at 1100 Hz / 96 dB SPL. If >3%, raise crossover to 1300-1400 Hz and update all simulation scripts. See `MEASUREMENTS.md` for the distortion test protocol.
- [ ] **Confirm realistic c-c spacing** from printed waveguide flange + 15W frame. Expected ~150-155 mm, not 140 mm nominal. Update `cc_mid_tw_mm` in simulation scripts and DESIGN_DECISIONS.md.

### Cabinet CAD

- [ ] **Verify mid chamber net volume** from `cabinet.scad` solid model — target 5.7 L.
- [ ] **Verify woofer mounting depth** fits 22 mm wall — check GRS 12SW-4HE spec (~136 mm total depth, opposed magnets have only ~4 mm gap in 276 mm internal width).
- [ ] **Confirm driver cutout diameters** — woofer 284 mm (GRS 12SW-4HE datasheet) and midrange 124 mm are estimates. Get exact values from datasheets / physical measurement.
- [x] **Verify divider plate position** in `cabinet.scad` — angled 12° divider plate separates mid chamber from bass volume. Net volume verification pending physical build.
- [x] **Add vertical braces** to `cabinet.scad` — two vertical shelf braces in bass volume at ±120 mm from woofer center, with woofer basket clearance cutouts.
- [ ] **Export STEP file** from cabinet + waveguide models.

### DSP platform

- [x] **MiniDSP 4×10 HD selected** as DSP platform.
- [x] **MiniDSP XML config generated** — `dsp-configs/mk3-sb26stac-1100hz.xml` (import via File → Import in MiniDSP plugin).
- [ ] **Verify DSP config with measurement** — import XML, measure, adjust delays and EQ.

---

## Simulation status

### Completed scripts

| Script | What it does | Status |
|---|---|---|
| `system_response_realistic.py` | Real datasheet curves + baffle step + WG loading. **Fixed July 4:** wg_loading transition formula corrected (parenthesization bug caused smeared gain). 15W datasheet extraction artifact at 400 Hz identified and fixed. | ✅ Verified |
| `spinorama_estimate.py` | Spinorama estimate (on-axis, listening window, early reflections, sound power, DI) using simplified driver models. | ✅ |
| `crossover_optimization.py` | Systematic crossover frequency sweep for SB26STAC (800-1600 Hz). Confirms 1100 Hz as optimal. | ✅ |
| `tweeter_comparison.py` | Tweeter selection analysis (excursion, sensitivity, directivity, Fs margin). | ✅ |
| `directivity_estimate.py` | DI mismatch across crossover. Updated for SB26STAC. | ✅ |
| `vertical_polar_map.py` | Vertical lobing heat-map. Updated for 1100 Hz crossover. | ✅ |

### Simulation issues found and fixed (July 4, 2026)

- [x] **wg_loading_db() parenthesization bug** — `np.log10(f_low) * 0.3` should have been `(np.log10(f_high) - np.log10(f_low)) * 0.3`. This caused the waveguide loading gain to smear across 500-5000 Hz instead of transitioning sharply at the control frequency. Fixed in `system_response_realistic.py`.
- [x] **15W datasheet extraction artifact** — The npz data file had a 27 dB V-shaped dip at 400 Hz (62.5 dB floor) caused by PDF grid-line misread. The clean CSV source (`assets/datasheets/15W-4434G00_freq_response.csv`) shows flat 90.8 dB at 400 Hz. Fixed by regenerating npz from CSV.

### Simulation results (pre-DSP, anechoic)

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

- [ ] **Import measured data** once prototype is built — spinorama.csv, polar data will become comparison targets.
- [ ] **Regenerate all plots** after any crossover frequency change — the plots in `simulations/plots/` are committed but can go stale if scripts are edited without re-running.

---

## CAD — open tasks

- [x] **SB26STAC waveguide CAD** — `cad/waveguide.scad` created. BCD 88.5 mm, throat 28 mm (dome + surround, no horn). STL rendered, manifold.
- [ ] **Waveguide: STEP export** — for external machining.
- [x] **Waveguide: add baffle roundover blend** — `Lr` parameter (25 mm) controls mouth roundover, documented in `cad/README.md`.
- [ ] **Cabinet: 2D cut drawings** — for workshop use.
- [ ] **Cabinet: mid chamber dimensioned drawing** — volume verification.
- [ ] **Verify `wg_through` parameter** in `cabinet.scad` once waveguide is printed.

---

## CI/CD

- [x] **simulations.yml** — pins numpy + matplotlib + scipy versions.
- [x] **cad-render.yml** — auto-renders STL + views on CAD changes.
- [x] **simulations.yml runs all 12 scripts** — verified, all scripts listed and passing.
- [ ] **cad-render.yml: STEP export** — once OpenSCAD→STEP pipeline confirmed.

---

## Build — ordered sequence

*(Not started. Full sequence in `docs/16_build_guide.md`.)*

- [ ] Order all drivers (2× GRS 12SW-4HE, 1× ScanSpeak 15W/4434G00, 1× SB26STAC-C000-4 per speaker)
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
    └─► waveguide printed + test-fit
            └─► distortion measurement at 1100 Hz
                    ├─► crossover frequency confirmed (or adjusted to 1300-1400 Hz)
                    │       └─► DSP config imported + verified
                    │               └─► build starts
                    └─► c-c confirmed from real parts
                            └─► DESIGN_REQUIREMENTS + DD updated
```
