# CAD

Parametric CAD models for the Mk3 Reference Loudspeaker.

## `waveguide.scad`

A fully parametric **OpenSCAD** model of the tweeter waveguide for the
SB Acoustics **SB26STAC-C000-4** — an oblate-spheroid (OS) constant-directivity
bore with a tangent rolled mouth. The SB26STAC is a conventional 26 mm soft
dome tweeter with **no built-in horn**, so the OS bore starts directly at the
dome (throat Ø28 mm = dome + ~1 mm surround per side) rather than at a horn
exit. The waveguide mounts **behind the cabinet baffle** via a 5 mm-thick
rectangular flange; the cabinet has an elliptical hole through the baffle
exposing the waveguide mouth from the front. Visually flush with the baffle
from the outside (the waveguide itself sits inside the cabinet, terminating at
the baffle back face).

- Mouth ≈ **~289 × 172 mm**, acoustic depth **90 mm** (`D_os + Lr` = 65 + 25),
  tube physical extent **z = -5 .. 85 mm** (overlaps the back plate by 5 mm at
  the throat end, ends flush with the baffle back face at z=85). Total part
  depth **98 mm** including back plate.
- Asymmetric coverage ≈ **100° horizontal / 64° vertical** (θh=50°, θv=32°).
- Horizontal pattern control down to ≈ **1620 Hz**.
- Crossover target: **1100 Hz LR4** (the SB26STAC's Fs=750 Hz gives a 350 Hz
  margin — no distortion-test gate required).

### Critical tunables (verify before printing)

- `throat_d` (28 mm from SB26STAC datasheet + surround estimate) **must be
  caliper-verified on the physical unit before final print** — this sets whether
  you get a throat resonance. Print throat test pieces against the physical
  tweeter first. SB Acoustics does not supply a STEP file for this tweeter.
- `Lr` (default **25 mm**) — depth of the mouth roundover. Larger = gentler
  baffle blend + less mouth diffraction, at the cost of total waveguide depth.
  With `Lr = 25` the tube is 90 mm long.
