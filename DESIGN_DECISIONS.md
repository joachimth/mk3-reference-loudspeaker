# Design Decisions

This file documents the important design decisions and the reasoning behind them.

---

# DD-001 - Use active DSP

## Decision

The loudspeaker will be an active DSP-controlled 3-way system.

## Reasoning

Active DSP allows:

- Accurate crossover slopes
- Driver delay correction
- Low-frequency EQ
- Baffle/waveguide correction
- Multiple target curves
- Easier iteration after measurements

## Consequence

The design depends on DSP and individual amplifier channels. A passive crossover is not currently part of the design goal.

---

# DD-002 - Use sealed bass alignment

## Decision

The bass system will be sealed.

## Reasoning

A sealed alignment offers:

- No port noise
- Easier integration with room gain
- Predictable roll-off
- Lower group delay than heavily tuned reflex systems
- Easy DSP extension

## Consequence

The system requires more amplifier power and excursion than a reflex design for the same SPL at very low frequencies.

---

# DD-003 - Use side-mounted push-push woofers

## Decision

Use two side-mounted woofers in a push-push configuration.

## Reasoning

Push-push placement reduces cabinet reaction forces and vibration. Side mounting also keeps the front baffle clear for the midrange and waveguide.

## Consequence

Woofer placement, wiring and mechanical coupling must be carefully planned.

---

# DD-004 - Select GRS 8SW-4HE-8 woofers

## Decision

Use 2 x GRS 8SW-4HE-8 per loudspeaker.

## Reasoning

The GRS woofer has:

- Low Fs
- Useful excursion
- Good fit for approx. 64-70 L sealed volume when used as a pair
- Attractive cost/performance ratio

## Consequence

Two 4-ohm woofers should normally be wired in series for an 8-ohm load unless the amplifier is explicitly stable into 2 ohms.

---

# DD-005 - Select ScanSpeak 15W/4434G00 midrange

## Decision

Use ScanSpeak 15W/4434G00 as the midrange driver.

## Reasoning

The 15W size offers a useful balance between:

- Low enough frequency range to meet the woofers around 150 Hz
- Small enough radiating diameter to match a waveguide around 1.2-1.6 kHz
- Good expected distortion performance

## Consequence

The vertical c-c spacing to the tweeter/waveguide remains a critical design constraint.

---

# DD-006 - Select Seas H2606 tweeter in waveguide

## Decision

Use Seas H2606 in a custom waveguide.

## Reasoning

A waveguide is needed to:

- Improve directivity match to the midrange
- Reduce tweeter excursion near crossover
- Improve power response
- Allow lower crossover frequency than a bare dome would normally support

## Consequence

The final crossover frequency must be validated by distortion measurements of H2606 in the actual printed waveguide.

---

# DD-007 - Select 300 mm cabinet width

## Decision

Use a 300 mm wide front baffle.

## Reasoning

The 300 mm width is the best current compromise between:

- Directivity
- Diffraction
- Practical waveguide integration
- Visual proportions
- Cabinet volume

280 mm was attractive but more mechanically constrained. Wider cabinets offered only small simulated improvements and increased size.

---

# DD-008 - Use R50 vertical front roundovers

## Decision

Use approx. R50 mm vertical front edge roundovers.

## Reasoning

The simulations suggested that larger roundovers reduce diffraction ripple and smooth the off-axis response.

## Consequence

The cabinet front construction must support a large radius, possibly through laminated/machined corner pieces or thick front edge stock.

---

# DD-009 - Retain WG212 rather than larger WG230

## Decision

Keep the current direction around a 212 mm waveguide mouth.

## Reasoning

The simplified directivity comparison suggested that larger waveguides did not provide enough benefit compared with the gains from lower crossover frequency and shorter c-c spacing.

## Consequence

Waveguide refinement should focus on profile, mouth termination, throat geometry and physical integration rather than simply increasing mouth size.

---

# DD-010 - Target 1250 Hz mid/tweeter crossover

## Decision

Use 1250 Hz LR4 acoustic crossover as the current simulation target.

## Reasoning

Lowering the mid/tweeter crossover improves the directivity match and vertical response in the simplified simulations.

## Consequence

The tweeter/waveguide combination must be measured carefully for distortion and headroom at 1250 Hz.

---

# DD-011 - Target 140 mm mid/tweeter c-c spacing

## Decision

Target 140 mm center-to-center spacing between waveguide/tweeter and midrange.

## Reasoning

Shorter c-c spacing reduces vertical lobing around the mid/tweeter crossover.

## Consequence

The front layout becomes mechanically tight. The waveguide flange and midrange recess must be designed together.
