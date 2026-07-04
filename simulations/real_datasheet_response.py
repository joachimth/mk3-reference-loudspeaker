#!/usr/bin/env python3
"""
Mk2 vs Mk3 system response simulation using REAL extracted datasheet curves.

Replaces the old simplified models (flat piston, tanh roll-in) with actual
frequency response data extracted from manufacturer PDFs.

Design parameters:
  mk2: GRS woofer (sealed 69L, LP@150) + 15W mid (HP@150 + LP@1250) + H2606 in WG212 (HP@1250)
  mk3: GRS woofer (sealed 69L, LP@150) + 15W mid (HP@150 + LP@1100) + SB26STAC (HP@1100, no WG)

Outputs:
  simulations/csv/mk2_system_real.csv
  simulations/csv/mk3_system_real.csv
  simulations/csv/mk2_vs_mk3_comparison.csv
  simulations/plots/mk2_system_real.png
  simulations/plots/mk3_system_real.png
  simulations/plots/mk2_vs_mk3_comparison.png
"""
import os
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Paths
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DATASHEET_DIR = os.path.join(REPO_ROOT, "assets", "datasheets")
CSV_DIR = os.path.join(SCRIPT_DIR, "csv")
PLOT_DIR = os.path.join(SCRIPT_DIR, "plots")
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# ============================================================
# Frequency grid: 1/24 octave, 20 Hz to 20 kHz
# ============================================================
F_MIN = 20.0
F_MAX = 20000.0
POINTS_PER_OCTAVE = 24
N_OCTAVES = np.log2(F_MAX / F_MIN)
N_POINTS = int(N_OCTAVES * POINTS_PER_OCTAVE) + 1
F = np.logspace(np.log10(F_MIN), np.log10(F_MAX), N_POINTS)


# ============================================================
# Data loaders
# ============================================================

def load_freq_response_csv(filepath, spl_col="spl_db"):
    """Load a datasheet frequency response CSV and interpolate onto F grid."""
    freqs_raw = []
    spls_raw = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                freq = float(row["freq_hz"])
                spl_str = row.get(spl_col, "")
                if spl_str and spl_str.strip():
                    spl = float(spl_str)
                    freqs_raw.append(freq)
                    spls_raw.append(spl)
            except (ValueError, KeyError):
                continue

    if len(freqs_raw) < 2:
        print(f"  WARNING: only {len(freqs_raw)} valid points in {filepath}")
        return np.full_like(F, np.nan)

    freqs_raw = np.array(freqs_raw)
    spls_raw = np.array(spls_raw)

    # Sort by frequency
    sort_idx = np.argsort(freqs_raw)
    freqs_raw = freqs_raw[sort_idx]
    spls_raw = spls_raw[sort_idx]

    # Log-frequency interpolation
    log_f_raw = np.log10(freqs_raw)
    log_f_target = np.log10(F)
    result = np.interp(log_f_target, log_f_raw, spls_raw, left=np.nan, right=np.nan)
    return result


# ============================================================
# Filter math
# ============================================================

def lr4_lp_mag(f, fc):
    """LR4 low-pass magnitude in dB."""
    s = 1j * f / fc
    H = 1.0 / (s**2 + np.sqrt(2) * s + 1) ** 2
    return 20 * np.log10(np.abs(H) + 1e-15)


def lr4_hp_mag(f, fc):
    """LR4 high-pass magnitude in dB."""
    s = 1j * f / fc
    H = s**4 / (s**2 + np.sqrt(2) * s + 1) ** 2
    return 20 * np.log10(np.abs(H) + 1e-15)


def lr4_lp_complex(f, fc):
    """LR4 low-pass complex response (for phase-coherent sum)."""
    s = 1j * f / fc
    H = 1.0 / (s**2 + np.sqrt(2) * s + 1) ** 2
    return H


def lr4_hp_complex(f, fc):
    """LR4 high-pass complex response."""
    s = 1j * f / fc
    H = s**4 / (s**2 + np.sqrt(2) * s + 1) ** 2
    return H


def sealed_hp_mag(f, fc, qtc):
    """Sealed cabinet 2nd-order high-pass magnitude in dB."""
    s = 1j * f / fc
    H = s**2 / (s**2 + s / qtc + 1)
    return 20 * np.log10(np.abs(H) + 1e-15)


