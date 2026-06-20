# Chapter 14 - DSP

---

## Overview

The Mk2 Reference Loudspeaker is an active design. All crossovers, delay alignment, and EQ are implemented in digital signal processing. There is no passive crossover.

Each driver has its own amplifier channel:
- 2 × woofer channels (or 1 if wired in series)
- 1 × midrange channel
- 1 × tweeter channel

Minimum: 3 channels of amplification and DSP. Maximum (with separate woofer channels): 4 channels.

---

## DSP platform options

The DSP platform has not been finalized. Candidate approaches:

| Platform | Notes |
|---|---|
| MiniDSP 2×4 HD | Common, affordable, good ecosystem, limited channels |
| MiniDSP 4×10 HD | More channels, Dirac Live capable |
| Hypex FusionAmp FA123 | Integrated 3-channel amp + DSP in one module |
| Hypex FusionAmp FA253 | Higher power 3-channel |
| ADAU1452-based custom | Most flexible, requires firmware development |
| Separate DAC + external DSP | Maximum flexibility, most complex |

For the prototype phase, a MiniDSP or Hypex FusionAmp is the likely first implementation. The ADAU1452 custom platform is a longer-term option for a more integrated final version (see Chapter 17).

---

## Signal chain

```
Source → DSP input → [Bass LP filter] → Bass amplifier → Woofers (series)
                   → [Mid HP filter]  → [Mid LP filter] → Mid amplifier → Midrange
                   → [Tweeter HP filter] → [Tweeter EQ] → Tweeter amplifier → H2606 / WG212
```

---

## Crossover filters

### Bass low-pass

| Filter | Value |
|---|---|
| Type | Linkwitz-Riley 4th order (LR4) |
| Frequency | 150 Hz |
| Slope | 24 dB/oct |

### Bass subsonic high-pass

| Filter | Value |
|---|---|
| Type | Butterworth 2nd order (or LR4) |
| Frequency | ~20 Hz |
| Purpose | Protect woofers from infrasonic content |

### Midrange high-pass

| Filter | Value |
|---|---|
| Type | LR4 |
| Frequency | 150 Hz |
| Slope | 24 dB/oct |

### Midrange low-pass

| Filter | Value |
|---|---|
| Type | LR4 |
| Frequency | 1250 Hz |
| Slope | 24 dB/oct |

### Tweeter high-pass

| Filter | Value |
|---|---|
| Type | LR4 |
| Frequency | 1250 Hz |
| Slope | 24 dB/oct |

---

## Delay alignment

The acoustic centers of the three driver systems are at different physical positions. DSP delay (time alignment) corrects for this.

**Approximate acoustic center positions (to be measured):**

- Woofers: acoustic center is approximately at the plane of the cone (outside the cabinet, roughly flush with side panel outer face)
- Midrange: acoustic center is approximately at the cone plane on the front baffle
- Tweeter/waveguide: acoustic center is set back from the baffle by the waveguide depth

The delay values will be calculated from measurements using VituixCAD:
1. Measure each driver individually in the cabinet
2. VituixCAD extracts acoustic offsets from the phase response
3. Delays are applied in the DSP to align all three drivers at the crossover frequencies

Initial delay estimates cannot be confirmed until the prototype is built and measured.

---

## EQ targets

### Baffle step correction

The baffle step is a +6 dB rise in sensitivity as frequency increases above the frequency where the wavelength becomes comparable to the baffle width:

```
f_baffle_step ≈ c / (π × width) = 344 / (π × 0.3) ≈ 365 Hz
```

Below this frequency, the driver radiates into 4π steradians (all directions). Above it, radiation is increasingly confined to 2π steradians (hemisphere). This causes a +6 dB rise that must be corrected in the DSP.

In practice, the transition is gradual and the exact correction shape depends on the cabinet geometry and roundovers. The correction will be applied after measurement.

### Waveguide correction

The WG212 waveguide may introduce small peaks or irregularities in the on-axis response of the H2606. These will be measured and corrected with targeted EQ notch filters in the tweeter channel.

### Bass shelf (Linkwitz Transform)

To extend the bass response below the natural sealed rolloff frequency (Fc ~34.5 Hz), a shelving boost (Linkwitz Transform) can be applied. This trades excursion headroom for deeper extension.

The amount of bass shelf will be determined from measurements and the excursion limits of the GRS woofers at maximum listening level.

---

## House curves

Three target curves are planned for different listening contexts:

| Curve | Description |
|---|---|
| Flat | Reference monitoring - flat predicted listening window |
| Harman | Gentle downward slope (approx. -1 dB/oct) per Harman preference research |
| Mild bass lift | +2-3 dB below 100 Hz for casual listening |

These are applied as gentle global shelving EQ in addition to the correction EQ.

---

## Level matching

The three driver channels must be level-matched so that the crossover sums correctly. This is done by:
1. Measuring the on-axis sensitivity of each driver
2. Applying gain reduction in the DSP to match levels at the crossover frequencies

**Expected level adjustment:** The ScanSpeak H2606/920000 has a rated sensitivity of 95.2 dB / 2.83V / 1m, compared with approximately 89.7 dB for the ScanSpeak 15W midrange. This means the tweeter channel will require roughly -5 to -7 dB of gain reduction relative to the midrange channel before any other correction EQ is applied; the exact value is set from measurement.

---

## Open items

- Select DSP/amplifier platform for prototype
- Measure all driver acoustic centers
- Calculate initial delay values from measurements
- Measure and apply baffle step correction
- Measure and apply waveguide correction EQ
- Determine bass shelf amount from excursion measurements
- Finalize house curve presets
- Document final DSP settings with backup preset files
