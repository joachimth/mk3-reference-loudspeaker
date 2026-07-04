# Chapter 6 - Waveguide Development

---

## Purpose

A waveguide serves several functions in a 3-way loudspeaker:

1. **Directivity control** - shapes the radiation pattern of the tweeter so it matches the narrowing directivity of the midrange below the crossover frequency
2. **Loading** - provides acoustic load that reduces tweeter excursion near the crossover
3. **Sensitivity increase** - concentrates forward energy, increasing on-axis sensitivity
4. **Lower crossover frequency** - a well-loaded tweeter can cross lower than a bare dome, reducing lobing

Without a waveguide, a bare 26 mm dome tweeter radiates almost omnidirectionally up to approximately 4-6 kHz. The midrange driver narrows significantly above about 1500 Hz. This mismatch in directivity causes a visible step in the DI curve and a response hole in the off-axis measurements at the crossover frequency.

---

## Design strategy

The waveguide is a custom 3D-printed design, intended to be printed in PLA or PETG and sanded/painted for the prototype. The final version may be machined or CNC-routed in a harder material.

Key design parameters:

| Parameter | Description |
|---|---|
| Mouth diameter | Defines directivity at the crossover frequency |
| Throat diameter | Must fit the H2606 dome and surround |
| Profile | Determines the waveguide's directivity behavior |
| Depth | Affects directivity and baffle integration |
| Flange shape | Determines how the waveguide integrates with the baffle |

---

## Variants compared

The simplified directivity simulations compared four waveguide mouth diameters:

| Variant | Mouth | Notes |
|---|---|---|
| WG212 | ~212 mm | Current candidate |
| WG220 | ~220 mm | Marginal improvement in directivity |
| WG230 | ~230 mm | More directional, larger baffle impact |
| WG240 | ~240 mm | Most directional but mechanically challenging in 300 mm cabinet |

---

## Selection: WG212

WG212 was selected as the current design direction (DD-009). The key finding from the simplified simulations was:

> The strongest improvement in spinorama quality comes from lowering the mid/tweeter crossover frequency and reducing the c-c spacing, not from increasing the waveguide mouth size.

A larger waveguide (WG230 or WG240) did increase horizontal directivity at the crossover frequency, but it:
- Demanded more baffle width to integrate cleanly
- Left less room for the midrange below the waveguide
- Made the 140 mm c-c spacing harder to achieve
- Required a larger cabinet front, increasing diffraction

The improvement from WG220 to WG240 was significantly smaller than the improvement from reducing the crossover frequency by 50-100 Hz.

---

## WG212 geometry (design candidate)

A parametric OpenSCAD model now exists:
[`../cad/mk2_waveguide_os.scad`](../cad/mk2_waveguide_os.scad) (see
[`../cad/README.md`](../cad/README.md)). It realises the WG212 as an **asymmetric
oblate-spheroid (OS)** waveguide — wide horizontally to match the still-broad
midrange at the crossover, narrower vertically to limit vertical lobing. The
geometry is recorded as DESIGN_DECISIONS.md **DD-012**:

| Parameter | Value (estimate) |
|---|---|
| Throat diameter | ~28 mm (placeholder — must match the real H2606 exit) |
| Profile | Oblate-spheroid bore + tangent rolled mouth (flush with baffle) |
| Nominal coverage | ~100° horizontal / ~64° vertical |
| Mouth | ~211.7 × 121.0 mm |
| Total depth | ~75 mm |
| Horizontal pattern-control limit | ~1620 Hz |
| Flange | 252 × 168 mm, R22 corners, flush/recessed into the baffle |

Because horizontal control only reaches down to ~1620 Hz, the waveguide best
supports a crossover **near that limit**. The v6b nominal target is still
1250 Hz LR4, but that sits below the control band — exactly the trade-off flagged
in DD-010 and [REVIEW.md](../REVIEW.md) §C2, to be settled by measuring the
printed waveguide.

