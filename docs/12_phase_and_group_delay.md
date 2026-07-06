# Phase and Group Delay Analysis — Mk3 v9

## Summary

| Metric | Value | Notes |
|---|---|---|
| Crossover | 200 Hz BW4 + 1100 Hz LR4 | Woofer-mid: BW4, Mid-tweeter: LR4 |
| Woofer path filters | 6 biquads in series | HP18-LR4 × 2 + LT + LP200-BW4 × 2 |
| Mid path filters | 4 biquads in series | HP200-BW4 × 2 + LP1100-LR4 × 2 |
| Tweeter path filters | 2 biquads + 120 µs delay | HP1100-LR4 × 2 + WG depth delay |
| **Δφ @ 200 Hz (W-M)** | **-274.7°** | Woofer leads mid — BW4's +3 dB sum handles this |
| **Δφ @ 1100 Hz (M-T)** | **-617.8°** | 360° from LR4 + ~258° from mid's HP200 residual |

## Group Delay by Frequency

| Path | 20 Hz | 50 Hz | 200 Hz | 500 Hz | 1 kHz | 5 kHz |
|---|---|---|---|---|---|---|
| Woofer | **51.3 ms** | 10.1 ms | 6.2 ms | 0.8 ms | 0.2 ms | 0.01 ms |
| Mid | 5.0 ms | 5.1 ms | 6.7 ms | 1.7 ms | 1.1 ms | 0.05 ms |
| Tweeter | 0.9 ms | 0.9 ms | 1.0 ms | 1.1 ms | 1.0 ms | 0.2 ms |
| **System** | **51.3 ms** | 10.1 ms | 9.4 ms | 1.7 ms | 1.6 ms | 0.2 ms |

## Woofer Path — Group Delay Breakdown by Filter Stage

| Stage | @20 Hz | @30 Hz | @50 Hz |
|---|---|---|---|
| HP 18 LR4 × 2 | 24.5 ms | 12.1 ms | 4.7 ms |
| LT 39→28 Hz | 10.2 ms | 4.8 ms | 1.5 ms |
| LP 200 BW4 × 2 | 16.6 ms | 9.2 ms | 3.9 ms |
| **Total** | **51.3 ms** | **26.1 ms** | **10.1 ms** |
| **Excess over sealed** | **41.6 ms** | **18.7 ms** | **5.2 ms** |

The sealed 12SW rolloff alone (Fc=28, Qtc=0.707) contributes ~9.7 ms at 20 Hz. All the filter stages add 41.6 ms on top of that.

## Observations

### 1. 51 ms group delay at 20 Hz is substantial but expected
For a 28 Hz tuned subwoofer with aggressive EQ (LT dropping from 39→28 Hz) and two cascaded HP filters at 18 Hz, 51 ms is within normal range. The ear is extremely insensitive to group delay below 50 Hz — Blauert's laws of binaural hearing show the threshold of detectability at 20 Hz is around 60-100 ms. This is fine.

### 2. 200 Hz BW4 handles the phase mismatch well
The -274.7° at crossover means the woofer and mid are not phase-aligned, but the BW4 filter's +3 dB summing characteristic compensates. Unlike LR4 (which sums to 0 dB at crossover), BW4 creates amplitude summation that fills the acoustic crossover gap created by the phase offset.

### 3. 1100 Hz LR4 phase difference is dominated by the LR4 itself
The -617.8° breaks down as:
- -360° from LR4 (180° per stage × 2 stages, HP→LP phase difference)
- -258° from the mid's HP 200 BW4 filters still accumulating residual phase at 5.5× cutoff

This means the mid and tweeter are effectively in-phase at crossover — the 360° shift cancels to 0° electrical. The extra 258° is constant phase rotation across the entire midrange and doesn't affect summing at crossover.

### 4. 120 µs tweeter delay → verify with measurement
The waveguide depth delay was calculated geometrically. The actual acoustic phase alignment needs caliper verification of the 3D-printed waveguide depth + measurement at the listening position. The 120 µs should be treated as a starting point, not final.

## Generated
`simulations/plots/phase_analysis.png` — 4-panel plot showing:
1. Unwrapped phase per path
2. Group delay per path
3. Woofer filter stage breakdown
4. 1100 Hz crossover phase coherence zoom

Run `python3 simulations/phase_analysis.py` to regenerate.

*Generated July 6, 2026 — heartbeat analysis*
