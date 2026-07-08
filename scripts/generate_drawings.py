#!/usr/bin/env python3
"""
Generate dimensioned SVG drawings for the Mk3 cabinet.

Parses cabinet.scad + driver SCAD files for all dimensions, then produces:
  1. front_baffle.svg   — front baffle with mid + tweeter cutouts, rebate, pilot holes
  2. side_panel.svg     — side panel with woofer cutout + pilot holes
  3. cut_list.svg       — panel cut list with dimensions + quantities
  4. assembly_dims.svg  — assembly measurement drawing (heights, spacing, edges)

All drawings are 2D orthogonal projections with dimension lines, labels,
and hole-position coordinates. SVG can be opened in any browser or
converted to PDF/PNG with rsvg-convert or Inkscape.

Usage:
    python3 generate_drawings.py                    # write SVGs to assets/drawings/
    python3 generate_drawings.py --outdir /tmp/     # custom output
"""
import os
import re
import math
import textwrap

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
_CAB_SCAD = os.path.join(_REPO_ROOT, "cad", "cabinet.scad")
_WG_SCAD = os.path.join(_REPO_ROOT, "cad", "waveguide.scad")
_MID_SCAD = os.path.join(_REPO_ROOT, "cad", "midrange.scad")


# ============================================================
#  SCAD parsing
# ============================================================
def _parse_var(text, name):
    """Extract a simple numeric variable from SCAD source."""
    pat = rf"^\s*{re.escape(name)}\s*=\s*([0-9.]+)\s*;"
    for line in text.splitlines():
        m = re.match(pat, line)
        if m:
            return float(m.group(1))
    return None


def _parse_list(text, name):
    """Extract a list like [160, 330, 730] from SCAD source."""
    pat = rf"^\s*{re.escape(name)}\s*=\s*\[([0-9,\s]+)\]\s*;"
    for line in text.splitlines():
        m = re.match(pat, line)
        if m:
            return [float(x.strip()) for x in m.group(1).split(",")]
    return None


def load_params():
    """Load all dimensions from cabinet.scad, waveguide.scad, midrange.scad."""
    with open(_CAB_SCAD) as f:
        cab = f.read()
    with open(_WG_SCAD) as f:
        wg = f.read()
    with open(_MID_SCAD) as f:
        mid = f.read()

    p = {}
    # Cabinet shell
    p["W"] = _parse_var(cab, "W")
    p["D"] = _parse_var(cab, "D")
    p["H"] = _parse_var(cab, "H")
    p["wall"] = _parse_var(cab, "wall")
    p["round_r"] = _parse_var(cab, "round_r")

    # Woofer
    p["woofer_frame_d"] = _parse_var(cab, "woofer_frame_d")
    p["woofer_cut_d"] = _parse_var(cab, "woofer_cut_d")
    p["woofer_bcd"] = _parse_var(cab, "woofer_bcd")
    p["woofer_hole_d"] = _parse_var(cab, "woofer_hole_d")
    p["woofer_n_holes"] = int(_parse_var(cab, "woofer_n_holes"))
    p["woofer_depth"] = _parse_var(cab, "woofer_depth")
    p["woofer_z"] = _parse_var(cab, "woofer_z")

    # Midrange placement
    p["mid_z"] = _parse_var(cab, "mid_z")
    p["cc"] = _parse_var(cab, "cc")
    p["tw_z"] = p["mid_z"] - p["cc"]

    # Midrange dims (from midrange.scad)
    p["mid_face_d"] = _parse_var(mid, "flange_od")
    p["mid_flange_t"] = _parse_var(mid, "flange_tyk")
    p["mid_cut_d"] = _parse_var(mid, "udskaering_dia") + 1.0  # +clearance
    p["mid_bcd"] = _parse_var(mid, "bolt_cirkel")
    p["mid_hole_d"] = _parse_var(mid, "bolt_hul_dia")
    p["mid_n_holes"] = int(_parse_var(mid, "antal_huller"))
    p["mid_bolt_offset"] = _parse_var(mid, "bolt_offset")
    p["mid_depth"] = _parse_var(mid, "total_dybde")

    # Waveguide dims (from waveguide.scad)
    p["wg_flange_w"] = _parse_var(wg, "flange_w")
    p["wg_flange_h"] = _parse_var(wg, "flange_h")
    p["wg_flange_t"] = _parse_var(wg, "flange_thick")
    p["wg_flange_r"] = _parse_var(wg, "corner_r")
    p["wg_bcd_x"] = _parse_var(wg, "baf_bcd_x")
    p["wg_bcd_y"] = _parse_var(wg, "baf_bcd_y")

    # Bracing
    p["shelf_zs"] = _parse_list(cab, "shelf_zs") or [160, 330, 730]
    p["shelf_rim"] = _parse_var(cab, "shelf_rim") or 45
    p["divider_tilt"] = _parse_var(cab, "divider_tilt") or 19

    # Derived
    p["w_in"] = p["W"] - 2 * p["wall"]
    p["d_in"] = p["D"] - 2 * p["wall"]
    p["h_in"] = p["H"] - 2 * p["wall"]

    # Validate
    for k, v in p.items():
        if v is None and k != "shelf_zs":
            raise ValueError(f"Could not parse '{k}' from SCAD files")

    return p


