# SB Acoustics SB26STAC-C000-4 — Tweeter Selection Analysis

**Date:** July 4, 2026
**Purpose:** Selection analysis for the Mk3 Reference Loudspeaker tweeter
**Datasheet:** `assets/datasheets/SB26STAC-C000-4.pdf`

This document records the analysis behind the selection of the SB26STAC-C000-4
as the project tweeter. It compares the SB26STAC against an earlier horn-dome
candidate (the ScanSpeak H2606/920000) that was evaluated and set aside during
the design process. The H2606 data is retained here as the historical
comparison baseline that justified the SB26STAC selection — it is not a current
design option.

---

## Driver Summary

The SB26STAC-C000-4 is a 26mm soft dome tweeter from SB Acoustics with a cast aluminium faceplate, copper-capped pole piece, and a non-reflective rear chamber with optimized damping. It is a **conventional flush-mount dome tweeter**, not a horn-loaded tweeter.

Key features: low Fs (750 Hz), CCAW voice coil, vented pole piece, silver lead wires, saturation-controlled motor.

---

## Side-by-side comparison (selection baseline)

| Parameter | SB26STAC-C000-4 | H2606/920000 (evaluated, set aside) | Notes |
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
| Power test freq | 2600 Hz | — | SB26 tested at 2600 Hz |
| **Faceplate Ø** | ~100 mm | 104 mm | SB26 is 4 mm smaller |
| Baffle cutout | 88.5 mm | ~96 mm | From drawing dimensions |
| Recess Ø | 53.0 mm | — | Recess around dome |
| **BCD** | **88.5 ±0.10 mm** | 95.0 mm | **6.5 mm smaller — confirmed from drawing** |
| Screw holes | 4-Ø4.0 + 4-Ø8.0 cb | 4-Ø4.0 | SB26 has counterbores |
| **Throat / horn exit** | **None (direct radiator)** | **Ø33 mm** | **SB26 has no horn** |
| Rear chamber | Yes (damped, vented) | Yes | Both have rear chambers |
| Ferrofluid | No | Yes | H2606 has ferrofluid cooling |
| Total depth | 39.7 mm | ~44 mm | SB26 is shallower |
| Net weight | 0.53 kg | — | |
| Price | ~€35-40 | ~€44 | SB26 is cheaper |
| STEP file | **Not available** | Yes (from ScanSpeak) | SB26 requires manual measurement |

---

## Analysis

### 1. Fs and crossover margin — THE deciding factor

This is the single most important difference. The H2606's Fs of 1030 Hz with only 220 Hz margin to a 1250 Hz crossover was the project's critical risk — it would have required a distortion test gate before the crossover could be confirmed.

The SB26STAC at Fs=750 Hz gives a **350 Hz margin** at the 1100 Hz crossover. An LR4 high-pass at 1100 Hz is 24 dB/oct above a resonance that's 1.47× below the crossover. This is a very comfortable margin — no distortion-test gate is required. The 1100 Hz crossover also sits below the 150 mm c-c broadside null (1147 Hz), so the null falls outside the active crossover band.

The higher Qts (1.12 vs 0.70) means the resonance peak is taller and broader, but with 350 Hz of separation and 24 dB/oct slopes, the resonance contribution at the crossover is negligible.

**Verdict: SB26STAC completely solves the crossover margin problem.**

### 2. Excursion — 3× more headroom

The H2606's 0.2mm Xmax is the physical reason a low crossover with that driver is risky. At low frequencies, dome excursion increases rapidly (4th power of 1/f for constant SPL). The SB26STAC's 0.6mm one-way linear travel gives 3× the displacement headroom. At 1100 Hz, this translates to +8.1 dB more maximum SPL before distortion rises — a massive improvement.

**Verdict: SB26STAC has dramatically better low-frequency headroom.**

### 3. Sensitivity — 3.7 dB lower, but better system match

The 91.5 dB sensitivity is 3.7 dB below the H2606's 95.2 dB. However:
- The 15W midrange is ~89.7 dB. The H2606 would require 5-7 dB of DSP attenuation to match. The SB26STAC needs only ~2 dB attenuation — a better natural match.
- In a waveguide, the SB26STAC gains 2-3 dB of loading, bringing effective sensitivity to ~94 dB.
- The active DSP system can compensate for any sensitivity difference. This is a non-issue for the design, just an amp power consideration.

