# Chapter 5 - Tweeter Investigations

---

## Requirements

The tweeter must:

- Cover the range from 1100 Hz to beyond 20 kHz
- Be suitable for mounting in a custom waveguide
- Have sufficient power handling and headroom at 1100 Hz
- Have low distortion at 1100 Hz and above
- Have a dome/surround geometry compatible with the waveguide throat design
- Fit within the 320 mm baffle at 140 mm c-c from the midrange

---

## Selected driver

### SB Acoustics SB26STAC-C000-4

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

## Why the SB26STAC was selected

The SB26STAC was chosen through a systematic selection analysis (see
`docs/SB26STAC-C000-4_analysis.md` for the full analysis and simulation
results). Its key advantages:

- **Fs 750 Hz gives 350 Hz margin at the 1100 Hz crossover** — a comfortable
  margin that requires no distortion-test gate before committing to the
  crossover frequency.
- **0.6 mm Xmax gives +8.1 dB excursion headroom** at 1100 Hz — 3× the linear
  travel of a typical 1" dome tweeter, substantially more maximum SPL capability
  near the crossover.
- **91.5 dB sensitivity is a better match to the 15W/4434G00's 89.7 dB** — only
  -1.8 dB of DSP pad is needed. This reduces wasted amplifier power and the
  thermal/level mismatch.
- **No ferrofluid** — vented pole piece instead, eliminating the long-term
  ferrofluid aging concern.

---

## Driver character

The SB26STAC is a conventional dome tweeter — no built-in horn. The dome radiates directly into the waveguide throat, which provides the acoustic loading and directivity control.

The fine weave fabric dome produces a smooth, non-aggressive character. The copper-capped pole piece reduces voice coil inductance and phase shift, improving transient response. The non-reflective rear chamber with vented pole piece provides damping without ferrofluid, eliminating the long-term aging concern.

The 0.6mm one-way Xmax is exceptional for a 1" dome tweeter. This directly translates to higher maximum SPL at the crossover frequency before distortion rises.

---

## Sensitivity matching

At 91.5 dB / 2.83V / 1m, the SB26STAC is 1.8 dB more sensitive than the 15W midrange (~89.7 dB). This requires only ~2 dB of DSP attenuation on the tweeter channel — a natural match.

In the waveguide, the SB26STAC will gain 2-3 dB of acoustic loading, bringing effective sensitivity to ~94 dB. The exact pad is finalized from measurement.

---

## Waveguide integration

The SB26STAC has no built-in horn — the 26mm dome radiates directly. The custom waveguide (`cad/waveguide.scad`) starts its OS bore at Ø28mm (dome + ~1mm surround per side) and provides the full directivity control.

Key waveguide dimensions:

| Parameter | Value |
|---|---|
| Throat diameter | 28 mm (dome + surround) |
| Coverage angles | 100° H × 64° V |
| Mouth size | 293 × 173 mm |
| Total depth | 98 mm |
| Rear plate | Ø115 mm |
| Faceplate pocket | Ø101 × 4mm deep |
| Baffle mounting | Flange recessed into baffle |

**Open item:** The throat diameter (28mm) is estimated from the 26mm dome + surround. The faceplate has a Ø53mm recess around the dome. Physical caliper measurement is needed to confirm the exact throat transition before the final print.

---

## Crossover integration

The tweeter is:
- **High-pass at 1100 Hz LR4**
- Approximately -2 dB gain adjustment in DSP to match midrange sensitivity
- DSP delay applied to align acoustic center with midrange

The 1100 Hz crossover is selected because:
1. **Fs margin:** 350 Hz above the 750 Hz resonance — comfortable, no distortion test gate
2. **Directivity:** Better DI match with the 15W at 1100 Hz (4.6 dB mismatch)
3. **Lobing:** The broadside null for 150mm c-c is at 1147 Hz — just above the 1100 Hz crossover, where LR4 suppression is strongest. ±15° ripple is under 0.7 dB.

See Chapter 11 (Crossovers) and Chapter 14 (DSP) for detail.

---

## Open items

- [ ] Purchase SB26STAC-C000-4 physical unit
- [ ] Caliper measurement: faceplate OD, BCD (88.5 from drawing — confirm), dome surround Ø, total depth, recess Ø, counterbore depth
- [ ] Confirm throat diameter (estimated 28mm — dome + surround)
- [ ] Print waveguide
- [ ] Test fit SB26STAC in waveguide
- [ ] Measure on-axis and off-axis response in waveguide
- [ ] Measure distortion at 1100 Hz (expected to pass comfortably)
- [ ] Confirm c-c spacing to 15W midrange is achievable at 140 mm
