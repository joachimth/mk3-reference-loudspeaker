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

The GRS alignment script reproduces the repo's stated **Qtc ≈ 0.62 / Fc ≈ 34.5 Hz
in ~69 L** (verified in [../REVIEW.md](../REVIEW.md) §A). The lobing script backs
up [../REVIEW.md](../REVIEW.md) §C2: even c-c 160 mm crossed at 1600 Hz keeps the
first vertical null near 42° — far outside the listening window.

## Running

```
pip install numpy matplotlib
python3 simulations/bass_alignment_maxspl.py
python3 simulations/bass_volume_compare.py
python3 simulations/vertical_lobing.py
python3 simulations/directivity_estimate.py
```

The directivity script implements the Bessel `J1` via a polynomial
approximation, so no SciPy is required.

Plots are written to `simulations/plots/`.
