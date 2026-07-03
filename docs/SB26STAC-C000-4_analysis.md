# SB Acoustics SB26STAC-C000-4 — Alternative Tweeter Analysis

**Date:** July 4, 2026
**Purpose:** Evaluation as replacement/alternative for ScanSpeak H2606/920000 in the mk2-reference-loudspeaker
**Datasheet:** `assets/datasheets/SB26STAC-C000-4.pdf`

---

## Driver Summary

The SB26STAC-C000-4 is a 26mm soft dome tweeter from SB Acoustics with a cast aluminium faceplate, copper-capped pole piece, and a non-reflective rear chamber with optimized damping. It is a **conventional flush-mount dome tweeter**, not a horn-loaded tweeter.

Key features: low Fs (750 Hz), CCAW voice coil, vented pole piece, silver lead wires, saturation-controlled motor.

---

## Side-by-side comparison

| Parameter | SB26STAC-C000-4 | H2606/920000 | Notes |
|---|---|---|---|
| **Type** | Conventional soft dome | Horn dome tweeter | Fundamentally different |
| Dome | 26mm fine weave fabric | 25mm coated textile | Similar |
| **Impedance** | 4 Ω | 6 Ω | SB26 draws more current |
| Re | 3.2 Ω | 4.7 Ω | |
| **Fs** | **750 Hz** | **1030 Hz** | **280 Hz lower — the key difference** |
| **Sensitivity** | 91.5 dB/2.83V/1m | 95.2 dB/2.83V/1m | SB26 is 3.7 dB less sensitive |
| Le | 0.04 mH | 0.05 mH | Similar |
| Sd | 6.2 cm² | 5.7 cm² | SB26 slightly larger |
| **Linear travel (p-p)** | **1.2 mm (0.6 mm one-way)** | **0.2 mm** | **SB26 has 3× more excursion** |
| Qms | 3.0 | 2.1 | SB26 has taller, broader resonance |
| Qes | 1.78 | 1.2 | |
| Qts | 1.12 | 0.70 | SB26 resonance is less damped |
| Bl | 1.6 Tm | 3.3 Tm | H2606 has 2× stronger motor |
| Mms | 0.3 g | 0.4 g | |
| Power (RMS) | 120 W | 100 W | SB26 rated higher |
| Power test freq | 2600 Hz | — | SB26 tested at 2600 Hz, not 1250 Hz |
| **Faceplate Ø** | ~100 mm | 104 mm | SB26 is 4 mm smaller |
| Baffle cutout | 88.5 mm | ~96 mm | From drawing dimensions |
| Recess Ø | 53.0 mm | — | Recess around dome |
| **BCD** | **88.5 ±0.10 mm** | 95.0 mm | **6.5 mm smaller — confirmed from drawing** |
| Screw holes | 4-Ø4.0 + 4-Ø8.0 cb | 4-Ø4.0 | SB26 has counterbores |
| **Throat / horn exit** | **None (direct radiator)** | **Ø33 mm** | **SB26 has no horn to couple to WG212** |
| Rear chamber | Yes (damped, vented) | Yes | Both have rear chambers |
| Ferrofluid | No | Yes | H2606 has ferrofluid cooling |
| Total depth | 39.7 mm | ~44 mm (from STEP) | SB26 is shallower |
| Net weight | 0.53 kg | — | |
| Price | ~€35-40 | ~€44 | SB26 is cheaper |
| STEP file | **Not available** | Yes (from ScanSpeak) | SB26 requires manual measurement |

---

## Analysis

### 1. Fs and crossover margin — THE deciding factor

This is the single most important difference. The current project's critical gate is whether the H2606 can cross at 1250 Hz with only 220 Hz margin above its 1030 Hz Fs. The distortion test at 1250 Hz is the blocking step before prototype build.

The SB26STAC at Fs=750 Hz gives **500 Hz margin** at 1250 Hz — more than double. An LR4 high-pass at 1250 Hz would be 24 dB/oct above a resonance that's 1.67× below the crossover. This is a very comfortable margin. You could even cross at 1000-1100 Hz and still have safe headroom, which would improve the directivity match with the 15W midrange (the 140mm c-c spacing produces a broadside null near 1229 Hz — a lower crossover would move below this null).

The higher Qts (1.12 vs 0.70) means the resonance peak is taller and broader, but with 500 Hz of separation and 24 dB/oct slopes, the resonance contribution at the crossover is negligible.

**Verdict: SB26STAC completely solves the crossover margin problem.**

### 2. Excursion — 3× more headroom