**Verdict: Minor disadvantage individually, better match system-wide.**

### 4. No horn loading — requires a dedicated waveguide

This is the fundamental design difference. The H2606 is a horn tweeter whose Ø33mm throat exit was designed to couple directly into a horn-continuation waveguide. The SB26STAC is a conventional dome with no horn — its 26mm dome radiates directly into the waveguide throat.

Using the SB26STAC means the waveguide is a pure directivity device rather than a horn extension:
- **Throat:** starts at ~28mm (the dome + surround) and transitions into the waveguide profile.
- **Mounting:** the faceplate is ~100mm with an 88.5 mm BCD and 4-Ø4.0 through + 4-Ø8.0 counterbore screws.
- **No STEP file:** all dimensions must be caliper-measured from a physical unit.
- **Directivity:** a bare dome in a waveguide has different throat impedance and radiation characteristics than a horn-loaded dome. The directivity simulations use the appropriate assumptions.

**Verdict: A dedicated non-horn-loaded waveguide design — which is what `cad/waveguide.scad` provides.**

### 5. No ferrofluid — thermal and damping differences

The H2606 uses ferrofluid for both cooling and mechanical damping. The SB26STAC uses a vented pole piece and damped rear chamber instead. Without ferrofluid:
- Thermal handling at sustained high SPL may be slightly worse (no fluid to conduct heat from the voice coil to the magnet)
- Mechanical damping is lower (Qms 3.0 vs 2.1), which contributes to the lower Fs but also means the resonance is less controlled
- No ferrofluid aging concern (ferrofluid can dry out over years)

**Verdict: Acceptable trade-off. The vented pole piece and rear chamber are a legitimate alternative approach.**

### 6. Mechanical dimensions

| Dimension | SB26STAC | H2606 | Waveguide impact |
|---|---|---|---|
| Faceplate Ø | ~100 mm | 104 mm | Back plate recess needs resize |
| BCD | 88.5 mm | 95 mm | 6.5 mm smaller — manageable |
| Throat | None (26mm dome) | Ø33 mm | Waveguide bore designed for bare dome |
| Depth | 39.7 mm | ~44 mm | Less depth needed in cabinet |
| Recess Ø | 53 mm | — | Feature in waveguide |

**The BCD is 88.5 ±0.10 mm — confirmed from the dimension drawing.**

---

## Overall assessment

### What the SB26STAC delivers
- **Crossover margin:** Fs 750 Hz gives 350 Hz margin at 1100 Hz. No distortion-test gate required.
- **Excursion:** 3× more linear travel means +8.1 dB more SPL headroom at the crossover frequency.
- **Sensitivity match:** Better natural match to the 15W midrange (1.8 dB gap vs 5.5 dB).
- **Directivity:** Lower crossover (1100 Hz) gives a smaller DI step with the 15W (4.6 dB mismatch vs 5.3 dB at 1250 Hz).
- **Lobing:** Crossing at 1100 Hz puts the broadside null (1147 Hz for 150mm c-c) just above the crossover, where LR4 suppression is strongest. ±15° ripple under 0.7 dB.

