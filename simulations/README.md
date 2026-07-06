# Simulations

Version-controlled, assumption-headed simulation scripts for the Mk3 Reference
Loudspeaker. This starts closing the "recreate simulations as version-controlled
scripts" task in [../SIMULATIONS.md](../SIMULATIONS.md).

**All outputs are simplified physics estimates, not measured data.** Every script
states its assumptions in a docstring. Final crossover/DSP decisions must come
from real measurements of the finished cabinet (see [../MEASUREMENTS.md](../MEASUREMENTS.md)).

## Current design scripts

These scripts document the current SB26STAC-C000-4 / 1100 Hz design and the
tweeter selection analysis:

| Script | What it computes | Output |
|---|---|---|
| `mk3_crossover_optimization.py` | Systematic crossover-frequency sweep for the SB26STAC scoring Fs margin, excursion headroom, directivity match, vertical lobing ripple and system-sum flatness. Confirms 1100 Hz as optimal. | `plots/mk3_crossover_optimization.png` |
| `system_response_realistic.py` | Realistic full-system on-axis response using actual digitized datasheet frequency-response curves, baffle step, waveguide loading and LR4 crossovers. Compares the current SB26STAC/1100 Hz design against the earlier horn-dome/1250 Hz baseline (historical). | `plots/mk2_vs_mk3_realistic_response.png` |
| `system_response_inroom.py` | Four-stage progression: anechoic (pre-DSP) → in-room (average living room 4.5×4×2.4m, room gain + HF absorption) → level-corrected (normalized @500 Hz) → post-DSP (EQ toward Harman in-room target, 1/3 octave PEQ simulation). Uses v9 drivers. | `plots/system_response_inroom.png`, `csv/system_response_inroom.csv` |
| `mk2_vs_mk3_spinorna.py` | Spinorama estimate (on-axis, listening window, early reflections, sound power, DI, PIR) using real datasheet curves and 26 mm vs 25 mm dome directivity. | `plots/mk2_vs_mk3_spinorna.png`, `plots/mk2_vs_mk3_system_response.png` |
| `h2606_vs_sb26stac_comparison.py` | Tweeter selection analysis (Fs, Xmax, sensitivity, excursion-limited max SPL, Fs-margin at each candidate crossover) documenting why the SB26STAC was chosen. | `plots/h2606_vs_sb26stac_comparison.png` |

## Original exploration scripts

These scripts cover the bass alignment, baffle diffraction, and the original
crossover/waveguide directivity exploration. The crossover-frequency scripts
(`crossover_simulation.py`, `system_response.py`, `vertical_polar_map.py`) were
written against the earlier candidate parameters and are kept for reference; the
current design values are captured by the scripts above.

| Script | What it computes | Output |
|---|---|---|
| `bass_alignment_maxspl.py` | Sealed alignment table (2 × GRS 12SW-4HE) + excursion-limited max-SPL ceiling + sealed response with a Linkwitz-Transform target (39→28 Hz, Q 0.76→0.707). Includes comparison against the previous 2 × GRS 8SW-4HE-8. | `plots/bass_alignment_maxspl.png` |
| `bass_volume_compare.py` | Sealed alignment (Qtc / Fc / F3) and group delay for 69–85 L net, highlighting the 75 L target — shows the alignment is robust to box-volume tolerance. | `plots/bass_volume_compare.png` |
| `vertical_lobing.py` | First vertical interference-null angle vs frequency for c-c and crossover options. | `plots/vertical_lobing.png` |
| `directivity_estimate.py` | Estimated directivity index (DI) of the 15W and the waveguide tweeter across the crossover — quantifies the DI step vs crossover frequency. | `plots/directivity_estimate.png` |
| `waveguide_profile.py` | Waveguide mouth-to-baffle termination cross-section — shows the sharp-lip diffraction problem and the flush / blended fixes. | `plots/waveguide_termination.png` |
| `crossover_simulation.py` | LR4 filters at 150 Hz + 1250 Hz: per-section amplitude and phase, coherent sum, zoomed panels around each crossover region. (Earlier candidate parameters.) | `plots/crossover_simulation.png`, `csv/crossover_simulation.csv` |
| `system_response.py` | Full-bandwidth on-axis estimate 20 Hz–20 kHz: sealed woofer + LR4 LP@150, piston mid + BP@150/1250, tweeter roll-in + LR4 HP@1250 (placeholder tweeter model — replace with real SB26STAC-in-waveguide FR). | `plots/system_response.png`, `csv/system_response.csv` |
| `polar_response.py` | 2D polar map (freq × angle), spinorama curves (on-axis, listening window, early reflections, sound power, DI, PIR), and horizontal polar cuts at 7 key frequencies. | `plots/polar_response.png`, `csv/spinorama.csv`, `csv/polar_horizontal.csv` |
| `vertical_polar_map.py` | Vertical 2D heat-map vs frequency + comparison of four crossover options + null-depth bar chart. (Earlier candidate parameters.) | `plots/vertical_polar_map.png`, `csv/vertical_polar_map.csv` |
| `design_versions_comparison.py` | Tabulates the design parameters for reference. | `design_versions.md`, `csv/design_versions.csv` |
| `baffle_step.py` | Baffle-step diffraction model for the 300 mm wide cabinet: SPL correction curve, low-frequency level loss, and the full on-axis response before/after step correction. | `plots/baffle_step.png`, `csv/baffle_step.csv` |

The GRS alignment script reproduces the repo's stated **Qtc ≈ 0.76 / Fc ≈ 39 Hz
in ~75 L** (12SW), transformed to 28 Hz / 0.707 via Linkwitz Transform. The lobing
script confirms that even c-c 160 mm crossed at 1600 Hz keeps the first vertical
null near 42° — far outside the listening window.

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
python3 simulations/mk3_crossover_optimization.py
python3 simulations/mk2_vs_mk3_realistic_response.py
python3 simulations/mk2_vs_mk3_spinorna.py
python3 simulations/h2606_vs_sb26stac_comparison.py
python3 simulations/system_response_inroom.py
```

The directivity script implements the Bessel `J1` via a polynomial
approximation, so no SciPy is required.

Plots are written to `simulations/plots/`.