# ============================================================
#  SVG helpers
# ============================================================
class SVG:
    """Simple SVG builder with dimension-line primitives."""

    def __init__(self, width, height, title=""):
        self.w = width
        self.h = height
        self.title = title
        self.elements = []
        self.styles = textwrap.dedent("""\
            .panel { fill: #f5f0e0; stroke: #333; stroke-width: 1.5; }
            .cutout { fill: none; stroke: #c0392b; stroke-width: 1.2; stroke-dasharray: 6,3; }
            .rebate { fill: #faebe0; stroke: #e67e22; stroke-width: 1.0; stroke-dasharray: 4,2; }
            .pilot { fill: #333; }
            .dim-line { stroke: #2980b9; stroke-width: 0.8; fill: none; }
            .dim-text { fill: #2980b9; font-family: sans-serif; font-size: 11px; text-anchor: middle; }
            .dim-text-v { fill: #2980b9; font-family: sans-serif; font-size: 11px; text-anchor: middle; }
            .label { fill: #333; font-family: sans-serif; font-size: 12px; text-anchor: middle; font-weight: bold; }
            .label-sm { fill: #555; font-family: sans-serif; font-size: 10px; text-anchor: middle; }
            .label-driver { fill: #c0392b; font-family: sans-serif; font-size: 11px; text-anchor: middle; font-weight: bold; }
            .title-text { fill: #222; font-family: sans-serif; font-size: 16px; font-weight: bold; }
            .note { fill: #555; font-family: sans-serif; font-size: 10px; }
            .arrow { stroke: #2980b9; stroke-width: 0.8; fill: #2980b9; }
            .center-line { stroke: #888; stroke-width: 0.5; stroke-dasharray: 8,3,2,3; }
        """)

    def rect(self, x, y, w, h, cls="panel", rx=0):
        rx_attr = f' rx="{rx}" ry="{rx}"' if rx else ""
        self.elements.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" class="{cls}"{rx_attr}/>'  )

    def rrect(self, x, y, w, h, r, cls="panel"):
        """Rounded rectangle (all corners same radius)."""
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{r:.1f}" ry="{r:.1f}" class="{cls}"/>'
        )

    def circle(self, cx, cy, r, cls="cutout"):
        self.elements.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" class="{cls}"/>')

    def line(self, x1, y1, x2, y2, cls="dim-line"):
        self.elements.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"/>')

    def text(self, x, y, text, cls="label"):
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.elements.append(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}">{escaped}</text>')

    def text_r(self, x, y, text, cls="dim-text-v", angle=-90):
        """Rotated text (for vertical dimension labels)."""
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.elements.append(
            f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" '
            f'transform="rotate({angle} {x:.1f} {y:.1f})">{escaped}</text>'
        )

    def dim_h(self, x1, x2, y, offset=25, label=None):
        """Horizontal dimension line with arrows."""
        if label is None:
            label = f"{x2 - x1:.0f}"
        # Extension lines
        self.line(x1, y - offset + 15, x1, y - offset, cls="dim-line")
        self.line(x2, y - offset + 15, x2, y - offset, cls="dim-line")
        # Dimension line
        self.line(x1, y - offset, x2, y - offset, cls="dim-line")
        # Arrows
        self._arrow_h(x1, y - offset, +1)
        self._arrow_h(x2, y - offset, -1)
        # Label
        mid = (x1 + x2) / 2
        self.text(mid, y - offset - 4, label, cls="dim-text")

    def dim_v(self, y1, y2, x, offset=25, label=None):
        """Vertical dimension line with arrows (y1 < y2 in SVG coords)."""
        if label is None:
            label = f"{abs(y2 - y1):.0f}"
        # Extension lines
        self.line(x + offset - 15, y1, x + offset, y1, cls="dim-line")
        self.line(x + offset - 15, y2, x + offset, y2, cls="dim-line")
        # Dimension line
        self.line(x + offset, y1, x + offset, y2, cls="dim-line")
        # Arrows
        self._arrow_v(y1, x + offset, +1)
        self._arrow_v(y2, x + offset, -1)
        # Label (rotated)
        mid = (y1 + y2) / 2
        self.text_r(x + offset + 14, mid, label)

    def _arrow_h(self, x, y, direction):
        s = 4
        self.elements.append(
            f'<polygon points="{x:.1f},{y:.1f} {x + direction*s:.1f},{y-s/2:.1f} '
            f'{x + direction*s:.1f},{y+s/2:.1f}" class="arrow"/>'
        )

    def _arrow_v(self, y, x, direction):
        s = 4
        self.elements.append(
            f'<polygon points="{x:.1f},{y:.1f} {x-s/2:.1f},{y + direction*s:.1f} '
            f'{x+s/2:.1f},{y + direction*s:.1f}" class="arrow"/>'
        )

    def center_cross(self, cx, cy, size=6):
        """Draw a center cross (for hole centers)."""
        self.line(cx - size, cy, cx + size, cy, cls="center-line")
        self.line(cx, cy - size, cx, cy + size, cls="center-line")

    def render(self):
        svg = f'<?xml version="1.0" encoding="UTF-8"?>\n'
        svg += f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'
        svg += f'<style>{self.styles}</style>\n'
        svg += f'<rect width="{self.w}" height="{self.h}" fill="white"/>\n'
        svg += "\n".join(self.elements)
        svg += "\n</svg>\n"
        return svg


