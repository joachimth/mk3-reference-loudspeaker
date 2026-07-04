# SB Acoustics SB26STAC-C000-4 — Datasheet Reference

**Source:** [Official SB Acoustics datasheet PDF](./SB26STAC-C000-4.pdf) + mounting drawing embedded in PDF.

**Driver family:** Conventional soft dome tweeter, 26 mm fine weave fabric dome, 4 Ω.
**Role in mk2:** Alternative tweeter (mk3-sb26stac branch). Used if H2606 distortion test fails at 1250 Hz.

---

## Mechanical dimensions (from drawing in PDF)

| Parameter | Value | Tolerance | Notes |
|---|---|---|---|
| Faceplate outer diameter | **~100 mm** | ±0.35 | `Ø 100.0±0.35` on drawing |
| Baffle cutout | **88.5 mm** | — | — |
| Recess diameter | **53.0 mm** | — | recess around dome |
| Mounting BCD (4-hole) | **88.5 mm** | ±0.10 | confirmed from drawing |
| Screw holes | 4 × ø4.0 + ø8.0 counterbore | +0.20/0.00 | — |
| Total depth | **39.7 mm** | — | shallower than H2606 (45.1) |
| Net weight | 0.53 kg | — | — |

> **No horn throat.** The SB26STAC is a conventional flush-mount dome. Unlike the H2606 (ø33 mm horn exit), it has no horn to couple to the WG212 waveguide. Using it requires a complete waveguide redesign (see `cad/mk2_waveguide_sb26stac.scad`).

---

## Thiele-Small parameters

| Parameter | Value | Unit | Use |
|---|---|---|---|
| Impedance | 4 | Ω | nominal |
| Re (DC resistance) | 3.2 | Ω | amplifier match |
| Fs (resonance) | **750 Hz** | Hz | **500 Hz margin at 1250 Hz crossover** |
| Sensitivity (2.83V/1m) | 91.5 | dB | 3.7 dB below H2606 |
| Le (inductance) | 0.04 | mH | — |
| Sd (effective dome area) | 6.2 | cm² | slightly larger than H2606 |
| Xmax (linear travel, p-p) | **1.2 mm (0.6 one-way)** | mm | **3× more than H2606 (0.2 mm)** |
| Qms | 3.0 | — | taller, broader resonance |
| Qes | 1.78 | — | — |
| Qts | 1.12 | — | less damped than H2606 (0.70) |
| Bl (force factor) | 1.6 | T·m | half of H2606 (3.3) |
| Mms | 0.3 | g | — |
| Power (RMS) | 120 | W | tested at 2600 Hz, IEC 268-5 |
| Ferrofluid | No | — | H2606 has ferrofluid |

Full parameter table: `SB26STAC-C000-4_params.csv`

---

## Frequency response (extracted from datasheet)

On-axis + 30° off-axis + 60° off-axis SPL, measured at 2.83V/1m on IEC baffle (mic distance 31.6 cm).
Data extracted from embedded JPEG image in PDF.

| Frequency | On-axis | 30° off-axis | 60° off-axis |
|---|---|---|---|
| 100 Hz | ~52 dB | ~57 dB | ~55 dB |
| 500 Hz | ~75 dB | ~78 dB | ~76 dB |
| 1 kHz | ~88 dB | ~88 dB | ~85 dB |
| 2 kHz | ~92 dB | ~92 dB | ~90 dB |
| 5 kHz | ~92 dB | ~90 dB | ~85 dB |
| 10 kHz | ~91 dB | ~87 dB | ~78 dB |
| 20 kHz | ~88 dB | ~80 dB | ~65 dB |
| 40 kHz | ~75 dB | ~60 dB | ~52 dB |

Full curves: `SB26STAC-C000-4_freq_response.csv` (1/12 octave resolution, 100-40000 Hz, 3 curves)

## Impedance

> **Not available in datasheet.** The SB26STAC-C000-4 PDF contains only a frequency response plot, not a separate impedance/phase graph. Impedance can be modeled from T-S parameters (Re=3.2 Ω, Fs=750 Hz, Qes=1.78, Qms=3.0, Le=0.04 mH).

---

## Comparison with H2606/920000

| Parameter | SB26STAC-C000-4 | H2606/920000 | Advantage |
|---|---|---|---|
| Fs | 750 Hz | 1030 Hz | **SB26** (more crossover margin) |
| Xmax | 0.6 mm | 0.2 mm | **SB26** (3× headroom) |
| Sensitivity | 91.5 dB | 95.2 dB | H2606 (3.7 dB louder) |
| Horn loading | No | Yes (ø33 mm) | **H2606** (waveguide coupling) |
| STEP file | No | Yes | **H2606** (CAD verification) |
| Price | ~€35-40 | ~€44 | SB26 (cheaper) |

Full analysis: `docs/SB26STAC-C000-4_analysis.md`

---

## Source files in this repo

- PDF: `assets/datasheets/SB26STAC-C000-4.pdf` (731 KB, official SB Acoustics)
- Frequency response CSV: `assets/datasheets/SB26STAC-C000-4_freq_response.csv` (on-axis + 30° + 60°, 100-40000 Hz)
- Parameters CSV: `assets/datasheets/SB26STAC-C000-4_params.csv` (all T-S + mechanical parameters)
- Verification plot: `assets/datasheets/SB26STAC-C000-4_extraction_verify.png`
- Markdown reference: `assets/datasheets/SB26STAC-C000-4.md` (this file)
- Analysis: `docs/SB26STAC-C000-4_analysis.md` (full comparison with H2606)
- Waveguide CAD: `cad/mk2_waveguide_sb26stac.scad` (alternative waveguide design)