def sealed_hp_complex(f, fc, qtc):
    """Sealed cabinet high-pass complex response."""
    s = 1j * f / fc
    H = s**2 / (s**2 + s / qtc + 1)
    return H


def baffle_step_mag(f, baffle_width_m, roundover_m=0.050):
    """
    Baffle step model for a rectangular baffle.
    Approximates the +6 dB transition from full-space to half-space radiation.
    
    f_step ≈ c / (π × width)
    The transition is modeled as a first-order shelving filter.
    """
    c = 344.0  # speed of sound m/s
    f_step = c / (np.pi * baffle_width_m)
    
    # First-order shelving: low-freq = -6dB (full space), high-freq = 0dB (half space)
    # H(s) = (s + 2*pi*f_step) / (s + 2*pi*f_step*2)  → gives +6dB shelf
    # In frequency domain:
    s = 1j * 2 * np.pi * f
    w0 = 2 * np.pi * f_step
    H = (s + 2 * w0) / (s + w0)
    return 20 * np.log10(np.abs(H) + 1e-15)


def baffle_step_complex(f, baffle_width_m):
    """Baffle step complex response for coherent sum."""
    c = 344.0
    f_step = c / (np.pi * baffle_width_m)
    s = 1j * 2 * np.pi * f
    w0 = 2 * np.pi * f_step
    H = (s + 2 * w0) / (s + w0)
    return H


def waveguide_loading_mag(f, throat_d_mm=33, mouth_d_mm=293, depth_mm=80):
    """
    Approximate waveguide loading gain for the H2606 in WG212.
    Below the waveguide control frequency, the tweeter radiates into free space.
    Above the control frequency, the waveguide constrains radiation into a narrower
    solid angle, increasing on-axis SPL.
    
    Control frequency ≈ c / (π × mouth_diameter)
    The gain is approximately +3 to +6 dB above the control frequency.
    """
    c = 344.0
    mouth_d_m = mouth_d_mm / 1000.0
    f_control = c / (np.pi * mouth_d_m)  # ~370 Hz for 293mm mouth
    
    # Smooth transition: +3 dB gain above f_control
    # Using a first-order shelving filter
    s = 1j * 2 * np.pi * f
    w0 = 2 * np.pi * f_control
    # Shelf: 0 dB below, +3 dB above
    gain_ratio = 10 ** (3.0 / 20)  # 3 dB = 1.413
    H = (s + gain_ratio * w0) / (s + w0)
    return 20 * np.log10(np.abs(H) + 1e-15)


def waveguide_loading_complex(f, throat_d_mm=33, mouth_d_mm=293):
    """Waveguide loading complex response."""
    c = 344.0
    mouth_d_m = mouth_d_mm / 1000.0
    f_control = c / (np.pi * mouth_d_m)
    s = 1j * 2 * np.pi * f
    w0 = 2 * np.pi * f_control
    gain_ratio = 10 ** (3.0 / 20)
    H = (s + gain_ratio * w0) / (s + w0)
    return H


# ============================================================
# Driver data loading
# ============================================================

print("Loading extracted datasheet curves...")

# GRS woofer on-axis SPL (raw, free-air measurement from spec sheet)
grs_spl = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "GRS-8SW-4HE-8_freq_response.csv"), "spl_db"
)
print(f"  GRS 8SW-4HE-8: {np.sum(np.isfinite(grs_spl))} valid points")

# 15W midrange on-axis SPL
mid15w_spl = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "15W-4434G00_freq_response.csv"), "spl_db"
)
print(f"  15W/4434G00: {np.sum(np.isfinite(mid15w_spl))} valid points")

# 15W off-axis
mid15w_off1 = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "15W-4434G00_freq_response.csv"), "spl_offaxis1_db"
)
mid15w_off2 = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "15W-4434G00_freq_response.csv"), "spl_offaxis2_db"
)

# H2606 tweeter on-axis SPL
h2606_spl = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "H2606-920000_freq_response.csv"), "spl_db"
)
print(f"  H2606/920000: {np.sum(np.isfinite(h2606_spl))} valid points")

# H2606 off-axis
h2606_off1 = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "H2606-920000_freq_response.csv"), "spl_offaxis1_db"
)
h2606_off2 = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "H2606-920000_freq_response.csv"), "spl_offaxis2_db"
)

