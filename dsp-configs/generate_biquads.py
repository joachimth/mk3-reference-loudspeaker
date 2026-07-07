#!/usr/bin/env python3
"""
Generate MiniDSP 4×10 HD biquad coefficients for Mk3 reference loudspeaker.

Usage:
    python3 generate_biquads.py                      # default: 200 Hz + 1250 Hz
    python3 generate_biquads.py 200 1600              # custom: 200 Hz mid + 1600 Hz tweeter
    python3 generate_biquads.py 200 1250 --fs 48000   # 48 kHz sample rate

Output: Markdown table with biquad coefficients ready to paste into MiniDSP plugin.
"""

import sys
import numpy as np
from scipy.signal import butter, bilinear

# ============================================================
# Defaults
# ============================================================
FS_DEFAULT = 96000  # MiniDSP 4×10 HD default
FC_BASS_DEFAULT = 150.0
FC_MID_DEFAULT = 1250.0

# GRS 8SW-4HE-8 T/S parameters (for Linkwitz Transform)
GRS_FS = 27.0
GRS_QTS = 0.36
GRS_VAS = 142.0  # liters
VB = 69.0        # sealed volume per speaker (liters)


def parse_args():
    args = sys.argv[1:]
    fc_bass = FC_BASS_DEFAULT
    fc_mid = FC_MID_DEFAULT
    fs = FS_DEFAULT

    i = 0
    while i < len(args):
        if args[i] == '--fs' and i + 1 < len(args):
            fs = float(args[i + 1])
            i += 2
        elif i == 0 and args[i].replace('.', '').isdigit():
            fc_bass = float(args[i])
            i += 1
        elif i == 1 and args[i].replace('.', '').isdigit():
            fc_mid = float(args[i])
            i += 1
        else:
            i += 1

    return fc_bass, fc_mid, fs


def butter_sos_2pole(fc, btype, fs):
    """2nd-order Butterworth, returns [b0 b1 b2 a0 a1 a2]."""
    sos = butter(2, fc, btype=btype, fs=fs, output='sos')
    return sos[0]


def lr4_biquads(fc, btype, fs):
    """Return two biquads for LR4 = two cascaded BW2 at same fc."""
    bq_list = []
    for _ in range(2):
        sos = butter_sos_2pole(fc, btype, fs)
        b0, b1, b2, a0, a1, a2 = sos
        bq_list.append([b0 / a0, b1 / a0, b2 / a0, -a1 / a0, -a2 / a0])
    return bq_list


def linkwitz_transform(fs):
    """Linkwitz Transform biquad for GRS 8SW-4HE-8 in 69L sealed."""
    alpha = GRS_VAS / VB
    Qtc = GRS_QTS * np.sqrt(1 + alpha)
    Fc = GRS_FS * np.sqrt(1 + alpha)

    # Target
    Fc_target = 28.0
    Q_target = 0.707

    # Pre-warped analog prototype
    T = 1.0 / fs
    wo = 2 * np.pi * Fc
    wt = 2 * np.pi * Fc_target

    # Pre-warp
    wo_pw = 2 / T * np.tan(wo * T / 2)
    wt_pw = 2 / T * np.tan(wt * T / 2)

    b_a = [1.0, wo_pw / Qtc, wo_pw ** 2]
    a_a = [1.0, wt_pw / Q_target, wt_pw ** 2]

    bz, az = bilinear(b_a, a_a, fs)
    b0, b1, b2 = bz / az[0]
    a1, a2 = az[1] / az[0], az[2] / az[0]
    return [b0, b1, b2, a1, a2]


def format_table(title, stages, fc=None):
    """Print biquad stages as markdown table section."""
    print(f"--- {title} ---")
    if fc:
        print(f"Frequency: {fc} Hz")
    if stages:
        print()
        print("| Stage | b0 | b1 | b2 | a1 | a2 |")
        print("|-------|-----|-----|-----|-----|-----|")
        for i, bq in enumerate(stages):
            print(f"| {i+1} | {bq[0]:.10f} | {bq[1]:.10f} | {bq[2]:.10f} | {bq[3]:.10f} | {bq[4]:.10f} |")
    print()


def main():
    fc_bass, fc_mid, fs = parse_args()

    print(f"# MiniDSP Biquad Coefficients")
    print(f"Sample rate: {fs:.0f} Hz")
    print(f"Crossover: bass LP {fc_bass:.0f} Hz LR4 / mid HP {fc_bass:.0f} Hz LR4")
    print(f"           mid LP {fc_mid:.0f} Hz LR4 / tweeter HP {fc_mid:.0f} Hz LR4")
    print()
    print("---")

    # === Woofer chain (5 biquads) ===
    print("## Woofer Chain")
    print()
    hp18 = lr4_biquads(18, 'high', fs)
    format_table("Subsonic HP 18 Hz LR4 (2 stages)", hp18, 18)

    lt = linkwitz_transform(fs)
    print("--- Linkwitz Transform (1 biquad) ---")
    print(f"Natural: Fc={GRS_FS * np.sqrt(1 + GRS_VAS/VB):.1f} Hz, Q={GRS_QTS * np.sqrt(1 + GRS_VAS/VB):.3f}")
    print(f"Target: Fc=28 Hz, Q=0.707")
    print()
    print("| Stage | b0 | b1 | b2 | a1 | a2 |")
    print("|-------|-----|-----|-----|-----|-----|")
    print(f"| 1 | {lt[0]:.10f} | {lt[1]:.10f} | {lt[2]:.10f} | {lt[3]:.10f} | {lt[4]:.10f} |")
    print()

    lp_bass = lr4_biquads(fc_bass, 'low', fs)
    format_table(f"LP {fc_bass:.0f} Hz LR4 (2 stages)", lp_bass, fc_bass)

    # === Midrange chain (4 biquads) ===
    print("## Midrange Chain")
    print()
    hp_mid = lr4_biquads(fc_bass, 'high', fs)
    format_table(f"HP {fc_bass:.0f} Hz LR4 (2 stages)", hp_mid, fc_bass)

    lp_mid = lr4_biquads(fc_mid, 'low', fs)
    format_table(f"LP {fc_mid:.0f} Hz LR4 (2 stages)", lp_mid, fc_mid)

    # === Tweeter chain (2 biquads) ===
    print("## Tweeter Chain")
    print()
    hp_tw = lr4_biquads(fc_mid, 'high', fs)
    format_table(f"HP {fc_mid:.0f} Hz LR4 (2 stages)", hp_tw, fc_mid)

    # === Controller summary ===
    print("## Controller Settings")
    print()
    print("| Channel | Driver | Biquads | Gain (dB) | Delay (ms) |")
    print("|---------|--------|---------|-----------|------------|")
    print("| Out 1 | GRS Woofer L | 5 | 0 | 0.19 |")
    print("| Out 2 | GRS Woofer L (2nd) | 5 | 0 | 0.19 |")
    print("| Out 3 | 15W/4434G00 Mid L | 4 | 0 | 0.12 |")
    print("| Out 4 | H2606 Tweeter L | 2 | -5.5 | 0 |")
    print("| Out 6 | GRS Woofer R | 5 | 0 | 0.19 |")
    print("| Out 7 | GRS Woofer R (2nd) | 5 | 0 | 0.19 |")
    print("| Out 8 | 15W/4434G00 Mid R | 4 | 0 | 0.12 |")
    print("| Out 9 | H2606 Tweeter R | 2 | -5.5 | 0 |")


if __name__ == "__main__":
    main()
