# Chapter 5 - Tweeter Investigations

---

## Requirements

The tweeter must:

- Cover the range from 1250 Hz to beyond 20 kHz
- Be suitable for mounting in a custom waveguide (WG212)
- Have sufficient power handling and headroom at 1250 Hz
- Have low distortion at 1250 Hz and above
- Have a faceplate and surround geometry compatible with the WG212 throat design
- Fit within the 300 mm baffle at 140 mm c-c from the midrange

A dome tweeter with a waveguide is strongly preferred over a bare dome, as the waveguide controls directivity and reduces the required crossover frequency.

---

## Investigated driver

### Seas H2606 (selected)

The Seas H2606 (Excel series, 26 mm aluminum dome) is the tweeter selected for this project.

**Key characteristics:**

| Parameter | Value |
|---|---|
| Nominal diameter | 26 mm dome |
| Re | ~5.5 Ω |
| Fs | ~600 Hz |
| Sensitivity | ~90 dB / 2.83V / 1m (in waveguide) |
| Faceplate diameter | ~80 mm |

**Why the Seas H2606:**

- The Excel series is well regarded for low distortion and extended frequency response
- The 26 mm dome has sufficient diaphragm area to handle the waveguide loading at 1250 Hz without excessive excursion
- The H2606 has a relatively shallow faceplate geometry suitable for waveguide integration
- Seas provides measured frequency response and impedance data

**Waveguide requirement:**

The H2606 must operate in the WG212 waveguide to achieve:
- Directivity matching to the ScanSpeak 15W midrange
- Reduced excursion demands near the 1250 Hz crossover
- Controlled horizontal and vertical radiation pattern
- Improved power response

A bare dome would not match the 15W midrange directivity at 1250 Hz and would require a higher crossover frequency to avoid directivity mismatch.

---

## Critical open question

**Can the H2606 in WG212 safely cross at 1250 Hz?**

This is the single most important measurement question in the project. The distortion level of the H2606 in the final printed WG212, at the actual crossover frequency of 1250 Hz, must be measured and verified before the crossover frequency is confirmed.

If distortion is too high at 1250 Hz, the crossover may need to be raised to 1350-1450 Hz, with consequences for the vertical lobing pattern and c-c spacing target.

---

## Crossover integration

The tweeter is:
- High-pass at 1250 Hz LR4
- No low-pass filter needed above 20 kHz

The tweeter is acoustically delayed relative to the midrange due to the waveguide depth and physical position. DSP delay correction will be applied to align the acoustic centers of the tweeter and midrange.

---

## Open items

- Print WG212 prototype
- Measure H2606 in WG212: on-axis, off-axis, distortion at 1250 Hz
- Confirm whether 1250 Hz LR4 is achievable
- Measure mounting geometry and confirm c-c spacing compatibility