# SB26STAC tweeter on-axis SPL
sb26_spl = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "SB26STAC-C000-4_freq_response.csv"), "spl_db"
)
print(f"  SB26STAC-C000-4: {np.sum(np.isfinite(sb26_spl))} valid points")

# SB26 off-axis
sb26_30deg = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "SB26STAC-C000-4_freq_response.csv"), "spl_30deg_db"
)
sb26_60deg = load_freq_response_csv(
    os.path.join(DATASHEET_DIR, "SB26STAC-C000-4_freq_response.csv"), "spl_60deg_db"
)


# ============================================================
# Design parameters
# ============================================================

# Cabinet
BAFFLE_WIDTH = 0.300  # 300 mm
ROUNDOVER = 0.050     # R50 mm
BASS_VOLUME = 69.0    # liters
FC_WOOFER = 34.5      # Hz, sealed alignment
QTC_WOOFER = 0.62

# Crossover frequencies
FC_BASS_MK2 = 150.0
FC_MID_MK2 = 1250.0
FC_BASS_MK3 = 150.0
FC_MID_MK3 = 1100.0

# Nominal sensitivities (dB @ 2.83V/1m, from datasheets)
SENS_WOOFER_SINGLE = 89.0   # GRS single driver
SENS_WOOFER_PAIR = 92.0     # 2x push-push: +3 dB from doubled Sd
SENS_MID = 89.7             # 15W/4434G00
SENS_H2606 = 95.2           # H2606/920000
SENS_SB26 = 91.5            # SB26STAC-C000-4

# Level matching: DSP gain reduction for each tweeter relative to mid
# At the mid/tweeter crossover, the tweeter is attenuated to match the mid
LEVEL_MATCH_H2606 = SENS_MID - SENS_H2606  # -5.5 dB
LEVEL_MATCH_SB26 = SENS_MID - SENS_SB26     # -1.8 dB


# ============================================================
# Simulation: Mk2 (H2606 in WG212, 1250 Hz crossover)
# ============================================================