The H2606's 0.2mm Xmax is the physical reason the 1250 Hz crossover is risky. At low frequencies, dome excursion increases rapidly (4th power of 1/f for constant SPL). The SB26STAC's 0.6mm one-way linear travel gives 3× the displacement headroom. At 1250 Hz, this translates to approximately 10 dB more maximum SPL before distortion rises — a massive improvement.

**Verdict: SB26STAC has dramatically better low-frequency headroom.**

### 3. Sensitivity — 3.7 dB lower, but better system match

The 91.5 dB sensitivity is 3.7 dB below the H2606's 95.2 dB. However:
- The 15W midrange is ~89.7 dB. The H2606 requires 5-7 dB of DSP attenuation to match. The SB26STAC would need only ~2 dB attenuation — a better natural match.
- In a waveguide, the SB26STAC would gain 2-3 dB of loading, bringing effective sensitivity to ~94 dB.
- The active DSP system can compensate for any sensitivity difference. This is a non-issue for the design, just an amp power consideration.

**Verdict: Minor disadvantage individually, better match system-wide.**

### 4. No horn loading — requires complete WG212 redesign

This is the fundamental problem. The H2606 is a horn tweeter whose Ø33mm throat exit was designed to couple directly into the WG212 waveguide. The WG212 continues the horn's expansion profile. The entire system was designed as: H2606 horn → WG212 waveguide → baffle aperture.

The SB26STAC is a conventional dome with no horn. Its 26mm dome radiates directly into free air (or into a waveguide throat if mounted in one). Using it in the WG212 would require:

- **New waveguide throat:** The WG212 throat (Ø33mm) is sized for the H2606 horn exit. The SB26STAC dome needs a throat that starts at ~26-28mm (the dome + surround) and transitions into the waveguide profile. The entire OS (oblate spheroid) bore must be redesigned.
- **New mounting:** The faceplate is ~100mm vs 104mm. The BCD is ~72-76mm (est.) vs 95mm. The screw pattern is completely different (4-Ø4.0 through + 4-Ø8.0 counterbore vs 4-Ø4.0 simple). The back plate and mounting flange in the WG212 must be redesigned.
- **No STEP file:** ScanSpeak provided a full STEP/IGS/Parasolid for the H2606, which enabled precise CAD integration. SB Acoustics does not provide STEP files for this tweeter. All dimensions would need manual measurement from a physical unit.
- **Different directivity:** A bare dome in a waveguide has different throat impedance and radiation characteristics than a horn-loaded dome. The directivity simulations (vertical_polar_map.py) would need to be re-run with different assumptions.

**Verdict: Not a drop-in replacement. Using the SB26STAC means going back to CAD design phase for the waveguide.**

### 5. No ferrofluid — thermal and damping differences

The H2606 uses ferrofluid for both cooling and mechanical damping. The SB26STAC uses a vented pole piece and damped rear chamber instead. Without ferrofluid:
- Thermal handling at sustained high SPL may be slightly worse (no fluid to conduct heat from the voice coil to the magnet)
- Mechanical damping is lower (Qms 3.0 vs 2.1), which contributes to the lower Fs but also means the resonance is less controlled
- No ferrofluid aging concern (ferrofluid can dry out over years)

**Verdict: Acceptable trade-off. The vented pole piece and rear chamber are a legitimate alternative approach.**

### 6. Mechanical dimensions

| Dimension | SB26STAC | H2606 | WG212 impact |
|---|---|---|---|
| Faceplate Ø | ~100 mm | 104 mm | Back plate recess needs resize |
| BCD | 88.5 mm | 95 mm | 6.5 mm smaller — manageable |
| Throat | None (26mm dome) | Ø33 mm | Waveguide bore must be redesigned |
| Depth | 39.7 mm | ~44 mm | Less depth needed in cabinet |
| Recess Ø | 53 mm | — | New feature |

**The BCD is 88.5 ±0.10 mm — confirmed from the dimension drawing.** This is only 6.5 mm smaller than the H2606's 95 mm, making the mounting plate redesign straightforward.

---

## Overall assessment

### What the SB26STAC solves
- **The #1 problem:** Fs 750 Hz gives 500 Hz crossover margin at 1250 Hz (vs 220 Hz). The distortion test gate disappears.
- **Excursion:** 3× more linear travel means 3× more SPL headroom at the crossover frequency.
- **Sensitivity match:** Better natural match to the 15W midrange (1.8 dB gap vs 5.5 dB).

### What it costs
- **Complete WG212 redesign:** New throat, new mounting, new OS profile. Weeks of CAD work.
- **No STEP file:** Physical unit needed for caliper measurement before CAD can begin.
- **Loss of horn loading:** 3.7 dB sensitivity loss, different directivity behavior.
- **Project delay:** The H2606 path is at "print and test" — switching means returning to design phase.

