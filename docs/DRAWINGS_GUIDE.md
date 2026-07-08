# SVG Drawing Generation Guide

## Overview

The `scripts/generate_drawings.py` script generates dimensioned technical drawings in SVG format from the OpenSCAD CAD models. These drawings are used for:

- Cabinet panel cut lists and assembly dimensions
- Driver cutout and hole-position layouts
- Build documentation and CNC routing templates

All drawings are parametric — they parse dimensions directly from the SCAD source files, so they stay in sync with the CAD model automatically.

## Generated Drawings

| Drawing | Purpose | Source |
|---------|---------|--------|
| `front_baffle.svg` | Front baffle with midrange + tweeter cutouts, rebate, pilot holes | `cabinet.scad`, `midrange.scad`, `waveguide.scad` |
| `side_panel.svg` | Side panel with woofer cutout + pilot holes | `cabinet.scad` |
| `cut_list.svg` | Panel cut list with dimensions + quantities | `cabinet.scad` |
| `assembly_dims.svg` | Assembly measurement drawing (heights, spacing, edges) | `cabinet.scad` |
| `panel_*.svg` (7 files) | Individual panel cut drawings (front baffle, sides, top, bottom, back, divider, shelf brace) | `cabinet.scad` |

All SVGs are written to `assets/drawings/`.

## Running the Script

```bash
python3 scripts/generate_drawings.py                    # write SVGs to assets/drawings/
python3 scripts/generate_drawings.py --outdir /tmp/     # custom output directory
```

## How It Works

### 1. SCAD Parameter Parsing

The script reads OpenSCAD files and extracts numeric variables using regex:

```python
_parse_var(text, "W")      # Extract: W = 300;
_parse_list(text, "shelf_zs")  # Extract: shelf_zs = [200, 400, 600];
```

This keeps drawings synchronized with the CAD model — if you change `W = 300` to `W = 320` in `cabinet.scad`, the next run regenerates all drawings with the new width.

### 2. SVG Class

A lightweight SVG builder with primitives for technical drawings:

```python
svg = SVG(width, height, title)
svg.rect(x, y, w, h, cls="panel")           # Rectangle
svg.circle(cx, cy, r, cls="cutout")         # Circle
svg.line(x1, y1, x2, y2, cls="dim-line")    # Line
svg.text(x, y, text, cls="label")           # Text
svg.text_wrap(x, y, text, cls="title-text") # Left-aligned text with word-wrap
svg.dim_h(x1, x2, y, label="100")           # Horizontal dimension line
svg.dim_v(x, y1, y2, label="50")            # Vertical dimension line
```

### 3. Text Wrapping

Titles and subtitles wrap automatically if they exceed the canvas width:

```python
svg.text_wrap(15, 25, "Mk3 Front Baffle — Cutout & Hole Layout", "title-text")
```

The method:
1. Estimates text width using `_est_text_width(text, font_size)`
2. Splits on word boundaries if text exceeds `max_width`
3. Renders each line at `x, y + i*line_height`
4. Returns the y position of the last line (for layout chaining)

Width estimation uses a simple model: `len(text) * font_size * 0.55`. This is a rough average for sans-serif fonts; it works well for most text but may underestimate very wide characters (W, M) or overestimate narrow ones (i, l).

### 4. Canvas Sizing

Canvas dimensions are determined purely by content:

```python
dw = W * scale + 2 * margin  # Width = scaled panel + margins
dh = H * scale + 2 * margin  # Height = scaled panel + margins
```

This replaced the old `_min_width()` logic, which tried to fit text by expanding the canvas. Now text wraps instead, keeping canvas size predictable.

## Styling

All drawings use a consistent CSS stylesheet embedded in the SVG:

```css
.panel { fill: #f5f0e0; stroke: #333; stroke-width: 1.5; }      /* Cabinet panels */
.cutout { fill: none; stroke: #c0392b; stroke-width: 1.2; }     /* Driver cutouts */
.rebate { fill: #faebe0; stroke: #e67e22; stroke-width: 1.0; }  /* Rebates/recesses */
.pilot { fill: #333; }                                           /* Pilot holes */
.dim-line { stroke: #2980b9; stroke-width: 0.8; fill: none; }   /* Dimension lines */
.dim-text { fill: #2980b9; font-family: sans-serif; font-size: 11px; } /* Dimension labels */
.title-text { fill: #222; font-family: sans-serif; font-size: 16px; font-weight: bold; }
.subtitle { fill: #555; font-family: sans-serif; font-size: 10px; }
```

Modify these in the `SVG.__init__()` method to change the appearance of all drawings at once.

## Viewing and Exporting

SVGs can be:

- **Opened in any browser** — right-click → Save As to download
- **Converted to PDF** — `rsvg-convert -f pdf drawing.svg -o drawing.pdf`
- **Converted to PNG** — `rsvg-convert -f png drawing.svg -o drawing.png`
- **Imported into CAM software** — most CNC routing software accepts SVG directly
- **Printed** — set scale to 1:1 (100%) in your PDF viewer

## Extending the Script

To add a new drawing:

1. Create a generator function:
   ```python
   def gen_my_drawing(p, outdir):
       """Generate my custom drawing."""
       svg = SVG(width, height, "My Drawing Title")
       # ... add elements ...
       svg.write(os.path.join(outdir, "my_drawing.svg"))
   ```

2. Call it from `main()`:
   ```python
   gen_my_drawing(p, outdir)
   ```

3. Run the script to generate the SVG.

## Troubleshooting

**Text is clipped or overlapping:**
- Check `_est_text_width()` — it may be underestimating width for your text
- Increase `max_width` in `text_wrap()` call
- Reduce font size in the CSS

**Dimensions are wrong:**
- Verify the SCAD variable names match what the script is parsing
- Check `load_params()` for the correct variable names
- Run with `--debug` to print parsed parameters (if implemented)

**SVG doesn't render correctly:**
- Validate the SVG: `xmllint --noout drawing.svg`
- Check that all text is properly escaped (& → &amp;, < → &lt;, > → &gt;)
- Ensure all coordinates are numeric (no NaN or Infinity)

## Future Improvements

- [ ] Character-width lookup table for more accurate text estimation
- [ ] Automatic scale calculation based on content
- [ ] Layer support (for CAM software)
- [ ] Tolerance/clearance annotations
- [ ] 3D isometric projections (for assembly drawings)