### What it costs (and how it's handled)
- **No STEP file** → physical unit needed for caliper verification (same as the GRS woofer situation).
- **Dedicated waveguide design** → `cad/waveguide.scad` (STL rendered and manifold-verified).
- **3.7 dB lower sensitivity** → compensated in DSP, and actually a better match to the 15W.
- **Loss of horn loading** → the waveguide provides the loading instead (that's its purpose).

**The SB26STAC-C000-4 wins on every acoustic parameter that matters.** The
H2606's only real advantages were the horn loading (higher sensitivity) and a
STEP file (CAD convenience) — both outweighed by the SB26STAC's acoustic
superiority.

---

## Datasheet location

`assets/datasheets/SB26STAC-C000-4.pdf`

## Waveguide CAD

The waveguide for the SB26STAC is `cad/waveguide.scad`.

**STL rendered and validated:** `cad/exports/waveguide.stl` (manifold)

### Key dimensions

| Parameter | Value |
|---|---|
| throat_d | 28 mm (dome + surround) |
| tw_face_d | 100.0 mm |
| tw_bcd | 88.5 mm |
| tw_ring_od | 115 mm |
| Counterbores | 4-Ø8.0 × 2mm |
| tw_recess_d | 53.0 mm |
| Mouth size | ~289 × 172 mm |
| Total depth | 98 mm (D_os + Lr = 65 + 25) |
| Flange | 242 × 143 mm |
| Coverage angles | θh=50°, θv=32° (~100° × 64°) |
| Crossover target | 1100 Hz LR4 |

The OS profile, coverage angles, mouth roundover, and baffle mounting are all
designed for the bare-dome throat interface. The cabinet baffle cutout, flange
mounting, and external appearance are driven by this waveguide model.

---

## Simulation results

### Excursion headroom at crossover

The single most important metric. Relative max SPL before distortion rises, normalized to H2606 @ 1250 Hz = 0 dB (historical baseline):

| Scenario | Driver | Fc | Fs | Margin | Xmax | Rel. max SPL |
|---|---|---|---|---|---|---|
| H2606 @ 1250 Hz (baseline) | H2606 | 1250 | 1030 | 220 Hz | 0.2 mm | **0.0 dB (reference)** |
| H2606 @ 1450 Hz | H2606 | 1450 | 1030 | 420 Hz | 0.2 mm | +2.6 dB |
| SB26 @ 1000 Hz | SB26STAC | 1000 | 750 | 250 Hz | 0.6 mm | **+6.4 dB** |
| **SB26 @ 1100 Hz (selected)** | SB26STAC | 1100 | 750 | 350 Hz | 0.6 mm | **+8.1 dB** |
| SB26 @ 1250 Hz | SB26STAC | 1250 | 750 | 500 Hz | 0.6 mm | **+10.3 dB** |

The SB26STAC has **6-10 dB more SPL headroom** at the crossover frequency than the H2606 baseline, depending on where you cross. This is the 3× excursion advantage (0.6mm vs 0.2mm) compounding with the lower Fs.

### Directivity match (DI mismatch with 15W midrange)

| Crossover | DI 15W | DI waveguide | Mismatch |
|---|---|---|---|
| 1000 Hz | 1.0 dB | 5.3 dB | **+4.3 dB** |
| 1100 Hz | 1.0 dB | 5.7 dB | **+4.6 dB** |
| 1250 Hz | 1.0 dB | 6.3 dB | +5.3 dB |
| 1450 Hz | 1.0 dB | 7.2 dB | +6.2 dB |
| 1600 Hz | 1.0 dB | 8.0 dB | +6.9 dB |

Lower crossover = smaller directivity step. The SB26STAC at 1100 Hz gives a **0.7 dB better directivity match** than the H2606 at 1250 Hz.

### Vertical lobing (c-c = 150 mm, LR4)

| Crossover | First null angle | Null depth | SPL at ±15° |
|---|---|---|---|
| 1000 Hz | 90° | -14.0 dB | -0.6 dB |
| 1100 Hz | 90° | -23.9 dB | -0.7 dB |
| 1250 Hz | 67° | -66.5 dB | -0.9 dB |
| 1450 Hz | 52° | -54.8 dB | -1.2 dB |

The broadside null for 150mm c-c is at 1147 Hz. Crossing **below** this (1100 Hz) pushes the null above the crossover frequency, meaning it falls outside the active crossover band. At ±15° the ripple is under 1 dB for all scenarios.

**Key insight:** Crossing at 1100 Hz with the SB26STAC is the sweet spot. The broadside null (1147 Hz) sits just above the crossover, so the LR4 rolloff suppresses it almost entirely. At ±15° the response is within 0.7 dB.

### Comparison plot

`sims/plots/h2606_vs_sb26stac_comparison.png` — 4-panel comparison: excursion headroom, directivity match, vertical lobing, and feature bar chart.

---

## Open items

- [ ] Purchase SB26STAC-C000-4 physical unit
- [ ] Caliper measurement: faceplate OD, BCD (88.5 from drawing — confirm), dome surround Ø, total depth, recess Ø, counterbore depth
- [ ] Confirm counterbore depth (estimated 2mm — not on drawing)
- [ ] Confirm throat diameter (estimated 28mm — dome + surround) against `cad/waveguide.scad`
- [ ] Print waveguide and test-fit SB26STAC
- [ ] Measure SB26STAC in-waveguide response and directivity at 1100 Hz (expected to pass comfortably)
