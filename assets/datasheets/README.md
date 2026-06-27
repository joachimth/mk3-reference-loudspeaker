# Datasheets

Official manufacturer datasheets and 3D CAD files for the drivers used in the Mk2 Reference Loudspeaker.

---

## ScanSpeak H2606/920000 — Tweeter

| File | What it is |
|---|---|
| [H2606-920000.pdf](H2606-920000.pdf) | Official ScanSpeak datasheet (updated May 18, 2020). T-S parameters, frequency response, mounting drawing. |
| [H2606-920000-drawing.png](H2606-920000-drawing.png) | Mounting dimension drawing extracted from datasheet. |
| [H2606-920000.STEP](H2606-920000.STEP) | Official ScanSpeak 3D CAD model (STEP AP203, dated Oct 22 2020). Use for waveguide throat verification and baffle layout. |
| [H2606-920000.IGS](H2606-920000.IGS) | IGES version of the same 3D model. |
| [H2606-920000.x_t](H2606-920000.x_t) | Parasolid version of the same 3D model. |

### Key mounting dimensions (from drawing + STEP)

| Dimension | Value | Source | Used in SCAD |
|---|---|---|---|
| Faceplate OD | ø104 ±0.2 mm | Drawing | `tw_face_d = 104.0` |
| Mounting pitch circle (BCD) | ø95 ±0.1 mm | Drawing | `tw_bcd = 95.0` |
| Mounting screw holes | ø4 ±0.10 mm × 4 at 90° | Drawing | `tw_hole_d = 4.0` |
| Faceplate thickness | 4 mm | Drawing | `tw_fp_recess = 4` |
| Total depth | 45.1 mm | Drawing | reference only |
| Baffle cutout (direct mount) | ø72 mm | Drawing | note in SCAD |
| **Horn exit diameter** | **ø33.0 mm** | **STEP** (r=16.5 at Y=44.09 mm) | **`throat_d = 33`** |

### Horn exit — derivation from STEP

The H2606/920000 has a built-in horn in its faceplate. The dome effective diameter is 26 mm; the horn expands to **ø33.0 mm** at the front face of the faceplate. This was extracted from the STEP file by finding all circular features at Y=44.09 mm (the front face region, ~1 mm behind the mounting face at Y=45.1 mm): the unique small-radius circle at that level is r=16.5 mm → **d=33.0 mm**.

The WG212 waveguide in `cad/mk2_waveguide_os.scad` is therefore an **extension waveguide**: it starts at the H2606's horn exit (ø33 mm) and continues the oblate-spheroid expansion to the full ~293 × 174 mm mouth (echoed on render). The H2606 is not mounted directly to the baffle; it mounts to the rear plate of the WG212.

**Verify with calipers** on the physical tweeter before printing the final waveguide. The ø33 mm is derived from CAD geometry, not a directly dimensioned drawing callout.

---

## GRS 8SW-4HE-8 — Woofer (Push-Push)

| File | What it is |
|---|---|
| [GRS-8SW-4HE-8-spec-sheet.pdf](GRS-8SW-4HE-8-spec-sheet.pdf) | Official GRS spec sheet (721 KB). T-S parameters and mechanical drawing. |
| [GRS-8SW-4HE-8.md](GRS-8SW-4HE-8.md) | Datasheet reference extracted from the PDF. Includes T-S params and open TODO items. |

**Status: PARTIAL.** PDF datasheet + T-S parameters in place. Mechanical drawing dimensions not clearly extracted from PDF (embedded fonts). Baffle cutout diameter (`woofer_cut_d` in cabinet.scad, currently hardcoded 185 mm) needs verification — see TODO in `GRS-8SW-4HE-8.md`. No STEP file available from GRS.

## ScanSpeak 15W/4434G00 — Midrange

| File | What it is |
|---|---|
| [15W-4434G00.pdf](15W-4434G00.pdf) | Official ScanSpeak datasheet (319 KB). T-S parameters and mounting drawing. |
| [15W-4434G00.md](15W-4434G00.md) | Datasheet reference extracted from the PDF + official ScanSpeak product page. Includes mechanical dims, T-S params, and open TODO items. |

**Status: PARTIAL.** PDF datasheet + dimensional reference in place. STEP file NOT available from ScanSpeak (Discovery series does not publish STEP). Baffle cutout diameter (`mid_cut_d` in cabinet.scad, currently hardcoded 124 mm) needs verification — see TODO in `15W-4434G00.md`.