- `protrusion` (default **0 mm**) — cylindrical extension past the flange
  front face. With `protrusion = 0` the waveguide tube ends **flush with the
  cabinet baffle back face** (z = 85) — the baffle has a through-cutout
  exposing the waveguide mouth from the outside. Set higher than 0 only if
  you want the tube to physically extend *through* the baffle past the
  outside face (then keep in sync with `cabinet.scad`'s `wall = 22;`).
- `flange_thick` (default **5 mm**) — thickness of the screw-mounting flange
  sitting against the cabinet baffle back. 5 mm is plenty for wood-screw
  mounting into the baffle; the baffle cutout in `cabinet.scad` derives its
  recess depth from this value automatically (`wg_flange_t_fn()`).
- `corner_r` (default **4 mm**) — flange corner radius. Kept tight so the
  flange fits cleanly in the cabinet cutout with no rounded-edge gap; bump
  up if you prefer a softer cabinet cutout.
- The mouth roundover must blend smoothly into the cabinet's baffle; a step
  there re-introduces diffraction. See
  [`../simulations/waveguide_profile.py`](../simulations/waveguide_profile.py)
  and `plots/waveguide_termination.png`.

### Building

Open in OpenSCAD, render with F6, export STL. `$fn` is high for export — drop to
64 while iterating. The model echoes the computed mouth size and depth on render.

### CI renders and STL downloads

The [`cad-render`](../.github/workflows/cad-render.yml) workflow runs automatically
on every push that changes a `.scad` file. It:

1. Renders both models to STL (waveguide + cabinet)
2. Renders 3 preview PNGs per model and commits them to [`../assets/renders/`](../assets/renders/)
3. Creates a [GitHub Release](../../../releases/latest) with the STL files as downloadable assets

| Preview | Description |
|---------|-------------|
| **Waveguide (6 views)** ||
| ![mouth](../assets/renders/waveguide_mouth.png) | Mouth (front view) |
| ![rear](../assets/renders/waveguide_rear.png) | Rear / back plate + mounting |
| ![side](../assets/renders/waveguide_side.png) | Side profile (OS bore curve) |
| ![top](../assets/renders/waveguide_top.png) | Top (throat view) |
| ![iso](../assets/renders/waveguide_iso.png) | Isometric 3/4 view |
| ![cutaway](../assets/renders/waveguide_cutaway.png) | Half-section cutaway |
| **Cabinet (10 views)** ||
| ![front](../assets/renders/cabinet_front.png) | Front (baffle with driver placeholders) |
| ![rear](../assets/renders/cabinet_rear.png) | Rear panel |
| ![left](../assets/renders/cabinet_left.png) | Left side (woofer visible) |
| ![right](../assets/renders/cabinet_right.png) | Right side (woofer visible) |
| ![top](../assets/renders/cabinet_top.png) | Top view |
| ![bottom](../assets/renders/cabinet_bottom.png) | Bottom view |
| ![exterior](../assets/renders/cabinet_exterior.png) | 3/4 exterior perspective |
| ![cutaway](../assets/renders/cabinet_cutaway.png) | Half-section cutaway (internals) |
| ![assembly](../assets/renders/cabinet_assembly.png) | Assembly (with waveguide) |
| ![full](../assets/renders/cabinet_full_cutaway.png) | Full assembly cutaway (all drivers) |

These are **design-direction geometry, not validated by measurement.** Mouth
size, throat and coverage must be confirmed against SB26STAC-in-waveguide
measurements.

## `cabinet.scad`

A fully parametric **OpenSCAD** model of the enclosure — the cabinet
geometry for the repo.

- External **300 × 370 × 1080 mm**, 22 mm walls, **R50** front vertical
  roundovers (rear edges square).
- **Side-mounted push-push** woofer cut-outs, opposed at the same height
  (~520 mm), with the rigid coupling block between the magnets (see
  [Chapter 8](../docs/08_push_push_bass.md)).
- Front baffle cut-outs for the **waveguide** (elliptical mouth + rounded flange
  recess, matched to `waveguide.scad`) and the **15W/4434G00** midrange at
  **~150 mm c-c**.
- `show_internals = true` renders a cut-away with the sealed mid chamber, a
  window brace at the woofer line and the bass/mid shelf brace.
- `show_waveguide = true` drops the waveguide model into the baffle (it `use`s
  `waveguide.scad`, so keep both files together). The waveguide is seated
  with its mouth poking `wg_through` (default 0.3 mm) **through** the baffle. Its
  seating depth is read from the waveguide via `wg_front_z()`, so it can't drift
  out of sync.

### Assembly and the coincident-face rule

OpenSCAD cannot show a hole or a join where two surfaces sit at exactly the same
plane — the boolean becomes non-manifold and renders as a flickering "smear"
instead of a clean opening. So every cutter here overshoots the panel it pierces
by `eps` (0.1 mm), and when the waveguide is seated its flush mouth is pushed
`wg_through` mm proud of the baffle so the two solids genuinely overlap. Keep
`wg_through > 0` (≥ 0.01 mm); set it to ~0.3 mm for a reliable preview. The
overlap is cosmetic for visualisation — it is not a real interference fit.

### Critical tunables (verify before cutting)

- `woofer_z`, `tw_z`, `mid_z` (driver heights) and `cc` set the baffle layout;
  confirm against the real flanges and the bracing layout
  ([Chapter 10](../docs/10_bracing.md)).
- The mid-chamber box here is **representational** — its net volume must be
  confirmed at **~5.7 L** from the solid model
  ([Chapter 9](../docs/09_volume_calculations.md)) before it is trusted.
- Cut-out diameters (woofer 185, mid 124 mm) are estimates pending datasheet
  templates.

This is a **dimension-check / visualisation model, not a cut list.**