| Task | Status |
|---|---|
| Define throat diameter (H2606 specific) | Placeholder (28 mm) — verify on prototype |
| Define profile (OS/Tractrix/custom) | Done — asymmetric OS |
| Define mouth and termination | Done — ~211.7 × 121, rolled flush mouth |
| Define depth | Done — ~75 mm |
| Define flange shape for baffle integration | Done — 252 × 168, R22 |
| Generate OpenSCAD or CAD model | Done — `cad/mk2_waveguide_os.scad` |
| Export STL for printing | Pending |
| Print prototype | Pending |
| Test fit H2606 | Pending |
| Measure in finished cabinet | Pending |

---

## Profile guidance

The waveguide profile determines how directivity transitions from the throat to the mouth. Common approaches:

**Oblate spheroidal (OS) profile** - mathematically derived profile that produces a constant directivity pattern with a smooth mouth termination. Used in professional studio monitors. Preferred when constant directivity across a wide range is important.

**Tractrix profile** - older profile, still widely used. Generally produces good results but may not achieve true constant directivity.

**Custom/optimized profiles** - can be designed using FEM simulation tools (e.g. Akabak, Comsol) but requires more expertise.

For this project, an OS-inspired profile is the starting point. The final profile will be verified by measuring the printed WG212 in the cabinet.

---

## Integration with the baffle

The WG212 flange must integrate cleanly with the front baffle:

- The flange should sit flush or slightly recessed into the baffle
- The baffle around the waveguide should be as smooth as possible (no sharp edges near the waveguide mouth)

**Mouth termination (avoid a sharp edge).** The waveguide must reach the baffle
*flush and tangent* — any forward lip or 90° step at the mouth diffracts and
shows up as off-axis / spinorama ripple, defeating the waveguide's purpose. The
first revision of `../cad/mk2_waveguide_os.scad` placed the mounting flange
forward of the mouth plane with a straight mouth cut, leaving exactly such a lip;
this was corrected so the flange sits *behind* the flush mouth plane (see
[`../simulations/waveguide_profile.py`](../simulations/waveguide_profile.py) and
`../simulations/plots/waveguide_termination.png`). For an even smoother transition
the mouth roundover can be enlarged (parameter `Lr`) so it rolls into the baffle
with continuous curvature, and the baffle opening itself should carry a matching
roundover.
- The midrange cutout is immediately below the waveguide; the gap between them sets the c-c distance
- The nominal c-c target is 140 mm, but the realistic buildable value is ~150 mm
  (DD-011 caveat); the narrow vertical mouth (~121 mm) of the asymmetric WG212
  helps keep this tight without lobing. The `cabinet.scad` model uses 150 mm.

---

## Open items

- Verify the throat against the real H2606 faceplate and update the model
- Export STL, print and test-fit the prototype
- Measure H2606 distortion + directivity in WG212 to confirm the crossover
  (1250 Hz nominal vs the ~1620 Hz control limit)

---

## SB26STAC waveguide (mk3)

> **mk3-sb26stac branch.** The SB26STAC-C000-4 is a conventional dome tweeter
> (no built-in horn), so the waveguide is a pure directivity device rather than
> a horn extension. See DD-013 and DD-014.

### Model

[`../cad/mk2_waveguide_sb26stac.scad`](../cad/mk2_waveguide_sb26stac.scad)

### Geometry

| Parameter | Value |
|---|---|
| Throat diameter | 28 mm (SB26STAC dome + surround, no horn) |
| Baffle cutout diameter (BCD) | 88.5 mm |
| Profile | Same OS profile family as the H2606 WG212 |
| Horn loading | None — conventional dome in waveguide |
| Crossover | 1100 Hz LR4 (DD-014) |

The throat is sized to the SB26STAC dome and surround rather than a horn exit,
and the profile uses the same oblate-spheroid bore family as the WG212 so the
directivity behavior is comparable. The 88.5 mm BCD matches the SB26STAC
faceplate cutout requirement.

### Open items (SB26STAC)

- Caliper-verify the SB26STAC dome, surround, and faceplate cutout diameter
  against `cad/mk2_waveguide_sb26stac.scad` before printing
- Export STL, print, and test-fit the SB26STAC in the waveguide
- Measure SB26STAC in-waveguide response and directivity at 1100 Hz to confirm
  the crossover (expected to pass comfortably given the 350 Hz Fs margin — no
  distortion-test gate required, unlike the H2606 at 1250 Hz)
