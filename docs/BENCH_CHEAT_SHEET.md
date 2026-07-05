# Mk3 Reference Loudspeaker — Bench Cheat Sheet

> Print this (one page). Keep it at the workbench or next to the MiniDSP plugin.

---

## System Overview

| Item | Value |
|---|---|
| **Design** | Active DSP 3-way, sealed, push-push woofers |
| **Cabinet width** | 300 mm |
| **Bass volume** | ~75 L (under divider plate) |
| **Front roundovers** | R50 mm vertical edges |

---

## Drivers

| Band | Driver | Quantity | Sensitivity | Notes |
|---|---|---|---|---|
| **Woofer** | GRS 12SW-4HE | 2 (push-push) | 84.5 dB | 12" high excursion, Fs 22 Hz, Xmax 12.5 mm |
| **Mid** | ScanSpeak 15W/4434G00 | 1 | 89.7 dB | Discovery series, 5" |
| **Tweeter** | SB Acoustics SB26STAC-C000-4 | 1 | 91.5 dB | Conventional dome, Fs 750 Hz, waveguide-mounted |

---

## Crossover

| Band | Frequency | Slope |
|---|---|---|
| Bass → Mid | **150 Hz** | LR4 (24 dB/oct) |
| Mid → Tweeter | **1100 Hz** | LR4 (24 dB/oct) |

### Why 1100 Hz
- SB26STAC Fs is 750 Hz — 350 Hz margin, no distortion gate needed.
- 1100 Hz is below the broadside null for ~150 mm c-c spacing (1147 Hz).
- Optimisation sweep scored 8.1/10 at this point.

### Wiring
- **Woofers:** wired in **series** → 8 Ω load per side
- Mid: single driver
- Tweeter: single driver
- **Level trim:** tweeter ~-1.8 dB DSP pad (91.5 dB → ~89.7 dB match to mid)

---

## Critical Dimensions

| Dimension | Value | Verified? |
|---|---|---|
| Mid/tweeter c-c spacing | **~150-160 mm** (realistic target; 140 mm ideal if D-flange waveguide) | [ ] |
| Tweeter waveguide throat | **28 mm** (SB26STAC dome + surround) | [ ] |
| Waveguide mouth | **~212 mm** | [ ] |
| Waveguide BCD | **88.5 mm** (3-hole, M3 or M4) | [ ] |
| 15W cutout | Ø118 mm | [ ] |
| 12SW cutout | Ø284 mm | [ ] |
| Cabinet internal width | 276 mm (300 - 2×12 mm sides) | [ ] |
| Opposed woofer magnet clearance | ~4 mm @ 276 mm internal width | [ ] ⚠️ |

> ⚠️ **Verify 12SW magnet clearance with physical driver before cutting panels.**
> Coupling block: h=20 mm, r=55 mm. Basket profile must be checked against a real
> 12SW. If the gap is too tight, increase cabinet width to 320 mm.

---

## DSP Chain (per channel)

```
Input → Subsonic HP 18 Hz LR4 → Linkwitz Transform → Crossover → Output
```

### Linkwitz Transform (12SW in ~75 L sealed)

| Parameter | Before LT | After LT |
|---|---|---|
| Fc | 39.0 Hz | 28 Hz |
| Qtc | 0.76 | 0.707 |

### Delay Estimates (for MiniDSP alignment)

| Driver | Estimated delay | Notes |
|---|---|---|
| Woofer | 0 µs | Reference point |
| Mid | ~0.4-0.6 ms | Acoustic center ~15-20 cm behind woofer |
| Tweeter | ~0.2-0.4 ms | Waveguide mouth behind mid, but smaller depth |

> Measure with REW timing reference for exact values.

---

## Verification Steps (in order)

- [ ] **1. Print waveguide** — verify throat (28 mm), BCD (88.5 mm), mouth (212 mm) with calipers
- [ ] **2. SB26STAC distortion test** — 1100 Hz, 96 dB. Target: ≤2% THD. If >3%, rethink XO
- [ ] **3. Measure T/S on 12SW** — verify actual Fs, Qts, Vas against datasheet
- [ ] **4. Mock up magnet clearance** — cut cardboard templates from STEP, check opposed gap
- [ ] **5. Full cabinet** — build, mount drivers, seal, wire series
- [ ] **6. DSP load** — import `mk3-sb26stac-1100hz.xml` → upload to MiniDSP
- [ ] **7. Nearfield measurements** — each driver individually with REW
- [ ] **8. Gated measurements** — quasi-anechoic at 1 m, full system
- [ ] **9. Iterate** — adjust delay, level, PEQ based on measured response

---

## Cabinet Construction Notes

- **12SW cutout:** 284 mm — significantly larger than the old 8SW (185 mm)
- **Bracing:** new angle divider plate (12°) in cad/ — reduces internal reflections
- **Vertical braces** added to all panels in cad/
- **Ideal panel material:** 24 mm plywood (18 mm minimum + 3 mm laminate)
- **Internal volume:** target ~75 L under divider plate after deducting braces

---

## Tooling Reference

| Tool | Purpose |
|---|---|
| **MiniDSP 4×10 HD** | Active crossover, EQ, delay |
| **REW** | Measurements, gating, distortion, timing |
| **OpenSCAD + cad/** | Waveguide profile, cabinet model, STL export |
| **dsp-configs/generate_minidsp_xml.py** | Regenerate MiniDSP XML (modify freq/gain/delay) |
| **dsp-configs/generate_biquads.py** | Regenerate biquad coefficients |

---

## Quick Links

| File | What it covers |
|---|---|
| `DESIGN_DECISIONS.md` | All DD entries with rationale |
| `docs/07_cabinet_development.md` | Cabinet design evolution |
| `docs/11_crossovers.md` | Crossover design and optimization |
| `docs/14_dsp.md` | Full DSP architecture |
| `docs/16_build_guide.md` | Assembly instructions |
| `cad/` | All CAD files (cabinet, waveguide, braces) |
| `simulations/` | Simulation scripts and outputs |
| `dsp-configs/` | MiniDSP XML configs + generators |

---

*Last updated: July 5, 2026 — v8 (12SW woofer upgrade).*
