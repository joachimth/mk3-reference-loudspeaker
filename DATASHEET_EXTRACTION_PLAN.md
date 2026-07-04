# Datasheet Extraction Plan

**Purpose:** Ensure ALL driver data from manufacturer datasheets is extracted into the repo in a consistent, machine-readable format. This includes Thiele-Small parameters, mechanical dimensions, frequency response curves, impedance/phase curves, and off-axis responses.

**Created:** July 4, 2026

---

## 1. What gets extracted

Every driver in the project gets a datasheet folder under `assets/datasheets/` containing:

| File | Content |
|---|---|
| `<model>.pdf` | Original manufacturer PDF (binary, preserved as-is) |
| `<model>.md` | Full datasheet reference: T-S params, mechanical dims, frequency response summary, impedance summary, source provenance, open items |
| `<model>_freq_response.csv` | On-axis frequency response: `freq_hz, spl_db` |
| `<model>_impedance.csv` | Impedance + phase: `freq_hz, impedance_ohm, phase_deg` |
| `<model>_offaxis.csv` | Off-axis responses (if available): `freq_hz, spl_30deg_db, spl_60deg_db, ...` |
| `<model>_params.csv` | All Thiele-Small + mechanical parameters in key-value CSV |

If a driver has no off-axis data in its datasheet, the off-axis CSV is omitted (not created empty).

---

## 2. CSV format standard

All frequency-domain CSVs use the same structure:

```
freq_hz,<measurement_columns>
20.0,88.5
21.2,88.7
...
20000.0,72.1
```

- **Frequency column:** `freq_hz`, always first column, log-spaced at 1/12 octave (120 points per octave, ~480 points for 20-20k Hz). This gives smooth curves without excessive data.
- **SPL columns:** `spl_db` (on-axis), `spl_30deg_db`, `spl_60deg_db`, etc.
- **Impedance:** `impedance_ohm`, `phase_deg`
- **Parameters CSV:** two columns `parameter,value` with units in a third `unit` column. One row per parameter.

**Interpolation:** Raw vector data is sampled at log-spaced frequencies. Linear interpolation in log-frequency space between raw data points. Values outside the extracted range are NOT extrapolated (left as blank/NaN).

---

## 3. Extraction methods by PDF type

### 3a. Vector PDF (curve data stored as line/curve path objects)

**Detection:** PyMuPDF `page.get_drawings()` returns paths with `l` (line) or `c` (bezier) operations in colors distinct from grid lines.

**Process:**
1. Extract all drawing paths, grouped by stroke color
2. Identify data curves vs grid lines:
   - Grid lines: many short segments at regular intervals, typically gray/black thin strokes
   - Data curves: colored strokes (blue for impedance, red for phase, black/dark for SPL) with many connected segments
3. Extract axis label text with positions (`page.get_text("dict")`)
4. Calibrate coordinate mapping: PDF (x,y) → (freq, dB/ohm/deg) using axis label positions
5. Reconstruct curve by connecting line segments (match endpoints)
6. Sample at standard 1/12 octave frequencies
7. Output CSV + verification PNG

**Drivers using this method:** GRS 8SW-4HE-8, SB26STAC-C000-4

### 3b. Raster PDF (curve data stored as embedded bitmap images)

**Detection:** PyMuPDF `page.get_drawings()` returns only `re` (rectangle) operations; `page.get_images()` returns bitmap images containing the plots.

**Process:**
1. Extract embedded images using `page.get_images()` + `doc.extract_image()`
2. Identify which image is the frequency response / impedance plot
3. Use image processing:
   - Convert to HSV, threshold for curve colors (typically blue/green/red lines)
   - Extract pixel coordinates of curve points
   - Use axis label text positions (if available) or known axis ranges from datasheet text
   - Map pixel coordinates to (freq, dB/ohm)
4. Sample at standard 1/12 octave frequencies
5. Output CSV + verification PNG

**Drivers using this method:** ScanSpeak 15W/4434G00, ScanSpeak H2606/920000

**Fallback for raster PDFs:** If automated image extraction fails (low contrast, unusual colors, scanned datasheet), manually digitize key points from the datasheet image using a visual tool. Record at minimum: corner frequencies (Fs, crossover region, bandpass edges), peak/dip values, and 10-20 points per decade. Document the manual extraction in the .md file with a "Manual digitization" section.

### 3c. No PDF available (web-only datasheet)

**Process:**
1. Download the datasheet PDF or save the web page as PDF
2. Store in `assets/datasheets/`
3. Follow 3a or 3b depending on PDF type
4. If only HTML/spec table available (no frequency response graph), extract T-S params and note "No frequency response graph available from manufacturer" in the .md file

---

## 4. Coordinate calibration

For all plots, the frequency axis is **logarithmic**. The mapping from PDF x-coordinate to frequency is:

```
freq = 10^(a + b * x_pdf)
```

where `a` and `b` are determined from two known (x, freq) pairs taken from axis labels.

For linear axes (dB SPL, ohms if linear, degrees):

```
value = c + d * y_pdf
```

where `c` and `d` are determined from two known (y, value) pairs.

For log impedance axes (some datasheets plot impedance in log scale):

```
impedance = 10^(e + f * y_pdf)
```

**Calibration source:** Always use the axis label text positions from the PDF itself, not estimated values. This ensures accuracy even if the PDF was re-scaled or cropped.

---

## 5. Verification

After extraction, for every driver:
1. **Verification PNG:** Render the extracted data as a matplotlib plot overlaid on the original datasheet image. Visually confirm the curves match.
2. **Sanity checks:**
   - SPL values within 50-120 dB range
   - Impedance values within 0.1-1000 ohm range
   - Phase within -180 to +180 degrees
   - Fs (from impedance peak) matches T-S parameter Fs within 10%
   - No NaN/inf values in output
3. **Store verification plot** in `assets/datasheets/` as `<model>_extraction_verify.png`

---

## 6. When a driver is swapped or added

Follow this checklist:

- [ ] Download/store the manufacturer PDF in `assets/datasheets/`
- [ ] Run `scripts/extract_datasheet.py <pdf_path> <model_name>` (auto-detects vector vs raster)
- [ ] Review verification PNG — confirm curves match
- [ ] Create/update `<model>.md` with all extracted data (T-S params, dims, frequency response summary, provenance)
- [ ] Create/update `<model>_params.csv` with parameter table
- [ ] Update `assets/datasheets/README.md` with the new driver entry
- [ ] Update `PARTS.md` and relevant `docs/` files to reference the new datasheet data
- [ ] Update `cabinet.scad` or waveguide SCAD if mechanical dimensions changed
- [ ] Commit all new files with message: `datasheet: extract <model> full data`

If the extraction script fails on a new PDF format, follow the fallback in section 3b/3c and document the manual process.

---

## 7. File inventory (current state)

| Driver | PDF | .md | freq_response.csv | impedance.csv | offaxis.csv | params.csv | Method |
|---|---|---|---|---|---|---|---|
| GRS 8SW-4HE-8 | YES | YES (partial) | PENDING | PENDING | PENDING | PENDING | Vector |
| ScanSpeak 15W/4434G00 | YES | YES (partial) | PENDING | PENDING | NO | PENDING | Raster |
| ScanSpeak H2606/920000 | YES | NO | PENDING | PENDING | PENDING | PENDING | Raster |
| SB Acoustics SB26STAC-C000-4 | YES | NO (analysis in docs/) | PENDING | PENDING | PENDING | PENDING | Vector |

**Goal:** All PENDING → YES/extracted.