### Recommendation

**Keep the SB26STAC-C000-4 as the documented fallback, not the primary.**

The pragmatic path:

1. **Continue with H2606 as planned.** Print the WG212, do the distortion test at 1250 Hz. This test is the gate — if it passes, the current design is validated and no changes are needed.
2. **If the H2606 distortion test fails at 1250 Hz**, the SB26STAC is the best alternative identified. It would require:
   - Purchasing a physical unit
   - Caliper measurement of faceplate, BCD, dome surround, depth
   - Complete WG212 redesign (new throat for bare dome, new mounting)
   - Re-running directivity simulations
   - New 3D print and test cycle
3. **If the fallback is needed, the crossover could be lowered to 1000-1100 Hz**, improving the directivity match with the 15W (moving below the 1229 Hz broadside null from the 140mm c-c spacing).

The SB26STAC is a genuinely good tweeter — well-regarded, excellent off-axis performance, and its Fs=750 Hz is exactly what this project needs. But it's a different animal from the H2606, and switching means restarting the waveguide design from zero. The H2606 path is 90% of the way to validation. Let the distortion test decide.

---

## Datasheet location

`assets/datasheets/SB26STAC-C000-4.pdf` — filed alongside the H2606 datasheet.

## Alternative waveguide CAD

A complete alternative waveguide has been designed: `cad/mk2_waveguide_sb26stac.scad`

**STL rendered and validated:** `cad/exports/sb26stac/waveguide_sb26stac.stl` (3.8MB, 18106 facets, simple manifold)

### Key dimension changes from H2606 version

| Parameter | H2606 WG212 | SB26STAC WG | Change |
|---|---|---|---|
| throat_d | 33 mm (horn exit) | 28 mm (dome + surround) | -5 mm |
| tw_face_d | 104.0 mm | 100.0 mm | -4 mm |
| tw_bcd | 95.0 mm | 88.5 mm | -6.5 mm |
| tw_ring_od | 130 mm | 115 mm | -15 mm (smaller BCD needs less material) |
| Counterbores | None | 4-Ø8.0 × 2mm | New feature |
| tw_recess_d | — | 53.0 mm | New (SB26 faceplate recess) |
| Mouth size | 293.5 × 174.4 mm | 293.1 × 173.5 mm | -0.4 × -0.9 mm (negligible) |
| Total depth | 98 mm | 98 mm | Same |
| Flange | 242 × 143 mm | 242 × 143 mm | Identical |
| Coverage angles | θh=50°, θv=32° | θh=50°, θv=32° | Identical |
| Crossover target | 1250 Hz LR4 | 1000-1100 Hz LR4 | Lower (Fs allows it) |

The OS profile, coverage angles, mouth roundover, and baffle mounting are all identical to the H2606 version. The changes are confined to the throat interface and rear mounting plate. This means the cabinet baffle cutout, flange mounting, and external appearance are effectively the same.

---

## Simulation results

### Excursion headroom at crossover

The single most important metric. Relative max SPL before distortion rises, normalized to H2606 @ 1250 Hz = 0 dB:

| Scenario | Driver | Fc | Fs | Margin | Xmax | Rel. max SPL |
|---|---|---|---|---|---|---|
| H2606 @ 1250 Hz | H2606 | 1250 | 1030 | 220 Hz | 0.2 mm | **0.0 dB (reference)** |
| H2606 @ 1450 Hz | H2606 | 1450 | 1030 | 420 Hz | 0.2 mm | +2.6 dB |
| SB26 @ 1000 Hz | SB26STAC | 1000 | 750 | 250 Hz | 0.6 mm | **+6.4 dB** |
| SB26 @ 1100 Hz | SB26STAC | 1100 | 750 | 350 Hz | 0.6 mm | **+8.1 dB** |
| SB26 @ 1250 Hz | SB26STAC | 1250 | 750 | 500 Hz | 0.6 mm | **+10.3 dB** |

The SB26STAC has **6-10 dB more SPL headroom** at the crossover frequency than the H2606, depending on where you cross. Even at the most aggressive 1000 Hz crossover (only 250 Hz above Fs), the SB26STAC still has 6.4 dB more headroom than the H2606 at its "safe" 1450 Hz fallback. This is the 3× excursion advantage (0.6mm vs 0.2mm) compound with the lower Fs.

### Directivity match (DI mismatch with 15W midrange)

| Crossover | DI 15W | DI WG212 | Mismatch |
|---|---|---|---|
| 1000 Hz | 1.0 dB | 5.3 dB | **+4.3 dB** |
| 1100 Hz | 1.0 dB | 5.7 dB | **+4.6 dB** |
| 1250 Hz | 1.0 dB | 6.3 dB | +5.3 dB |
| 1450 Hz | 1.0 dB | 7.2 dB | +6.2 dB |
| 1600 Hz | 1.0 dB | 8.0 dB | +6.9 dB |

