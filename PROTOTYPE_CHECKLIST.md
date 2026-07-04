# Prototype Checklist — Next Gate

## What you need to do before building the cabinet

3 steps. That's it. Do them in order.

---

## Step 1 — Print the SB26STAC waveguide

| Property | Current value | Status |
|---|---|---|
| STL source | `cad/exports/sb26stac/waveguide_sb26stac.stl` (or local: `openscad -o wg_sb26stac.stl cad/waveguide.scad`) | ✅ Ready |
| Material | PETG recommended | |
| Orientation | Print flat — flange down, throat up | |
| Post-print | Slow cool to avoid warping | |

**Known dimensions (do NOT change without measurement):**

| Dimension | Value | Source | Caliper verify? |
|---|---|---|---|
| Throat diameter | ø28 mm (dome + surround) | SB26STAC datasheet + SCAD | ☐ |
| BCD (screw circle) | ø88.5 mm | SCAD (SB26STAC faceplate) | ☐ |
| Mouth size (H×V) | from SCAD echo | SCAD | |
| Total depth | from SCAD | SCAD | |
| Flange (W×H) | from SCAD | SCAD | |

### SB26STAC tweeter mounting — verify before bonding

| Dimension | Expected | Check with caliper | Pass? |
|---|---|---|---|
| Faceplate OD | ~100 mm | ☐ Measure from physical unit | ☐ |
| Screw hole BCD | ø88.5 mm | ☐ Centre-to-centre across | ☐ |
| Throat through-hole | ø28 mm — dome + surround must sit fully inside bore | ☐ Visual check after test-fit | ☐ |
| Recess depth | from datasheet | ☐ | ☐ |

> **Note:** SB26STAC-C000-4 has no STEP file from SB Acoustics. All dimensions are from the PDF datasheet and must be caliper-verified before committing to a print.

### Baffle mounting holes — verify before drilling

| Dimension | Expected | Check | Pass? |
|---|---|---|---|
| BCD x | from SCAD | ☐ | ☐ |
| BCD y | from SCAD | ☐ | ☐ |
| Screw diameter | from datasheet | ☐ | ☐ |

---

## Step 2 — Confirm driver cutout diameters from real parts

**These are still estimates — confirm from physical driver before cutting baffle.**

| Driver | Cutout diameter | Status | Verify from |
|---|---|---|---|
| GRS 8SW-4HE-8 (woofer) | ø185 mm | ⚠️ Estimate — spec sheet embedded fonts block text extraction | ☐ Caliper on physical unit |
| ScanSpeak 15W/4434G00 (mid) | ø72 mm | ✅ Corrected June 28 from 15W chassis drawing | ☐ Verify anyway |
| SB26STAC waveguide mouth (baffle aperture) | from SCAD | ✅ Auto-propagating from waveguide.scad | ☐ Measure printed part |

---

## Step 3 — Distortion test: SB26STAC at 1100 Hz

This is **the design gate**. If the SB26STAC can't do 1100 Hz with low distortion, the crossover frequency shifts up.

**Setup:**
- Mount SB26STAC in the printed waveguide
- Use a solid baffle (cardboard or ply test panel) with the waveguide aperture cut
- Measure nearfield with measurement mic (UMIK-1 or similar)
- Signal: 2.83 V sine sweep

**What to check:**

| Frequency | Acceptable THD | Action |
|---|---|---|
| 1100 Hz | < 2% | ✅ Crossover target confirmed at 1100 Hz LR4 |
| 1300 Hz | < 2% | Shift crossover up; update fc_mid in all simulation scripts |
| 1500 Hz | < 2% | Same as above |
| 1800 Hz | < 1% | Safe fallback position |

**Why 1100 Hz specifically:** SB26STAC Fs = 750 Hz. Crossover at 1100 Hz is 350 Hz above resonance. The SB26STAC has 0.6 mm Xmax, giving +8.1 dB excursion headroom at crossover. This is a comfortable margin. If distortion is too high, raise to 1300-1500 Hz.

**Recording (note these):**
- Measured THD at 1100 Hz: _____ %
- Measured THD at 1300 Hz: _____ %
- Measured THD at 1500 Hz: _____ %
- Any audible anomalies: ___________

**After the test:**
- [ ] If 1100 Hz passes: confirm fc = 1100 Hz, update DESIGN_DECISIONS.md
- [ ] If 1100 Hz fails: update fc_mid in all simulation scripts + MiniDSP XML config
- [ ] Measure real c-c from printed waveguide flange to 15W frame — expected 150-155 mm (not 140 mm)
- [ ] Update cc_mid_tw_mm in design_versions_comparison.py + DESIGN_DECISIONS.md DD-011

---

## Then you can: start the cabinet build

The cabinet CAD is fully parametric. Once these 3 steps are done:

1. Order drivers (2× GRS, 1× 15W, 1× SB26STAC-C000-4 per speaker)
2. DSP: MiniDSP 4×10 HD — import `mk3-sb26stac-1100hz.xml`
3. Follow `docs/16_build_guide.md` — 10 phases, build log in `BUILD_LOG.md`
4. 22 mm birch plywood, ~4 sheets per pair

---

## CAD current state (as of July 4, 2026)

| Model | File | Notes |
|---|---|---|
| `cad/waveguide.scad` | primary | SB26STAC waveguide: BCD 88.5 mm, throat 28 mm, no horn loading. STL rendered, manifold. |
| `cad/cabinet.scad` | shared | Fully dynamic from waveguide.scad; waveguide recessed inside cabinet, baffle aperture model. |

**Don't cut panels from SCAD outputs until parts are physically verified.**

---

## Quick reference — key dimensions

| Item | Value |
|---|---|
| Cabinet W×D×H | 300 × 370 × 1080 mm (22 mm birch ply) |
| Woofer (each) | GRS 8SW-4HE-8, 8 Ω, side-mounted push-push |
| Woofer centers | ~520 mm from bottom, opposed at same height |
| Midrange | ScanSpeak 15W/4434G00, 8 Ω |
| Tweeter | SB Acoustics SB26STAC-C000-4 in custom waveguide |
| Mid/tweeter c-c | Target 140 mm, expected 150-155 mm (verify from real parts) |
| Bass crossover | 150 Hz LR4 |
| Mid/tweeter crossover | 1100 Hz LR4 (unconfirmed — Step 3) |
| FR roundovers | R50 on cabinet front vertical edges |
| DSP | MiniDSP 4×10 HD |
