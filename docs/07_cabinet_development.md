# Chapter 7 - Cabinet Development

---

## Design history

The cabinet geometry was developed iteratively across the early concept versions.

| Width | Roundover | Notes |
|---|---|---|
| Initial concept | - | Active 3-way with push-push woofers |
| 280 mm | R20-R40 | Narrower baffle explored, R40 promising |
| 300 mm | R50 | 300/R50 selected as best compromise (DD-007) |
| 320 mm | R19 | Current v9 cabinet — width increased for 12SW magnet clearance |

---

## Current dimensions

| Parameter | Value |
|---|---|
| External width | 320 mm |
| External depth | 380 mm |
| External height | 1180 mm |
| Material | 22 mm birch plywood |
| Front edge roundovers | R19 (vertical edges) |
| Rear/other edges | R20-R30 or chamfers (TBD) |

---

## Cabinet width: 320 mm

The 320 mm wide front baffle is the current v9 cabinet width. Originally 300 mm
was selected (DD-007) as the best compromise, but the width was increased to
320 mm to provide adequate clearance for the opposed GRS 12SW-4HE magnets (only
~4 mm gap at 276 mm internal width with 300 mm external). The 320 mm width gives
276 mm + 2×9 mm = improved internal clearance.

The 320 mm width is the best compromise between:

- **Directivity:** A narrower baffle reduces baffle diffraction effects at high frequencies. 280 mm was investigated but showed only small additional benefits over 300 mm (the original DD-007 width).
- **Diffraction:** The R19 roundovers on the 320 mm baffle smooth diffraction more than was achievable on the narrower 280 mm version with practical roundover radii.
- **Mechanical fit:** 320 mm provides enough width for the waveguide and the woofer cutouts while leaving adequate material for the box sides and bracing.
- **Cabinet volume:** 320 mm provides more internal volume than 280 mm, easing the ~65 L bass chamber requirement (volume under the divider plate).
- **Visual proportion:** 320 mm is a reasonable proportion for a tall reference loudspeaker.

---

## R50 front edge roundovers

The R19 vertical front roundovers (revised from R50 in v9 — see DD-016 and
CHANGELOG) were selected from a comparison of R20, R30, R40, R50, and R70 radii in simplified diffraction simulation.

Larger roundovers produce smoother diffraction, reducing the diffraction ripple in the off-axis response and the predicted in-room response. R19 is a practical radius for the 320 mm wide cabinet using typical woodworking methods (router jig or router table).

The roundover applies to the vertical front edges only. The horizontal top and bottom edges may use smaller roundovers or chamfers depending on the mechanical construction.

---

## Driver placement

### Tweeter / waveguide

The waveguide is mounted at the top of the driver array on the front baffle. The tweeter dome center is approximately 140 mm above the midrange center.

Exact height from the cabinet top is to be determined from the final front baffle layout, with the waveguide centered as close to the top as practical while leaving adequate material above the cutout.

### Midrange

The ScanSpeak 18W/4424G00 is mounted directly below the waveguide. The center-to-center spacing to the tweeter is 165 mm (DD-016, physical minimum with these flanges).

The midrange operates in a dedicated sealed chamber (see Chapter 9: Volume calculations).

### Woofers

Two GRS 12SW-4HE woofers (12" high excursion) are side-mounted in a push-push
configuration, opposed at the same height on the two side panels (directly across
from each other — see Chapter 8). The current placement targets:

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

- Waveguide cutout
- ScanSpeak 18W/4424G00 midrange cutout
- R19 vertical front edge roundovers
- 165 mm c-c spacing between waveguide and 18W centers (DD-016)
- Adequate wood remaining between cutouts and edges for structural integrity

The mechanical tightness of this layout is a known constraint (DD-011). The waveguide flange and midrange recess must be designed together.

---

## Internal layout

| Region | Contents |
|---|---|
| Upper section | Mid chamber (~11 L sealed, 18W/4424G00) |
| Main bass chamber | Bass volume (~65 L net, under divider plate) |
| Woofer positions | Side walls, push-push |
| Bracing | Shelf, window, vertical (see Chapter 10) |

---

## Open items

- Finalize exact external dimensions and tolerances
- Develop full 2D front baffle layout drawing
- Verify woofer frame dimensions fit side walls
- Determine front baffle thickness (single vs. double layer)
- Confirm waveguide flange dimensions once CAD is complete
- Generate OpenSCAD or STEP cabinet model
