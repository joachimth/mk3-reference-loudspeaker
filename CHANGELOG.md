# Changelog

All notable design changes for the Mk3 Reference Loudspeaker are documented here.

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
