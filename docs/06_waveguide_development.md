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

## WG212 design tasks

The waveguide CAD is not yet completed. Required steps:

| Task | Status |
|---|---|
| Define throat diameter (H2606 specific) | Pending |
| Define profile (OS/Tractrix/custom) | Pending |
| Define mouth radius and termination | Pending |
| Define depth | Pending |
| Define flange shape for baffle integration | Pending |
| Generate OpenSCAD or CAD model | Pending |
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
- The midrange cutout is immediately below the waveguide; the gap between them sets the c-c distance
- The c-c distance target is 140 mm (center of WG212 tweeter dome to center of 15W midrange)

---

## Open items

- Complete WG212 CAD design
- Determine throat geometry to fit H2606
- Print and test prototype
- Measure H2606 distortion in WG212 at 1250 Hz to confirm crossover suitability
