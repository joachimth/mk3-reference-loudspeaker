# Prototype Checklist — Next Gate

## What you need to do before building the cabinet

3 steps. That's it. Do them in order.

---

## Step 1 — Print the WG212 waveguide

| Property | Current value | Status |
|---|---|---|
| STL source | CI release from `cad-render.yml` (or local: `openscad -o wg212.stl cad/mk2_waveguide_os.scad`) | ✅ Ready |
| Material | PETG recommended | |
| Orientation | Print flat — flange down, throat up | |
| Post-print | Slow cool to avoid warping | |

**Known dimensions (do NOT change without measurement):**

| Dimension | Value | Source | Caliper verify? |
|---|---|---|---|
| Throat diameter | ø33.0 mm | H2606 STEP file | ☐ |
| Mouth size (H×V) | ~293.5 x 174.4 mm | SCAD echo | |
| Total depth | 90 mm (D_os=65 + Lr=25) + 5 mm flange + 8 mm back plate | SCAD | |
| Flange (W×H) | 242 x 143 mm | SCAD | |
| Flange corner radius | 4 mm | SCAD | |
| Back plate OD | ø130 mm | SCAD | |

### H2606 tweeter mounting — verify before bonding

| Dimension | Expected | Check with caliper | Pass? |
|---|---|---|---|
| Faceplate pocket | ø104.0 ±0.2 mm, 4 mm deep | ☐ Measure depth + diameter | ☐ |
| Screw hole BCD | ø95.0 ±0.1 mm | ☐ Centre-to-centre across: 95.0 mm | ☐ |
| Screw hole diameter | ø4.0 mm | ☐ | ☐ |
| Throat through-hole | ø33.0 mm — dome must sit fully inside bore | ☐ Visual check after test-fit | ☐ |

### Baffle mounting holes — verify before drilling

| Dimension | Expected | Check | Pass? |
|---|---|---|---|
| BCD x | 212 mm | ☐ | ☐ |
| BCD y | 128 mm | ☐ | ☐ |
| Screw diameter | ø4.5 mm | ☐ | ☐ |

---

## Step 2 — Confirm driver cutout diameters from real parts

**These are still estimates — confirm from physical driver before cutting baffle.**

| Driver | Cutout diameter | Status | Verify from |
|---|---|---|---|
| GRS 8SW-4HE-8 (woofer) | ø185 mm | ⚠️ Estimate — spec sheet embedded fonts block text extraction | ☐ Caliper on physical unit |
| ScanSpeak 15W/4434G00 (mid) | ø72 mm | ✅ Corrected June 28 from 15W chassis drawing | ☐ Verify anyway |
| WG212 mouth (baffle aperture) | ~293.5 x 174.4 mm (from SCAD) | ✅ Auto-propagating from waveguide.scad | ☐ Measure printed part |

---

## Step 3 — Distortion test: H2606 at 1250 Hz

This is **the design gate**. If the H2606 can't do 1250 Hz with low distortion, the entire crossover target shifts up.

**Setup:**
- Mount H2606 in the printed WG212
- Use a solid baffle (cardboard or ply test panel) with the waveguide aperture cut
- Measure nearfield with measurement mic (UMIK-1 or similar)
- Signal: 2.83 V (1 W at 8 Ω) sine sweep

**What to check:**

| Frequency | Acceptable THD | Action |
|---|---|---|
| 1250 Hz | < 1–2% | ✅ Crossover target confirmed at 1250 Hz LR4 |
| 1350 Hz | < 1–2% | Shift crossover up; update fc_mid in all simulation scripts |
| 1450 Hz | < 1–2% | Same as above |
| 1600 Hz | < 1–2% | H2606 should be clean here — fallback position |

**Why 1250 Hz specifically:** H2606 Fs = 1030 Hz. Crossover at 1250 Hz is only 220 Hz above resonance — tight margin. LR4 filter slope (24 dB/oct) helps, but the waveguide loading may reduce excursion demand at the crossover point. If distortion is too high, the safe fallback is 1350–1450 Hz.

**Recording (note these):**
- Measured THD at 1250 Hz: _____ %
- Measured THD at 1350 Hz: _____ %
- Measured THD at 1450 Hz: _____ %
- Any audible anomalies: ___________

**After the test:**
- [ ] If 1250 Hz passes: confirm fc = 1250 Hz, update DESIGN_DECISIONS.md DD-010
- [ ] If 1250 Hz fails: update fc_mid in all 11 simulations + fc_mid_tw in system_response.py
- [ ] Measure real c-c from printed WG212 flange to 15W frame — expected 150-155 mm (not 140 mm)
- [ ] Update cc_mid_tw_mm in design_versions_comparison.py + DESIGN_DECISIONS.md DD-011

---

## Then you can: start the cabinet build

The cabinet CAD is fully parametric. Once these 3 steps are done:

1. Order drivers (2× GRS, 1× 15W, 1× H2606 per speaker)
2. Select DSP platform (MiniDSP 4×10 HD recommended)
3. Follow `docs/16_build_guide.md` — 10 phases, build log in `BUILD_LOG.md`
4. 22 mm birch plywood, ~4 sheets per pair

---

## CAD current state (as of July 1, 2026)

| Model | Latest commit | Notes |
|---|---|---|
| `cad/mk2_waveguide_os.scad` | d807ab0 | WG212: Lr=25, protrusion=0, corner_r=4, tube z=-5..85. All H2606 dims from datasheet/STEP. |
| `cad/cabinet.scad` | 0b18a30 | Fully dynamic from waveguide.scad; waveguide recessed inside cabinet, baffle aperture model. |
| `cad/mk2_cabinet_cutouts.scad` | in cabint.scad | Woofer cutout 185mm (verify!), mid cutout 72mm (confirmed), waveguide mouth auto-sized. |

Two known bugs in cabinet.scad (pre-existing, non-blocking):
- Y = 163..185 mm woofer cutout overlap calculated wrong
- Mouth cutout no-op past certain geometry

**Don't cut panels from SCAD outputs until parts are physically verified.**

---

## Quick reference — key dimensions

| Item | Value |
|---|---|
| Cabinet W×D×H | 300 × 370 × 1080 mm (22 mm birch ply) |
| Woofer (each) | GRS 8SW-4HE-8, 8 Ω, side-mounted push-push |
| Woofer centers | ~520 mm from bottom, opposed at same height |
| Midrange | ScanSpeak 15W/4434G00, 8 Ω |
| Tweeter | ScanSpeak H2606/920000 in WG212 waveguide |
| Mid/tweeter c-c | Target 140 mm, expected 150-155 mm (verify from real parts) |
| Bass crossover | 150 Hz LR4 |
| Mid/tweeter crossover | 1250 Hz LR4 (unconfirmed — Step 3) |
| FR roundovers | R50 on cabinet front vertical edges |
| DSP | MiniDSP 4×10 HD (recommended) |
