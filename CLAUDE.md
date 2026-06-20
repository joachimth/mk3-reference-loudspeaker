# CLAUDE.md

Guidance for AI assistants (and humans) working in this repository.

## What this repository is

This is the **design documentation** for the *Mk2 Reference Loudspeaker* — a
DIY active 3-way reference loudspeaker, inspired by the Genelec 8361,
Dutch & Dutch 8C, and Revel Salon2.

It is a **documentation-only repository**. There is no source code, no build
system, no tests, no package manager. Everything is Markdown. The "product" is
the engineering reasoning behind the speaker design, captured as a living
"Design Bible" plus supporting reference files.

The project is currently at the **simulation / design-candidate stage** (design
version **v6b**). No physical prototype has been built yet. Most numbers are
simplified simulation estimates, not measured data — preserve that distinction
in any edits.

## Repository layout

```
.
├── README.md                 # Entry point + current-spec summary table
├── docs/                     # The Design Bible (numbered chapters)
│   ├── 00_design_bible.md    # Master index for the chapters
│   ├── 01_project_goals.md
│   ├── 02_theory.md
│   ├── 03_woofer_selection.md
│   ├── 04_midrange_selection.md
│   ├── 05_tweeter_selection.md
│   ├── 06_waveguide_development.md
│   ├── 07_cabinet_development.md
│   ├── 08_push_push_bass.md
│   ├── 09_volume_calculations.md
│   ├── 10_bracing.md
│   ├── 11_crossovers.md
│   ├── 12_directivity.md
│   ├── 13_spinorama.md
│   ├── 14_dsp.md
│   ├── 15_measurements.md
│   ├── 16_build_guide.md
│   └── 17_future_versions.md
├── DESIGN_REQUIREMENTS.md    # Acoustic + mechanical targets (the spec)
├── DESIGN_DECISIONS.md       # Numbered decisions DD-001..DD-011 with rationale
├── PARTS.md                  # Driver + materials list
├── SIMULATIONS.md            # Simulation work + assumptions (estimates, not measured)
├── MEASUREMENTS.md           # Measurement plan (not yet executed)
├── BUILD_LOG.md              # Physical build log (template; build not started)
├── ROADMAP.md                # Version history v1..v11 + future plans
├── CHANGELOG.md              # Design change log, newest version first
├── REFERENCES.md             # Books, researchers, software
├── TODO.md                   # Outstanding tasks (checkbox lists)
└── LICENSE                   # MIT
```

## The two key conventions

### 1. Design versions (vN / vNb)

The whole project is organized around incrementing design versions, tracked in
`ROADMAP.md` (full history) and `CHANGELOG.md` (changes, newest first). The
current reference candidate is **v6b**. v7+ are planned/future and describe
intended work, not completed work.

When the design changes, bump or annotate the version and record it in both
`ROADMAP.md` and `CHANGELOG.md`.

### 2. Numbered design decisions (DD-NNN)

`DESIGN_DECISIONS.md` records each significant choice as `DD-NNN` with three
sections: **Decision**, **Reasoning**, and (usually) **Consequence**. The next
new decision is `DD-012`. Keep this format when adding one.

## The current spec (v6b) — keep it consistent

This summary appears verbatim (or near-verbatim) in **multiple files**:
`README.md`, `docs/00_design_bible.md`, `ROADMAP.md`, `CHANGELOG.md`,
`DESIGN_REQUIREMENTS.md`, and `PARTS.md`. If you change any spec value, you
**must update every place it appears** — otherwise the docs contradict each
other.

| Parameter | Value |
|---|---|
| Woofers | 2 × GRS 8SW-4HE-8 (push-push, side-mounted, series → 8 Ω) |
| Midrange | ScanSpeak 15W/4434G00 (sealed mid chamber ~5.7 L) |
| Tweeter | ScanSpeak H2606/920000 in custom WG212 waveguide |
| Cabinet | 300 × 370 × 1080 mm, 22 mm birch plywood, R50 front roundovers |
| Bass volume | ~69 L sealed, Fc ~34.5 Hz, Qtc ~0.62 |
| Bass/mid xover | 150 Hz LR4 |
| Mid/tweeter xover | 1250 Hz LR4 |
| Mid/tweeter c-c | 140 mm |
| System | Active, DSP-controlled (no passive crossover) |

