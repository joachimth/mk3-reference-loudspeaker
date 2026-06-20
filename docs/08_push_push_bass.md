# Chapter 8 - Push-Push Bass

---

## What is push-push?

A push-push bass configuration uses two woofer drivers mounted on opposite sides of the cabinet (or the same side in opposing orientations), wired so that as one cone moves outward (away from the cabinet), the other cone also moves outward.

From the perspective of an external observer, both cones move in the same direction simultaneously. From the perspective of the cabinet, the reaction forces from the two drivers act in opposite directions and therefore cancel each other.

---

## Why push-push?

### Cabinet vibration reduction

Each woofer driver exerts a reaction force on the cabinet equal and opposite to the force it exerts on the air. In a conventional single-woofer design, this force causes the cabinet to vibrate at bass frequencies.

In push-push, the two reaction forces are opposite and cancel at the cabinet. The net force on the cabinet is close to zero. This significantly reduces cabinet vibration and the associated structural resonances.

### Front baffle kept clear

Side mounting both woofers leaves the front baffle free for the midrange and tweeter/waveguide array. This simplifies the front baffle layout and avoids a woofer cutout near the midrange driver.

### Symmetrical cabinet structure

Two symmetrically placed woofers produce a mechanically symmetric cabinet structure. The side panels experience equal loading.

---

## Physical arrangement

For the Mk2 Reference Loudspeaker, both woofers are mounted on the side panels:

- One woofer on the left side panel
- One woofer on the right side panel
- Both woofers facing outward (magnets facing inward)
- **Centers opposed at the same height** (directly across from each other)

Mounting the two drivers directly opposite at the same height is the correct
push-push arrangement: the two reaction forces share a single line of action and
cancel as a clean couple, with no rocking moment. A vertical stagger (mounting
one driver higher than the other) offsets that line of action and re-introduces
a rocking moment on the cabinet, so it is avoided. (An earlier layout proposed a
~350 mm / ~700 mm stagger; this has been dropped — see [REVIEW.md](../REVIEW.md) §C3.)

The geometry fits: the GRS overall depth is ~117 mm, so in the ~256 mm internal
width two opposed magnets leave roughly `256 − 2×117 ≈ 22 mm` of static clearance
between them (the magnets are fixed to the baskets/walls and do not move). That
gap is enough to bond a short rigid coupling block between the two magnet
assemblies — see *Mechanical coupling* below.

---

## Wiring

In a push-push configuration, the wiring polarity determines whether the drivers work together or against each other.

**Correct wiring (push-push):**
- Both driver cones move outward simultaneously
- The magnetic polarity of the two drivers is opposite relative to the current direction
- In practice: wire the two 4-ohm drivers in series, with one driver's positive terminal connected to the other's negative terminal

**Verification test:**
1. Apply a DC voltage (e.g. from a battery) briefly to the series combination
2. Both cones should move in the same direction (both out or both in)
3. If one moves out and one moves in, the wiring is incorrect (push-pull, not push-push)

---

## Push-push vs push-pull

These two terms are often confused.

| Configuration | Cone movement | Cabinet reaction | Acoustic output |
|---|---|---|---|
| Push-push | Both move out together | Forces cancel | Normal (full) |
| Push-pull | One out, one in | Forces add | Cancels (net zero) |

Push-pull cancels the acoustic output - it is not useful for producing bass. Push-push is the correct configuration for a bass radiator system.

---

## Mechanical coupling

With the two drivers opposed at the same height, a short rigid **coupling block**
is bonded across the ~22 mm gap between the magnet assemblies. This ties the two
motors together so they cannot independently excite the cabinet side panels — the
ideal force-cancelling arrangement, and the main reason same-height opposed
placement is preferred over a stagger.

The block must not significantly obstruct the bass chamber air flow. Its size and
fixing are finalized in CAD and confirmed in the prototype phase.

---

## Expected benefits

- Reduced cabinet panel excitation in the bass range
- Potentially audible reduction in bass coloration from cabinet resonances
- Clean front baffle for midrange/tweeter integration

---

## Open items

- Confirm the opposed woofer center height matches the bracing layout
- Verify the coupling block fits the ~22 mm magnet gap in the 300 × 370 mm cross-section without choking air flow
- Develop polarity test procedure for prototype verification
- Measure cabinet vibration with and without push-push coupling (optional)
