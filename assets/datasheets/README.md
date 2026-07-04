# Datasheets

Official manufacturer datasheets and 3D CAD files for the drivers used in the Mk3 Reference Loudspeaker.

All frequency response and impedance curves have been extracted from the PDFs into machine-readable CSV files. See `DATASHEET_EXTRACTION_PLAN.md` in the repo root for the extraction methodology.

---

## Driver summary

| Driver | Role | PDF | .md | Freq CSV | Imp CSV | Params CSV | Method |
|---|---|---|---|---|---|---|---|
| SB Acoustics SB26STAC-C000-4 | Tweeter | YES | [SB26STAC-C000-4.md](SB26STAC-C000-4.md) | YES | NO | YES | Raster |
| ScanSpeak 15W/4434G00 | Midrange | YES | [15W-4434G00.md](15W-4434G00.md) | YES | YES | YES | Raster |
| GRS 12SW-4HE | Woofer (push-push, v8) | YES | — | — | — | — | — |
| GRS 8SW-4HE-8 | Woofer (historical, v3–v7) | YES | [GRS-8SW-4HE-8.md](GRS-8SW-4HE-8.md) | YES | YES | YES | Vector |

---

## SB Acoustics SB26STAC-C000-4 — Tweeter

| File | What it is |
|---|---|
| [SB26STAC-C000-4.pdf](SB26STAC-C000-4.pdf) | Official SB Acoustics datasheet (731 KB) |
| [SB26STAC-C000-4.md](SB26STAC-C000-4.md) | Full datasheet reference with extracted curves |
| [SB26STAC-C000-4_freq_response.csv](SB26STAC-C000-4_freq_response.csv) | On-axis + 30° + 60° off-axis SPL (1/12 octave, 100-40k Hz) |
| [SB26STAC-C000-4_params.csv](SB26STAC-C000-4_params.csv) | All T-S + mechanical parameters |
| [SB26STAC-C000-4_extraction_verify.png](SB26STAC-C000-4_extraction_verify.png) | Verification plot |

**Key dimensions:** Faceplate ~ø100, BCD ø88.5, no horn throat. Fs=750 Hz, sensitivity 91.5 dB, Xmax 0.6 mm.

**No STEP file from SB Acoustics** — all dimensions must be caliper-verified on a physical unit. Impedance can be modeled from T-S parameters (no impedance plot in datasheet).

---

## ScanSpeak 15W/4434G00 — Midrange

| File | What it is |
|---|---|
| [15W-4434G00.pdf](15W-4434G00.pdf) | Official ScanSpeak datasheet (319 KB) |
| [15W-4434G00.md](15W-4434G00.md) | Full datasheet reference with extracted curves |
| [15W-4434G00_freq_response.csv](15W-4434G00_freq_response.csv) | On-axis + 2 off-axis SPL (1/12 octave, 100-10k Hz) |
| [15W-4434G00_impedance.csv](15W-4434G00_impedance.csv) | Impedance (1/12 octave, 100-10k Hz) |
| [15W-4434G00_params.csv](15W-4434G00_params.csv) | All T-S + mechanical parameters |
| [15W-4434G00_extraction_verify.png](15W-4434G00_extraction_verify.png) | Verification plot |

**Key dimensions:** Faceplate ø104, BCD ø95, rear cutout ø72. Fs=43 Hz, sensitivity 89.5 dB. No STEP file (Discovery series).

---

## GRS 12SW-4HE — Woofer (Push-Push, v8)

| File | What it is |
|---|---|
| [GRS-12SW-4HE.pdf](GRS-12SW-4HE.pdf) | Official GRS spec sheet |

**Key parameters:** Fs=22 Hz, Qts=0.43, Vas=80.4 L, Sd=504 cm², Xmax=12.5 mm (Klippel verified), Bl=16.2 Tm, sensitivity 84.5 dB, 250 W, 4 Ω. Baffle cutout 284 mm. No STEP file from GRS.

Frequency response / impedance / T/S params CSV extraction pending (spec sheet uses embedded custom fonts that block text extraction — see `DATASHEET_EXTRACTION_PLAN.md`).

---

## GRS 8SW-4HE-8 — Woofer (Historical, v3–v7, superseded by 12SW)

| File | What it is |
|---|---|
| [GRS-8SW-4HE-8-spec-sheet.pdf](GRS-8SW-4HE-8-spec-sheet.pdf) | Official GRS spec sheet (721 KB) |
| [GRS-8SW-4HE-8.md](GRS-8SW-4HE-8.md) | Full datasheet reference with extracted curves |
| [GRS-8SW-4HE-8_freq_response.csv](GRS-8SW-4HE-8_freq_response.csv) | On-axis SPL (1/12 octave, 20-10k Hz) |
| [GRS-8SW-4HE-8_impedance.csv](GRS-8SW-4HE-8_impedance.csv) | Impedance + phase (1/12 octave, 20-20k Hz) |
| [GRS-8SW-4HE-8_params.csv](GRS-8SW-4HE-8_params.csv) | All T-S parameters |
| [GRS-8SW-4HE-8_extraction_verify.png](GRS-8SW-4HE-8_extraction_verify.png) | Verification plot |

**Key parameters:** Fs=48 Hz, Qts=0.89, Vas=22 L, Xmax=6 mm, sensitivity 89 dB. Baffle cutout 185 mm. No STEP file from GRS. **Superseded by GRS 12SW-4HE in v8** — retained for historical comparison.

---

## CSV format

All frequency-domain CSVs use 1/12 octave log-spaced frequency grid (20 Hz to 20 kHz, or as available from datasheet). See `DATASHEET_EXTRACTION_PLAN.md` for full format specification.

Extraction script: `scripts/extract_datasheet.py`
