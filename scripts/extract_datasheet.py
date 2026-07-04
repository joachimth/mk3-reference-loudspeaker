#!/usr/bin/env python3
"""
Datasheet extraction tool for mk2-reference-loudspeaker.

Extracts frequency response, impedance/phase, and off-axis curves
from manufacturer PDF datasheets. Handles both vector PDFs (curve
data as path objects) and raster PDFs (curve data as embedded images).

Usage:
    python3 extract_datasheet.py <pdf_path> [--model <name>] [--raster]

Output:
    <model>_freq_response.csv
    <model>_impedance.csv
    <model>_offaxis.csv   (if off-axis data found)
    <model>_params.csv    (if T-S params extractable from text)
    <model>_extraction_verify.png

All output files are written next to the PDF.
"""

import argparse
import csv
import math
import os
import sys
from pathlib import Path

import fitz  # PyMuPDF
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Standard frequency grid: 1/12 octave, 20 Hz to 20 kHz
# ============================================================

def standard_freq_grid(fmin=20.0, fmax=20000.0, points_per_octave=12):
    """Log-spaced frequency grid."""
    n_octaves = math.log10(fmax / fmin) / math.log10(2)
    n_points = int(n_octaves * points_per_octave) + 1
    freqs = np.logspace(math.log10(fmin), math.log10(fmax), n_points)
    return freqs


def log_interp(freqs_raw, values_raw, freqs_target):
    """Linear interpolation in log-frequency space."""
    log_f_raw = np.log10(freqs_raw)
    log_f_target = np.log10(freqs_target)
    # Sort by frequency
    sort_idx = np.argsort(log_f_raw)
    log_f_raw = log_f_raw[sort_idx]
    values_raw = np.array(values_raw)[sort_idx]
    # Interpolate
    result = np.interp(log_f_target, log_f_raw, values_raw,
                       left=np.nan, right=np.nan)
    return result


# ============================================================
# Vector PDF extraction
# ============================================================

def extract_vector_segments(page):
    """Extract all line segments from a PDF page, grouped by color."""
    drawings = page.get_drawings()
    segments_by_color = {}

    for d in drawings:
        color = d.get("color")
        if color is None:
            continue
        color_key = tuple(round(c, 3) for c in color)

        for item in d["items"]:
            if item[0] == "l":  # line
                p1, p2 = item[1], item[2]
                if color_key not in segments_by_color:
                    segments_by_color[color_key] = []
                segments_by_color[color_key].append((p1.x, p1.y, p2.x, p2.y))
            elif item[0] == "c":  # bezier curve
                p1, c1, c2, p2 = item[1], item[2], item[3], item[4]
                if color_key not in segments_by_color:
                    segments_by_color[color_key] = []
                for i in range(10):
                    t1, t2 = i / 10, (i + 1) / 10
                    x1 = (1-t1)**3*p1.x + 3*(1-t1)**2*t1*c1.x + 3*(1-t1)*t1**2*c2.x + t1**3*p2.x
                    y1 = (1-t1)**3*p1.y + 3*(1-t1)**2*t1*c1.y + 3*(1-t1)*t1**2*c2.y + t1**3*p2.y
                    x2 = (1-t2)**3*p1.x + 3*(1-t2)**2*t2*c1.x + 3*(1-t2)*t2**2*c2.x + t2**3*p2.x
                    y2 = (1-t2)**3*p1.y + 3*(1-t2)**2*t2*c1.y + 3*(1-t2)*t2**2*c2.y + t2**3*p2.y
                    segments_by_color[color_key].append((x1, y1, x2, y2))

    return segments_by_color


def reconstruct_curve(segments, max_gap=5.0):
    """
    Reconstruct a continuous curve from individual line segments.
    Connects segments where endpoints match within max_gap (PDF points).
    Returns list of (x, y) points in order along the curve.
    """
    if not segments:
        return []

    # Build point list from segments
    pts = []
    for x1, y1, x2, y2 in segments:
        pts.append((x1, y1, x2, y2))

    # Greedy chain reconstruction: start from leftmost segment, connect endpoints
    used = [False] * len(pts)
    # Find starting segment (leftmost x)
    start_idx = min(range(len(pts)), key=lambda i: min(pts[i][0], pts[i][2]))
    used[start_idx] = True

    # Determine direction: go from left to right
    s = pts[start_idx]
    if s[0] <= s[2]:
        chain = [(s[0], s[1]), (s[2], s[3])]
    else:
        chain = [(s[2], s[3]), (s[0], s[1])]

    # Extend forward (right)
    changed = True
    while changed:
        changed = False
        last_x, last_y = chain[-1]
        best_idx = -1
        best_dist = max_gap
        for i in range(len(pts)):
            if used[i]:
                continue
            x1, y1, x2, y2 = pts[i]
            # Try connecting from last point to either end of this segment
            d1 = math.hypot(x1 - last_x, y1 - last_y)
            d2 = math.hypot(x2 - last_x, y2 - last_y)
            if d1 < best_dist and d1 <= d2:
                best_dist = d1
                best_idx = i
                best_dir = 1  # x1,y1 first
            elif d2 < best_dist:
                best_dist = d2
                best_idx = i
                best_dir = 2  # x2,y2 first

        if best_idx >= 0:
            used[best_idx] = True
            x1, y1, x2, y2 = pts[best_idx]
            if best_dir == 1:
                chain.append((x2, y2))
            else:
                chain.append((x1, y1))
            changed = True

    # Extend backward (left)
    changed = True
    while changed:
        changed = False
        first_x, first_y = chain[0]
        best_idx = -1
        best_dist = max_gap
        for i in range(len(pts)):
            if used[i]:
                continue
            x1, y1, x2, y2 = pts[i]
            d1 = math.hypot(x1 - first_x, y1 - first_y)
            d2 = math.hypot(x2 - first_x, y2 - first_y)
            if d1 < best_dist and d1 <= d2:
                best_dist = d1
                best_idx = i
                best_dir = 2  # prepend x2,y2 (so x1,y1 connects to chain[0])
            elif d2 < best_dist:
                best_dist = d2
                best_idx = i
                best_dir = 1

        if best_idx >= 0:
            used[best_idx] = True
            x1, y1, x2, y2 = pts[best_idx]
            if best_dir == 2:
                chain.insert(0, (x1, y1))
            else:
                chain.insert(0, (x2, y2))
            changed = True

    return chain


