# Prototype Checklist — Next Gate

## What you need to do before building the cabinet

3 steps. That's it. Do them in order.

---

## Step 1 — Print the SB26STAC waveguide

| Property | Current value | Status |
|---|---|---|
| STL source | `cad/exports/waveguide.stl` (or local: `openscad -o waveguide.stl cad/waveguide.scad`) | ✅ Ready |
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
| GRS 12SW-4HE (woofer) | ø284 mm | ⚠️ Estimate from datasheet (embedded fonts block text extraction) | ☐ Caliper on physical unit |
| ScanSpeak 18W/4424G00 (mid) | Ø144.3 mm (Ø179.2 faceplate) | From official datasheet + cad/midrange.scad | ☐ Verify anyway |
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
| 1800 Hz | < 1% | Safe upper limit |

**Why 1100 Hz specifically:** SB26STAC Fs = 750 Hz. Crossover at 1100 Hz is 350 Hz above resonance. The SB26STAC has 0.6 mm Xmax, giving +8.1 dB excursion headroom at crossover. This is a comfortable margin. If distortion is too high, raise to 1300-1500 Hz.

**Recording (note these):**
- Measured THD at 1100 Hz: _____ %
- Measured THD at 1300 Hz: _____ %
- Measured THD at 1500 Hz: _____ %
- Any audible anomalies: ___________

**After the test:**
- [ ] If 1100 Hz passes: confirm fc = 1100 Hz, update DESIGN_DECISIONS.md
- [ ] If 1100 Hz fails: update fc_mid in all simulation scripts + MiniDSP XML config
- [ ] Measure real c-c from printed waveguide flange to 18W frame — expected 165 mm (DD-016)
- [ ] Update cc_mid_tw_mm in design_versions_comparison.py + DESIGN_DECISIONS.md DD-011

---

## Then you can: start the cabinet build

The cabinet CAD is fully parametric. Once these 3 steps are done:

1. Order drivers (2× GRS, 1× 18W/4424G00, 1× SB26STAC-C000-4 per speaker)
2. DSP: MiniDSP 4×10 HD — import `mk3-v9-200-1100-bw4-lr4.xml`
3. Follow `docs/16_build_guide.md` — 10 phases, build log in `BUILD_LOG.md`
4. 22 mm birch plywood, ~4 sheets per pair

---

## CAD current state (as of July 4, 2026)

| Model | File | Notes |
|---|---|---|
| `cad/waveguide.scad` | primary | SB26STAC waveguide: BCD 88.5 mm, throat 28 mm, no horn loading. STL rendered, manifold. |
| `cad/cabinet.scad` | shared | Fully dynamic from waveguide.scad; waveguide recessed inside cabinet, baffle aperture model. Updated for GRS 12SW-4HE (284 mm cutout, ~332 mm frame, ~136 mm depth, 75 L bass under divider plate). |

**Don't cut panels from SCAD outputs until parts are physically verified.**

---

## Quick reference — key dimensions

| Item | Value |
|---|---|
| Cabinet W×D×H | 320 × 380 × 1180 mm (22 mm birch ply) |
| Woofer (each) | GRS 12SW-4HE, 4 Ω, 12" high excursion, side-mounted push-push |
| Woofer centers | ~520 mm from bottom, opposed at same height |
| Midrange | ScanSpeak 18W/4424G00, 4 Ω |
| Tweeter | SB Acoustics SB26STAC-C000-4 in custom waveguide |
| Mid/tweeter c-c | 165 mm (physical minimum with 18W faceplate — verify from real parts, DD-016) |
| Bass crossover | 200 Hz BW4 |
| Mid/tweeter crossover | 1100 Hz LR4 (unconfirmed — Step 3) |
| FR roundovers | R19 on cabinet front vertical edges |
| DSP | MiniDSP 4×10 HD |
