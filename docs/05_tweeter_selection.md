# Chapter 5 - Tweeter Investigations

---

## Requirements

The tweeter must:

- Cover the range from 1250 Hz to beyond 20 kHz
- Be suitable for mounting in a custom waveguide (WG212), or used with its built-in horn
- Have sufficient power handling and headroom at 1250 Hz
- Have low distortion at 1250 Hz and above
- Have a dome/surround geometry compatible with the WG212 throat design
- Fit within the 300 mm baffle at 140 mm c-c from the midrange

---

## Investigated driver

### ScanSpeak H2606/920000 (selected)

The ScanSpeak Discovery H2606/920000 is a horn dome tweeter selected for this project. It is formerly known as the Vifa H26TG05-06.

**Key specifications:**

| Parameter | Value |
|---|---|
| Series | Discovery |
| Type | Horn Dome Tweeter |
| Dome diameter | 25 mm / 1" |
| Dome material | Coated textile |
| Impedance | 6 Ω |
| Re | 4.7 Ω |
| Fs | 1030 Hz |
| Sensitivity | 95.2 dB / 2.83V / 1m |
| Le | 0.05 mH |
| Qms | 2.1 |
| Qes | 1.2 |
| Qts | 0.70 |
| BL | 3.3 Tm |
| Mms | 0.4 g |
| Xmax | 0.2 mm |
| Sd | 5.7 cm² |
| Power (RMS) | 100 W |
| Power (max) | 200 W |
| Price | ~€44 |

---

## Driver character

The H2606/920000 is a horn-loaded tweeter. The built-in horn shapes its radiation pattern and provides acoustic loading, which:

- Increases sensitivity significantly (95.2 dB is very high for a 1" dome)
- Reduces the excursion required near the crossover frequency
- Narrows the radiation pattern even before any additional custom waveguide is applied

The very limited Xmax of 0.2 mm is typical for a horn tweeter - the horn loading means that very little cone displacement is needed to produce significant acoustic output. The driver is not designed for large excursion but for efficient, low-distortion operation in its passband.

The textile dome provides a softer character than metal or polymer horn tweeters. Combined with the horn loading, the result is a high-sensitivity, relatively smooth horn tweeter that is less aggressive-sounding than hard-dome horn designs.

---

## Sensitivity mismatch

At 95.2 dB / 2.83V / 1m, the H2606/920000 is significantly more sensitive than the ScanSpeak 15W/4434G00 midrange (~89.7 dB). This means the tweeter channel will require substantial gain reduction in the DSP - on the order of 5 to 7 dB of attenuation relative to the midrange channel - to achieve a flat summed response at the crossover. The exact pad is finalised from measurement (the tweeter gains some sensitivity in the waveguide, and baffle step lowers the mid's effective level).

This is handled in DSP and does not affect the acoustic design, but it must be accounted for in the level-matching step.

---

## Waveguide integration

The H2606/920000 already has a built-in horn. The WG212 custom waveguide is designed to further control the radiation pattern and optimize the directivity match with the ScanSpeak 15W midrange.

Two approaches are possible:

**Option A - Use built-in horn, no custom WG212**
The tweeter is mounted directly in the baffle with its factory horn. No custom waveguide. The built-in horn provides some directivity control. This is simpler but may not achieve the target directivity match with the 15W at 1250 Hz.

**Option B - Custom WG212 designed around H2606/920000 dome**
The built-in horn is removed (or the driver is adapted) and the dome assembly is mounted into the custom WG212 waveguide. The WG212 provides a larger, optimized radiation pattern.

The current design direction is Option B - the WG212 is designed specifically to work with this driver. The throat diameter of WG212 must be designed to accept the H2606/920000 dome and surround geometry.

---

## Critical open question

**Can the H2606/920000 in WG212 safely cross at 1250 Hz?**

The Fs of 1030 Hz means the tweeter is resonating at 1030 Hz. The 1250 Hz LR4 crossover is only 220 Hz above resonance. The high-pass filter at 1250 Hz must provide sufficient protection below resonance.

The distortion level at 1250 Hz in the actual WG212 must be measured on the prototype before the crossover frequency is confirmed. If distortion is too high, the crossover may need to be raised to 1350-1450 Hz.

---

## Crossover integration

The tweeter is:
- High-pass at 1250 Hz LR4
- Approximately -5 to -7 dB gain adjustment in DSP to match midrange sensitivity (finalised from measurement)
- DSP delay applied to align acoustic center with midrange

See Chapter 11 (Crossovers) and Chapter 14 (DSP) for detail.

---

## Open items

- Complete WG212 CAD with throat geometry specific to H2606/920000 surround
- Print WG212 prototype
- Test fit H2606/920000 in WG212
- Measure on-axis and off-axis response in WG212
- Measure distortion at 1250 Hz - critical for crossover decision
- Confirm c-c spacing to 15W midrange is achievable at 140 mm
