# Parts — Mk3 Reference Loudspeaker

All quantities and prices are **per pair** unless noted otherwise.
Prices are indicative (sourced June 2026); verify before ordering.

---

## Drivers

| Part | Qty/pair | Unit price | Supplier | Notes |
|---|---|---|---|---|
| GRS 12SW-4HE (12" woofer) | 4 | ~€75 | Parts-Express | 2 per enclosure, push-push. Fs 22 Hz, Qts 0.43, Vas 80.4 L, Xmax 12.5 mm (Klippel), Sd 504 cm², 250 W |
| ScanSpeak 18W/4424G00 (midrange) | 2 | ~€95 | Scan-Speak / Hifi-Skabet | v9: replaces 15W/4434G00 (DD-016). Fs 49 Hz, Qts 0.38, Vas 24.1 L, Sd 137 cm², 91 dB, 4 Ω. Parametric model `cad/midrange.scad` |
| SB Acoustics SB26STAC-C000-4 (tweeter) | 2 | ~€35 | SB Acoustics / Parts-Express | Custom waveguide, no horn loading |

## Waveguide

| Part | Qty/pair | Notes |
|---|---|---|
| SB26STAC custom waveguide | 2 | 3D print from `cad/waveguide.scad`. BCD 88.5 mm, throat 28 mm. No STEP file from SB Acoustics — caliper-verify all dimensions. |

## Cabinet

| Part | Notes |
|---|---|
| 22 mm birch plywood | ~3 sheets per cabinet (verify cut list from CAD). Standard 1220 × 2440 mm sheet. |
| PVA woodworking glue | Titebond III or equivalent |
| Wood screws + threaded inserts | For driver mounting |
| Gasket tape (closed-cell foam, 5 mm) | All driver openings |
| Damping felt/foam | Mid chamber: fully lined. Bass chamber: 50 mm rear/top/sides. |
| Terminal cup or amplifier plate cutout | Depends on DSP/amp selection |

Approximate external dimensions (v9): **320 × 400 × 1180 mm**, 22 mm walls, R19 front roundovers (see CHANGELOG v9 for why 300 mm / R50 were revised).

### Alternative material: massiv fyr bordplade (25 mm)

Jem & Fix sælger massive fyrrebordplader i 25 × 620 × 2420 mm som en potentiel kabinetalternativ.
Produkt: [Massiv bordplade i fyr — 25 mm × 62 × 242 cm](https://www.jemogfix.dk/massiv-bordplade-i-fyr-25-mm-x-62-x-242-cm/4137/9048870/)

**Implikationer ved 25 mm vs. 22 mm:**
- Indvendige mål: 270 × 350 × 1130 mm (vs. 276 × 356 × 1136 mm med 22 mm ply) — ca. 5% mindre volumen
- `cabinet.scad` skal opdateres: `wall = 25;`
- Massiv fyr er tungere og densere end krydsfinér — potentielt bedre kabinetttræ masse, men blødere overflade (dents lettere)
- Kræver grundning/oliering på alle sider inden samling (som med ply)

**Skæreliste — 5 stk. 620 × 2420 mm bordplader — ET PAR (venstre + højre):**

| Plade | Snit (bredde) | Stykke | Mål (mm) | Position på plade |
|---|---|---|---|---|
| Plade 1 | 400 mm rip | Side L (V) | 400 × 1180 | 0–1180 mm |
| Plade 1 | 400 mm rip | Side L (H) | 400 × 1180 | 1180–2360 mm |
| Plade 1 | 220 mm rip | Reserve | — | hele længden |
| Plade 2 | 400 mm rip | Side R (V) | 400 × 1180 | 0–1180 mm |
| Plade 2 | 400 mm rip | Side R (H) | 400 × 1180 | 1180–2360 mm |
| Plade 2 | 220 mm rip | Reserve | — | hele længden |
| Plade 3 | 320 mm rip | Front (V) | 320 × 1180 | 0–1180 mm |
| Plade 3 | 320 mm rip | Front (H) | 320 × 1180 | 1180–2360 mm |
| Plade 3 | 300 mm rip | Divider (V) | 270 × 350 | 0–350 mm |
| Plade 3 | 300 mm rip | Hylde 1–3 (V) | 270 × 350 | 350–1400 mm |
| Plade 4 | 320 mm rip | Bagplade (V) | 320 × 1180 | 0–1180 mm |
| Plade 4 | 320 mm rip | Bagplade (H) | 320 × 1180 | 1180–2360 mm |
| Plade 4 | 300 mm rip | Divider (H) | 270 × 350 | 0–350 mm |
| Plade 4 | 300 mm rip | Hylde 1–3 (H) | 270 × 350 | 350–1400 mm |
| Plade 5 | 320 mm rip | Toplåg (V) | 320 × 400 | 0–400 mm |
| Plade 5 | 320 mm rip | Bundplade (V) | 320 × 400 | 400–800 mm |
| Plade 5 | 320 mm rip | Toplåg (H) | 320 × 400 | 800–1200 mm |
| Plade 5 | 320 mm rip | Bundplade (H) | 320 × 400 | 1200–1600 mm |
| Plade 5 | 300 mm rip | Reserve | — | hele længden |

*Divider og hylde braces skæres til 270 mm fra de 300 mm strips (30 mm trim). Plade 5 efterlader ca. 0.9 m² reservetræ på strip A + hele strip B — velegnet til højttalerstativ, rondeller til portkanaler, mv.*

## Electronics / DSP

**MiniDSP 4×10 HD** selected as DSP platform for initial prototyping. USB/optical in, 10 outputs, well-documented with REW export. Pre-built XML config available (see DSP Filter Plan below).

## DSP Filter Plan (v9)

| Driver path | Filters |
|---|---|
| Woofer (×2) | Subsonic HP ~18 Hz LR2, Linkwitz Transform (39.0→28 Hz, Q 0.76→0.707), LP 200 Hz BW4, gain 0 dB |
| Midrange | HP 200 Hz BW4, LP 1100 Hz LR4, gain -4.0 dB |
| Tweeter | HP 1100 Hz LR4, gain -9.0 dB |

**Note:** 1100 Hz crossover frequency is **unconfirmed** — depends on SB26STAC distortion measurement in the waveguide. If distortion is too high, raise to 1300-1500 Hz. Pre-built MiniDSP XML config: `dsp-configs/mk3-v9-200-1100-bw4-lr4.xml`.

## Open Items

- [ ] Caliper-verify SB26STAC-C000-4 dimensions → update `cad/waveguide.scad`
- [ ] Caliper-verify 18W/4424G00 flange/cutout/depth → update `cad/midrange.scad`
- [ ] Print SB26STAC waveguide prototype → fit-check against SB26STAC and 18W/4424G00
- [ ] Measure SB26STAC distortion at 1100 Hz → confirm or adjust crossover
- [ ] Re-validate 1100 Hz LR4 for the 18 cm midrange cone (directivity) and 165 mm c-c (vertical lobing)
- [ ] Confirm actual c-c spacing (165 mm computed minimum; `cad/cabinet.scad` echoes it from part dimensions)
- [ ] Confirm woofer cutout diameter (284 mm per GRS 12SW-4HE datasheet) and basket depth clearance (~136 mm total) before cutting side panels
- [ ] Verify opposed 12SW magnet gap (~48 mm computed from datasheet depth at 320 mm width) and coupling block length before cutting panels
- [ ] Finalize cut list from CAD model before ordering sheet material
