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
| Midrange / tweeter | 1250 Hz | LR4 (24 dB/oct) | ScanSpeak 15W → ScanSpeak H2606/920000 / WG212 |

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

## Midrange / tweeter: 1250 Hz

The 1250 Hz crossover was selected in v6b (DD-010) based on simplified directivity simulations showing that:
- Lower crossover frequencies improve directivity matching between the midrange and the waveguide tweeter
- The 140 mm c-c spacing produces acceptable vertical lobing at 1250 Hz but would produce worse lobing at higher frequencies
- The H2606 in WG212 is expected to handle 1250 Hz LR4, but this must be verified by distortion measurement

**Midrange low-pass:** 1250 Hz LR4
The 15W is rolled off above 1250 Hz.

**Tweeter high-pass:** 1250 Hz LR4
The H2606 in WG212 is high-passed at 1250 Hz.

**Phase alignment:** The acoustic centers of the midrange and the tweeter/waveguide are at different positions. DSP delay will be used to align them. The waveguide also adds physical depth to the tweeter's acoustic center.

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

This means the 140 mm c-c spacing produces a broadside null near 1229 Hz - close to the 1250 Hz crossover frequency. This is acceptable because:
- LR4 slopes transition the energy between drivers over a wide range
- The crossover suppresses the 15W output at 1250 Hz (it is already at -6 dB at the crossover frequency)
- The lobing at the listening angle (±15° vertical) is much less severe than the theoretical broadside null

Shorter c-c spacing reduces lobing severity and pushes the null higher. Increasing the crossover frequency with the same c-c spacing worsens the lobing.

---

## DSP implementation

See Chapter 14 (DSP) for the filter coefficients, delay values, and EQ.

---

## Open items

- Measure H2606 in WG212 distortion at 1250 Hz to confirm crossover viability
- Measure acoustic centers of all three driver systems in the final cabinet
- Calculate and apply DSP delay values
- Verify crossover summation in measurement (flat on-axis, smooth off-axis)
- Adjust crossover frequency if distortion measurement requires it