def simulate_system(name, tweeter_spl_raw, fc_mid_tweeter,
                    apply_waveguide=True, tweeter_level_match=0.0):
    """
    Simulate full system response using real datasheet curves.
    
    Parameters:
        name: "mk2" or "mk3"
        tweeter_spl_raw: on-axis SPL from datasheet (interpolated to F grid)
        fc_mid_tweeter: crossover frequency between mid and tweeter
        apply_waveguide: True for H2606 in WG212, False for SB26STAC
        tweeter_level_match: dB attenuation for tweeter channel
    
    Returns dict with all intermediate and final curves.
    """
    print(f"\n{'='*60}")
    print(f"Simulating {name}")
    print(f"{'='*60}")
    
    results = {}
    
    # --- Woofer (2x GRS in sealed 69L) ---
    # Raw datasheet SPL is free-air. In sealed cabinet:
    # 1. Apply sealed high-pass (Fc=34.5, Qtc=0.62) — replaces free-air response below ~100 Hz
    # 2. The datasheet SPL above ~100 Hz is valid for the driver in a cabinet
    # 3. Pair: +3 dB from doubled radiating area
    # 4. Apply baffle step (woofers are on the SIDE of the cabinet, not front baffle)
    #    Side-mounted woofers radiate into full space below baffle step,
    #    then transition to half-space. Actually for side-mounted woofers,
    #    the baffle step is at the cabinet width frequency.
    
    # Start with raw datasheet curve
    woofer_raw = grs_spl.copy()
    
    # Apply sealed cabinet response below 200 Hz (replace free-air roll-off)
    # The datasheet shows free-air response with Fs=48 Hz.
    # In sealed box: Fc=34.5, Qtc=0.62.
    # Above ~200 Hz, sealed response ≈ flat, matching datasheet.
    # Below ~200 Hz, replace with sealed response.
    # Blend: use sealed HP for f < 200, use datasheet for f > 200
    sealed = sealed_hp_mag(F, FC_WOOFER, QTC_WOOFER)
    
    # Find the crossover blend frequency: where datasheet and sealed meet
    # Use 150 Hz as blend point (well above Fc, below usable range of datasheet near-field)
    blend_f = 150.0
    blend_weight = 1.0 / (1.0 + (F / blend_f)**4)  # smooth transition
    
    # Normalize sealed to match datasheet level at 150 Hz
    # At 150 Hz, sealed response is nearly flat (well above Fc)
    sealed_normalized = sealed - sealed[np.argmin(np.abs(F - 150.0))] + \
                        woofer_raw[np.argmin(np.abs(F - 150.0))]
    
    woofer_cabinet = blend_weight * sealed_normalized + (1 - blend_weight) * woofer_raw
    
    # Pair gain: +3 dB for two drivers
    woofer_pair = woofer_cabinet + 3.0
    
    # Baffle step for side-mounted woofers on 300mm cabinet
    # Woofers are on the narrow sides, so baffle width ≈ 300mm (cabinet width)
    baffle = baffle_step_mag(F, BAFFLE_WIDTH)
    woofer_with_baffle = woofer_pair + baffle
    
    # LR4 low-pass at 150 Hz
    woofer_filtered = woofer_with_baffle + lr4_lp_mag(F, FC_BASS_MK2)
    
    # Level: normalize woofer to ~89 dB at 100 Hz (in-band reference)
    woofer_ref_idx = np.argmin(np.abs(F - 100.0))
    woofer_level = woofer_filtered[woofer_ref_idx]
    woofer_final = woofer_filtered
    
    results["woofer_raw"] = woofer_raw
    results["woofer_sealed"] = woofer_cabinet
    results["woofer_pair"] = woofer_pair
    results["woofer_baffle"] = woofer_with_baffle
    results["woofer_filtered"] = woofer_filtered
    
    # --- Midrange (15W/4434G00) ---
    # Raw datasheet SPL is on-axis, IEC baffle measurement.
    # In cabinet: apply baffle step for front-baffle mounted driver.
    mid_raw = mid15w_spl.copy()
    
    # Baffle step for front baffle (300mm width)
    mid_with_baffle = mid_raw + baffle
    
    # LR4 HP at 150 Hz + LP at mid/tweeter crossover
    mid_hp = lr4_hp_mag(F, FC_BASS_MK2)
    mid_lp = lr4_lp_mag(F, fc_mid_tweeter)
    mid_filtered = mid_with_baffle + mid_hp + mid_lp
    
    results["mid_raw"] = mid_raw
    results["mid_baffle"] = mid_with_baffle
    results["mid_filtered"] = mid_filtered
    
    # --- Tweeter ---
    tw_raw = tweeter_spl_raw.copy()
    
    # Waveguide loading (mk2 only: H2606 in WG212)
    if apply_waveguide:
        wg_gain = waveguide_loading_mag(F)
        tw_with_wg = tw_raw + wg_gain
        results["tweeter_waveguide_gain"] = wg_gain
    else:
        tw_with_wg = tw_raw
    
    # Baffle step for tweeter on front baffle
    tw_with_baffle = tw_with_wg + baffle
    
    # LR4 HP at mid/tweeter crossover
    tw_hp = lr4_hp_mag(F, fc_mid_tweeter)
    tw_filtered = tw_with_baffle + tw_hp
    
    # Level matching: attenuate tweeter to match mid at crossover
    # Level matching: attenuate tweeter to match mid at crossover
    # IMPORTANT: Match at the tweeter's flat passband (3-5 kHz), NOT at the crossover
    # frequency. At crossover, the tweeter may be in an Fs dip (especially SB26STAC
    # with Fs=750 Hz). The DSP EQ will flatten the dip separately.
    # Use the nominal sensitivity difference as the primary level match.
    tw_passband_idx = np.argmin(np.abs(F - 3000.0))
    mid_passband_idx = np.argmin(np.abs(F - 3000.0))
    
    # Get tweeter SPL in its flat band (average 2-5 kHz)
    tw_band_mask = (F >= 2000) & (F <= 5000) & np.isfinite(tw_with_baffle)
    mid_band_mask = (F >= 500) & (F <= 1000) & np.isfinite(mid_with_baffle)
    
    if np.any(tw_band_mask) and np.any(mid_band_mask):
        tw_band_avg = np.nanmean(tw_with_baffle[tw_band_mask])
        mid_band_avg = np.nanmean(mid_with_baffle[mid_band_mask])
        level_adjust = mid_band_avg - tw_band_avg + tweeter_level_match
    else:
        # Fallback: use nominal sensitivity difference
        level_adjust = tweeter_level_match
    
    tw_final = tw_filtered + level_adjust
    
    results["tweeter_raw"] = tw_raw
    results["tweeter_wg"] = tw_with_wg
    results["tweeter_baffle"] = tw_with_baffle
    results["tweeter_filtered"] = tw_filtered
    results["tweeter_level_adjust"] = level_adjust
    results["tweeter_final"] = tw_final
    
    # --- System sum (coherent, in-phase at crossover for LR4) ---
    # LR4 crossovers sum flat when drivers are in phase.
    # For the simplified sum, we use power summation (energetic sum)
    # which is accurate when drivers are in phase at crossover (LR4 property).
    # Full coherent sum requires phase tracking, which we approximate here.
    
    # Use complex domain for proper summation
    # Woofer: sealed HP + baffle step + LR4 LP
    w_complex = (10 ** (grs_spl / 20) *  # raw amplitude
                 sealed_hp_complex(F, FC_WOOFER, QTC_WOOFER) *  # cabinet
                 (10 ** (baffle_step_mag(F, BAFFLE_WIDTH) / 20)) *  # baffle (approx as gain)
                 lr4_lp_complex(F, FC_BASS_MK2) *  # crossover
                 (10 ** (3.0 / 20)))  # pair gain
    
    # For woofer, we need to handle the blend properly.
    # Simple approach: use the magnitude-based sum (power sum) which is valid
    # for well-behaved LR4 crossovers with aligned phases.
    
    # Power sum: sum of squared pressures
    w_p = 10 ** (woofer_final / 20)
    m_p = 10 ** (mid_filtered / 20)
    t_p = 10 ** (tw_final / 20)
    
    # Coherent sum (assuming LR4 phase alignment = in-phase at crossover):
    # At crossover, both drivers are at -6 dB and in phase → they sum to 0 dB.
    # Away from crossover, the off-band driver is strongly attenuated, so
    # phase errors have minimal effect. Power sum is a good approximation.
    system_sum = 20 * np.log10(np.sqrt(w_p**2 + m_p**2 + t_p**2) + 1e-15)
    
    results["system_sum"] = system_sum
    
    # Also compute coherent (voltage) sum for comparison
    coherent_sum = 20 * np.log10(np.abs(w_p + m_p + t_p) + 1e-15)
    results["coherent_sum"] = coherent_sum
    
    print(f"  Woofer: ref {woofer_level:.1f} dB at 100 Hz")
    xo_idx = np.argmin(np.abs(F - fc_mid_tweeter))
    print(f"  Mid: {mid_filtered[xo_idx]:.1f} dB at {fc_mid_tweeter} Hz crossover")
    print(f"  Tweeter: {tw_filtered[xo_idx]:.1f} dB at crossover, adjusted by {level_adjust:.1f} dB")
    print(f"  Tweeter level match: passband avg {tw_band_avg:.1f} dB vs mid band avg {mid_band_avg:.1f} dB")
    print(f"  System sum range: {np.nanmin(system_sum[np.isfinite(system_sum)]):.1f} - "
          f"{np.nanmax(system_sum[np.isfinite(system_sum)]):.1f} dB")
    
    return results


