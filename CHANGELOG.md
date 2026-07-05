# Changelog

All notable design changes for the Mk3 Reference Loudspeaker are documented here.

## v9 (in progress) — 18W/4424G00 midrange, mid-over-waveguide layout

### Changed

- **Midrange driver changed** from ScanSpeak 15W/4434G00 to **ScanSpeak
  18W/4424G00** (Discovery, 18 cm, 4 Ω): Fs 49 Hz, Qts 0.38, Vas 24.1 L,
  Sd 137 cm², 91 dB — sensitivity now within 0.5 dB of the SB26STAC.
  Drawing dims: Ø179.2 faceplate, Ø144.3 cutout, Ø167 BCD (6×Ø5.3),
  72.2 mm depth. Parametric model: `cad/midrange.scad`; datasheet:
  `assets/datasheets/18W-4424G00.pdf` + `.md`. See DD-016.
- **Front layout flipped**: the midrange now sits at the TOP of the baffle
  with the waveguide BELOW it, and the full-width tilted divider plate runs
  between them. The mid chamber is the top section of the cabinet (~11 L
  net — near the 18W's 13 L closed-box recommendation, predicted Qtc ~0.68,
  Fc ~88 Hz), and the bass volume below grows to **~65 L net** (predicted
  Qtc ~0.80, Fc ~41 Hz before Linkwitz Transform).
- **Mid/tweeter c-c increased to 165 mm** — the physical minimum with the
  Ø179.2 mid faceplate and the 143 mm waveguide flange both flush-recessed
  (DD-011's 140 mm target is not reachable with these parts).
- **Cabinet external width documented as 320 mm** (spec tables previously
  said 300 mm; 256 mm internal cannot fit two opposed 136 mm-deep
  12SW-4HE). Front roundovers documented as R19 (R50 leaves only 220 mm
  flat baffle — narrower than the 242 mm waveguide flange).

### Added

- **`cad/cabinet.scad` rewritten** around real datasheet dimensions with
  automatic volume calculation and mechanical self-checks (echoed in litres /
  mm on every render, updating with any parameter change):
  - Bass and mid chamber volume in litres + predicted sealed Qtc/Fc from
    datasheet T-S values; WARNINGs on collisions or missed targets.
  - **Waveguide front-mounted**: flange recessed flush into the front baffle
    face (matching its countersunk front screws), with a tapered body
    clearance hole derived from the waveguide profile exports.
  - **Divider plate height derived** from the midrange basket envelope
    (tilt 12°, front low); braces are ring shelves with open centres
    (single connected bass air volume), notched for the woofer baskets.
  - **Push-push magnet gap computed** from datasheet depths: ~48 mm at
    276 mm internal width (not ~4 mm as previously noted); the coupling
    block length derives from the gap.
  - Flush-mount rebates, pilot holes on all datasheet bolt circles, and the
    real `cad/midrange.scad` driver model in assembly renders.
- `assets/datasheets/15W-4434G00.md` corrected: the earlier mechanical
  table (104 / 95 / 45.1 / Ø72) did not match the official drawing
  (Ø149.3 faceplate, Ø136.5 BCD, 61.9 mm depth) — the Ø72 figure had
  produced an impossible midrange cutout in earlier cabinet models.

### Notes

- Net bass volume ~65 L vs the 75 L docs target (docs/09's own estimate was
  ~66 L) — Qtc ~0.80 / Fc ~41 Hz still works with the Linkwitz Transform,
  at some excursion-headroom cost. Verify in simulation before build.
- 1100 Hz LR4 mid/tweeter crossover is unchanged but must be re-validated
  for the larger 18 cm cone (directivity at the top of the mid band) and
  the 165 mm c-c (vertical lobing) once parts are measured.

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