def calibrate_log_freq_axis(axis_labels):
    """
    Calibrate log frequency axis from (x_position, freq_value) pairs.
    Returns (a, b) such that freq = 10^(a + b * x).
    """
    # Use two well-separated points
    log_fs = [math.log10(f) for _, f in axis_labels]
    xs = [x for x, _ in axis_labels]
    # Linear fit: log_f = a + b * x
    if len(axis_labels) >= 2:
        b = (log_fs[-1] - log_fs[0]) / (xs[-1] - xs[0])
        a = log_fs[0] - b * xs[0]
    else:
        raise ValueError("Need at least 2 axis labels for calibration")
    return a, b


def calibrate_linear_axis(axis_labels):
    """
    Calibrate linear axis from (y_position, value) pairs.
    Returns (c, d) such that value = c + d * y.
    """
    if len(axis_labels) >= 2:
        ys = [y for y, _ in axis_labels]
        vs = [v for _, v in axis_labels]
        d = (vs[-1] - vs[0]) / (ys[-1] - ys[0])
        c = vs[0] - d * ys[0]
    else:
        raise ValueError("Need at least 2 axis labels for calibration")
    return c, d


def pdf_xy_to_freq(x, a, b):
    """Convert PDF x-coordinate to frequency."""
    return 10 ** (a + b * x)


def pdf_y_to_value(y, c, d):
    """Convert PDF y-coordinate to axis value."""
    return c + d * y


def chain_to_freq_value(chain, freq_cal, val_cal):
    """Convert reconstructed curve points to (freq, value) pairs."""
    a, b = freq_cal
    c, d = val_cal
    freqs = [pdf_xy_to_freq(x, a, b) for x, y in chain]
    values = [pdf_y_to_value(y, c, d) for x, y in chain]
    return freqs, values