# ============================================================
#  Drawing generators
# ============================================================
def gen_front_baffle(p, outdir):
    """Front baffle with midrange + waveguide cutouts, rebates, pilot holes."""
    W, H = p["W"], p["H"]
    wall = p["wall"]
    rr = p["round_r"]
    scale = 0.5  # mm to SVG units
    margin = 80
    dw = W * scale + 2 * margin
    dh = H * scale + 2 * margin
    svg = SVG(dw, dh, "Front Baffle")

    # Panel (rounded front edges)
    px = margin
    py = margin
    pw = W * scale
    ph = H * scale
    svg.rrect(px, py, pw, ph, rr * scale, "panel")

    # Title
    svg.text(dw / 2, 25, "Mk3 Front Baffle — Cutout & Hole Layout", "title-text")
    svg.text(dw / 2, 42, f"Panel: {W:.0f} × {H:.0f} mm, {wall:.0f} mm birch ply, R{rr:.0f} front edges", "note")

    # Convert z-height to SVG y (bottom of panel = bottom of SVG)
    def z_to_y(z):
        return py + ph - z * scale

    cx = px + pw / 2

    # --- Midrange (top) ---
    mid_r = p["mid_cut_d"] / 2 * scale
    mid_face_r = p["mid_face_d"] / 2 * scale
    mid_y = z_to_y(p["mid_z"])

    # Rebate (faceplate)
    svg.circle(cx, mid_y, mid_face_r, "rebate")
    # Cutout
    svg.circle(cx, mid_y, mid_r, "cutout")
    svg.center_cross(cx, mid_y, 8)

    # Mid pilot holes (BCD)
    for i in range(p["mid_n_holes"]):
        a = math.radians(p["mid_bolt_offset"] + i * 360 / p["mid_n_holes"])
        hx = cx + (p["mid_bcd"] / 2) * math.cos(a) * scale
        hy = mid_y + (p["mid_bcd"] / 2) * math.sin(a) * scale
        svg.circle(hx, hy, 1.5, "pilot")

    svg.text(cx, mid_y - mid_face_r - 12,
             f"Midrange 18W/4424G00  Ø{p['mid_cut_d']:.1f} cutout, Ø{p['mid_face_d']:.1f} rebate, "
             f"{p['mid_n_holes']}×Ø{p['mid_hole_d']:.1f} on Ø{p['mid_bcd']:.0f} BCD",
             "label-driver")

    # --- Waveguide/tweeter (below mid) ---
    tw_y = z_to_y(p["tw_z"])
    wg_w = (p["wg_flange_w"] + 1.0) * scale  # +clearance
    wg_h = (p["wg_flange_h"] + 1.0) * scale
    wg_r = p["wg_flange_r"] * scale

    # Rebate (flange recess)
    svg.rrect(cx - wg_w / 2, tw_y - wg_h / 2, wg_w, wg_h, wg_r, "rebate")

    # Pilot holes for waveguide baffle screws (4 corners on BCD)
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            hx = cx + sx * (p["wg_bcd_x"] / 2) * scale
            hy = tw_y + sy * (p["wg_bcd_y"] / 2) * scale
            svg.circle(hx, hy, 1.5, "pilot")

    svg.center_cross(cx, tw_y, 8)
    svg.text(cx, tw_y + wg_h / 2 + 14,
             f"Waveguide SB26STAC  {p['wg_flange_w']:.0f}×{p['wg_flange_h']:.0f} mm recess, "
             f"R{p['wg_flange_r']:.0f}, 4×Ø3 pilot on {p['wg_bcd_x']:.0f}×{p['wg_bcd_y']:.0f} BCD",
             "label-driver")

    # --- Dimensions ---
    # Overall width
    svg.dim_h(px, px + pw, py + ph + 20, offset=35, label=f"{W:.0f}")
    # Overall height (left side)
    svg.dim_v(py, py + ph, px, offset=35, label=f"{H:.0f}")

    # Mid center height from bottom
    svg.dim_v(py + ph, mid_y, px - 15, offset=20, label=f"z={p['mid_z']:.0f}")
    # Tweeter center height from bottom
    svg.dim_v(py + ph, tw_y, px - 15, offset=55, label=f"z={p['tw_z']:.0f}")

    # Center-to-center
    svg.dim_v(mid_y, tw_y, cx + max(mid_face_r, wg_w / 2) + 15, offset=20,
              label=f"cc={p['cc']:.0f}")

    # Center line
    svg.line(cx, py - 5, cx, py + ph + 5, "center-line")

    # Legend
    ly = py + ph + 50
    svg.text(margin, ly, "---  Red dashed: cutout    Orange dashed: rebate/recess    Filled dots: pilot holes (Ø3)  ---", "note")

    outpath = os.path.join(outdir, "front_baffle.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_side_panel(p, outdir):
    """Side panel with woofer cutout + pilot holes."""
    D, H = p["D"], p["H"]
    wall = p["wall"]
    scale = 0.5
    margin = 80
    dw = D * scale + 2 * margin
    dh = H * scale + 2 * margin
    svg = SVG(dw, dh, "Side Panel")

    px = margin
    py = margin
    pw = D * scale
    ph = H * scale

    # Panel (square corners — side panels are flat)
    svg.rect(px, py, pw, ph, "panel")

    svg.text(dw / 2, 25, "Mk3 Side Panel — Woofer Cutout & Hole Layout", "title-text")
    svg.text(dw / 2, 42, f"Panel: {D:.0f} × {H:.0f} mm, {wall:.0f} mm birch ply (flat, no roundover)", "note")

    def z_to_y(z):
        return py + ph - z * scale

    cx = px + pw / 2
    wz = z_to_y(p["woofer_z"])

    # Woofer cutout
    cut_r = p["woofer_cut_d"] / 2 * scale
    frame_r = p["woofer_frame_d"] / 2 * scale
    svg.circle(cx, wz, frame_r, "rebate")
    svg.circle(cx, wz, cut_r, "cutout")
    svg.center_cross(cx, wz, 10)

    # Woofer pilot holes (8 on BCD)
    for i in range(p["woofer_n_holes"]):
        a = math.radians(i * 360 / p["woofer_n_holes"])
        hx = cx + (p["woofer_bcd"] / 2) * math.cos(a) * scale
        hy = wz + (p["woofer_bcd"] / 2) * math.sin(a) * scale
        svg.circle(hx, hy, 1.5, "pilot")

    svg.text(cx, wz - frame_r - 12,
             f"GRS 12SW-4HE  Ø{p['woofer_cut_d']:.0f} cutout, Ø{p['woofer_frame_d']:.0f} frame, "
             f"{p['woofer_n_holes']}×Ø{p['woofer_hole_d']:.1f} on Ø{p['woofer_bcd']:.0f} BCD",
             "label-driver")

    # Note: second woofer is on the OPPOSITE side panel
    svg.text(cx, wz + frame_r + 20,
             "(Opposed push-push: 2nd woofer on opposite side, same height)", "label-sm")

    # Dimensions
    svg.dim_h(px, px + pw, py + ph + 20, offset=35, label=f"{D:.0f}")
    svg.dim_v(py, py + ph, px, offset=35, label=f"{H:.0f}")
    svg.dim_v(py + ph, wz, px - 15, offset=20, label=f"z={p['woofer_z']:.0f}")

    # Center line
    svg.line(cx, py - 5, cx, py + ph + 5, "center-line")

    # Brace shelf positions (on side panel too — shelves span the interior)
    for sz in p["shelf_zs"]:
        sy = z_to_y(sz)
        svg.line(px + 5, sy, px + pw - 5, sy, "center-line")
        svg.text(px + pw + 8, sy + 3, f"shelf z={sz:.0f}", "label-sm")

    outpath = os.path.join(outdir, "side_panel.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_cut_list(p, outdir):
    """Panel cut list with dimensions, quantities, and notes."""
    W, D, H, wall = p["W"], p["D"], p["H"], p["wall"]

    panels = [
        ("Front baffle", W, H, 1, "R19 front vertical edges, mid + WG cutouts"),
        ("Back panel", W, H, 1, "Square edges"),
        ("Side panel L", D, H, 1, "Woofer cutout Ø284, 8×Ø5.5 on Ø319 BCD"),
        ("Side panel R", D, H, 1, "Woofer cutout Ø284, 8×Ø5.5 on Ø319 BCD (opposed)"),
        ("Top panel", W, D, 1, "Square edges"),
        ("Bottom panel", W, D, 1, "Square edges"),
        ("Divider plate", W, D, 1, f"Tilted {p['divider_tilt']:.0f}°, cut to fit cavity"),
        ("Shelf brace 1", W - 2*wall, D - 2*wall, 1, f"Ring shelf, rim {p['shelf_rim']:.0f} mm, z={p['shelf_zs'][0]:.0f}"),
        ("Shelf brace 2", W - 2*wall, D - 2*wall, 1, f"Ring shelf, rim {p['shelf_rim']:.0f} mm, z={p['shelf_zs'][1]:.0f}"),
        ("Shelf brace 3", W - 2*wall, D - 2*wall, 1, f"Ring shelf, rim {p['shelf_rim']:.0f} mm, z={p['shelf_zs'][2]:.0f}"),
    ]

    row_h = 32
    header_h = 60
    col_x = [20, 170, 260, 340, 420, 600]
    col_labels = ["Panel", "Width (mm)", "Height/Depth (mm)", "Qty", "Thickness", "Notes"]
    total_h = header_h + len(panels) * row_h + 80
    total_w = 780

    svg = SVG(total_w, total_h, "Cut List")
    svg.text(total_w / 2, 25, "Mk3 Cabinet — Panel Cut List", "title-text")
    svg.text(total_w / 2, 42, f"Material: {wall:.0f} mm birch plywood  |  External: {W:.0f} × {D:.0f} × {H:.0f} mm", "note")

    # Header
    svg.rect(15, header_h - 10, total_w - 30, row_h, "panel")
    for i, label in enumerate(col_labels):
        svg.text(col_x[i] + 20, header_h + 8, label, "label-sm")

    # Rows
    total_area = 0
    for idx, (name, w, h, qty, notes) in enumerate(panels):
        y = header_h + row_h + idx * row_h
        if idx % 2 == 0:
            svg.rect(15, y, total_w - 30, row_h, cls="")  # no fill class needed
            svg.elements.append(f'<rect x="15" y="{y:.1f}" width="{total_w-30}" height="{row_h}" fill="#f8f8f4"/>')
        svg.text(col_x[0], y + 20, name, "label-sm")
        svg.text(col_x[1] + 20, y + 20, f"{w:.0f}", "label-sm")
        svg.text(col_x[2] + 20, y + 20, f"{h:.0f}", "label-sm")
        svg.text(col_x[3] + 20, y + 20, str(qty), "label-sm")
        svg.text(col_x[4] + 20, y + 20, f"{wall:.0f}", "label-sm")
        svg.text(col_x[5] + 20, y + 20, notes, "label-sm")
        total_area += w * h * qty

    # Summary
    sy = header_h + row_h + len(panels) * row_h + 20
    svg.text(20, sy, f"Total panels: {len(panels)}  |  Total panel area: {total_area/1e6:.2f} m²  "
             f"|  Plywood volume: {total_area * wall / 1e9:.2f} L", "note")
    svg.text(20, sy + 18, "NOTE: Divider plate and shelf braces are cut to fit the internal cavity "
             f"({p['w_in']:.0f} × {p['d_in']:.0f} mm). Measure actual internal dims before cutting.", "note")
    svg.text(20, sy + 34, "All dimensions from cabinet.scad (single source of truth). "
             "Verify driver cutouts against datasheet before cutting.", "note")

    outpath = os.path.join(outdir, "cut_list.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_assembly_dims(p, outdir):
    """Assembly measurement drawing — overall dims, driver heights, spacing."""
    W, D, H = p["W"], p["D"], p["H"]
    wall = p["wall"]
    rr = p["round_r"]
    scale = 0.35
    margin = 100

    # Two views: front elevation + side elevation
    view_w = max(W, D) * scale + margin
    view_h = H * scale + margin
    dw = view_w * 2 + 40
    dh = view_h + 80
    svg = SVG(dw, dh, "Assembly Dimensions")

    svg.text(dw / 2, 25, "Mk3 Cabinet — Assembly Measurement Drawing", "title-text")

    # --- Front elevation (left) ---
    fx = margin / 2
    fy = 60
    fw = W * scale
    fh = H * scale

    svg.rrect(fx, fy, fw, fh, rr * scale, "panel")
    svg.text(fx + fw / 2, fy - 8, "FRONT", "label")

    def fz(z):
        return fy + fh - z * scale

    fcx = fx + fw / 2

    # Mid (top)
    mid_r = p["mid_face_d"] / 2 * scale
    svg.circle(fcx, fz(p["mid_z"]), mid_r, "cutout")
    svg.text(fcx, fz(p["mid_z"]) - mid_r - 8, "MID", "label-sm")

    # Tweeter (below)
    tw_w = p["wg_flange_w"] * scale
    tw_h = p["wg_flange_h"] * scale
    svg.rrect(fcx - tw_w / 2, fz(p["tw_z"]) - tw_h / 2, tw_w, tw_h, p["wg_flange_r"] * scale, "cutout")
    svg.text(fcx, fz(p["tw_z"]) + tw_h / 2 + 12, "WG", "label-sm")

    # Dimensions on front view
    svg.dim_h(fx, fx + fw, fy + fh + 10, offset=20, label=f"W={W:.0f}")
    svg.dim_v(fy, fy + fh, fx, offset=20, label=f"H={H:.0f}")
    svg.dim_v(fy + fh, fz(p["mid_z"]), fx - 12, offset=35, label=f"{p['mid_z']:.0f}")
    svg.dim_v(fy + fh, fz(p["tw_z"]), fx - 12, offset=60, label=f"{p['tw_z']:.0f}")
    svg.dim_v(fz(p["mid_z"]), fz(p["tw_z"]), fcx + max(mid_r, tw_w / 2) + 12, offset=15,
              label=f"cc={p['cc']:.0f}")

    # --- Side elevation (right) ---
    sx = view_w + 40
    sy = 60
    sw = D * scale
    sh = H * scale

    svg.rect(sx, sy, sw, sh, "panel")
    svg.text(sx + sw / 2, sy - 8, "SIDE", "label")

    def sz(z):
        return sy + sh - z * scale

    scx = sx + sw / 2

    # Woofer
    woofer_r = p["woofer_cut_d"] / 2 * scale
    svg.circle(scx, sz(p["woofer_z"]), woofer_r, "cutout")
    svg.text(scx, sz(p["woofer_z"]) - woofer_r - 8, "12SW", "label-sm")

    # Divider (tilted line)
    div_z_front = p["mid_z"] - 80  # approximate front edge
    div_z_rear = div_z_front + p["d_in"] * math.tan(math.radians(p["divider_tilt"]))
    # Draw tilted line across the side view
    front_y = sz(div_z_front)
    rear_y = sz(div_z_rear)
    svg.line(sx + 3, front_y, sx + sw - 3, rear_y, "center-line")
    svg.text(sx + sw + 8, (front_y + rear_y) / 2, f"divider {p['divider_tilt']:.0f}°", "label-sm")

    # Shelf braces
    for shz in p["shelf_zs"]:
        shz_y = sz(shz)
        svg.line(sx + 5, shz_y, sx + sw - 5, shz_y, "center-line")

    # Dimensions on side view
    svg.dim_h(sx, sx + sw, sy + sh + 10, offset=20, label=f"D={D:.0f}")
    svg.dim_v(sy, sy + sh, sx, offset=20, label=f"H={H:.0f}")
    svg.dim_v(sy + sh, sz(p["woofer_z"]), sx - 12, offset=35, label=f"{p['woofer_z']:.0f}")

    # Notes at bottom
    ny = sy + sh + 50
    svg.text(margin / 2, ny,
             f"Internal: {p['w_in']:.0f} × {p['d_in']:.0f} × {p['h_in']:.0f} mm  |  "
             f"Wall: {wall:.0f} mm  |  Roundover: R{rr:.0f}", "note")
    svg.text(margin / 2, ny + 16,
             f"Driver heights: MID z={p['mid_z']:.0f}  WG/TW z={p['tw_z']:.0f}  "
             f"Woofer z={p['woofer_z']:.0f}  |  C-C mid/tw: {p['cc']:.0f} mm", "note")
    svg.text(margin / 2, ny + 32,
             f"Shelf braces at z={[int(z) for z in p['shelf_zs']]}  |  "
             f"Divider tilt: {p['divider_tilt']:.0f}°", "note")

    outpath = os.path.join(outdir, "assembly_dims.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


# ============================================================
#  Per-panel cut drawings
# ============================================================
def _panel_base(svg, p, w_mm, h_mm, title, subtitle, scale=0.5, margin=80):
    """Set up a standard panel drawing with title and return (px, py, pw, ph, scale)."""
    dw = w_mm * scale + 2 * margin
    dh = h_mm * scale + 2 * margin + 30
    svg.w = int(dw)
    svg.h = int(dh)
    svg.elements = []

    px = margin
    py = margin + 30
    pw = w_mm * scale
    ph = h_mm * scale

    svg.text(dw / 2, 20, title, "title-text")
    svg.text(dw / 2, 38, subtitle, "note")
    return px, py, pw, ph, scale


def _dim_outer(svg, px, py, pw, ph, w_label, h_label):
    """Add standard outer dimension lines to a panel."""
    svg.dim_h(px, px + pw, py + ph + 10, offset=25, label=w_label)
    svg.dim_v(py, py + ph, px, offset=25, label=h_label)


def gen_panel_front_baffle(p, outdir):
    """Front baffle as a standalone per-panel cut drawing."""
    svg = SVG(100, 100)
    px, py, pw, ph, sc = _panel_base(
        svg, p, p["W"], p["H"],
        "Front Baffle — Cut Drawing",
        f"{p['W']:.0f} × {p['H']:.0f} mm, {p['wall']:.0f} mm ply, R{p['round_r']:.0f} front edges"
    )
    svg.rrect(px, py, pw, ph, p["round_r"] * sc, "panel")

    cx = px + pw / 2
    def z_to_y(z): return py + ph - z * sc

    # Midrange
    mid_cut_r = p["mid_cut_d"] / 2 * sc
    mid_face_r = p["mid_face_d"] / 2 * sc
    mid_y = z_to_y(p["mid_z"])
    svg.circle(cx, mid_y, mid_face_r, "rebate")
    svg.circle(cx, mid_y, mid_cut_r, "cutout")
    svg.center_cross(cx, mid_y, 8)
    for i in range(p["mid_n_holes"]):
        a = math.radians(p["mid_bolt_offset"] + i * 360 / p["mid_n_holes"])
        hx = cx + (p["mid_bcd"] / 2) * math.cos(a) * sc
        hy = mid_y + (p["mid_bcd"] / 2) * math.sin(a) * sc
        svg.circle(hx, hy, 1.5, "pilot")
    svg.text(cx, mid_y - mid_face_r - 10,
             f"Ø{p['mid_cut_d']:.1f} cut  Ø{p['mid_face_d']:.1f} rebate  {p['mid_n_holes']}×Ø{p['mid_hole_d']:.1f}",
             "label-sm")

    # Waveguide
    tw_y = z_to_y(p["tw_z"])
    wg_w = (p["wg_flange_w"] + 1.0) * sc
    wg_h = (p["wg_flange_h"] + 1.0) * sc
    svg.rrect(cx - wg_w / 2, tw_y - wg_h / 2, wg_w, wg_h, p["wg_flange_r"] * sc, "rebate")
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            hx = cx + sx * (p["wg_bcd_x"] / 2) * sc
            hy = tw_y + sy * (p["wg_bcd_y"] / 2) * sc
            svg.circle(hx, hy, 1.5, "pilot")
    svg.center_cross(cx, tw_y, 8)
    svg.text(cx, tw_y + wg_h / 2 + 12,
             f"{p['wg_flange_w']:.0f}×{p['wg_flange_h']:.0f} recess  4×Ø3 pilot", "label-sm")

    # Dimensions
    _dim_outer(svg, px, py, pw, ph, f"W={p['W']:.0f}", f"H={p['H']:.0f}")
    svg.dim_v(py + ph, mid_y, px - 12, offset=18, label=f"z={p['mid_z']:.0f}")
    svg.dim_v(py + ph, tw_y, px - 12, offset=42, label=f"z={p['tw_z']:.0f}")
    svg.line(cx, py - 5, cx, py + ph + 5, "center-line")

    outpath = os.path.join(outdir, "panel_front_baffle.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_panel_back(p, outdir):
    """Back panel — simple rectangle, no cutouts."""
    svg = SVG(100, 100)
    px, py, pw, ph, sc = _panel_base(
        svg, p, p["W"], p["H"],
        "Back Panel — Cut Drawing",
        f"{p['W']:.0f} × {p['H']:.0f} mm, {p['wall']:.0f} mm ply, square edges"
    )
    svg.rect(px, py, pw, ph, "panel")
    _dim_outer(svg, px, py, pw, ph, f"W={p['W']:.0f}", f"H={p['H']:.0f}")
    svg.text(px + pw / 2, py + ph / 2, "No cutouts", "label-sm")

    outpath = os.path.join(outdir, "panel_back.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_panel_side(p, outdir, side="left"):
    """Side panel with woofer cutout. Left and right are identical (opposed mounting)."""
    label = "Side Panel LEFT" if side == "left" else "Side Panel RIGHT"
    filename = f"panel_side_{side}.svg"
    svg = SVG(100, 100)
    px, py, pw, ph, sc = _panel_base(
        svg, p, p["D"], p["H"],
        f"{label} — Cut Drawing",
        f"{p['D']:.0f} × {p['H']:.0f} mm, {p['wall']:.0f} mm ply, woofer on {'left' if side=='left' else 'right (opposed)'} face"
    )
    svg.rect(px, py, pw, ph, "panel")

    cx = px + pw / 2
    def z_to_y(z): return py + ph - z * sc
    wz = z_to_y(p["woofer_z"])

    cut_r = p["woofer_cut_d"] / 2 * sc
    frame_r = p["woofer_frame_d"] / 2 * sc
    svg.circle(cx, wz, frame_r, "rebate")
    svg.circle(cx, wz, cut_r, "cutout")
    svg.center_cross(cx, wz, 10)
    for i in range(p["woofer_n_holes"]):
        a = math.radians(i * 360 / p["woofer_n_holes"])
        hx = cx + (p["woofer_bcd"] / 2) * math.cos(a) * sc
        hy = wz + (p["woofer_bcd"] / 2) * math.sin(a) * sc
        svg.circle(hx, hy, 1.5, "pilot")
    svg.text(cx, wz - frame_r - 10,
             f"Ø{p['woofer_cut_d']:.0f} cut  Ø{p['woofer_frame_d']:.0f} frame  {p['woofer_n_holes']}×Ø{p['woofer_hole_d']:.1f} on Ø{p['woofer_bcd']:.0f} BCD",
             "label-sm")

    # Shelf brace positions
    for sz in p["shelf_zs"]:
        sy = z_to_y(sz)
        svg.line(px + 5, sy, px + pw - 5, sy, "center-line")
        svg.text(px + pw + 8, sy + 3, f"shelf z={sz:.0f}", "label-sm")

    _dim_outer(svg, px, py, pw, ph, f"D={p['D']:.0f}", f"H={p['H']:.0f}")
    svg.dim_v(py + ph, wz, px - 12, offset=18, label=f"z={p['woofer_z']:.0f}")
    svg.line(cx, py - 5, cx, py + ph + 5, "center-line")

    outpath = os.path.join(outdir, filename)
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_panel_top_bottom(p, outdir, which="top"):
    """Top or bottom panel — rectangle with rounded front edge (top/bottom follow the front roundover)."""
    label = f"{which.title()} Panel"
    filename = f"panel_{which}.svg"
    svg = SVG(100, 100)
    px, py, pw, ph, sc = _panel_base(
        svg, p, p["W"], p["D"],
        f"{label} — Cut Drawing",
        f"{p['W']:.0f} × {p['D']:.0f} mm, {p['wall']:.0f} mm ply, R{p['round_r']:.0f} front edge"
    )
    # Rounded front edge (one side)
    svg.rrect(px, py, pw, ph, p["round_r"] * sc, "panel")
    _dim_outer(svg, px, py, pw, ph, f"W={p['W']:.0f}", f"D={p['D']:.0f}")
    svg.text(px + pw / 2, py + ph / 2, "No cutouts", "label-sm")

    outpath = os.path.join(outdir, filename)
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_panel_divider(p, outdir):
    """Divider plate — full-width tilted plate, cut to fit internal cavity."""
    w_in = p["w_in"]
    d_in = p["d_in"]
    svg = SVG(100, 100)
    px, py, pw, ph, sc = _panel_base(
        svg, p, w_in, d_in,
        "Divider Plate — Cut Drawing",
        f"{w_in:.0f} × {d_in:.0f} mm, {p['wall']:.0f} mm ply, tilted {p['divider_tilt']:.0f}° in cabinet"
    )
    svg.rect(px, py, pw, ph, "panel")

    # Show tilt annotation: front edge is low, rear edge is high
    tilt_note = f"Front edge sits at z={p['mid_z'] - 80:.0f} mm, rises {p['divider_tilt']:.0f}° toward rear"
    svg.text(px + pw / 2, py + ph / 2, "Cut to internal cavity shape\n(front edge follows rounded side walls)", "label-sm")
    svg.text(px + pw / 2, py + ph + 25, tilt_note, "note")

    _dim_outer(svg, px, py, pw, ph, f"int W={w_in:.0f}", f"int D={d_in:.0f}")

    # Tilt indicator line
    mid_y = py + ph / 2
    svg.line(px + 10, mid_y + 15, px + pw - 10, mid_y - 15, "center-line")
    svg.text(px + pw / 2, mid_y - 20, f"tilt {p['divider_tilt']:.0f}°", "label-sm")

    outpath = os.path.join(outdir, "panel_divider.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath


def gen_panel_shelf_brace(p, outdir):
    """Shelf brace — ring shape (outer = internal cavity, inner = outer - rim width)."""
    w_in = p["w_in"]
    d_in = p["d_in"]
    rim = p["shelf_rim"]
    rr = p["round_r"]
    svg = SVG(100, 100)

    # Need to show outer ring + inner cutout
    scale = 0.5
    margin = 80
    dw = w_in * scale + 2 * margin
    dh = d_in * scale + 2 * margin + 50
    svg.w = int(dw)
    svg.h = int(dh)
    svg.elements = []

    svg.text(dw / 2, 20, "Shelf Brace ×3 — Cut Drawing", "title-text")
    svg.text(dw / 2, 38,
             f"Outer: {w_in:.0f} × {d_in:.0f} mm (internal cavity)  Rim: {rim:.0f} mm  "
             f"Thickness: {p['wall']:.0f} mm  Qty: 3 (z={[int(z) for z in p['shelf_zs']]})",
             "note")

    px = margin
    py = margin + 30
    pw = w_in * scale
    ph = d_in * scale

    # Outer ring (rounded corners matching internal cavity)
    svg.rrect(px, py, pw, ph, rr * scale, "panel")
    # Inner cutout (inset by rim)
    inner_w = (w_in - 2 * rim) * scale
    inner_h = (d_in - 2 * rim) * scale
    inner_x = px + rim * scale
    inner_y = py + rim * scale
    svg.rrect(inner_x, inner_y, inner_w, inner_h, max(0, (rr - rim)) * scale, "cutout")

    svg.text(px + pw / 2, py + ph / 2, f"Open centre\n{w_in - 2*rim:.0f} × {d_in - 2*rim:.0f} mm", "label-sm")

    # Dimensions
    svg.dim_h(px, px + pw, py + ph + 10, offset=25, label=f"outer {w_in:.0f}")
    svg.dim_v(py, py + ph, px, offset=25, label=f"outer {d_in:.0f}")
    svg.dim_h(inner_x, inner_x + inner_w, py + ph + 35, offset=20,
              label=f"inner {w_in - 2*rim:.0f}")

    outpath = os.path.join(outdir, "panel_shelf_brace.svg")
    with open(outpath, "w") as f:
        f.write(svg.render())
    return outpath



def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate cabinet dimensioned drawings (SVG)")
    parser.add_argument("--outdir", default=os.path.join(_REPO_ROOT, "assets", "drawings"),
                        help="Output directory for SVG files")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    p = load_params()

    print(f"Cabinet: {p['W']:.0f} × {p['D']:.0f} × {p['H']:.0f} mm, {p['wall']:.0f} mm walls")
    print(f"Mid z={p['mid_z']:.0f}, TW z={p['tw_z']:.0f}, Woofer z={p['woofer_z']:.0f}, cc={p['cc']:.0f}")
    print()

    files = []
    # Overview drawings
    files.append(gen_front_baffle(p, args.outdir))
    files.append(gen_side_panel(p, args.outdir))
    files.append(gen_cut_list(p, args.outdir))
    files.append(gen_assembly_dims(p, args.outdir))
    # Per-panel cut drawings
    files.append(gen_panel_front_baffle(p, args.outdir))
    files.append(gen_panel_back(p, args.outdir))
    files.append(gen_panel_side(p, args.outdir, "left"))
    files.append(gen_panel_side(p, args.outdir, "right"))
    files.append(gen_panel_top_bottom(p, args.outdir, "top"))
    files.append(gen_panel_top_bottom(p, args.outdir, "bottom"))
    files.append(gen_panel_divider(p, args.outdir))
    files.append(gen_panel_shelf_brace(p, args.outdir))

    for f in files:
        print(f"  ✓ {os.path.basename(f)}")
    print(f"\n{len(files)} SVG files written to {args.outdir}/")


if __name__ == "__main__":
    main()
