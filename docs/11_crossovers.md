# Chapter 11 - Crossovers

---

## Approach

The Mk2 Reference Loudspeaker uses an active DSP crossover. There is no passive crossover. Each driver has its own amplifier channel.

See Chapter 14 (DSP) for the full DSP implementation. This chapter covers the crossover topology and the acoustic targets.

---

## Crossover frequencies

| Crossover | Frequency | Slope | Drivers |
|---|---|---|---|
| Bass / midrange | 150 Hz | LR4 (24 dB/oct) | GRS woofers → ScanSpeak 15W |
| Midrange / tweeter | **1100 Hz** | LR4 (24 dB/oct) | ScanSpeak 15W → SB26STAC-C000-4 / WG212 |

---

## Linkwitz-Riley 4th-order (LR4) crossover

The LR4 crossover is the standard choice for active multi-way loudspeakers. Its properties:

- **-6 dB at the crossover frequency** for each driver
- **Summed acoustic response is flat** at all frequencies when drivers are in phase and perfectly aligned
- **4th order (24 dB/octave) slopes** provide fast rolloff, reducing out-of-band driver stress and lobing
- **In phase at the crossover frequency** - the two acoustic outputs are in phase (0°) at Fc, each at -6 dB, and sum flat **without** any polarity inversion. (This is the defining LR4 property. LR2, by contrast, is 180° out of phase at Fc and needs a polarity flip on one driver.)

DSP delay is used separately to align the drivers' physical **acoustic-centre
offsets** so the summation holds off-axis as well as on-axis — it is not
correcting a 180° crossover phase.

LR4 crossovers can be implemented as a cascade of two 2nd-order Butterworth filters, or directly as a 4th-order IIR filter in the DSP.

---

## Bass / midrange: 150 Hz

The 150 Hz crossover was selected to:
- Relieve the ScanSpeak 15W of bass reproduction (below 150 Hz is handled by the woofers)
- Keep the GRS woofers within their optimal operating range
- Allow the 15W to reproduce the lower midrange (150-500 Hz) without excessive excursion

**Woofer low-pass:** 150 Hz LR4
The woofers are rolled off at 150 Hz. Below 150 Hz the full bass SPL is produced by the GRS push-push system. The bass system also receives a high-pass filter at approximately 20 Hz to protect the woofers from infrasonic content.

**Midrange high-pass:** 150 Hz LR4
The 15W midrange is high-passed at 150 Hz. This removes bass loading from the midrange driver and the mid chamber.

**Phase alignment:** The acoustic centers of the woofers and the midrange are at different physical positions. DSP delay must be applied to align them at the crossover frequency.

---

## Midrange / tweeter: 1100 Hz

The 1100 Hz crossover was selected for mk3 (v7) based on a systematic
optimization sweep (see `simulations/mk3_crossover_optimization.py`)
that scored crossover frequencies from 800 to 1600 Hz against five
criteria: Fs margin, excursion headroom, directivity match, vertical
lobing, and system sum flatness.

### Optimization results

| Fc [Hz] | Fs margin | Excursion | DI mismatch | ±15° ripple | Score | Broadside |
|---|---|---|---|---|---|---|
| 1000 | 250 Hz | +6.4 dB | 4.3 dB | -0.6 dB | 6.9 | below |
| 1050 | 300 Hz | +7.2 dB | 4.5 dB | -0.6 dB | 7.7 | below |
| **1100** | **350 Hz** | **+8.1 dB** | **4.6 dB** | **-0.7 dB** | **8.1** | **below** |
| 1150 | 400 Hz | +8.8 dB | 4.9 dB | -0.7 dB | 8.2 | above |
| 1200 | 450 Hz | +9.6 dB | 5.1 dB | -0.8 dB | 8.2 | above |
| 1250 | 500 Hz | +10.3 dB | 5.3 dB | -0.9 dB | 8.1 | above |
| 1300 | 550 Hz | +11.0 dB | 5.5 dB | -1.0 dB | 8.1 | above |

**Optimal band: 1100-1200 Hz** (scores 8.1-8.2, statistically tied).

**Why 1100 Hz is chosen over 1200 Hz despite identical scores:**
- Below broadside null (1147 Hz for 150mm c-c) — the null is fully outside
  the active crossover band, not partially inside it
