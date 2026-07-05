# Changelog

All notable design changes for the Mk3 Reference Loudspeaker are documented here.

## v8 (unreleased) — cabinet CAD rework: datasheet-driven, self-checking

### Changed

- **`cad/cabinet.scad` rewritten** around real datasheet dimensions with
  automatic volume calculation and mechanical self-checks (echoed in litres /
  mm on every render, updating with any parameter change):
  - **Midrange cutout corrected** from Ø72 to **~Ø123 (estimate)**. The
    Ø72 value came from a mis-extracted datasheet table; the real ScanSpeak
    15W/4434G00 drawing shows Ø149.3 faceplate, Ø136.5 mounting BCD (4×Ø5.3),
    61.9 mm depth, 4.8 mm flange, Ø114 basket — a Ø72 hole cannot pass the
    Ø114 basket. `assets/datasheets/15W-4434G00.md` corrected accordingly.
  - **Waveguide is now front-mounted**: flange recessed flush into the front
    baffle face (matching its countersunk front screws), with a body
    clearance hole derived from the waveguide profile exports.
  - **Divider plate height is derived** from the midrange basket envelope
    (tilt 12°, front low) and checked against the woofer cutout; braces are
    ring shelves with open centres (single connected bass air volume) and
    are notched for the woofer baskets.
  - **Push-push magnet gap computed** from datasheet depths: ~48 mm at
    276 mm internal width (not ~4 mm as previously noted); the coupling
    block length now derives from the gap.
  - Flush-mount rebate for the 15W faceplate, pilot holes on all datasheet
    bolt circles, driver placeholders at datasheet envelopes.

### Notes

- The self-check currently reports **net bass volume ~45 L vs the 75 L
  target** and **mid chamber ~31 L vs the 5.7 L target** for the modeled
  full-width-divider layout — the documented targets and the cabinet layout
  do not close yet (see docs/09). Options: mid sub-enclosure, taller/wider
  cabinet, or revised alignment targets.
- External width is modeled at **320 mm** (docs tables still say 300 mm —
  256 mm internal cannot fit two opposed 136 mm-deep 12SW-4HE).

## v8 — GRS 12SW-4HE woofer upgrade

### Changed

- **Woofer upgraded** from GRS 8SW-4HE-8 (8") to **GRS 12SW-4HE (12" high
  excursion)**. Push-push configuration retained (2 per enclosure, side-mounted).
  The 8SW remains in the repo as a historical comparison driver.
- **Bass volume** increased from ~69 L (total) to **~75 L under the divider plate**.
- **Sealed alignment** changed: Fc ~39 Hz, Qtc ~0.76 (was Fc ~34.5 Hz, Qtc ~0.62).
- **Linkwitz Transform** updated: Fc 39.0→28 Hz, Qtc 0.76→0.707 (was 47.2→28 Hz,
  0.63→0.707).
- **Woofer cutout** increased from 185 mm to **284 mm**.
- **Cabinet CAD** (`cad/cabinet.scad`) updated for 12SW frame (~332 mm overall,
  ~136 mm mounting depth, 284 mm cutout, coupling block h=20/r=55 mm).

### Added

- New key 12SW T/S parameters: Fs 22 Hz, Qts 0.43, Vas 80.4 L, Sd 504 cm²,
  Xmax 12.5 mm (Klippel verified), Bl 16.2 Tm, sensitivity 84.5 dB, 250 W,
  ~€75 per driver.
- **Max SPL @ 30 Hz: +16 dB** over the previous 8SW design.
- **Displacement: 12.6 cm³** (was 2.0 cm³) — 6.3× more, from the larger Sd and
  much higher Xmax.

### Notes

- Opposed magnet clearance is tight (~4 mm gap at 276 mm internal width vs ~22 mm
  for the old 8SW). The coupling block and basket depth must be verified before
  cutting panels.
- Design decisions recorded as DD-015.

## v7 — SB26STAC tweeter, 1100 Hz crossover

### Added

- **SB Acoustics SB26STAC-C000-4** conventional dome tweeter selected as the
  tweeter. Fs 750 Hz, 0.6 mm Xmax, 91.5 dB, 4 Ω.
- **1100 Hz LR4** mid/tweeter crossover selected.
- **Custom non-horn-loaded waveguide** (`cad/waveguide.scad`) — the SB26STAC is a
  conventional dome and is not horn-loaded, so it uses a waveguide geometry that
  provides directivity control without relying on a built-in horn.
- **+8.1 dB excursion headroom** at the crossover frequency — the lower Fs
  (750 Hz) and 1100 Hz crossover place the operating point at ~1.47 × Fs,
  reducing distortion/excursion risk.
- New simulation scripts: `system_response_realistic.py`,
  `spinorama_estimate.py`, `crossover_optimization.py`,
  `tweeter_comparison.py` (see `simulations/`).
