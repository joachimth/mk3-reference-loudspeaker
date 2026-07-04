# Chapter 15 - Measurements

---

## Purpose

Measurements validate the simulated design and provide the data needed to finalize the DSP crossover, delay alignment, and EQ. No crossover or DSP settings are finalized until real measurements are taken on the physical prototype.

---

## Required tools

| Tool | Purpose |
|---|---|
| Measurement microphone | Calibrated (e.g. UMIK-1 or calibrated XLR mic + preamp) |
| REW (Room EQ Wizard) | Measurement software, free |
| VituixCAD | Crossover and spinorama analysis |
| Turntable or angle jig | Rotating the loudspeaker for polar measurements |
| Tape measure / laser distance meter | Microphone placement |
| Quiet measurement environment | Minimum background noise |
| Outdoor ground-plane area (optional) | Extended time window for high-quality bass measurements |

---

## Measurement environment

For the initial prototype measurements, a large room or garden outdoor ground-plane measurement is preferred. The longer reflection-free time window allows lower-frequency measurements without gating artifacts.

Indoor measurements can be used for the upper frequency range (above approximately 300-500 Hz) where the measurement window is short enough to gate out room reflections.

For full spinorama measurements, a quiet room with a turntable setup is needed. An anechoic chamber is ideal but not required - gated measurements in a large room can produce adequate results for DIY purposes.

---

## Driver measurements

### Woofer (GRS 8SW-4HE-8)

- Nearfield measurement of each woofer individually (microphone very close to cone, ~1 cm)
- Combined nearfield response (both woofers driven together)
- Polarity check: verify push-push wiring (both cones moving in same direction)
- Impedance measurement
- Distortion measurement at rated SPL levels (THD vs frequency)

### Midrange (ScanSpeak 15W/4434G00)

- On-axis response in the cabinet
- Horizontal off-axis: 0° to 60° in 10° steps
- Vertical off-axis: -30° to +30° in 10° steps
- Distortion in the 150-1500 Hz range
- Impedance in cabinet

### Tweeter / Waveguide (SB Acoustics SB26STAC-C000-4 in waveguide)

- On-axis response in the waveguide mounted in cabinet
- Horizontal off-axis: 0° to 60° in 10° steps
- Vertical off-axis: -30° to +30° in 10° steps
- **Distortion at 1100 Hz** - confirms crossover viability (expected to pass comfortably given the 350 Hz Fs margin)
- Impedance in waveguide

---

## System measurements (assembled prototype)

After driver measurements and initial DSP setup:

- On-axis full system response
- Horizontal polar: 0° to 60° minimum (0° to 90° extended)
- Vertical polar: -30° to +30°
- Listening window (CEA-2034 average)
- Full spinorama set in VituixCAD

---

## Horizontal measurement angles

**Minimum set:**

| Angle |
|---|
| 0° |
| 10° |
| 20° |
| 30° |
| 40° |
| 50° |
| 60° |

**Extended set:**

| Angle |
|---|
| 70° |
| 80° |
| 90° |

---

## Vertical measurement angles

**Minimum set:**

| Angle |
|---|
| -30° |
| -20° |
| -15° |
| -10° |
| 0° |
| +10° |
| +15° |
| +20° |
| +30° |

**Focus area:** 800 Hz to 3000 Hz, particularly the mid/tweeter crossover region.

---

## Nearfield / farfield merge

At low frequencies the measurement window is too short for accurate farfield measurement indoors. The procedure:

1. Measure bass nearfield (microphone very close to the woofer cone)
2. Measure the farfield response gated at the reflection-free time window
3. Merge the two curves in VituixCAD or REW at the appropriate frequency (typically 300-600 Hz)
4. Apply baffle diffraction correction to the nearfield data

---

## VituixCAD workflow

1. Import all driver measurements (on-axis and off-axis)
2. Enter acoustic offsets (driver center positions relative to a reference point)
3. Build active crossover model (LR4 at 150 Hz and 1100 Hz)
4. Add delay compensation values
5. Optimize crossover frequency and slopes
6. Compute CEA-2034 spinorama curves
7. Evaluate DI, listening window, sound power, PIR
8. Export DSP targets for implementation

---

## Open questions to resolve through measurement

| Question | How to answer |
|---|---|
| Can SB26STAC in waveguide cross at 1100 Hz? | Measure distortion in waveguide |
| Is 140 mm c-c achievable mechanically? | Verify in cabinet construction |
| Does waveguide response match simulation? | Measure waveguide on/off-axis |
| How much EQ is needed at baffle/waveguide transition? | Measure on-axis and compare to target |
| Does push-push reduce cabinet vibration? | Measure cabinet acceleration (optional) |
| What is the optimal bass shelf amount? | Measure excursion at maximum SPL |

---

## Open items

- Build prototype cabinet
- Set up measurement rig (microphone stand, turntable or angle jig)
- Calibrate measurement microphone
- Follow VituixCAD import workflow
- Document all measurement results in this file
