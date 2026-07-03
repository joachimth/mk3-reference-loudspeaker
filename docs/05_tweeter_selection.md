# Chapter 5 - Tweeter Investigations (mk3)

---

## Requirements

The tweeter must:

- Cover the range from 1100 Hz to beyond 20 kHz
- Be suitable for mounting in a custom waveguide (WG212)
- Have sufficient power handling and headroom at 1100 Hz
- Have low distortion at 1100 Hz and above
- Have a dome/surround geometry compatible with the WG212 throat design
- Fit within the 300 mm baffle at 140 mm c-c from the midrange

---

## Selected driver

### SB Acoustics SB26STAC-C000-4 (mk3 primary)

A 26mm soft dome tweeter with cast aluminium faceplate, copper-capped pole piece, and a non-reflective rear chamber with optimized damping.

**Key specifications:**

| Parameter | Value |
|---|---|
| Series | SB26 |
| Type | Conventional soft dome (no built-in horn) |
| Dome diameter | 26 mm / 1" |
| Dome material | Fine weave fabric |
| Impedance | 4 Ω |
| Re | 3.2 Ω |
| **Fs** | **750 Hz** |
| **Sensitivity** | **91.5 dB / 2.83V / 1m** |
| Le | 0.04 mH |
| Qms | 3.0 |
| Qes | 1.78 |
| Qts | 1.12 |
| BL | 1.6 Tm |
| Mms | 0.3 g |
| **Xmax (one-way)** | **0.6 mm** |
| **Linear travel (p-p)** | **1.2 mm** |
| Sd | 6.2 cm² |
| Power (RMS) | 120 W |
| Power test | IEC 268-5, HP Butterworth 2600 Hz 12 dB/oct |
| Faceplate Ø | 100.0 ±0.35 mm |
| BCD | 88.5 ±0.10 mm |
| Mounting holes | 4-Ø4.0 + 4-Ø8.0 counterbore |
| Recess Ø | 53.0 mm |
| Total depth | 39.7 mm |
| Net weight | 0.53 kg |
| Price | ~€37 |
| STEP file | **Not available** (manual caliper measurement required) |

Datasheet: `assets/datasheets/SB26STAC-C000-4.pdf`

---

## Why the SB26STAC replaces the H2606/920000

The mk2 design used the ScanSpeak H2606/920000 horn dome tweeter. The H2606's Fs of 1030 Hz with only 220 Hz margin to the 1250 Hz crossover was the project's critical risk — requiring a distortion test gate before the crossover could be confirmed.

The SB26STAC solves this problem and improves on every acoustic metric:

| Metric | H2606/920000 (mk2) | SB26STAC-C000-4 (mk3) | Improvement |
|---|---|---|---|
| Fs | 1030 Hz | 750 Hz | 280 Hz lower |
| Crossover margin | 220 Hz (1250-1030) | 350 Hz (1100-750) | +130 Hz |
| Xmax | 0.2 mm | 0.6 mm | 3× more |
| Excursion headroom at crossover | 0 dB (ref) | +8.1 dB | +8.1 dB |
| Sensitivity vs 15W (89.7 dB) | +5.5 dB gap | +1.8 dB gap | Better match |
| DI mismatch at crossover | 5.3 dB | 4.6 dB | -0.7 dB |
| Ferrofluid | Yes (aging concern) | No (vented pole piece) | No aging |
| Price | ~€44 | ~€37 | €7 cheaper |

The H2606's advantages (horn loading → higher sensitivity, STEP file availability) are outweighed by the SB26STAC's acoustic superiority. See `docs/SB26STAC-C000-4_analysis.md` for the full analysis and simulation results.

---

## Driver character

The SB26STAC is a conventional dome tweeter — no built-in horn. The dome radiates directly into the WG212 waveguide throat, which provides the acoustic loading and directivity control. This is a different approach from the H2606, which had a built-in horn that coupled to the WG212.

