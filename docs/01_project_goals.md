# Chapter 1 - Project Goals and Philosophy

---

## The goal

The Mk3 Reference Loudspeaker is a DIY active 3-way loudspeaker designed to perform at reference level. The design should be able to stand alongside the best commercial studio monitors and high-end home speakers in terms of directivity, distortion, and tonal accuracy.

The goal is not to build the cheapest possible speaker. The goal is to build the best loudspeaker achievable with careful engineering, thoughtful driver selection, and modern DSP.

---

## Acoustic targets

- Approximately ±1.5 dB on-axis response after DSP
- Smooth, controlled directivity across the full frequency range
- Useful listening window of at least ±15° vertical and ±30° horizontal
- Smooth predicted in-room response (gently descending from bass to treble)
- Low directivity index variation - a rising DI is preferred over an irregular one
- Low harmonic distortion, particularly in the midrange and crossover regions

---

## Main design principles

**Controlled directivity first.** The design is based on the principle that controlled and smooth directivity is more important than optimizing the on-axis response in isolation. A well-controlled loudspeaker sounds consistent at different listening positions and in different rooms.

**Active DSP as a tool, not a crutch.** DSP allows precise crossover slopes, driver delay compensation, baffle step correction, and EQ. The goal is to build a mechanically well-designed loudspeaker where DSP fine-tunes rather than fixes fundamental problems.

**Simulation before prototype.** Design decisions are validated in simulation before committing to expensive physical work. Cabinet width, roundover radius, waveguide size, c-c spacing, and crossover frequency have all been explored through simplified simulations.

**Spinorama as the validation standard.** The CEA-2034 spinorama is the primary quality metric. Good spinorama results predict good in-room performance.

**Long-term maintainability.** The design uses off-the-shelf drivers, standard materials, and common DSP hardware. The documentation is version-controlled and open, so the design can be revisited and improved over time.

---

## Inspiration

The design is directly inspired by three loudspeakers that represent the current state of the art in controlled directivity and measured performance:

**Genelec 8361A** - A professional studio monitor using a coaxial mid/tweeter in a large waveguide. Excellent directivity control from a relatively compact enclosure. Sets the standard for in-room consistency.

**Dutch & Dutch 8C** - An active cardioid loudspeaker with powerful DSP and a waveguide-mounted tweeter. Known for exceptional in-room response measurements and a remarkably flat predicted in-room response.

**Revel Salon2** - A passive 4-way loudspeaker optimized with Harman's spinorama-based design process. One of the most thoroughly measured consumer loudspeakers available, with excellent directivity and very low distortion.

All three demonstrate that optimizing for the full spinorama - not just the on-axis response - produces loudspeakers that perform consistently in real rooms with real listeners.

---

## Scope and boundaries

This project covers:

- Driver selection
- Cabinet design
- Waveguide design
- Simulation and analysis
- Physical prototype build
- Acoustic measurement
- DSP implementation and tuning

This project does not cover:

- Passive crossover design (not part of the active DSP approach)
- Room treatment (assumed as a separate concern)
- Streaming, amplifier selection beyond DSP/amplifier platform (addressed separately in electronics section)