Lower crossover = smaller directivity step. The SB26STAC at 1000-1100 Hz gives a **0.7-1.0 dB better directivity match** than the H2606 at 1250 Hz, and 1.6-1.9 dB better than the H2606 fallback at 1450 Hz. Both waveguides use identical coverage angles so the difference is purely from the crossover frequency being lower.

### Vertical lobing (c-c = 150 mm, LR4)

| Crossover | First null angle | Null depth | SPL at ±15° |
|---|---|---|---|
| 1000 Hz | 90° | -14.0 dB | -0.6 dB |
| 1100 Hz | 90° | -23.9 dB | -0.7 dB |
| 1250 Hz | 67° | -66.5 dB | -0.9 dB |
| 1450 Hz | 52° | -54.8 dB | -1.2 dB |

The broadside null for 150mm c-c is at 1147 Hz. Crossing **below** this (1000-1100 Hz) pushes the null above the crossover frequency, meaning it falls outside the active crossover band. The null at 1000 Hz is shallow (-14 dB at 90°) and entirely outside the listening window. At ±15° the ripple is under 1 dB for all scenarios — all are acoustically acceptable.

**Key insight:** Crossing at 1100 Hz with the SB26STAC is the sweet spot. The broadside null (1147 Hz) sits just above the crossover, so the LR4 rolloff suppresses it almost entirely. At ±15° the response is within 0.7 dB.

### Comparison plot

`sims/plots/h2606_vs_sb26stac_comparison.png` — 4-panel comparison: excursion headroom, directivity match, vertical lobing, and feature bar chart.

---

## Revised recommendation (with waveguide + simulations)

With the alternative waveguide designed and simulated, the picture is clearer:

**The SB26STAC-C000-4 is a technically superior choice for this project.** The numbers are not subtle:

1. **Excursion:** +6.4 to +10.3 dB more headroom at crossover. The H2606's 0.2mm Xmax is the project's weakest link. The SB26STAC eliminates this concern entirely.
2. **Directivity:** 0.7-1.0 dB better DI match at 1000-1100 Hz vs 1250 Hz. The lower crossover moves closer to the 15W's near-omni region.
3. **Lobing:** Crossing at 1100 Hz puts the broadside null (1147 Hz) just above the crossover, where LR4 suppression is strongest. ±15° ripple under 0.7 dB.
4. **Crossover margin:** 350-500 Hz vs 220 Hz. No distortion test needed as a gate.

**The cost is real but manageable:**
- No STEP file → need physical unit for caliper verification (same as the GRS woofer situation)
- WG212 rear plate redesigned (already done in SCAD, STL rendered and manifold-verified)
- 3.7 dB lower sensitivity → compensated in DSP, and actually a better match to the 15W
- Loss of horn loading → the WG212 provides the loading instead (that's its purpose)

**If I were designing from scratch, I'd pick the SB26STAC.** The H2606's only real advantage is the horn loading (higher sensitivity) and the STEP file (CAD convenience). The SB26STAC wins on every acoustic parameter that matters.

**But:** the H2606 path is 90% to validation. The waveguide is printed-ready, the STEP is verified, the only gate is one distortion test. Switching means buying a unit, caliper-measuring, printing a new waveguide, and testing. That's 2-3 weeks of work to replace a path that might already work.

**My recommendation:**

1. **Print and test the H2606 WG212 first.** If the 1250 Hz distortion test passes, you're done. Ship it.
2. **If it fails, switch to SB26STAC without hesitation.** The alternative waveguide is designed, the STL is ready, and the simulations show it's the better driver. Cross at 1100 Hz.
3. **For a future mk3 or clean-sheet design:** start with the SB26STAC. The numbers favor it.

## Open items if fallback is needed

- [ ] Purchase SB26STAC-C000-4 physical unit
- [ ] Caliper measurement: faceplate OD, BCD (88.5 from drawing — confirm), dome surround Ø, total depth, recess Ø, counterbore depth
- [ ] Confirm counterbore depth (estimated 2mm — not on drawing)
- [ ] Redesign WG212 throat for bare 26mm dome (no horn exit)
- [ ] New OS bore profile starting at ~26-28mm
- [ ] New mounting plate for ~100mm faceplate with 4-Ø4.0 + counterbores
- [ ] Re-run vertical_polar_map.py with new waveguide geometry
- [ ] Consider lowering crossover to 1000-1100 Hz (below 1229 Hz broadside null)
