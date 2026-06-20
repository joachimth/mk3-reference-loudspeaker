# Chapter 2 - Loudspeaker Theory

This chapter summarizes the key acoustic concepts that inform the design decisions in this project.

---

## Frequency response

The on-axis frequency response is the most commonly cited loudspeaker measurement. It describes how much sound pressure the loudspeaker produces at each frequency when measured directly in front of the speaker.

On-axis response alone is a poor predictor of real-world performance. Most of the sound reaching a listener in a room arrives as reflections, not as direct sound. For this reason, the full set of measurements described by the spinorama standard is more useful than on-axis response in isolation.

A flat on-axis response is still important. Large deviations will usually be audible regardless of room conditions.

---

## Listening window

The listening window is the average of several measurements taken over a small angular range around the on-axis position. The standard CEA-2034 listening window averages:

- 0° (on-axis)
- ±10° horizontal
- ±10° vertical

This average is more representative of the direct sound arriving at a real seated listener than the strict on-axis measurement alone.

---

## Early reflections

Early reflections arrive at the listener within approximately 20 ms after the direct sound. They originate from the floor, ceiling, and side walls near the loudspeaker. In a typical room, early reflections contribute significantly to tonal balance and perceived spaciousness.

The early reflections curve in the CEA-2034 standard averages several specific off-axis angles intended to represent these room reflection paths.

A smooth early reflections curve - and a small difference between the early reflections and the listening window - predicts good in-room behavior.

---

## Sound power

The sound power response is the energy average of the loudspeaker output across all directions. In a highly reverberant space the sound power response dominates the perceived tonal balance. In a typical listening room it contributes alongside the direct sound and early reflections.

A loudspeaker with smooth sound power (usually gently declining from bass to treble) tends to sound tonally neutral across a range of rooms.

---

## Predicted in-room response

The predicted in-room response (PIR) is a weighted sum of the listening window, early reflections, and sound power curves. The weighting is designed to approximate the integrated response a listener hears in a typical room.

The Harman target for PIR is a gentle downward slope from bass to treble, approximately -1 to -2 dB per octave. This slope matches the frequency balance most listeners prefer and accounts for the typical room high-frequency absorption.

---

## Directivity Index (DI)

The Directivity Index describes how directional the loudspeaker is at each frequency. It is defined as the difference between the on-axis response and the sound power response, in dB.

A high DI means the loudspeaker radiates much more sound forward than in other directions. A low DI means the loudspeaker radiates sound more evenly in all directions.

For a reference loudspeaker, a DI that rises smoothly with frequency is preferred. This matches the directivity of a natural sound source (voices and instruments also become more directional at high frequencies) and produces a consistent sense of space.

Sudden changes or dips in the DI indicate directivity problems - usually crossover lobing, cabinet diffraction, or driver beaming effects.

---

## Lobing

When two drivers are crossing over in the same frequency region, their outputs combine in a frequency- and angle-dependent way. The resulting polar pattern shows lobes - directions where the combined output is boosted or cancelled.

Lobing is reduced by:

- Shortening the center-to-center distance between the drivers
- Lowering the crossover frequency
- Using steeper crossover slopes

In the vertical plane, lobing is particularly important because the listening window must remain smooth over the typical ±15° vertical range of a seated listener.

---

## Group delay

Group delay is the derivative of the phase response with respect to frequency. A constant group delay means all frequencies arrive at the listener at the same time. A non-constant group delay means some frequencies are delayed relative to others.

High-order passive crossovers and ported bass alignments can introduce significant group delay at low frequencies. Active LR4 crossovers are relatively well-behaved in this regard. DSP allows delay compensation between drivers to minimize group delay at the crossover frequencies.

---

## FIR vs IIR filters

**IIR (Infinite Impulse Response)** filters are the standard digital implementation of classical analog filter designs (Linkwitz-Riley, Butterworth, etc.). They are computationally efficient and widely used in DSP hardware. They introduce phase shift as a side effect of their filtering action.

**FIR (Finite Impulse Response)** filters can be designed with linear phase response - meaning they introduce no phase distortion, only a fixed time delay. This allows crossovers with no phase shift at the crossover point. FIR filters require more computational resources and introduce a fixed latency.

For the initial prototype, IIR (LR4) crossovers will be used. FIR filters are noted as a future upgrade path in v10.

---

## Toole and Olive research

Floyd Toole and Sean Olive at Harman International conducted extensive research on loudspeaker perception in real rooms, correlating acoustic measurements with listener preference ratings.

Key findings:

- Listener preference correlates strongly with a flat and smooth listening window, a smooth and consistent sound power response, and a narrow difference between on-axis and early reflections curves.
- Coloration and resonances in the off-axis response are as audible as on-axis problems.
- A gently declining predicted in-room response is preferred over a flat one, due to typical room high-frequency absorption.
- The spinorama standard (CEA-2034) was developed as a standardized set of measurements to capture these properties.

These findings are the primary basis for the design optimization strategy in this project. The goal is not to optimize for any single measurement, but to produce a well-shaped spinorama set.
