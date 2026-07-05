# CAD Reference Files

3D geometry for the three mk3 drivers. Used as dimensional ground-truth for the
parametric OpenSCAD models in `cad/`.

## Files

| File | Driver | Type | Source |
|---|---|---|---|
| `18W-4424G00.STEP` | ScanSpeak 18W/4424G00 (midrange) | Manufacturer STEP | ScanSpeak |
| `18W-4424G00_ref.stl` | ScanSpeak 18W/4424G00 (midrange) | Reference STL | Derived from STEP |
| `SB26STAC-C000-4.stp` | SB Acoustics SB26STAC-C000-4 (tweeter) | STEP | GrabCAD user model (similar unit) |
| `SB26STAC-C000-4_ref.stl` | SB Acoustics SB26STAC-C000-4 (tweeter) | Reference STL | Derived from STEP |

## Notes

- The 18W/4424G00 STEP is the official ScanSpeak geometry.
- The SB26STAC STEP is from a GrabCAD user who modeled a similar SB Acoustics
  tweeter. Dimensions were verified against the SB26STAC-C000-4 datasheet and
  adjusted in the parametric SCAD model (`cad/SB26STAC-C000-4.scad`).
- The `_ref.stl` files are tessellated references derived from the STEP files,
  useful for quick visual checks without a STEP-capable CAD viewer.
- The GRS 12SW-4HE woofer has no manufacturer STEP file. Its parametric model
  (`cad/GRS-12SW-4HE.scad`) is built from the datasheet drawing only.