# Run simulations
mk2 = simulate_system(
    "mk2 (H2606/WG212, 1250 Hz)",
    h2606_spl,
    fc_mid_tweeter=FC_MID_MK2,
    apply_waveguide=True,
    tweeter_level_match=LEVEL_MATCH_H2606,
)

mk3 = simulate_system(
    "mk3 (SB26STAC, 1100 Hz)",
    sb26_spl,
    fc_mid_tweeter=FC_MID_MK3,
    apply_waveguide=False,
    tweeter_level_match=LEVEL_MATCH_SB26,
)


# ============================================================
# CSV exports
# ============================================================

def export_csv(filepath, freq, columns):
    """Export CSV with frequency and named columns."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["freq_hz"] + list(columns.keys()))
        for i in range(len(freq)):
            row = [f"{freq[i]:.2f}"]
            for name, data in columns.items():
                val = data[i]
                row.append(f"{val:.4f}" if np.isfinite(val) else "")
            writer.writerow(row)
    print(f"  Wrote {filepath}")


print("\nExporting CSVs...")

export_csv(
    os.path.join(CSV_DIR, "mk2_system_real.csv"),
    F,
    {
        "woofer_raw_db": mk2["woofer_raw"],
        "woofer_sealed_db": mk2["woofer_sealed"],
        "woofer_pair_baffle_db": mk2["woofer_baffle"],
        "woofer_filtered_db": mk2["woofer_filtered"],
        "mid_raw_db": mk2["mid_raw"],
        "mid_baffle_db": mk2["mid_baffle"],
        "mid_filtered_db": mk2["mid_filtered"],
        "tweeter_raw_db": mk2["tweeter_raw"],
        "tweeter_wg_db": mk2["tweeter_wg"],
        "tweeter_filtered_db": mk2["tweeter_filtered"],
        "tweeter_final_db": mk2["tweeter_final"],
        "system_sum_db": mk2["system_sum"],
        "coherent_sum_db": mk2["coherent_sum"],
    },
)

export_csv(
    os.path.join(CSV_DIR, "mk3_system_real.csv"),
    F,
    {
        "woofer_raw_db": mk3["woofer_raw"],
        "woofer_sealed_db": mk3["woofer_sealed"],
        "woofer_pair_baffle_db": mk3["woofer_baffle"],
        "woofer_filtered_db": mk3["woofer_filtered"],
        "mid_raw_db": mk3["mid_raw"],
        "mid_baffle_db": mk3["mid_baffle"],
        "mid_filtered_db": mk3["mid_filtered"],
        "tweeter_raw_db": mk3["tweeter_raw"],
        "tweeter_filtered_db": mk3["tweeter_filtered"],
        "tweeter_final_db": mk3["tweeter_final"],
        "system_sum_db": mk3["system_sum"],
        "coherent_sum_db": mk3["coherent_sum"],
    },
)

export_csv(
    os.path.join(CSV_DIR, "mk2_vs_mk3_comparison.csv"),
    F,
    {
        "mk2_system_db": mk2["system_sum"],
        "mk3_system_db": mk3["system_sum"],
        "difference_db": mk2["system_sum"] - mk3["system_sum"],
        "mk2_tweeter_db": mk2["tweeter_final"],
        "mk3_tweeter_db": mk3["tweeter_final"],
        "mk2_mid_db": mk2["mid_filtered"],
        "mk3_mid_db": mk3["mid_filtered"],
    },
)


# ============================================================
# Plots
# ============================================================

def plot_system(name, results, fc_mid, color_scheme, filename):
    """Plot individual driver responses and system sum."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle(f"{name} — System Response (Real Datasheet Curves)", fontsize=14, fontweight="bold")
    
    # (1) Individual drivers with processing chain
    ax = axes[0, 0]
    ax.set_title("Individual Driver Responses")
    ax.semilogx(F, results["woofer_filtered"], color="tab:red", lw=2, label="Woofer (2×GRS, sealed + baffle + LP@150)")
    ax.semilogx(F, results["mid_filtered"], color="tab:green", lw=2, label=f"Mid (15W, baffle + HP@150 + LP@{fc_mid:.0f})")
    ax.semilogx(F, results["tweeter_final"], color="tab:blue", lw=2, label=f"Tweeter (HP@{fc_mid:.0f} + level match)")
    ax.axvline(150, color="0.4", ls=":", alpha=0.5)
    ax.axvline(fc_mid, color="0.4", ls=":", alpha=0.5)
    ax.set_xlim(20, 20000)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("SPL [dB]")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8, loc="lower left")
    
    # (2) System sum
    ax = axes[0, 1]
    ax.set_title("System On-Axis Response")
    ax.semilogx(F, results["system_sum"], color="0.15", lw=2.8, label="System sum (power)")
    ax.semilogx(F, results["coherent_sum"], color="0.5", lw=1.5, ls="--", label="Coherent sum (voltage)")
    ax.axvline(150, color="0.4", ls=":", alpha=0.5)
    ax.axvline(fc_mid, color="0.4", ls=":", alpha=0.5)
    ax.axhline(0, color="0.4", ls=":", alpha=0.3)
    # Normalize to 0 dB at 1 kHz
    ref_idx = np.argmin(np.abs(F - 1000.0))
    ref_val = results["system_sum"][ref_idx]
    if np.isfinite(ref_val):
        ax.set_ylim(ref_val - 15, ref_val + 10)
    ax.set_xlim(20, 20000)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("SPL [dB]")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=9)
    
    # (3) Woofer processing chain
    ax = axes[1, 0]
    ax.set_title("Woofer Processing Chain")
    ax.semilogx(F, results["woofer_raw"], color="tab:red", lw=1, alpha=0.4, label="Raw datasheet")
    ax.semilogx(F, results["woofer_sealed"], color="tab:red", lw=1.2, ls="--", label="Sealed cabinet (Fc=34.5, Q=0.62)")
    ax.semilogx(F, results["woofer_pair"], color="tab:red", lw=1.5, ls="-.", label="+ Pair (+3 dB)")
    ax.semilogx(F, results["woofer_baffle"], color="tab:red", lw=1.8, ls=":", label="+ Baffle step (300mm)")
    ax.semilogx(F, results["woofer_filtered"], color="tab:red", lw=2.5, label="+ LR4 LP@150 Hz")
    ax.axvline(150, color="0.4", ls=":", alpha=0.5)
    ax.set_xlim(20, 2000)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("SPL [dB]")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=7.5, loc="lower left")
    
    # (4) Tweeter processing chain
    ax = axes[1, 1]
    ax.set_title("Tweeter Processing Chain")
    ax.semilogx(F, results["tweeter_raw"], color="tab:blue", lw=1, alpha=0.4, label="Raw datasheet")
    if "tweeter_waveguide_gain" in results:
        ax.semilogx(F, results["tweeter_wg"], color="tab:blue", lw=1.2, ls="--", label="+ WG212 loading (+3 dB)")
    ax.semilogx(F, results["tweeter_baffle"], color="tab:blue", lw=1.5, ls="-.", label="+ Baffle step")
    ax.semilogx(F, results["tweeter_filtered"], color="tab:blue", lw=1.8, ls=":", label=f"+ LR4 HP@{fc_mid:.0f} Hz")
    ax.semilogx(F, results["tweeter_final"], color="tab:blue", lw=2.5, label=f"+ Level match ({results['tweeter_level_adjust']:.1f} dB)")
    ax.axvline(fc_mid, color="0.4", ls=":", alpha=0.5)
    ax.set_xlim(100, 20000)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("SPL [dB]")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=7.5, loc="lower left")
    
    plt.tight_layout()
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, dpi=150)
    plt.close()
    print(f"  Wrote {path}")


