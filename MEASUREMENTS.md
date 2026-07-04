# Measurements

This file contains the measurement plan for the Mk3 Reference Loudspeaker.

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

## Woofer (GRS 12SW-4HE)

- Nearfield measurement of each woofer (12" high excursion, Fs 22 Hz, Xmax 12.5 mm)
- Combined nearfield response
- Check polarity and push-push wiring (battery test — both cones move same direction)
- Distortion measurement at relevant levels — verify Klippel Xmax holds in cabinet
- Verify Linkwitz Transform target (39→28 Hz, Q 0.76→0.707) against measured sealed response
- Measure max SPL @ 30 Hz — target +16 dB over the previous 8SW design

## Midrange

- On-axis response in cabinet
- Horizontal off-axis response
- Vertical off-axis response
- Distortion around 150-2000 Hz

## Tweeter / Waveguide

- On-axis response in the waveguide
- Horizontal off-axis response
- Vertical off-axis response
- Distortion around 1000-5000 Hz
- Confirm whether 1100 Hz LR4 is practical for the SB26STAC-C000-4

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

- Can SB26STAC-C000-4 safely cross at 1100 Hz?
- Is 140 mm c-c mechanically achievable?
- Does the measured waveguide response match the simplified simulation?
- How much EQ is needed around the baffle/waveguide transition?
- Does the push-push bass reduce cabinet vibration as expected?
