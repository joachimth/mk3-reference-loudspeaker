# Simulations

Version-controlled, assumption-headed simulation scripts for the Mk2 Reference
Loudspeaker. This starts closing the "recreate simulations as version-controlled
scripts" task in [../SIMULATIONS.md](../SIMULATIONS.md).

**All outputs are simplified physics estimates, not measured data.** Every script
states its assumptions in a docstring. Final crossover/DSP decisions must come
from real measurements of the finished cabinet (see [../MEASUREMENTS.md](../MEASUREMENTS.md)).

## Scripts

| Script | What it computes | Output |
|---|---|---|
| `bass_alignment_maxspl.py` | Sealed alignment table (2 × GRS 8SW-4HE) + excursion-limited max-SPL ceiling (GRS vs SB23 reference) + sealed response with a Linkwitz-Transform target. | `plots/bass_alignment_maxspl.png` |
| `bass_volume_compare.py` | Sealed alignment (Qtc / Fc / F3) and group delay for 64–72 L net, highlighting the 69 L target — shows the alignment is robust to box-volume tolerance. | `plots/bass_volume_compare.png` |
| `vertical_lobing.py` | First vertical interference-null angle vs frequency for c-c and crossover options. | `plots/vertical_lobing.png` |
| `directivity_estimate.py` | Estimated directivity index (DI) of the 15W and the WG212 tweeter across the crossover — quantifies the DI step vs crossover frequency (DD-010 / REVIEW §C2). | `plots/directivity_estimate.png` |
| `waveguide_profile.py` | WG212 mouth-to-baffle termination cross-section — shows the sharp-lip diffraction problem and the flush / blended fixes. | `plots/waveguide_termination.png` |
| `crossover_simulation.py` | LR4 filters at 150 Hz + 1250 Hz: per-section amplitude and phase, coherent sum, zoomed panels around each crossover region. | `plots/crossover_simulation.png`, `csv/crossover_simulation.csv` |
| `system_response.py` | Full-bandwidth on-axis estimate 20 Hz–20 kHz: sealed woofer + LR4 LP@150, piston mid + BP@150/1250, tweeter roll-in + LR4 HP@1250 (placeholder — replace with real H2606-in-WG212 FR). | `plots/system_response.png`, `csv/system_response.csv` |
| `polar_response.py` | 2D polar map (freq × angle), spinorama curves (on-axis, listening window, early reflections, sound power, DI, PIR), and horizontal polar cuts at 7 key frequencies. | `plots/polar_response.png`, `csv/spinorama.csv`, `csv/polar_horizontal.csv` |
| `vertical_polar_map.py` | Vertical 2D heat-map vs frequency + comparison of four crossover options (1250/1350/1450/1600 Hz) + null-depth bar chart. Key input to the WG212 distortion-test decision. | `plots/vertical_polar_map.png`, `csv/vertical_polar_map.csv` |
| `design_versions_comparison.py` | Tabulates v1–v6b design parameters for reference. | `design_versions.md`, `csv/design_versions.csv` |
| `baffle_step.py` | Baffle-step diffraction model for the 300 mm wide cabinet: SPL correction curve, low-frequency level loss, and the full on-axis response before/after step correction. | `plots/baffle_step.png`, `csv/baffle_step.csv` |
| `mk2_vs_mk3_realistic_response.py` | **mk3** — realistic full-system on-axis response for mk2 (H2606, 1250 Hz) vs mk3 (SB26STAC, 1100 Hz) using actual digitized datasheet frequency-response curves, baffle step, WG212 loading and LR4 crossovers. | `plots/mk2_vs_mk3_realistic_response.png` |
| `mk2_vs_mk3_spinorama.py` | **mk3** — spinorama comparison between mk2 and mk3 (on-axis, listening window, early reflections, sound power, DI, PIR) using real datasheet curves and 26 mm vs 25 mm dome directivity. | `plots/mk2_vs_mk3_spinorama.png`, `plots/mk2_vs_mk3_system_response.png` |
| `mk3_crossover_optimization.py` | **mk3** — systematic crossover-frequency sweep for the SB26STAC scoring Fs margin, excursion headroom, directivity match, vertical lobing ripple and system-sum flatness. | `plots/mk3_crossover_optimization.png` |
| `h2606_vs_sb26stac_comparison.py` | **mk3** — head-to-head tweeter comparison (Fs, Xmax, sensitivity, excursion-limited max SPL, Fs-margin at each candidate crossover) between H2606 and SB26STAC. | `plots/h2606_vs_sb26stac_comparison.png` |

The GRS alignment script reproduces the repo's stated **Qtc ≈ 0.62 / Fc ≈ 34.5 Hz
in ~69 L** (verified in [../REVIEW.md](../REVIEW.md) §A). The lobing script backs
up [../REVIEW.md](../REVIEW.md) §C2: even c-c 160 mm crossed at 1600 Hz keeps the
first vertical null near 42° — far outside the listening window.

## Running

```
pip install "numpy>=1.26" "matplotlib>=3.8"
python3 simulations/bass_alignment_maxspl.py
python3 simulations/bass_volume_compare.py
python3 simulations/vertical_lobing.py
python3 simulations/directivity_estimate.py
python3 simulations/waveguide_profile.py
python3 simulations/crossover_simulation.py
python3 simulations/system_response.py
python3 simulations/polar_response.py
python3 simulations/vertical_polar_map.py
python3 simulations/design_versions_comparison.py
python3 simulations/baffle_step.py
python3 simulations/mk2_vs_mk3_realistic_response.py
python3 simulations/mk2_vs_mk3_spinorama.py
python3 simulations/mk3_crossover_optimization.py
python3 simulations/h2606_vs_sb26stac_comparison.py
```

The directivity script implements the Bessel `J1` via a polynomial
approximation, so no SciPy is required.

Plots are written to `simulations/plots/`.