print("\nGenerating plots...")
plot_system("Mk2 (H2606/920000 in WG212, 1250 Hz)", mk2, FC_MID_MK2, {}, "mk2_system_real.png")
plot_system("Mk3 (SB26STAC-C000-4, 1100 Hz)", mk3, FC_MID_MK3, {}, "mk3_system_real.png")

# Comparison plot
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle("Mk2 vs Mk3 Comparison (Real Datasheet Curves)", fontsize=14, fontweight="bold")

# (1) System response comparison
ax = axes[0, 0]
ax.set_title("System On-Axis Response")
ax.semilogx(F, mk2["system_sum"], color="tab:blue", lw=2.5, label="Mk2 (H2606/WG212, 1250 Hz)")
ax.semilogx(F, mk3["system_sum"], color="tab:orange", lw=2.5, label="Mk3 (SB26STAC, 1100 Hz)")
ax.axvline(150, color="0.4", ls=":", alpha=0.5, label="150 Hz XO")
ax.axvline(1250, color="tab:blue", ls=":", alpha=0.4, label="1250 Hz XO (mk2)")
ax.axvline(1100, color="tab:orange", ls=":", alpha=0.4, label="1100 Hz XO (mk3)")
ax.axhline(0, color="0.4", ls=":", alpha=0.3)
# Normalize both to 0 dB at 1 kHz
ref_idx = np.argmin(np.abs(F - 1000.0))
mk2_ref = mk2["system_sum"][ref_idx]
mk3_ref = mk3["system_sum"][ref_idx]
if np.isfinite(mk2_ref) and np.isfinite(mk3_ref):
    ax.set_ylim(min(mk2_ref, mk3_ref) - 12, max(mk2_ref, mk3_ref) + 8)
