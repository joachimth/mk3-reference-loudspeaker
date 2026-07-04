# Parts — Mk3 Reference Loudspeaker

All quantities and prices are **per pair** unless noted otherwise.
Prices are indicative (sourced June 2026); verify before ordering.

---

## Drivers

| Part | Qty/pair | Unit price | Supplier | Notes |
|---|---|---|---|---|
| GRS 8SW-4HE-8 (8" woofer) | 4 | ~€45 | Parts-Express | 2 per enclosure, push-push |
| ScanSpeak 15W/4434G00 (midrange) | 2 | ~€120 | Scan-Speak / Hifi-Skabet | — |
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

Approximate external dimensions (v7): **300 × 370 × 1080 mm**, 22 mm walls, R50 front roundovers.

## Electronics / DSP

**MiniDSP 4×10 HD** selected as DSP platform for initial prototyping. USB/optical in, 10 outputs, well-documented with REW export. Pre-built XML config available (see DSP Filter Plan below).

## DSP Filter Plan (v7 target)

| Driver path | Filters |
|---|---|
| Woofer (×2) | Subsonic HP ~18 Hz LR4, Linkwitz Transform (Fc ~28 Hz, Q 0.71), LP 150 Hz LR4, polarity/delay |
| Midrange | HP 150 Hz LR4, LP 1100 Hz LR4, delay |
| Tweeter | HP 1100 Hz LR4, level trim ~-1.8 dB, delay |

**Note:** 1100 Hz crossover frequency is **unconfirmed** — depends on SB26STAC distortion measurement in the waveguide. If distortion is too high, raise to 1300-1500 Hz. Pre-built MiniDSP XML config: `dsp-configs/mk3-sb26stac-1100hz.xml`.

## Open Items

- [ ] Caliper-verify SB26STAC-C000-4 dimensions → update `cad/waveguide.scad`
- [ ] Print SB26STAC waveguide prototype → fit-check against SB26STAC and 15W/4434G00
- [ ] Measure SB26STAC distortion at 1100 Hz → confirm or adjust crossover
- [ ] Confirm actual c-c spacing (nominal 140 mm; expect ~150-155 mm from physical parts)
- [ ] Finalize cut list from CAD model before ordering sheet material
