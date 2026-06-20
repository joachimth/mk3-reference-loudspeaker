# Assets

Drawings, plots, and data files for the Mk2 Reference Loudspeaker.

These were imported from an external design session. They are kept here as
**reference material**. Treat the numbers in them as simplified, physics-based
**estimates / sketches — not measured data** and not the authoritative spec.

## ⚠️ These files describe an SB23-based study, not the current v6b spec

The current reference candidate (**v6b**) uses **GRS 8SW-4HE-8** woofers (see
`../DESIGN_DECISIONS.md` DD-004, and the v6b table in `../README.md`). The
drawings and DSP table below depict an **alternative / earlier SB23 line** and
disagree with v6b on several values. They are recorded for reference only; the
v6b spec in the rest of the repo is unchanged.

| Parameter | Current v6b (repo) | These assets |
|---|---|---|
| Woofer | GRS 8SW-4HE-8 | SB23 (SB23NRXS45-8) |
| Cabinet height | 1080 mm | 1050 mm |
| Bass volume | ~69 L sealed | ~50 L (`mk2_kabinet_tegning`) / ~64 L (`mk2_cab_ark1_ydre`, `..._snit_lodret`) |
| Mid/tweeter c-c | 140 mm | 157 mm (`mk2_kabinet_tegning`) / 160 mm (`mk2_cab_ark1_ydre`) |
| Bass/mid xover | 150 Hz LR4 | 180 Hz LR4 |
| Mid/tweeter xover | 1250 Hz LR4 | 1600 Hz LR4 |
| Waveguide / mid / tweeter | WG212 / 15W/4434G00 / H2606/920000 | same |

Note the assets are also **internally inconsistent** (c-c 157 vs 160 mm; bass
~50 vs ~64 L), so they are a set of in-progress sketches rather than one
finalized design.

## File index

This folder holds the **SB23 study** (the alternative direction) — its write-up,
drawings, data, and plots. Duplicates that also belonged in the type-based
folders have been removed: the review is at [../REVIEW.md](../REVIEW.md), the
runnable scripts + their plots are in [../simulations/](../simulations/), and the
waveguide model is in [../cad/mk2_waveguide_os.scad](../cad/mk2_waveguide_os.scad).

### Write-up + data

| File | What it is |
|---|---|
| [mk2_design_bible_sb23.md](mk2_design_bible_sb23.md) | **The SB23 study's full design write-up** (Danish): OS waveguide, ~1600 Hz LR4, c-c ~157–160 mm, 2 × SB23 sealed ~64 L (Qtc ≈ 0.75 / Fc ≈ 54 Hz). Textual companion to the drawings. Alternative direction, **not** the repo's v6b spec. |
| [mk2_parametre.csv](mk2_parametre.csv) | Parameter list for the SB23 study (cabinet, alignment, waveguide, crossovers). |
| [mk2_stykliste.csv](mk2_stykliste.csv) | Cut list / bill of materials for the SB23 cabinet (panel sizes, bracing, magnet coupling rod). |
| [mk2_dsp.csv](mk2_dsp.csv) | DSP filter plan per driver (HP/LP, Linkwitz Transform, delay, rest-EQ). |

### Drawings

| File | What it is |
|---|---|
| [mk2_kabinet_tegning.png](mk2_kabinet_tegning.png) | Cabinet dimensions and driver placement (labelled WG 212 mm, c-c 157 mm). |
| [mk2_cab_ark1_ydre.png](mk2_cab_ark1_ydre.png) | Sheet 1 — external dimensions (front / side / top), 300 × 370 × 1050 mm. |
| [mk2_cab_ark2_snit_lodret.png](mk2_cab_ark2_snit_lodret.png) | Sheet 2 — vertical section A-A (chambers + bracing, 22 mm walls). |
| [mk2_cab_ark3_snit_vandret.png](mk2_cab_ark3_snit_vandret.png) | Sheet 3 — horizontal section (push-push side woofers, internal width). |
| [mk2_cab_ark4_baffel.png](mk2_cab_ark4_baffel.png) | Sheet 4 — baffle layout (WG + mid cutouts, recesses). |
| [mk2_kabinet_tegninger.pdf](mk2_kabinet_tegninger.pdf) | Combined cabinet drawings (PDF). |
| [mk2_waveguide_profil.png](mk2_waveguide_profil.png) | Rendered OS waveguide profile (companion to `../cad/mk2_waveguide_os.scad`). |

### Plots (estimates, not measured)

| File | What it is |
|---|---|
| [mk2_estimeret_respons.png](mk2_estimeret_respons.png) | Estimated spinorama-style response: on-axis target, estimated in-room, sound power, directivity index. |
| [mk2_di_handoff.png](mk2_di_handoff.png) | Directivity-index hand-off across the mid/tweeter crossover. |
| [mk2_vertikal_lobing.png](mk2_vertikal_lobing.png) | Vertical lobing estimate for the SB23 study's c-c / crossover. |

The design bible's inline image and file references (`mk2_waveguide_profil.png`,
`mk2_kabinet_tegning.png`, `mk2_parametre.csv`, `mk2_dsp.csv`) all resolve within
this folder.