Note: the tweeter is **ScanSpeak** H2606/920000 — an earlier revision
incorrectly attributed it to Seas; see commit `bc6c3df`. Do not reintroduce
"Seas H2606".

## Writing conventions

- **Markdown only.** GitHub-flavored. Tables for parameter lists, `## headings`,
  checkbox lists (`- [ ]` / `- [x]`) for tasks.
- **Units are metric** and explicit: mm, L (litres), Hz, Ω, dB. Crossover slopes
  are written as `LR4` (Linkwitz-Riley 4th order). Center-to-center spacing is
  `c-c`. Roundover radii are `RNN` (e.g. `R50`).
- **Hedge appropriately.** Use "approx." / "~" / "target" / "estimate" for any
  value that comes from simplified simulation rather than measurement. The repo
  is deliberately careful that simulated direction ≠ final measured truth (see
  the top of `SIMULATIONS.md` and `MEASUREMENTS.md`). Preserve this tone.
- Design Bible chapters generally open with a `## Requirements` or context
  section, walk through options investigated, and end with a status / decision.
  Match that structure when adding or extending a chapter.
- Cross-link with relative Markdown links (e.g. `[Chapter 8](08_push_push_bass.md)`
  from within `docs/`, or `docs/...` from the repo root).
- Keep the chapter status table in `docs/00_design_bible.md` and the file index
  in `README.md` in sync with the actual files in `docs/`.

## Development workflow

There is nothing to build, lint, or run. The workflow is purely editorial:

1. Make the documentation change.
2. Propagate any spec change to every file that repeats it (see the v6b table above).
3. If it's a design change, update `CHANGELOG.md` and `ROADMAP.md`; if it's a
   decision, add/extend a `DD-NNN` entry; tick or add items in `TODO.md`.
4. Commit with a clear, conventional-style message and push.

### Git conventions

- Commit messages follow a loose conventional style seen in history:
  `docs: ...`, `fix: ...`, or short imperative summaries (`Add chapter 3 woofer selection`).
- **Do all work on the assigned feature branch** (currently
  `claude/claude-md-docs-uigw74`). Create it locally if needed. Never push to
  `main` without explicit permission.
- Use `git push -u origin <branch>`.
- **Do not open a pull request unless explicitly asked.**

## What does NOT exist yet (don't assume it does)

These are referenced as aspirations in `TODO.md` / `SIMULATIONS.md` but are not
in the repo:

- Python simulation scripts, plots, or CSV data (`simulations/` is planned, not present)
- CAD / OpenSCAD / STEP / STL files for the cabinet or WG212 waveguide
- VituixCAD project files, REW measurements or presets
- Any actual measurement data (the build hasn't started)

If asked to "add the simulation" or "generate the CAD," confirm scope first —
these would be new artifact types for this repo, not edits to existing ones.

## Domain glossary (quick reference)

- **Push-push** — two woofers mounted on opposite sides, wired so cones move
  outward together, cancelling cabinet reaction forces. The rear/opposite driver
  is wired reversed polarity to achieve this (see Chapter 8).
- **Spinorama** — the standardized set of curves (on-axis, listening window,
  early reflections, sound power, predicted in-room, directivity index).
- **WG212** — the project's custom ~212 mm-mouth waveguide for the tweeter.
- **Qtc / Fc** — total system Q and resonant frequency of the sealed bass alignment.
- **LR4** — Linkwitz-Riley 4th-order (24 dB/oct) acoustic crossover target.
- **DSP / active** — crossovers, delay, and EQ are done electronically per driver
  channel; there is intentionally no passive crossover (decision DD-001).