def write_csv(filepath, header, rows):
    """Write CSV file."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def sample_to_grid(freqs_raw, values_raw, freq_grid):
    """Sample raw curve data onto standard frequency grid."""
    # Remove NaN/infinite
    valid = np.isfinite(freqs_raw) & np.isfinite(values_raw)
    freqs_clean = freqs_raw[valid]
    values_clean = values_raw[valid]
    if len(freqs_clean) < 2:
        return np.full_like(freq_grid, np.nan)
    return log_interp(freqs_clean, values_clean, freq_grid)


# ============================================================
# Per-driver extraction configurations
# ============================================================

# These are manually calibrated from axis label positions in each PDF.
# See extraction notes in the .md files for derivation.

DRIVER_CONFIGS = {
    "GRS-8SW-4HE-8": {
        "pdf": "GRS-8SW-4HE-8-spec-sheet.pdf",
        "method": "vector",
        "freq_response": {
            # Frequency axis labels (x_center, freq_hz) from PDF text
            "freq_labels": [
                (305.4, 20), (365.6, 50), (406.95, 100), (457.05, 200),
                (518.0, 500), (559.85, 1000), (609.9, 2000), (670.05, 5000),
                (711.45, 10000), (758.6, 20000),
            ],
            # SPL axis labels (y_center, dB) from PDF text
            "spl_labels": [
                (406.25, 105), (419.65, 100), (432.25, 95), (445.65, 90),
                (458.35, 85), (472.05, 80), (484.35, 75), (497.05, 70),
                (510.45, 65), (523.15, 60), (536.55, 55),
            ],
            # Curve colors (R, G, B) in PDF
            "on_axis_color": (0.013, 0.019, 0.020),  # near-black, thick
            # No off-axis curves in GRS datasheet — gray colors are grid lines
            "off_axis_colors": [],
        },
        "impedance": {
            "freq_labels": [
                (299.2, 5), (316.05, 10), (332.95, 20), (355.1, 50),
                (371.95, 100), (388.75, 200), (410.85, 500), (427.75, 1000),
                (444.45, 2000), (466.65, 5000), (483.5, 10000), (500.2, 20000),
            ],
            # Impedance axis (log): y_center, ohms
            "imp_labels": [
                (336.35, 2), (297.65, 5), (267.5, 10), (237.3, 20),
                (197.5, 50), (169.35, 100),
            ],
            "imp_log": True,  # impedance is log scale
            # Phase axis (linear): y_center, degrees
            "phase_labels": [
                (169.35, 180), (178.4, 120), (189.8, 60), (201.25, 0),
                (212.6, -60), (223.95, -120), (235.4, -180),
            ],
            "imp_color": (0.254, 0.332, 0.647),  # blue
            "phase_color": (0.931, 0.13, 0.141),  # red
        },
    },
    "SB26STAC-C000-4": {
        "pdf": "SB26STAC-C000-4.pdf",
        "method": "raster",
        # Frequency response is in embedded JPEG image (1502x670 px)
        # Plot area: x=[78, 1411], y=[22, 627] in image pixels
        # Major freq grid lines at x = [78, 233, 324, 436, 591, 745, 836, 950, 1103, 1258, 1411]
        #   → [100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000, 40000] Hz
        # Horizontal grid lines at y = [22, 73, 123, 174, 224, 274, 325, 375, 426, 476, 527, 577, 627]
        #   → [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40] dB (left axis)
        #   → [16.0, 14.7, 13.3, 12.0, 10.7, 9.3, 8.0, 6.7, 5.3, 4.0, 2.7, 1.3, 0.0] ohm (right axis)
        # Curves: blue=on-axis, green=30° off, red=60° off (SPL, left axis)
        #         black=impedance (right axis)
        "raster_config": {
            "image_index": 0,
            "image_w": 1502,
            "image_h": 670,
            "freq_grid_x": [78, 233, 324, 436, 591, 745, 836, 950, 1103, 1258, 1411],
            "freq_grid_f": [100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000, 40000],
            "spl_grid_y": [22, 73, 123, 174, 224, 274, 325, 375, 426, 476, 527, 577, 627],
            "spl_grid_v": [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40],
            "ohm_grid_y": [22, 73, 123, 174, 224, 274, 325, 375, 426, 476, 527, 577, 627],
            "ohm_grid_v": [16.0, 14.7, 13.3, 12.0, 10.7, 9.3, 8.0, 6.7, 5.3, 4.0, 2.7, 1.3, 0.0],
            "spl_colors": {
                "blue": {"h_min": 0.55, "h_max": 0.68, "s_min": 0.45, "v_min": 0.35, "label": "onaxis"},
                "green": {"h_min": 0.25, "h_max": 0.45, "s_min": 0.25, "v_min": 0.2, "label": "30deg"},
                "red": {"h_min_red": True, "s_min": 0.25, "v_min": 0.2, "label": "60deg"},
            },
            "impedance_color": "black",  # dark curve for impedance on right axis
        },
    },
    "15W-4434G00": {
        "pdf": "15W-4434G00.pdf",
        "method": "raster",
        "raster_config": {
            "image_index": 5,  # 1281x756 px plot image
            "image_w": 1281,
            "image_h": 756,
            # Major freq grid lines (x_px, Hz): 3 decade lines
            "freq_grid_x": [359, 684, 1008],
            "freq_grid_f": [100, 1000, 10000],
            # SPL axis (left, linear): 11 grid lines, 100 to 50 dB top-to-bottom
            "spl_grid_y": [40, 106, 172, 238, 304, 370, 436, 502, 568, 634, 700],
            "spl_grid_v": [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50],
            # Impedance axis (right, log2): 6 grid lines
            "ohm_grid_y": [329, 412, 489, 569, 648, 717],
            "ohm_grid_v": [64, 32, 16, 8, 4, 2],
            "ohm_log_base": 2,  # log2 scale
            # Curve colors: black=on-axis, red/green=off-axis, blue=impedance
            "spl_colors": {
                "black": {"use_dark": True, "s_max": 0.1, "v_max": 0.3, "label": "onaxis"},
                "green": {"h_min": 0.25, "h_max": 0.45, "s_min": 0.2, "v_min": 0.2, "label": "offaxis1"},
                "red": {"h_min_red": True, "s_min": 0.2, "v_min": 0.2, "label": "offaxis2"},
            },
            "impedance_color": "blue",
            "imp_h_min": 0.50, "imp_h_max": 0.70, "imp_s_min": 0.2, "imp_v_min": 0.2,
        },
    },
    "H2606-920000": {
        "pdf": "H2606-920000.pdf",
        "method": "raster",
        "raster_config": {
            "image_index": 5,  # 1281x756 px plot image (same size as 15W)
            "image_w": 1281,
            "image_h": 756,
            # Major freq grid lines: left frame=100Hz, 1000Hz, 10000Hz
            "freq_grid_x": [35, 480, 924],
            "freq_grid_f": [100, 1000, 10000],
            # SPL axis (left, linear): same as 15W
            "spl_grid_y": [40, 106, 172, 238, 304, 370, 436, 502, 568, 634, 700],
            "spl_grid_v": [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50],
            # Impedance axis (right, log2): same as 15W
            "ohm_grid_y": [329, 412, 489, 569, 648, 717],
            "ohm_grid_v": [64, 32, 16, 8, 4, 2],
            "ohm_log_base": 2,
            "spl_colors": {
                "black": {"use_dark": True, "s_max": 0.1, "v_max": 0.3, "label": "onaxis"},
                "green": {"h_min": 0.25, "h_max": 0.45, "s_min": 0.2, "v_min": 0.2, "label": "offaxis1"},
                "red": {"h_min_red": True, "s_min": 0.2, "v_min": 0.2, "label": "offaxis2"},
            },
            "impedance_color": "blue",
            "imp_h_min": 0.50, "imp_h_max": 0.70, "imp_s_min": 0.2, "imp_v_min": 0.2,
        },
    },
}


# ============================================================
# Main extraction functions
# ============================================================

def extract_vector_driver(pdf_path, config, output_dir, model_name):
    """Extract curves from a vector PDF."""
    doc = fitz.open(pdf_path)
    page = doc[0]

    segments_by_color = extract_vector_segments(page)
    freq_grid = standard_freq_grid()

    results = {}

    # --- Frequency response ---
    fr_cfg = config.get("freq_response")
    if fr_cfg and fr_cfg.get("freq_labels") and fr_cfg.get("spl_labels"):
        # Calibrate axes
        freq_cal = calibrate_log_freq_axis(fr_cfg["freq_labels"])
        spl_cal = calibrate_linear_axis(fr_cfg["spl_labels"])

        # On-axis curve
        on_color = fr_cfg["on_axis_color"]
        if on_color in segments_by_color:
            chain = reconstruct_curve(segments_by_color[on_color])
            freqs, spls = chain_to_freq_value(chain, freq_cal, spl_cal)
            spl_grid = sample_to_grid(np.array(freqs), np.array(spls), freq_grid)
            results["freq_response_onaxis"] = (freq_grid, spl_grid)

        # Off-axis curves
        offaxis_data = {}
        for color, label in fr_cfg.get("off_axis_colors", []):
            if color in segments_by_color:
                chain = reconstruct_curve(segments_by_color[color])
                freqs, spls = chain_to_freq_value(chain, freq_cal, spl_cal)
                spl_grid = sample_to_grid(np.array(freqs), np.array(spls), freq_grid)
                offaxis_data[label] = spl_grid
        if offaxis_data:
            results["freq_response_offaxis"] = (freq_grid, offaxis_data)

    # --- Impedance / Phase ---
    imp_cfg = config.get("impedance")
    if imp_cfg and imp_cfg.get("freq_labels") and imp_cfg.get("imp_labels"):
        freq_cal = calibrate_log_freq_axis(imp_cfg["freq_labels"])

        # Impedance (log scale)
        if imp_cfg.get("imp_log"):
            imp_labels = imp_cfg["imp_labels"]
            log_imps = [math.log10(o) for _, o in imp_labels]
            ys = [y for y, _ in imp_labels]
            d = (log_imps[-1] - log_imps[0]) / (ys[-1] - ys[0])
            c = log_imps[0] - d * ys[0]
            imp_cal = (c, d)  # log10(ohm) = c + d*y
        else:
            imp_cal = calibrate_linear_axis(imp_cfg["imp_labels"])

        imp_color = imp_cfg.get("imp_color")
        if imp_color and imp_color in segments_by_color:
            chain = reconstruct_curve(segments_by_color[imp_color])
            a, b = freq_cal
            c, d = imp_cal
            freqs = np.array([pdf_xy_to_freq(x, a, b) for x, y in chain])
            if imp_cfg.get("imp_log"):
                imps = np.array([10 ** (c + d * y) for x, y in chain])
            else:
                imps = np.array([c + d * y for x, y in chain])
            imp_grid = sample_to_grid(freqs, imps, freq_grid)
        else:
            imp_grid = np.full_like(freq_grid, np.nan)

        # Phase (linear scale)
        phase_grid = np.full_like(freq_grid, np.nan)
        phase_color = imp_cfg.get("phase_color")
        if phase_color and phase_color in segments_by_color:
            phase_cal = calibrate_linear_axis(imp_cfg["phase_labels"])
            chain = reconstruct_curve(segments_by_color[phase_color])
            a, b = freq_cal
            c, d = phase_cal
            freqs = np.array([pdf_xy_to_freq(x, a, b) for x, y in chain])
            phases = np.array([c + d * y for x, y in chain])
            phase_grid = sample_to_grid(freqs, phases, freq_grid)

        results["impedance"] = (freq_grid, imp_grid, phase_grid)

    doc.close()

    # --- Write output files ---
    files_written = []

    # Frequency response CSV
    if "freq_response_onaxis" in results:
        freqs, spls = results["freq_response_onaxis"]
        rows = []
        for i, f in enumerate(freqs):
            row = [f"{f:.2f}", f"{spls[i]:.2f}" if np.isfinite(spls[i]) else ""]
            # Add off-axis columns
            if "freq_response_offaxis" in results:
                _, offaxis = results["freq_response_offaxis"]
                for label in sorted(offaxis.keys()):
                    val = offaxis[label][i]
                    row.append(f"{val:.2f}" if np.isfinite(val) else "")
            rows.append(row)

        header = ["freq_hz", "spl_db"]
        if "freq_response_offaxis" in results:
            _, offaxis = results["freq_response_offaxis"]
            for label in sorted(offaxis.keys()):
                header.append(f"spl_{label}_db")

        csv_path = os.path.join(output_dir, f"{model_name}_freq_response.csv")
        write_csv(csv_path, header, rows)
        files_written.append(csv_path)

    # Impedance CSV
    if "impedance" in results:
        freqs, imps, phases = results["impedance"]
        rows = []
        for i, f in enumerate(freqs):
            rows.append([
                f"{f:.2f}",
                f"{imps[i]:.4f}" if np.isfinite(imps[i]) else "",
                f"{phases[i]:.2f}" if np.isfinite(phases[i]) else "",
            ])
        csv_path = os.path.join(output_dir, f"{model_name}_impedance.csv")
        write_csv(csv_path, ["freq_hz", "impedance_ohm", "phase_deg"], rows)
        files_written.append(csv_path)

    # Verification plot
    create_verification_plot(pdf_path, results, output_dir, model_name)

    return files_written, results


def extract_raster_driver(pdf_path, config, output_dir, model_name):
    """
    Extract curves from a raster PDF (embedded bitmap images).
    Uses grid-line calibration from raster_config.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]

    raster_cfg = config.get("raster_config")
    if raster_cfg is None:
        # Fallback: generic raster extraction (legacy)
        return _extract_raster_generic(pdf_path, doc, page, output_dir, model_name)

    # Extract the target image
    images = page.get_images(full=True)
    img_idx = raster_cfg.get("image_index", 0)
    if img_idx >= len(images):
        print(f"  ERROR: image index {img_idx} not found ({len(images)} images)")
        doc.close()
        return [], {}

    xref = images[img_idx][0]
    base_img = doc.extract_image(xref)
    img_bytes = base_img["image"]
    img_ext = base_img["ext"]
    temp_img_path = os.path.join(output_dir, f"{model_name}_plot_img.{img_ext}")
    with open(temp_img_path, "wb") as f:
        f.write(img_bytes)
    doc.close()

    # Process the image
    from PIL import Image
    import matplotlib.colors as mcolors

    img = Image.open(temp_img_path)
    arr = np.array(img.convert("RGB"))
    h, w = arr.shape[:2]
    hsv = mcolors.rgb_to_hsv(arr / 255.0)

    # Calibrate frequency axis (log scale)
    freq_x = np.array(raster_cfg["freq_grid_x"])
    freq_f = np.array(raster_cfg["freq_grid_f"], dtype=float)
    log_f = np.log10(freq_f)
    b_freq = (log_f[-1] - log_f[0]) / (freq_x[-1] - freq_x[0])
    a_freq = log_f[0] - b_freq * freq_x[0]

    # Calibrate SPL axis (linear)
    spl_y = np.array(raster_cfg["spl_grid_y"])
    spl_v = np.array(raster_cfg["spl_grid_v"], dtype=float)
    d_spl = (spl_v[-1] - spl_v[0]) / (spl_y[-1] - spl_y[0])
    c_spl = spl_v[0] - d_spl * spl_y[0]

    # Calibrate ohm axis
    ohm_y = np.array(raster_cfg["ohm_grid_y"])
    ohm_v = np.array(raster_cfg["ohm_grid_v"], dtype=float)
    ohm_log_base = raster_cfg.get("ohm_log_base", 0)  # 0=linear, 2=log2, 10=log10
    if ohm_log_base:
        log_ohm = np.log(ohm_v) / np.log(ohm_log_base)
        d_ohm = (log_ohm[-1] - log_ohm[0]) / (ohm_y[-1] - ohm_y[0])
        c_ohm = log_ohm[0] - d_ohm * ohm_y[0]
    else:
        d_ohm = (ohm_v[-1] - ohm_v[0]) / (ohm_y[-1] - ohm_y[0])
        c_ohm = ohm_v[0] - d_ohm * ohm_y[0]

    # Plot area bounds
    x_min, x_max = int(min(freq_x)) - 2, int(max(freq_x)) + 2
    y_min, y_max = int(min(spl_y)) - 2, int(max(spl_y)) + 2

    # Color masks for SPL curves
    spl_results = {}
    spl_colors_cfg = raster_cfg["spl_colors"]

    for color_name, color_cfg in spl_colors_cfg.items():
        if color_cfg.get("use_dark"):
            # Dark curve (black on-axis) — low saturation, low value
            mask = (hsv[:, :, 2] < color_cfg["v_max"]) & (hsv[:, :, 1] < color_cfg["s_max"])
        elif "h_min_red" in color_cfg:
            # Red wraps around in HSV
            mask = ((hsv[:, :, 0] < 0.05) | (hsv[:, :, 0] > 0.95)) & \
                   (hsv[:, :, 1] > color_cfg["s_min"]) & (hsv[:, :, 2] > color_cfg["v_min"])
        else:
            mask = (hsv[:, :, 0] > color_cfg["h_min"]) & (hsv[:, :, 0] < color_cfg["h_max"]) & \
                   (hsv[:, :, 1] > color_cfg["s_min"]) & (hsv[:, :, 2] > color_cfg["v_min"])

        # Restrict to plot area
        mask[:y_min] = False
        mask[y_max:] = False
        mask[:, :x_min] = False
        mask[:, x_max:] = False

        # For dark (black) curves, filter out grid lines and axis frame
        if color_cfg.get("use_dark"):
            # Remove horizontal grid lines: rows with many dark pixels
            row_dark = np.sum(mask, axis=1)
            grid_threshold = w * 0.25
            non_grid = row_dark < grid_threshold
            mask = mask & non_grid[:, np.newaxis]
            # Remove vertical grid lines
            col_dark = np.sum(mask, axis=0)
            non_grid_cols = col_dark < h * 0.25
            mask = mask & non_grid_cols[np.newaxis, :]

        n_pixels = np.sum(mask)
        if n_pixels < 50:
            print(f"  {color_name}: too few pixels ({n_pixels}), skipping")
            continue

        # Extract curve using cluster tracking for robustness against JPEG noise
        from scipy.ndimage import label as _label  # not used, but available

        curve_x = []
        curve_y = []
        prev_y = None
        track_gap = 30  # max vertical jump between adjacent columns

        for x in range(x_min, x_max + 1):
            ys = np.where(mask[:, x])[0]
            if len(ys) == 0:
                continue

            # Cluster y-values into groups (gap > 10 pixels = new cluster)
            clusters = []
            cluster_start = ys[0]
            prev = ys[0]
            for y in ys[1:]:
                if y - prev > 10:
                    clusters.append((cluster_start, prev))
                    cluster_start = y
                prev = y
            clusters.append((cluster_start, prev))

            # Pick the cluster closest to previous y (curve tracking)
            if prev_y is not None:
                best_cluster = None
                best_dist = track_gap
                for cs, ce in clusters:
                    cm = (cs + ce) // 2
                    d = abs(cm - prev_y)
                    if d < best_dist:
                        best_dist = d
                        best_cluster = (cs, ce)
                if best_cluster is None:
                    continue
                y_val = (best_cluster[0] + best_cluster[1]) // 2
            else:
                # Start: pick cluster nearest to expected curve position
                # For SPL curves, start near the top (high SPL = low y)
                best_cluster = min(clusters, key=lambda c: abs((c[0]+c[1])//2 - y_min - 50))
                y_val = (best_cluster[0] + best_cluster[1]) // 2

            curve_x.append(x)
            curve_y.append(float(y_val))
            prev_y = y_val

        # Convert to freq and SPL
        freqs = 10 ** (a_freq + b_freq * np.array(curve_x))
        spls = c_spl + d_spl * np.array(curve_y)

        label = color_cfg["label"]
        spl_results[label] = (freqs, spls)
        print(f"  {color_name} ({label}): {len(curve_x)} pts, freq=[{freqs.min():.0f}, {freqs.max():.0f}] Hz, SPL=[{spls.min():.1f}, {spls.max():.1f}] dB")

    # Impedance curve
    imp_freqs = None
    imp_vals = None
    imp_color = raster_cfg.get("impedance_color", "black")

    if imp_color == "blue":
        # Blue impedance curve on right (ohm) axis
        imp_mask = (hsv[:, :, 0] > raster_cfg["imp_h_min"]) & \
                   (hsv[:, :, 0] < raster_cfg["imp_h_max"]) & \
                   (hsv[:, :, 1] > raster_cfg["imp_s_min"]) & \
                   (hsv[:, :, 2] > raster_cfg["imp_v_min"])
    else:
        # Dark impedance curve
        imp_mask = (hsv[:, :, 2] < 0.3) & (hsv[:, :, 1] < 0.15)

    # Restrict to plot area
    imp_mask[:y_min] = False
    imp_mask[y_max:] = False
    imp_mask[:, :x_min] = False
    imp_mask[:, x_max:] = False

    if np.sum(imp_mask) > 100:
        # Use cluster tracking for impedance curve too
        curve_x = []
        curve_y = []
        prev_y = None
        track_gap = 30

        for x in range(x_min, x_max + 1):
            ys = np.where(imp_mask[:, x])[0]
            if len(ys) == 0:
                continue

            clusters = []
            cluster_start = ys[0]
            prev = ys[0]
            for y in ys[1:]:
                if y - prev > 10:
                    clusters.append((cluster_start, prev))
                    cluster_start = y
                prev = y
            clusters.append((cluster_start, prev))

            if prev_y is not None:
                best_cluster = None
                best_dist = track_gap
                for cs, ce in clusters:
                    cm = (cs + ce) // 2
                    d = abs(cm - prev_y)
                    if d < best_dist:
                        best_dist = d
                        best_cluster = (cs, ce)
                if best_cluster is None:
                    continue
                y_val = (best_cluster[0] + best_cluster[1]) // 2
            else:
                best_cluster = min(clusters, key=lambda c: abs((c[0]+c[1])//2 - (y_min+y_max)//2))
                y_val = (best_cluster[0] + best_cluster[1]) // 2

            curve_x.append(x)
            curve_y.append(float(y_val))
            prev_y = y_val

        if len(curve_x) > 20:
            imp_freqs = 10 ** (a_freq + b_freq * np.array(curve_x))
            if ohm_log_base:
                log_ohm_vals = c_ohm + d_ohm * np.array(curve_y)
                imp_vals = ohm_log_base ** log_ohm_vals
            else:
                imp_vals = c_ohm + d_ohm * np.array(curve_y)
            print(f"  impedance: {len(curve_x)} pts, freq=[{imp_freqs.min():.0f}, {imp_freqs.max():.0f}] Hz, Z=[{imp_vals.min():.2f}, {imp_vals.max():.2f}] ohm")

    # Write CSVs
    files_written = []
    freq_grid = standard_freq_grid()

    # Frequency response CSV
    if spl_results:
        # On-axis is first
        onaxis_key = "onaxis" if "onaxis" in spl_results else list(spl_results.keys())[0]
        offaxis_keys = [k for k in spl_results if k != onaxis_key]

        # Sample all curves to grid
        sampled = {}
        for label, (freqs, vals) in spl_results.items():
            sampled[label] = sample_to_grid(freqs, vals, freq_grid)

        rows = []
        for i, f in enumerate(freq_grid):
            row = [f"{f:.2f}"]
            row.append(f"{sampled[onaxis_key][i]:.2f}" if np.isfinite(sampled[onaxis_key][i]) else "")
            for label in sorted(offaxis_keys):
                val = sampled[label][i]
                row.append(f"{val:.2f}" if np.isfinite(val) else "")
            rows.append(row)

        header = ["freq_hz", "spl_db"] + [f"spl_{l}_db" for l in sorted(offaxis_keys)]
        csv_path = os.path.join(output_dir, f"{model_name}_freq_response.csv")
        write_csv(csv_path, header, rows)
        files_written.append(csv_path)

    # Impedance CSV
    if imp_freqs is not None:
        imp_grid = sample_to_grid(imp_freqs, imp_vals, freq_grid)
        phase_grid = np.full_like(freq_grid, np.nan)  # No phase data in SB26 plot

        rows = []
        for i, f in enumerate(freq_grid):
            rows.append([
                f"{f:.2f}",
                f"{imp_grid[i]:.4f}" if np.isfinite(imp_grid[i]) else "",
                "",
            ])
        csv_path = os.path.join(output_dir, f"{model_name}_impedance.csv")
        write_csv(csv_path, ["freq_hz", "impedance_ohm", "phase_deg"], rows)
        files_written.append(csv_path)

    # Build results dict for verification plot
    results = {}
    if spl_results:
        onaxis_key = "onaxis" if "onaxis" in spl_results else list(spl_results.keys())[0]
        onaxis_freqs, onaxis_spls = spl_results[onaxis_key]
        results["freq_response_onaxis"] = (onaxis_freqs, onaxis_spls)

        offaxis = {}
        for label, (freqs, vals) in spl_results.items():
            if label != onaxis_key:
                offaxis[label] = (freqs, vals)
        if offaxis:
            results["freq_response_offaxis"] = (onaxis_freqs, offaxis)

    if imp_freqs is not None:
        phase_dummy = np.full_like(imp_freqs, np.nan)
        results["impedance"] = (imp_freqs, imp_vals, phase_dummy)

    # Verification plot
    create_verification_plot(pdf_path, results, output_dir, model_name)

    # Clean up temp image
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    return files_written, results


def process_raster_curves(img_path, text_spans, output_dir, model_name, page_w, page_h):
    """
    Process rendered page image to extract curves.
    Uses color-based segmentation to find curve pixels,
    then maps to frequency/value using axis labels.
    """
    from PIL import Image

    img = Image.open(img_path)
    img_array = np.array(img.convert("RGB"))

    # Scale factor: page points to pixels at 300 DPI
    # 1 point = 1/72 inch, at 300 DPI = 300/72 ≈ 4.167 pixels per point
    scale = 300.0 / 72.0

    # Find axis labels in text
    # Look for frequency labels (numbers + Hz/kHz text)
    freq_values = []
    spl_values = []
    imp_values = []
    phase_values = []

    # Parse text spans for axis labels
    for span in text_spans:
        text = span["text"].strip()
        x, y = span["x"], span["y"]

        # Frequency axis labels: pure numbers or with k/kHz
        try:
            val = float(text)
            freq_values.append((x, y, val, text))
        except ValueError:
            pass

    print(f"  Text spans with numeric values: {len(freq_values)}")

    # The raster approach needs per-driver tuning.
    # For ScanSpeak datasheets, the frequency response and impedance
    # curves are typically blue/green/red lines on white background.
    # We'll use HSV color filtering.

    # Convert to HSV for color detection
    hsv = matplotlib.colors.rgb_to_hsv(img_array / 255.0)

    # Detect blue curve (typical impedance or on-axis response)
    # Blue: H around 0.55-0.65, high S, high V
    blue_mask = (hsv[:, :, 0] > 0.50) & (hsv[:, :, 0] < 0.70) & (hsv[:, :, 1] > 0.3) & (hsv[:, :, 2] > 0.3)

    # Detect green curve (typical off-axis or impedance)
    green_mask = (hsv[:, :, 0] > 0.25) & (hsv[:, :, 0] < 0.45) & (hsv[:, :, 1] > 0.3) & (hsv[:, :, 2] > 0.3)

    # Detect red curve (typical phase or response)
    red_mask = ((hsv[:, :, 0] < 0.05) | (hsv[:, :, 0] > 0.95)) & (hsv[:, :, 1] > 0.3) & (hsv[:, :, 2] > 0.3)

    # Detect black/dark curve (typical on-axis response)
    dark_mask = (hsv[:, :, 2] < 0.3) & (hsv[:, :, 1] < 0.2)

    print(f"  Blue pixels: {np.sum(blue_mask)}")
    print(f"  Green pixels: {np.sum(green_mask)}")
    print(f"  Red pixels: {np.sum(red_mask)}")
    print(f"  Dark pixels: {np.sum(dark_mask)}")

    # Save color masks for inspection
    for name, mask in [("blue", blue_mask), ("green", green_mask), ("red", red_mask), ("dark", dark_mask)]:
        if np.sum(mask) > 100:
            mask_img = Image.fromarray((mask * 255).astype(np.uint8))
            mask_img.save(os.path.join(output_dir, f"{model_name}_mask_{name}.png"))

    # The actual curve extraction from raster images requires knowing
    # the plot area boundaries. We'll try to detect these from the
    # text label positions and the image layout.
    #
    # For now, we output the color masks and the page render for
    # manual verification. The full automated extraction for raster
    # PDFs will be completed with per-driver configuration.

    # Attempt basic curve extraction for ScanSpeak format:
    # Typical layout: frequency response on left, impedance on right
    # or frequency response on top, impedance on bottom.

    results = {}

    # Try to extract from the largest colored curve
    # We'll look for horizontal bands of colored pixels that form curves

    for color_name, mask in [("blue", blue_mask), ("green", green_mask), ("red", red_mask)]:
        if np.sum(mask) < 500:
            continue

        # Find bounding box of colored pixels
        rows, cols = np.where(mask)
        if len(rows) < 10:
            continue

        # For each column in the bounding box, find the median y position
        # This gives us the curve as (x_pixel, y_pixel) pairs
        x_min, x_max = cols.min(), cols.max()
        curve_x = []
        curve_y = []
        for x in range(x_min, x_max + 1):
            col_mask = mask[:, x]
            ys = np.where(col_mask)[0]
            if len(ys) > 0:
                # Use median y to handle multi-pixel-thick curves
                curve_x.append(x / scale)  # convert back to PDF points
                curve_y.append(np.median(ys) / scale)

        if len(curve_x) > 20:
            # Store raw pixel coordinates (in PDF point space)
            results[f"raw_{color_name}"] = (np.array(curve_x), np.array(curve_y))
            print(f"  {color_name} curve: {len(curve_x)} points, x=[{min(curve_x):.1f}, {max(curve_x):.1f}], y=[{min(curve_y):.1f}, {max(curve_y):.1f}]")

    return results


def create_verification_plot(pdf_path, results, output_dir, model_name):
    """Create verification plot showing extracted data."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f"{model_name} — Extraction Verification", fontsize=14)

    # Frequency response
    ax = axes[0]
    ax.set_title("Frequency Response")
    if "freq_response_onaxis" in results:
        freqs, spls = results["freq_response_onaxis"]
        if isinstance(spls, dict):
            # Off-axis dict format
            pass
        else:
            ax.plot(freqs, spls, 'b-', label="On-axis", linewidth=1)
    if "freq_response_offaxis" in results:
        onaxis_freqs, offaxis = results["freq_response_offaxis"]
        # offaxis values may come from the same x as onaxis, or may need
        # their own x arrays stored separately. For raster extraction, the
        # off-axis dict stores just y-values that share the on-axis x.
        # But if they have different lengths, we plot what we can.
        for label, vals in offaxis.items():
            if isinstance(vals, tuple):
                ox, oy = vals
                ax.plot(ox, oy, '--', label=label, linewidth=0.8)
            else:
                ax.plot(onaxis_freqs[:len(vals)], vals, '--', label=label, linewidth=0.8)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("SPL [dB]")
    ax.set_xscale("log")
    ax.set_xlim(20, 20000)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)

    # Impedance
    ax = axes[1]
    ax.set_title("Impedance / Phase")
    if "impedance" in results:
        freqs, imps, phases = results["impedance"]
        ax.plot(freqs, imps, 'b-', label="Impedance [Ω]", linewidth=1)
        ax.set_ylabel("Impedance [Ω]")
        ax2 = ax.twinx()
        ax2.plot(freqs, phases, 'r-', label="Phase [°]", linewidth=0.8)
        ax2.set_ylabel("Phase [°]")
        ax2.legend(fontsize=8, loc="upper right")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(20, 20000)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")

    plt.tight_layout()
    plot_path = os.path.join(output_dir, f"{model_name}_extraction_verify.png")
    fig.savefig(plot_path, dpi=150)
    plt.close()
    print(f"  Verification plot: {plot_path}")


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Extract datasheet curves from PDF")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--model", help="Model name (default: PDF filename stem)")
    parser.add_argument("--output-dir", help="Output directory (default: same as PDF)")
    parser.add_argument("--raster", action="store_true", help="Force raster extraction method")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    model_name = args.model or Path(pdf_path).stem
    output_dir = args.output_dir or os.path.dirname(pdf_path)

    print(f"\n{'='*60}")
    print(f"Extracting: {model_name}")
    print(f"PDF: {pdf_path}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}")

    # Check if we have a config for this model
    config = DRIVER_CONFIGS.get(model_name)
    if config is None:
        # Auto-detect method
        doc = fitz.open(pdf_path)
        page = doc[0]
        drawings = page.get_drawings()
        has_vector_curves = any(
            item[0] in ("l", "c")
            for d in drawings
            for item in d["items"]
        )
        doc.close()
        method = "raster" if args.raster or not has_vector_curves else "vector"
        config = {"pdf": os.path.basename(pdf_path), "method": method}
        print(f"  Auto-detected method: {method}")
    else:
        print(f"  Using config: method={config['method']}")

    if config["method"] == "vector":
        files, results = extract_vector_driver(pdf_path, config, output_dir, model_name)
    else:
        files, results = extract_raster_driver(pdf_path, config, output_dir, model_name)

    print(f"\n  Files written:")
    for f in files:
        print(f"    {f}")

    # Sanity checks
    print(f"\n  Sanity checks:")
    for key, val in results.items():
        if key == "freq_response_onaxis":
            freqs, spls = val
            finite = np.isfinite(spls)
            if np.any(finite):
                print(f"    {key}: {np.sum(finite)} valid points, SPL range [{np.nanmin(spls):.1f}, {np.nanmax(spls):.1f}] dB")
        elif key == "impedance":
            freqs, imps, phases = val
            finite_i = np.isfinite(imps)
            finite_p = np.isfinite(phases)
            if np.any(finite_i):
                print(f"    impedance: {np.sum(finite_i)} valid points, range [{np.nanmin(imps):.2f}, {np.nanmax(imps):.2f}] Ω")
            if np.any(finite_p):
                print(f"    phase: {np.sum(finite_p)} valid points, range [{np.nanmin(phases):.1f}, {np.nanmax(phases):.1f}]°")


if __name__ == "__main__":
    main()
