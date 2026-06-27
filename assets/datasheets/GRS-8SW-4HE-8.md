# GRS 8SW-4HE-8 — Woofer (Push-Push Configuration)

**Source:** [Official GRS spec sheet (PDF)](./GRS-8SW-4HE-8-spec-sheet.pdf) + Parts Express product page.

**Driver family:** GRS 8SW-4HE, 8" poly-cone subwoofer, 4 Ω.
**Role in mk2:** Dual push-push woofers (two units, opposed mounting for cabinet symmetry).

---

## Thiele-Small parameters (from official spec sheet)

| Parameter | Value | Unit | Use |
|---|---|---|---|
| Impedance (Re) | 3.8 | Ω | amplifier match |
| Inductance (Le) | 0.8 | mH | — |
| Resonance (Fs) | 48 | Hz | sealed/ported box sim, HPF design |
| Mechanical Q (Qms) | 4.33 | — | damping, box tuning |
| Electrical Q (Qes) | 1.13 | — | damping, box tuning |
| Total Q (Qts) | 0.89 | — | sealed box design |
| Moving mass (Mms) | 33.2 | g | — |
| Compliance (Cms) | 0.33 | mm/N | — |
| Effective cone area (Sd) | 216.8 | cm² | displacement, SPL calcs |
| Displacement volume (Vd) | 130 | cm³ | — |
| Force factor (BL) | 5.8 | T·m | motor strength |
| Equivalent volume (Vas) | 22 | L | sealed box sizing |
| Maximum excursion (Xmax) | 6 | mm | linear travel limit |
| Voice coil diameter | 38 | mm | — |

---

## Mechanical dimensions

| Parameter | Value | Tolerance | Symbol / use in SCAD | Notes |
|---|---|---|---|---|
| Cone diameter | 8" (203.2 mm) | — | — | nominal size |
| Baffle cutout diameter | **185 mm** | — | `woofer_cut_d` | from cabinet.scad; verify against physical unit or drawing |
| Voice coil diameter | 38 mm | — | — | from spec sheet |

> **Source-of-truth:** T-S parameters from official GRS spec sheet. Mechanical drawing dimensions not clearly extracted from PDF (embedded fonts). Baffle cutout (185 mm) is currently hardcoded in `cabinet.scad` — **needs verification** against the physical unit or official drawing.

---

## Open items / TODO

- [ ] **Mechanical drawing extraction** — PDF text extraction failed due to embedded fonts. Need to:
  - either manually extract dimensions from the PDF (visual inspection of the drawing), OR
  - caliper-verify against a physical unit once received.

- [ ] **Baffle cutout diameter (`woofer_cut_d`)** — currently hardcoded at **185 mm** in `cabinet.scad`. **Action:** verify against the official drawing or physical unit. Update `cabinet.scad` to source from this file.

- [ ] **Cabinet.scad integration** — add `woofer_*` module constants (cut_d, mounting dims if applicable) sourced from this file. Currently:
  - `woofer_cut_d = 185` is hardcoded in cabinet.scad (no source).
  - No other woofer dimensions exposed.

- [ ] **STEP / 3D model file** — GRS does not publish STEP files for this model. Either model manually from the mechanical drawing or caliper-verify the physical unit.

---

## Source files in this repo

- PDF: `assets/datasheets/GRS-8SW-4HE-8-spec-sheet.pdf` (721 KB, official GRS spec sheet from Parts Express)
- Markdown reference: `assets/datasheets/GRS-8SW-4HE-8.md` (this file)
- SCAD integration: pending (see TODO above)
