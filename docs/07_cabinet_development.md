# Chapter 7 - Cabinet Development

---

## Design history

The cabinet geometry was developed iteratively across versions v2 through v6b.

| Version | Width | Roundover | Notes |
|---|---|---|---|
| v2 | Initial concept | - | Active 3-way with push-push woofers |
| v4 | 280 mm | R20-R40 | Narrower baffle explored, R40 promising |
| v5 | 300 mm | R50 | 300/R50 selected as best compromise |
| v6b | 300 mm | R50 | Retained through directivity optimization |

---

## Current dimensions

| Parameter | Value |
|---|---|
| External width | 300 mm |
| External depth | 370 mm |
| External height | 1080 mm |
| Material | 22 mm birch plywood |
| Front edge roundovers | R50 (vertical edges) |
| Rear/other edges | R20-R30 or chamfers (TBD) |

---

## Cabinet width: 300 mm

The 300 mm wide front baffle was selected in v5 (DD-007) as the best compromise between:

- **Directivity:** A narrower baffle reduces baffle diffraction effects at high frequencies. 280 mm was investigated but showed only small additional benefits over 300 mm.
- **Diffraction:** The R50 roundovers on the 300 mm baffle smooth diffraction more than was achievable on the narrower 280 mm version with practical roundover radii.
- **Mechanical fit:** 300 mm provides enough width for the waveguide (WG212) and the woofer cutouts while leaving adequate material for the box sides and bracing.
- **Cabinet volume:** 300 mm provides more internal volume than 280 mm, easing the 69 L bass chamber requirement.
- **Visual proportion:** 300 mm is a reasonable proportion for a tall reference loudspeaker.

---

## R50 front edge roundovers

The R50 vertical front roundovers (DD-008) were selected from a comparison of R20, R30, R40, R50, and R70 radii in simplified diffraction simulation.

Larger roundovers produce smoother diffraction, reducing the diffraction ripple in the off-axis response and the predicted in-room response. R50 is a practical limit for the 300 mm wide cabinet using typical woodworking methods (router jig or router table).

The roundover applies to the vertical front edges only. The horizontal top and bottom edges may use smaller roundovers or chamfers depending on the mechanical construction.

---

## Driver placement

### Tweeter / waveguide

The WG212 waveguide is mounted at the top of the driver array on the front baffle. The tweeter dome center is approximately 140 mm above the midrange center.

Exact height from the cabinet top is to be determined from the final front baffle layout, with the waveguide centered as close to the top as practical while leaving adequate material above the cutout.

### Midrange

The ScanSpeak 15W is mounted directly below the WG212. The center-to-center spacing to the tweeter is 140 mm (design target).

The midrange operates in a dedicated sealed chamber (see Chapter 9: Volume calculations).

### Woofers

Two GRS 8SW-4HE-8 woofers are side-mounted in a push-push configuration, opposed
at the same height on the two side panels (directly across from each other — see
Chapter 8). The current placement targets:

- Both woofer centers: approximately 520 mm from the cabinet bottom (nominal;
  same height on both sides)

This height is subject to revision based on:
- Internal bracing layout
- Mid chamber boundaries
- The coupling block between the opposed magnets (push-push symmetry)

---

## Material: 22 mm birch plywood

22 mm Baltic birch plywood is the primary structural material. It offers:

- Consistent density and stiffness compared with MDF
- Good screw retention for threaded inserts
- Manageable weight
- Better moisture resistance than MDF
- Suitability for CNC or hand cutting

The front baffle may use a double layer (44 mm) around the driver cutouts for driver mounting depth and rigidity, depending on the final design.

---

## Front baffle layout

The front baffle must accommodate:

- WG212 waveguide cutout
- ScanSpeak 15W midrange cutout
- R50 vertical front edge roundovers
- 140 mm c-c spacing between WG212 and 15W centers
- Adequate wood remaining between cutouts and edges for structural integrity

The mechanical tightness of this layout is a known constraint (DD-011). The waveguide flange and midrange recess must be designed together.

---

## Internal layout

| Region | Contents |
|---|---|
| Upper section | Mid chamber (5.7 L sealed) |
| Main bass chamber | Bass volume (~69 L net) |
| Woofer positions | Side walls, push-push |
| Bracing | Shelf, window, vertical (see Chapter 10) |

---

## Open items

- Finalize exact external dimensions and tolerances
- Develop full 2D front baffle layout drawing
- Verify woofer frame dimensions fit side walls
- Determine front baffle thickness (single vs. double layer)
- Confirm WG212 flange dimensions once CAD is complete
- Generate OpenSCAD or STEP cabinet model