ax.set_xlim(20, 20000)
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("SPL [dB]")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8)

# (2) Difference plot
ax = axes[0, 1]
ax.set_title("Mk2 - Mk3 Difference")
diff = mk2["system_sum"] - mk3["system_sum"]
ax.semilogx(F, diff, color="0.15", lw=2)
ax.axhline(0, color="0.4", ls="-", alpha=0.5)
ax.axhline(3, color="0.6", ls=":", alpha=0.3)
ax.axhline(-3, color="0.6", ls=":", alpha=0.3)
ax.axvline(1250, color="tab:blue", ls=":", alpha=0.4)
ax.axvline(1100, color="tab:orange", ls=":", alpha=0.4)
ax.set_xlim(100, 20000)
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("Δ SPL [dB]")
ax.grid(True, which="both", alpha=0.25)
ax.set_title("Mk2 - Mk3 (positive = mk2 louder)")

# (3) Tweeter comparison
ax = axes[1, 0]
ax.set_title("Tweeter Comparison (After Crossover + Level Match)")
ax.semilogx(F, mk2["tweeter_final"], color="tab:blue", lw=2, label="H2606 in WG212 (HP@1250)")
ax.semilogx(F, mk3["tweeter_final"], color="tab:orange", lw=2, label="SB26STAC (HP@1100)")
ax.semilogx(F, h2606_spl, color="tab:blue", lw=1, alpha=0.3, ls="--", label="H2606 raw")
ax.semilogx(F, sb26_spl, color="tab:orange", lw=1, alpha=0.3, ls="--", label="SB26 raw")
ax.axvline(1250, color="tab:blue", ls=":", alpha=0.4)
ax.axvline(1100, color="tab:orange", ls=":", alpha=0.4)
ax.set_xlim(200, 20000)
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("SPL [dB]")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8)

