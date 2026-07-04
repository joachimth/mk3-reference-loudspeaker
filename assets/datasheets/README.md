# Datasheets

Official manufacturer datasheets and 3D CAD files for the drivers used in the Mk2 Reference Loudspeaker.

All frequency response and impedance curves have been extracted from the PDFs into machine-readable CSV files. See `DATASHEET_EXTRACTION_PLAN.md` in the repo root for the extraction methodology.

---

## Driver summary

| Driver | Role | PDF | .md | Freq CSV | Imp CSV | Params CSV | Method |
|---|---|---|---|---|---|---|---|
| ScanSpeak H2606/920000 | Tweeter (primary) | YES | [H2606-920000.md](H2606-920000.md) | YES | YES | YES | Raster |
| SB Acoustics SB26STAC-C000-4 | Tweeter (fallback) | YES | [SB26STAC-C000-4.md](SB26STAC-C000-4.md) | YES | NO | YES | Raster |
| ScanSpeak 15W/4434G00 | Midrange | YES | [15W-4434G00.md](15W-4434G00.md) | YES | YES | YES | Raster |
| GRS 8SW-4HE-8 | Woofer (push-push) | YES | [GRS-8SW-4HE-8.md](GRS-8SW-4HE-8.md) | YES | YES | YES | Vector |

---

## ScanSpeak H2606/920000 — Tweeter (Primary)

| File | What it is |
|---|---|
| [H2606-920000.pdf](H2606-920000.pdf) | Official ScanSpeak datasheet (235 KB, updated May 18 2020) |
| [H2606-920000-drawing.png](H2606-920000-drawing.png) | Mounting dimension drawing extracted from datasheet |
| [H2606-920000.STEP](H2606-920000.STEP) | Official ScanSpeak 3D CAD model (STEP AP203) |
| [H2606-920000.IGS](H2606-920000.IGS) | IGES version of the same 3D model |
| [H2606-920000.x_t](H2606-920000.x_t) | Parasolid version of the same 3D model |
| [H2606-920000.md](H2606-920000.md) | Full datasheet reference with extracted curves |
| [H2606-920000_freq_response.csv](H2606-920000_freq_response.csv) | On-axis + 2 off-axis SPL (1/12 octave, 200-10k Hz) |
| [H2606-920000_impedance.csv](H2606-920000_impedance.csv) | Impedance (1/12 octave, 200-10k Hz) |
| [H2606-920000_params.csv](H2606-920000_params.csv) | All T-S + mechanical parameters |
| [H2606-920000_extraction_verify.png](H2606-920000_extraction_verify.png) | Verification plot (extracted vs original) |

**Key dimensions:** Faceplate ø104, BCD ø95, horn exit ø33 (from STEP). Fs=1030 Hz, sensitivity 95.2 dB.

---

## SB Acoustics SB26STAC-C000-4 — Tweeter (Fallback)

| File | What it is |
|---|---|
| [SB26STAC-C000-4.pdf](SB26STAC-C000-4.pdf) | Official SB Acoustics datasheet (731 KB) |
| [SB26STAC-C000-4.md](SB26STAC-C000-4.md) | Full datasheet reference with extracted curves |
| [SB26STAC-C000-4_freq_response.csv](SB26STAC-C000-4_freq_response.csv) | On-axis + 30° + 60° off-axis SPL (1/12 octave, 100-40k Hz) |
| [SB26STAC-C000-4_params.csv](SB26STAC-C000-4_params.csv) | All T-S + mechanical parameters |
| [SB26STAC-C000-4_extraction_verify.png](SB26STAC-C000-4_extraction_verify.png) | Verification plot |

**Key dimensions:** Faceplate ~ø100, BCD ø88.5, no horn throat. Fs=750 Hz, sensitivity 91.5 dB, Xmax 0.6 mm (3× H2606).

**No impedance plot in datasheet** — impedance can be modeled from T-S parameters.

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

## GRS 8SW-4HE-8 — Woofer (Push-Push)

| File | What it is |
|---|---|
| [GRS-8SW-4HE-8-spec-sheet.pdf](GRS-8SW-4HE-8-spec-sheet.pdf) | Official GRS spec sheet (721 KB) |
| [GRS-8SW-4HE-8.md](GRS-8SW-4HE-8.md) | Full datasheet reference with extracted curves |
| [GRS-8SW-4HE-8_freq_response.csv](GRS-8SW-4HE-8_freq_response.csv) | On-axis SPL (1/12 octave, 20-10k Hz) |
| [GRS-8SW-4HE-8_impedance.csv](GRS-8SW-4HE-8_impedance.csv) | Impedance + phase (1/12 octave, 20-20k Hz) |
| [GRS-8SW-4HE-8_params.csv](GRS-8SW-4HE-8_params.csv) | All T-S parameters |
| [GRS-8SW-4HE-8_extraction_verify.png](GRS-8SW-4HE-8_extraction_verify.png) | Verification plot |

**Key parameters:** Fs=48 Hz, Qts=0.89, Vas=22 L, Xmax=6 mm, sensitivity 89 dB. Baffle cutout 185 mm (needs physical verification). No STEP file from GRS.

---

## CSV format

All frequency-domain CSVs use 1/12 octave log-spaced frequency grid (20 Hz to 20 kHz, or as available from datasheet). See `DATASHEET_EXTRACTION_PLAN.md` for full format specification.

Extraction script: `scripts/extract_datasheet.py`
