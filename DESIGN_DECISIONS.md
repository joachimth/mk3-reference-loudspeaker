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

# DD-006 - Select ScanSpeak H2606/920000 tweeter in WG212 waveguide

## Decision

Use ScanSpeak H2606/920000 (Discovery, horn dome, textile) in the custom WG212 waveguide.

## Reasoning

The H2606/920000 is a horn-loaded tweeter with high sensitivity (95.2 dB / 2.83V), low excursion requirements, and a soft textile dome character. The built-in horn already provides some directivity control. The custom WG212 extends this to better match the midrange directivity at 1250 Hz and optimizes the radiation pattern for the cabinet geometry.

The driver's Fs of 1030 Hz means the 1250 Hz crossover is 220 Hz above resonance - this must be verified by distortion measurement.

## Consequence

The WG212 throat diameter must be designed specifically for the H2606/920000 dome and surround geometry. The high sensitivity (95.2 dB) requires roughly 5 to 7 dB of DSP attenuation relative to the midrange channel (~89.7 dB), finalised from measurement. The final crossover frequency must be validated by distortion measurements of the H2606/920000 in the actual printed waveguide.

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

## Caveat (review)

[REVIEW.md](REVIEW.md) §C2 notes the directivity rationale is only half-right:
1250 Hz sits roughly 300-450 Hz *below* the WG212's pattern-control limit
(~1500-1700 Hz), so in that octave the waveguide is not yet controlling and the
directivity-match benefit is limited — lowering the crossover mainly improves
*lobing*, not constant directivity. It also asks the H2606 (Fs 1030 Hz) to work
at only ~1.2 × Fs on an LR4 high-pass, which is a distortion/headroom risk. 1250
Hz is retained as the pre-measurement target, but the usable value may land
higher (expect ~1400-1700 Hz); set it from measured H2606-in-WG distortion and DI.

---

# DD-011 - Target 140 mm mid/tweeter c-c spacing

## Decision

Target 140 mm center-to-center spacing between waveguide/tweeter and midrange.

## Reasoning

Shorter c-c spacing reduces vertical lobing around the mid/tweeter crossover.

## Consequence

The front layout becomes mechanically tight. The waveguide flange and midrange recess must be designed together.

## Caveat (review)

[REVIEW.md](REVIEW.md) §C1 estimates the geometric minimum c-c at ~145-160 mm:
the 15W frame is ~Ø149 (half ~74.5 mm) and a WG212 flange is ~140-150 mm tall
(half ~70-75 mm), so 140 mm is only achievable with a deliberately compact /
bottom-trimmed ("D-shaped") flange. The lobing analysis
(`simulations/vertical_lobing.py`) shows ~155-160 mm crossed near the waveguide
control limit is still clean vertically, so treat **~150-160 mm** as the
realistic target and set the final value from the actual WG flange + mid recess
in CAD rather than over-committing to 140 mm.

---

# DD-012 - WG212 geometry: asymmetric oblate-spheroid waveguide

## Decision

Define the WG212 as an **asymmetric oblate-spheroid (OS)** waveguide for the
H2606/920000, parametrised in [`cad/mk2_waveguide_os.scad`](cad/mk2_waveguide_os.scad):

- Throat ~28 mm (placeholder, to be matched to the real H2606 exit)
- OS bore with a tangent rolled mouth that ends flush with the baffle
- Nominal coverage ~100° horizontal / ~64° vertical
- Mouth ~211.7 × 121.0 mm, total depth ~75 mm
- Flange 252 × 168 mm, R22 corners
- Horizontal pattern-control limit ~1620 Hz

## Reasoning

A 5" midrange is still close to omnidirectional at the 1250-1600 Hz crossover, so
the waveguide is matched **wide horizontally** rather than narrow. A **narrower
vertical** coverage limits vertical lobing and lets the mid sit at a tight c-c.
The OS profile gives a smooth throat (no diffraction edge) and the flush rolled
mouth suppresses mouth-diffraction ripple. Terminating control at ~1620 Hz keeps
the waveguide working in its controlled band for a crossover near that frequency.

## Consequence

The ~1620 Hz control limit sits above the v6b nominal 1250 Hz target, reinforcing
the DD-010 caveat: the crossover may need to rise toward ~1500-1700 Hz once the
printed waveguide is measured. The ~75 mm depth must be accommodated behind the
baffle, and the 28 mm throat must be verified against the physical H2606 before
printing. The mouth must terminate **flush** with the baffle (no forward lip or
sharp edge) to avoid diffraction; the model was corrected to seat the flange
behind the flush mouth plane (see docs/06 and `simulations/waveguide_profile.py`).
This is simulation-stage geometry, not validated by measurement.