# (4) Midrange comparison (same driver, different crossover)
ax = axes[1, 1]
ax.set_title("Midrange (15W/4434G00) — Same Driver, Different Crossover")
ax.semilogx(F, mk2["mid_filtered"], color="tab:blue", lw=2, label="Mk2: LP@1250 Hz")
ax.semilogx(F, mk3["mid_filtered"], color="tab:orange", lw=2, label="Mk3: LP@1100 Hz")
ax.semilogx(F, mid15w_spl, color="tab:green", lw=1, alpha=0.3, ls="--", label="Raw datasheet")
ax.axvline(1250, color="tab:blue", ls=":", alpha=0.4)
ax.axvline(1100, color="tab:orange", ls=":", alpha=0.4)
ax.axvline(150, color="0.4", ls=":", alpha=0.5)
ax.set_xlim(50, 5000)
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("SPL [dB]")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8)

plt.tight_layout()
comp_path = os.path.join(PLOT_DIR, "mk2_vs_mk3_comparison.png")
fig.savefig(comp_path, dpi=150)
plt.close()
print(f"  Wrote {comp_path}")

# Print summary statistics
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")

for label, results in [("Mk2", mk2), ("Mk3", mk3)]:
    sys_sum = results["system_sum"]
    valid = np.isfinite(sys_sum)
    if np.any(valid):
        # Normalize to 1 kHz
        ref_idx = np.argmin(np.abs(F - 1000.0))
        ref = sys_sum[ref_idx]
        normalized = sys_sum - ref
        
        # Band-limited metrics
        def band_avg(arr, f_lo, f_hi):
            mask = (F >= f_lo) & (F <= f_hi) & np.isfinite(arr)
            return np.mean(arr[mask]) if np.any(mask) else np.nan
        
        print(f"\n{label}:")
        print(f"  System sum (normalized to 0 dB @ 1 kHz):")
        print(f"    20-100 Hz avg:   {band_avg(normalized, 20, 100):.1f} dB")
        print(f"    100-500 Hz avg:  {band_avg(normalized, 100, 500):.1f} dB")
        print(f"    500-2k Hz avg:   {band_avg(normalized, 500, 2000):.1f} dB")
        print(f"    2k-10k Hz avg:   {band_avg(normalized, 2000, 10000):.1f} dB")
        print(f"    10k-20k Hz avg:  {band_avg(normalized, 10000, 20000):.1f} dB")
        print(f"    ±3 dB bandwidth: {F[np.where(np.isfinite(normalized) & (np.abs(normalized) <= 3))[0][0]]:.0f} - "
              f"{F[np.where(np.isfinite(normalized) & (np.abs(normalized) <= 3))[0][-1]]:.0f} Hz")

print("\nDone.")