The fine weave fabric dome produces a smooth, non-aggressive character. The copper-capped pole piece reduces voice coil inductance and phase shift, improving transient response. The non-reflective rear chamber with vented pole piece provides damping without ferrofluid, eliminating the long-term aging concern.

The 0.6mm one-way Xmax is exceptional for a 1" dome tweeter — 3× the H2606's 0.2mm. This directly translates to higher maximum SPL at the crossover frequency before distortion rises.

---

## Sensitivity matching

At 91.5 dB / 2.83V / 1m, the SB26STAC is 1.8 dB more sensitive than the 15W midrange (~89.7 dB). This requires only ~2 dB of DSP attenuation on the tweeter channel — a much more natural match than the H2606 which needed 5-7 dB of padding.

In the WG212 waveguide, the SB26STAC will gain 2-3 dB of acoustic loading, bringing effective sensitivity to ~94 dB. The exact pad is finalized from measurement.

---

## Waveguide integration

The SB26STAC has no built-in horn — the 26mm dome radiates directly. The WG212 waveguide (SB26STAC version: `cad/mk2_waveguide_sb26stac.scad`) starts its OS bore at Ø28mm (dome + ~1mm surround per side) and provides the full directivity control.

Key waveguide dimensions for the SB26STAC version:

| Parameter | Value |
|---|---|
| Throat diameter | 28 mm (dome + surround) |
| Coverage angles | 100° H × 64° V (same as H2606 version) |
| Mouth size | 293 × 173 mm |
| Total depth | 98 mm (same as H2606 version) |
| Rear plate | Ø115 mm (vs Ø130 for H2606) |
| Faceplate pocket | Ø101 × 4mm deep |
| Baffle mounting | Identical to H2606 version |

The OS profile, coverage angles, mouth roundover, and baffle flange are identical to the H2606 version. Only the throat interface and rear mounting plate differ.

**Open item:** The throat diameter (28mm) is estimated from the 26mm dome + surround. The faceplate has a Ø53mm recess around the dome. Physical caliper measurement is needed to confirm the exact throat transition before the final print.

---

## Crossover integration

The tweeter is:
- **High-pass at 1100 Hz LR4** (was 1250 Hz in mk2)
- Approximately -2 dB gain adjustment in DSP to match midrange sensitivity (was -5 to -7 dB)
- DSP delay applied to align acoustic center with midrange

The 1100 Hz crossover is selected because:
1. **Fs margin:** 350 Hz above the 750 Hz resonance — comfortable, no distortion test gate
2. **Directivity:** Better DI match with the 15W at 1100 Hz (4.6 dB mismatch) vs 1250 Hz (5.3 dB)
3. **Lobing:** The broadside null for 150mm c-c is at 1147 Hz — just above the 1100 Hz crossover, where LR4 suppression is strongest. ±15° ripple is under 0.7 dB.

See Chapter 11 (Crossovers) and Chapter 14 (DSP) for detail.

---

## Alternative: ScanSpeak H2606/920000 (mk2 fallback)

The H2606/920000 remains documented as the mk2 fallback. If the SB26STAC path encounters unexpected issues (e.g., the dome doesn't couple well to the waveguide throat), the H2606 design on the `main` branch is ready to go. See `docs/SB26STAC-C000-4_analysis.md` for the complete comparison.

---

## Open items

- [ ] Purchase SB26STAC-C000-4 physical unit
- [ ] Caliper measurement: faceplate OD, BCD (88.5 from drawing — confirm), dome surround Ø, total depth, recess Ø, counterbore depth
- [ ] Confirm throat diameter (estimated 28mm — dome + surround)
- [ ] Print WG212 (SB26STAC version)
- [ ] Test fit SB26STAC in WG212
- [ ] Measure on-axis and off-axis response in WG212
- [ ] Measure distortion at 1100 Hz (expected to pass comfortably)
- [ ] Confirm c-c spacing to 15W midrange is achievable at 140 mm
