# Assets

Datasheets and CAD render preview images for the Mk3 Reference Loudspeaker.

The numbers in the datasheets are the authoritative driver data used for the
simulation and CAD work. The CAD renders are auto-generated previews from the
OpenSCAD models — see [`cad/README.md`](../cad/README.md).

## Subfolders

| Folder | Contents |
|---|---|
| [`datasheets/`](datasheets/) | Official manufacturer datasheets (PDF) + extracted T/S parameters and frequency-response / impedance curves (CSV) for each driver. See [`datasheets/README.md`](datasheets/README.md). |
| [`renders/`](renders/) | Auto-generated preview images from the OpenSCAD CAD models (waveguide + cabinet views). Updated automatically by the [`cad-render`](../.github/workflows/cad-render.yml) workflow. See [`renders/README.md`](renders/README.md). |