- Better DI match (4.6 vs 5.1 dB) — closer to 15W's near-omni region
- Fs margin of 350 Hz is already comfortable — additional margin has
  diminishing returns (the sigmoid scoring reflects this)

The crossover could be raised to 1150-1200 Hz with negligible penalty if
measurement shows the 15W has cone breakup or directivity issues at 1100 Hz.

> **mk2 comparison:** H2606 @ 1250 Hz scored 8.1 — but with Fs margin of only
> 220 Hz (vs 350 Hz for SB26STAC @ 1100) and +0.0 dB excursion headroom
> (vs +8.1 dB). The SB26STAC wins on the two safety criteria while matching
> on the acoustic criteria.

### Selection rationale

- **Fs margin:** 350 Hz above the 750 Hz resonance — comfortable, no distortion test gate required (unlike mk2's H2606 at 1250 Hz with only 220 Hz margin).
- **Directivity match:** At 1100 Hz the 15W midrange is closer to omni, giving a smaller DI step (4.6 dB mismatch vs 5.3 dB at 1250 Hz).
- **Vertical lobing:** The broadside null for 150mm c-c is at 1147 Hz — just above the 1100 Hz crossover. The LR4 rolloff suppresses the null almost entirely. At ±15° the ripple is under 0.7 dB.
- **Excursion headroom:** The SB26STAC's 0.6mm Xmax gives +8.1 dB more max SPL at 1100 Hz than the H2606 at 1250 Hz.

**Midrange low-pass:** 1100 Hz LR4
The 15W is rolled off above 1100 Hz.

**Tweeter high-pass:** 1100 Hz LR4
The SB26STAC in WG212 is high-passed at 1100 Hz.

**Phase alignment:** The acoustic centers of the midrange and the tweeter/waveguide are at different positions. DSP delay will be used to align them. The waveguide also adds physical depth to the tweeter's acoustic center.

> **mk2 comparison:** The original v6b design crossed at 1250 Hz with the H2606/920000. The 1250 Hz crossover was unconfirmed pending a distortion test due to the H2606's Fs=1030 Hz (220 Hz margin). The mk3 crossover at 1100 Hz with Fs=750 Hz removes this gate entirely.

---

## Vertical lobing at the mid/tweeter crossover

The two-driver interference pattern at the mid/tweeter crossover creates lobing in the vertical plane. The lobing frequency and severity depend on:

- The center-to-center (c-c) spacing between the midrange and tweeter
- The crossover frequency
- The crossover slope

For two drivers with a c-c spacing of d, the first lobe null occurs at approximately:

```
f_null = c / (2 × d × sin(θ))
```

where c is the speed of sound (~344 m/s), d is the c-c spacing in meters, and θ is the off-axis angle.

For d = 140 mm and θ = 90° (broadside null):
```
f_null = 344 / (2 × 0.14) ≈ 1229 Hz
```

For d = 150 mm (practical minimum before 15W frames touch):
```
f_null = 344 / (2 × 0.15) ≈ 1147 Hz
```

At the mk3 crossover of 1100 Hz, the broadside null (1147 Hz for 150mm c-c) sits **just above** the crossover frequency. The LR4 rolloff means the tweeter is already -6 dB at 1100 Hz and dropping fast, so the null at 1147 Hz is strongly suppressed. At ±15° the ripple is under 0.7 dB.

This is an improvement over the mk2 design (1250 Hz), where the broadside null (1147 Hz) fell **below** the crossover — in the active band where both drivers are contributing.

Shorter c-c spacing reduces lobing severity and pushes the null higher. Increasing the crossover frequency with the same c-c spacing worsens the lobing.

---

## DSP implementation

See Chapter 14 (DSP) for the filter coefficients, delay values, and EQ.

---

## Open items

- Measure SB26STAC in waveguide response/distortion at 1100 Hz (expected to pass comfortably — no Fs-margin gate)
- Measure acoustic centers of all three driver systems in the final cabinet
- Calculate and apply DSP delay values
- Verify crossover summation in measurement (flat on-axis, smooth off-axis)
- Adjust crossover frequency if distortion measurement requires it
