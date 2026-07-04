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

# DD-004 - Select GRS 8SW-4HE-8 woofers (superseded by DD-015)

## Decision

Use 2 x GRS 8SW-4HE-8 per loudspeaker.

**Superseded in v8 by DD-015** (GRS 12SW-4HE). Retained for historical reference.

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
- Small enough radiating diameter to match a waveguide around 1.1-1.6 kHz
- Good expected distortion performance

## Consequence

The vertical c-c spacing to the tweeter/waveguide remains a critical design constraint.

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

# DD-009 - Retain ~212 mm waveguide mouth rather than larger WG230

## Decision

Keep the current direction around a ~212 mm waveguide mouth.

## Reasoning

The simplified directivity comparison suggested that larger waveguides did not provide enough benefit compared with the gains from lower crossover frequency and shorter c-c spacing.

## Consequence

Waveguide refinement should focus on profile, mouth termination, throat geometry and physical integration rather than simply increasing mouth size.

---

# DD-011 - Target 140 mm mid/tweeter c-c spacing

## Decision

Target 140 mm center-to-center spacing between waveguide/tweeter and midrange.

## Reasoning

Shorter c-c spacing reduces vertical lobing around the mid/tweeter crossover.

## Consequence

The front layout becomes mechanically tight. The waveguide flange and midrange recess must be designed together.

## Caveat (review)

The geometric minimum c-c is ~145-160 mm: the 15W frame is ~Ø149 (half ~74.5 mm)
and a waveguide flange is ~140-150 mm tall (half ~70-75 mm), so 140 mm is only
achievable with a deliberately compact / bottom-trimmed ("D-shaped") flange. The
lobing analysis (`simulations/vertical_lobing.py`) shows ~155-160 mm crossed near
the waveguide control limit is still clean vertically, so treat **~150-160 mm** as
the realistic target and set the final value from the actual waveguide flange + mid
recess in CAD rather than over-committing to 140 mm.

---

# DD-013 - Select SB Acoustics SB26STAC-C000-4 tweeter

## Decision

Use SB Acoustics SB26STAC-C000-4 as the tweeter.

## Reasoning

The SB26STAC-C000-4 conventional dome tweeter is selected for its acoustic
advantages:

- **Fs 750 Hz gives 350 Hz margin at the 1100 Hz crossover** — a comfortable
  margin that requires no distortion-test gate before committing to the
  crossover frequency.
- **0.6 mm Xmax gives +8.1 dB excursion headroom** at 1100 Hz, substantially more
  maximum SPL capability near the crossover.
- **91.5 dB sensitivity is a better match to the 15W/4434G00's 89.7 dB** — only
  -1.8 dB of DSP pad is needed. This reduces wasted amplifier power and the
  thermal/level mismatch.
- **No horn loading** — the SB26STAC is a conventional dome used in a custom
  waveguide rather than a horn-loaded tweeter. The waveguide provides directivity
  control without relying on the driver's built-in horn.

The selection analysis comparing the SB26STAC against the earlier horn-dome
candidate is documented in `docs/SB26STAC-C000-4_analysis.md`.

## Consequence

A waveguide model (`cad/waveguide.scad`) is required with a throat sized for the
SB26STAC dome and surround (28 mm) and no horn loading. The crossover is set at
1100 Hz (see DD-014).

---

# DD-014 - Target 1100 Hz LR4 mid/tweeter crossover

## Decision

Use 1100 Hz LR4 acoustic crossover as the mid/tweeter target.

## Reasoning

The SB26STAC-C000-4's Fs of 750 Hz gives a comfortable 350 Hz margin at 1100 Hz.
The crossover optimization sweep (`simulations/mk3_crossover_optimization.py`)
confirms 1100 Hz as optimal, scoring 8.1 across Fs margin, excursion headroom,
directivity match, vertical lobing, and system sum flatness. The 1100 Hz point
sits below the broadside null (1147 Hz for 150 mm c-c) so the null is outside the
active crossover band, and the LR4 rolloff suppresses it almost entirely (under
0.7 dB ripple at ±15°).

Because the Fs margin is comfortable, no distortion-test gate is required before
committing to 1100 Hz.

## Consequence

The midrange low-pass and tweeter high-pass are both 1100 Hz LR4.

---

# DD-015 - Upgrade woofer to GRS 12SW-4HE

## Decision

Replace the GRS 8SW-4HE-8 (8") with the **GRS 12SW-4HE (12" high excursion)** as
the push-push woofer, 2 per enclosure. Sealed alignment retained; bass volume
increased to ~75 L under the divider plate.

## Reasoning

The 12SW-4HE offers a substantial low-frequency performance improvement over the
8SW while keeping the push-push, sealed, DSP-controlled architecture:

- **Fs 22 Hz** (vs 48 Hz) — much deeper native bass extension
- **Xmax 12.5 mm Klippel-verified** (vs 4.5 mm) — 2.8× more linear excursion
- **Sd 504 cm²** (vs 220 cm²) — 2.3× more radiating area
- **Displacement 12.6 cm³** per pair (vs 2.0 cm³) — 6.3× more, giving **+16 dB
  max SPL @ 30 Hz** over the previous design
- **Bl 16.2 Tm** (vs 10.5) — stronger motor
- **Vas 80.4 L** per driver (vs 28 L) — suits a ~75 L sealed chamber
- **Qts 0.43** (vs 0.38) — works well with a Linkwitz Transform to 0.707
- Cost increase is modest: ~€75 vs ~€45 per driver

The push-push configuration, side mounting, sealed alignment, and 150 Hz LR4
bass/mid crossover are all retained. Only the woofer driver and bass volume change.

## Consequence

- **Bass volume:** ~75 L under the divider plate (was ~69 L total).
- **Sealed alignment:** Fc ~39 Hz, Qtc ~0.76 (was ~34.5 Hz / 0.62).
- **Linkwitz Transform:** Fc 39.0 → 28 Hz, Qtc 0.76 → 0.707 (was 47.2 → 28 Hz,
  0.63 → 0.707).
- **Woofer cutout:** 284 mm (was 185 mm) — larger side-panel cutout.
- **Opposed magnet clearance:** only ~4 mm at 276 mm internal width (vs ~22 mm
  for the 8SW). The coupling block (h=20 mm, r=55 mm) and basket profile must be
  verified against a physical 12SW before committing the cabinet.
- **Sensitivity:** 84.5 dB (vs 85.0) — slightly more amplifier power needed, but
  the displacement advantage dominates at low frequencies.
- **Power handling:** 250 W (vs 100 W) — higher thermal capacity.
- DD-004 (8SW selection) is superseded; the 8SW remains in the repo as a
  historical comparison driver.
