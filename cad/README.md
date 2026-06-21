# CAD

Parametric CAD models for the Mk2 Reference Loudspeaker.

## `mk2_waveguide_os.scad`

A fully parametric **OpenSCAD** model of the tweeter waveguide for the
ScanSpeak **H2606/920000** — an oblate-spheroid (OS) constant-directivity bore
with a tangent rolled mouth that ends flush with the baffle.

- Mouth ≈ **211.7 × 121.0 mm**, total depth **75 mm** (the WG212 family).
- Asymmetric coverage ≈ **100° horizontal / 64° vertical**.
- Horizontal pattern control down to ≈ **1620 Hz**, i.e. designed to support a
  clean LR4 crossover to the 15W/4434G00 **near the waveguide's control limit**
  rather than well below it (this relates to the crossover discussion in
  [../REVIEW.md](../REVIEW.md) §C2 — the repo's current target is 1250 Hz LR4).

### Critical tunables (verify before printing)

- `throat_d` (28 mm placeholder) **must be matched to the real H2606 dome /
  faceplate exit** — this sets whether you get a throat resonance. Print throat
  test pieces against the physical tweeter first.
- The mouth roundover must blend smoothly into the cabinet's baffle roundover;
  a step there re-introduces diffraction.
- **Mouth-to-baffle termination:** the flange now sits *behind* the flush mouth
  plane so the bore meets the baffle with no forward lip (an earlier version left
  a sharp 90° edge there — a diffraction source). `Lr` controls the mouth
  roundover; increase it for an even gentler baffle blend at the cost of depth.
  See [`../simulations/waveguide_profile.py`](../simulations/waveguide_profile.py)
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
| ![mouth](../assets/renders/waveguide_mouth.png) | Waveguide mouth view |
| ![rear](../assets/renders/waveguide_rear.png) | Waveguide rear / back plate |
| ![exterior](../assets/renders/cabinet_exterior.png) | Cabinet exterior |
| ![cutaway](../assets/renders/cabinet_cutaway.png) | Cabinet cutaway |

A rendered profile of this waveguide is in
[../assets/mk2_waveguide_profil.png](../assets/mk2_waveguide_profil.png).

These are **design-direction geometry, not validated by measurement.** Mouth
size, throat and coverage must be confirmed against H2606-in-waveguide
measurements.

## `cabinet.scad`

A fully parametric **OpenSCAD** model of the v6b enclosure — the first cabinet
geometry in the repo.

- External **300 × 370 × 1080 mm**, 22 mm walls, **R50** front vertical
  roundovers (rear edges square).
- **Side-mounted push-push** woofer cut-outs, opposed at the same height
  (~520 mm), with the rigid coupling block between the magnets (see
  [Chapter 8](../docs/08_push_push_bass.md)).
- Front baffle cut-outs for the **WG212** (elliptical mouth + rounded flange
  recess, matched to `mk2_waveguide_os.scad`) and the **15W/4434G00** midrange at
  **~150 mm c-c**.
- `show_internals = true` renders a cut-away with the sealed mid chamber, a
  window brace at the woofer line and the bass/mid shelf brace.
- `show_waveguide = true` drops the WG212 model into the baffle (it `use`s
  `mk2_waveguide_os.scad`, so keep both files together). The waveguide is seated
  with its mouth poking `wg_through` (default 0.3 mm) **through** the baffle. Its
  seating depth is read from the waveguide via `wg_front_z()`, so it can't drift
  out of sync. (If it only sits flush near ~84.5 mm, your waveguide file is the
  old flange-forward version — the flush model seats at `D_tot` = 75 mm.)

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
