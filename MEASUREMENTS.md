# Measurements

This file contains the measurement plan for Mk2 Reference Loudspeaker.

---

# Goal

Validate the simulated design with real acoustic measurements and use the data to create the final DSP tuning.

---

# Required Tools

- Measurement microphone, e.g. UMIK-1 or calibrated XLR microphone
- REW
- VituixCAD
- Turntable or angle jig
- Tape measure / laser distance meter
- Quiet measurement environment
- Optional: ground-plane outdoor measurement area

---

# Driver Measurements

## Woofer

- Nearfield measurement of each woofer
- Combined nearfield response
- Check polarity and push-push wiring
- Distortion measurement at relevant levels

## Midrange

- On-axis response in cabinet
- Horizontal off-axis response
- Vertical off-axis response
- Distortion around 150-2000 Hz

## Tweeter / Waveguide

- On-axis response in WG212
- Horizontal off-axis response
- Vertical off-axis response
- Distortion around 1000-5000 Hz
- Confirm whether 1100 Hz LR4 is practical

> **mk3 branch note:** On the `mk3-sb26stac` branch the tweeter is
> SB26STAC-C000-4 (not H2606) and the distortion test target is **1100 Hz**
> (not 1250 Hz). Confirm whether 1100 Hz LR4 is practical for the SB26STAC.

---

# Horizontal Measurement Angles

Minimum set:

- 0 deg
- 10 deg
- 20 deg
- 30 deg
- 40 deg
- 50 deg
- 60 deg

Extended set:

- 70 deg
- 80 deg
- 90 deg

---

# Vertical Measurement Angles

Minimum set:

- -30 deg
- -20 deg
- -15 deg
- -10 deg
- 0 deg
- +10 deg
- +15 deg
- +20 deg
- +30 deg

Focus area:

- 800 Hz to 3000 Hz
- Mid/tweeter crossover region
- Listening window around +/-15 deg

---

# Nearfield / Farfield Merge

Tasks:

- Measure bass nearfield
- Measure farfield response
- Merge low-frequency and farfield data
- Apply baffle diffraction/room-window handling carefully

---

# VituixCAD Workflow

- Import all driver measurements
- Add acoustic offsets
- Build active crossover model
- Optimize LR4 acoustic slopes
- Verify directivity
- Export DSP targets

---

# Validation Targets

## On-axis

Target: approx. +/-1.5 dB after DSP in the main listening range.

## Listening window

Target: smooth and close to on-axis without sudden dips.

## Predicted in-room

Target: smooth downward slope from bass to treble.

## Directivity Index

Target: smooth and generally rising with frequency.

## Vertical response

Target: useful listening window around +/-15 deg.

---

# Open Questions

- Can H2606 in WG212 safely cross at 1250 Hz? (mk2 main line)
- Can SB26STAC-C000-4 safely cross at 1100 Hz? (mk3-sb26stac branch)
- Is 140 mm c-c mechanically achievable?
- Does the measured WG212 response match the simplified simulation?
- How much EQ is needed around the baffle/waveguide transition?
- Does the push-push bass reduce cabinet vibration as expected?
