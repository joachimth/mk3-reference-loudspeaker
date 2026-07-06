"""
Phase and group delay analysis for Mk3 v9 DSP crossover
=========================================================

Analyzes the phase response and group delay of each driver path
and their summed combination for the Mk3 v9 crossover (200 Hz BW4 + 1100 Hz LR4).

Shows:
  1. Phase response per driver path
  2. Group delay per driver path  
  3. Summed phase coherence at crossover points
  4. Excess group delay from cascaded filters (woofer: 4 filters deep!)

The woofer path in particular deserves scrutiny: Sub HP 18 LR4 × 2 +
LT 39→28 Hz + LP 200 BW4 × 2 = 6 biquad stages in series. That's a
lot of phase shift accumulating at the bottom end.

Output: simulations/plots/phase_analysis.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from cabinet_params import baffle_step_db_side, baffle_step_db_front

c_speed = 343.0

# ============================================================
#  Frequency grid
# ============================================================
f = np.logspace(np.log10(10), np.log10(22000), 6000)
fs = 96000  # MiniDSP sample rate

# ============================================================
#  Biquad building blocks for phase calculation
#  We compute complex transfer functions, not just magnitude
# ============================================================

def biquad_tf(b0, b1, b2, a1, a2):
    """Returns H(s) evaluation function for biquad coeffs at frequency f(s)."""
    # Convert to analog prewarped s-plane
    # Direct form: H(z) = (b0 + b1 z^-1 + b2 z^-2) / (1 + a1 z^-1 + a2 z^-2)
    # We'll compute directly in z-domain
    def response(f_hz):
        omega = 2 * np.pi * f_hz / fs
        z1 = np.exp(-1j * omega)
        z2 = np.exp(-2j * omega)
        num = b0 + b1 * z1 + b2 * z2
        den = 1.0 + a1 * z1 + a2 * z2
        return num / den
    return response

def butterworth_4th_tf(fc, lp=True):
    """4th-order Butterworth transfer function (cascade of two 2nd-order sections).
    
    Returns function H(f) -> complex.
    
    4th-order BW: two cascaded 2nd-order sections.
    Section 1: Q=0.541 (1/1.8478)
    Section 2: Q=1.307 (1/0.7654)
    """
    wc = 2 * np.pi * fc
    T = 1.0 / fs
    
    # Bilinear transform pre-warping
    wp = 2.0 / T * np.tan(wc * T / 2.0)
    
    # Normalized s-plane poles for BW4
    # s^4 + 2.6131 s^3 + 3.4142 s^2 + 2.6131 s + 1
    # Section 1: Q1 = 0.5412 (1/1.8478)
    # Section 2: Q2 = 1.3066 (1/0.7654)
    
    def analog_section(s, Q):
        """H(s) = 1/(s^2 + s/Q + 1) for LP, s^2/(s^2 + s/Q + 1) for HP"""
        if lp:
            return 1.0 / (s**2 + s/Q + 1.0)
        else:
            return s**2 / (s**2 + s/Q + 1.0)
    
    def response(f_hz):
        s = 1j * f_hz / (wp / (2*np.pi))
        H1 = analog_section(s, 0.5412)
        H2 = analog_section(s, 1.3066)
        return H1 * H2
    
    return response

def butterworth_2nd_tf(fc, lp=True):
    """2nd-order Butterworth. H(s) = 1/(s^2 + sqrt(2)*s + 1) or s^2/(...)."""
    def response(f_hz):
        s = 1j * f_hz / fc
        if lp:
            return 1.0 / (s**2 + np.sqrt(2)*s + 1.0)
        else:
            return s**2 / (s**2 + np.sqrt(2)*s + 1.0)
    return response

def linkwitz_riley_4th_tf(fc, lp=True):
    """LR4 = cascade of two LR2 sections, each Q=0.707"""
    def response(f_hz):
        s = 1j * f_hz / fc
        if lp:
            H = 1.0 / (s**2 + s/0.7071 + 1.0)
        else:
            H = s**2 / (s**2 + s/0.7071 + 1.0)
        return H * H
    return response

def linkwitz_riley_2nd_tf(fc, lp=True):
    """LR2 = Sallen-Key Q=0.707"""
    def response(f_hz):
        s = 1j * f_hz / fc
        if lp:
            return 1.0 / (s**2 + s/0.7071 + 1.0)
        else:
            return s**2 / (s**2 + s/0.7071 + 1.0)
    return response

def sub_hp_18_lr4_tf():
    """18 Hz LR4 highpass."""
    return linkwitz_riley_4th_tf(18.0, lp=False)

def lt_tf(f0=39.0, f1=28.0, Q0=0.76, Q1=0.707):
    """Linkwitz Transform from (f0, Q0) to (f1, Q1).
    
    H(s) = (s^2 + s·ω0/Q0 + ω0²) / (s^2 + s·ω1/Q1 + ω1²)
    """
    w0 = 2*np.pi*f0
    w1 = 2*np.pi*f1
    
    def response(f_hz):
        s = 1j * 2*np.pi * f_hz
        num = s**2 + s*w0/Q0 + w0**2
        den = s**2 + s*w1/Q1 + w1**2
        return num / den
    
    return response


# ============================================================
#  Build driver path transfer functions
# ============================================================

# Woofer path: 12SW × 2 in sealed + baffle step + filters
# H_w(s) = Sub HP18-LR4 × Sub HP18-LR4 × LT × LP200-BW4 × LP200-BW4
woofer_hp1 = sub_hp_18_lr4_tf()
woofer_hp2 = sub_hp_18_lr4_tf()  # second LR4 stage
woofer_lt = lt_tf()
woofer_lp1 = butterworth_4th_tf(200.0, lp=True)
woofer_lp2 = butterworth_4th_tf(200.0, lp=True)  # second BW4 stage

def woofer_path_tf(freqs):
    H = np.ones_like(freqs, dtype=complex)
    H *= woofer_hp1(freqs)
    H *= woofer_hp2(freqs)
    H *= woofer_lt(freqs)
    H *= woofer_lp1(freqs)
    H *= woofer_lp2(freqs)
    return H

# Mid path: HP200-BW4 × HP200-BW4 × LP1100-LR4 × LP1100-LR4
mid_hp1 = butterworth_4th_tf(200.0, lp=False)
mid_hp2 = butterworth_4th_tf(200.0, lp=False)
mid_lp1 = linkwitz_riley_4th_tf(1100.0, lp=True)
mid_lp2 = linkwitz_riley_4th_tf(1100.0, lp=True)

def mid_path_tf(freqs):
    H = np.ones_like(freqs, dtype=complex)
    H *= mid_hp1(freqs)
    H *= mid_hp2(freqs)
    H *= mid_lp1(freqs)
    H *= mid_lp2(freqs)
    return H

# Tweeter path: HP1100-LR4 × HP1100-LR4 + 120 µs delay
tweeter_hp1 = linkwitz_riley_4th_tf(1100.0, lp=False)
tweeter_hp2 = linkwitz_riley_4th_tf(1100.0, lp=False)

def tweeter_path_tf(freqs):
    H = np.ones_like(freqs, dtype=complex)
    H *= tweeter_hp1(freqs)
    H *= tweeter_hp2(freqs)
    # 120 µs delay = phase shift of -2π·f·120e-6
    H *= np.exp(-2j * np.pi * freqs * 120e-6)
    return H

# ============================================================
#  Compute phase and group delay
# ============================================================

def compute_phase(H):
    """Unwrapped phase in radians."""
    return np.unwrap(np.angle(H))

def group_delay(phase, freqs):
    """Group delay = -dφ/dω in seconds.
    
    τ_g = -dφ/dω = -dφ/(2π·df) when phase is in radians and freqs in Hz
    """
    df = np.diff(freqs)
    dphi = np.diff(phase)
    tau = -dphi / (2 * np.pi * df)
    # Pad last value (match length)
    return np.append(tau, tau[-1])


# Compute for all three paths
H_w = woofer_path_tf(f)
H_m = mid_path_tf(f)
H_t = tweeter_path_tf(f)

phi_w = compute_phase(H_w)
phi_m = compute_phase(H_m)
phi_t = compute_phase(H_t)

gd_w = group_delay(phi_w, f)
gd_m = group_delay(phi_m, f)
gd_t = group_delay(phi_t, f)

# Summed system (acoustic, not electrical — skip baffle step & driver response
# for pure phase analysis of the filter chain)
H_sum = H_w + H_m + H_t
phi_sum = compute_phase(H_sum)
gd_sum = group_delay(phi_sum, f)

# Phase difference at crossover points
idx_200 = np.argmin(np.abs(f - 200))
idx_1100 = np.argmin(np.abs(f - 1100))

phase_diff_wm_200 = np.rad2deg(phi_w[idx_200] - phi_m[idx_200])
phase_diff_mt_1100 = np.rad2deg(phi_m[idx_1100] - phi_t[idx_1100])

# ============================================================
#  Print summary
# ============================================================
print("=" * 70)
print("Mk3 v9 — Phase & Group Delay Analysis")
print("=" * 70)
print(f"\nCrossover: 200 Hz BW4 (woofer-mid) | 1100 Hz LR4 (mid-tweeter)")
print(f"Tweeter delay: 120 µs (waveguide depth compensation)")
print(f"\n--- Phase at crossover points ---")
print(f"200 Hz:    φ_woofer={np.rad2deg(phi_w[idx_200]):.1f}°  φ_mid={np.rad2deg(phi_m[idx_200]):.1f}°  Δ={phase_diff_wm_200:.1f}°")
print(f"1100 Hz:   φ_mid={np.rad2deg(phi_m[idx_1100]):.1f}°  φ_tweeter={np.rad2deg(phi_t[idx_1100]):.1f}°  Δ={phase_diff_mt_1100:.1f}°")
print(f"\n--- Group delay ---")
print(f"{'Path':<12s} {'@20Hz':>8s} {'@50Hz':>8s} {'@200Hz':>8s} {'@500Hz':>8s} {'@1kHz':>8s} {'@5kHz':>8s}")
print("-" * 68)
for name, gd in [("Woofer", gd_w), ("Mid", gd_m), ("Tweeter", gd_t), ("System", gd_sum)]:
    vals = [gd[np.argmin(np.abs(f - x))] * 1000 for x in [20, 50, 200, 500, 1000, 5000]]
    print(f"{name:<12s} {vals[0]:>8.2f} {vals[1]:>8.2f} {vals[2]:>8.2f} {vals[3]:>8.2f} {vals[4]:>8.2f} {vals[5]:>8.2f}")

# Excess group delay at 20 Hz (woofer path has 4 filter stages in series)
print(f"\n--- Excess group delay analysis ---")
print(f"Woofer path filter chain: HP18-LR4 × 2 + LT 39→28 Hz + LP200-BW4 × 2 = 6 biquads")
print(f"  20 Hz group delay: {gd_w[np.argmin(np.abs(f-20))]*1000:.1f} ms")
print(f"  30 Hz group delay: {gd_w[np.argmin(np.abs(f-30))]*1000:.1f} ms")
print(f"  50 Hz group delay: {gd_w[np.argmin(np.abs(f-50))]*1000:.1f} ms")
# Compare to just the sealed rolloff (no filters)
# The 12SW in a sealed box has Fc=28, Qtc=0.707
s = 1j * f / 28.0
H_sealed = s**2 / (s**2 + s/0.707 + 1.0)
phi_sealed = compute_phase(H_sealed)
gd_sealed = group_delay(phi_sealed, f)
excess_20 = gd_w[np.argmin(np.abs(f-20))] - gd_sealed[np.argmin(np.abs(f-20))]
excess_30 = gd_w[np.argmin(np.abs(f-30))] - gd_sealed[np.argmin(np.abs(f-30))]
print(f"  Excess over sealed rolloff @20 Hz: {excess_20*1000:.1f} ms")
print(f"  Excess over sealed rolloff @30 Hz: {excess_30*1000:.1f} ms")

# ============================================================
#  Plot
# ============================================================
fig, axes = plt.subplots(4, 1, figsize=(16, 18), sharex=True)

colors = {"Woofer": "#dc2626", "Mid": "#059669", "Tweeter": "#2563eb", "System": "#7c3aed"}

# Panel 1: Phase response
ax = axes[0]
ax.semilogx(f, np.rad2deg(phi_w), lw=2, color=colors["Woofer"], alpha=0.8, label="Woofer path")
ax.semilogx(f, np.rad2deg(phi_m), lw=2, color=colors["Mid"], alpha=0.8, label="Mid path")
ax.semilogx(f, np.rad2deg(phi_t), lw=2, color=colors["Tweeter"], alpha=0.8, label="Tweeter path")
ax.semilogx(f, np.rad2deg(phi_sum), lw=3, color=colors["System"], alpha=0.9, label="System sum")
ax.axvline(200, color="0.5", ls=":", lw=1, alpha=0.5)
ax.axvline(1100, color="0.5", ls=":", lw=1, alpha=0.5)
# Mark phase at crossover
ax.plot(200, np.rad2deg(phi_w[idx_200]), 'o', color=colors["Woofer"], ms=6)
ax.plot(200, np.rad2deg(phi_m[idx_200]), 'o', color=colors["Mid"], ms=6)
ax.plot(1100, np.rad2deg(phi_m[idx_1100]), 'o', color=colors["Mid"], ms=6)
ax.plot(1100, np.rad2deg(phi_t[idx_1100]), 'o', color=colors["Tweeter"], ms=6)
ax.set_ylabel("Phase [°]")
ax.set_title("Unwrapped Phase Response — Mk3 v9 DSP Filter Chain", fontsize=13, fontweight="bold")
ax.legend(fontsize=9, loc="upper left")
ax.grid(True, which="both", alpha=0.2)
ax.set_ylim(-1800, 200)  # Woofer accumulates lots of phase

# Panel 2: Group delay
ax = axes[1]
ax.semilogx(f, gd_w*1000, lw=2, color=colors["Woofer"], alpha=0.8, label="Woofer path")
ax.semilogx(f, gd_m*1000, lw=2, color=colors["Mid"], alpha=0.8, label="Mid path")
ax.semilogx(f, gd_t*1000, lw=2, color=colors["Tweeter"], alpha=0.8, label="Tweeter path")
ax.semilogx(f, gd_sum*1000, lw=3, color=colors["System"], alpha=0.9, label="System sum")
ax.axvline(200, color="0.5", ls=":", lw=1, alpha=0.5)
ax.axvline(1100, color="0.5", ls=":", lw=1, alpha=0.5)
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.set_ylabel("Group delay [ms]")
ax.set_title("Group Delay — Each path sees different filter depth", fontsize=13, fontweight="bold")
ax.legend(fontsize=9, loc="upper right")
ax.grid(True, which="both", alpha=0.2)
ax.set_ylim(0, 25)

# Panel 3: Woofer path filter stage breakdown
ax = axes[2]
# Compute individual stage group delays
H_stages = {}
H_stages["HP 18 LR4 ×2"] = woofer_hp1(f) * woofer_hp2(f)
H_stages["LT 39→28 Hz"] = woofer_lt(f)
H_stages["LP 200 BW4 ×2"] = woofer_lp1(f) * woofer_lp2(f)

total_gd = np.zeros_like(f)
for name, H_stage in H_stages.items():
    gd_stage = group_delay(compute_phase(H_stage), f)
    total_gd += gd_stage
    ax.semilogx(f, gd_stage*1000, lw=1.5, ls="--", alpha=0.7, label=name)

ax.semilogx(f, total_gd*1000, lw=2.5, color="#7c3aed", alpha=0.9, label="Sum (woofer path)")
ax.axvline(200, color="0.5", ls=":", lw=1, alpha=0.5)
ax.axvline(18, color="0.5", ls=":", lw=1, alpha=0.3)
ax.set_ylabel("Group delay per stage [ms]")
ax.set_title("Woofer path — Group Delay Breakdown by Filter Stage", fontsize=13, fontweight="bold")
ax.legend(fontsize=9, loc="upper right")
ax.grid(True, which="both", alpha=0.2)
ax.set_ylim(0, 20)
ax.set_xlim(8, 22000)

# Panel 4: 1100 Hz crossover phase coherence zoom
ax = axes[3]
# Zoom region around mid-tweeter crossover
zoom_f = f[(f > 500) & (f < 4000)]
idx_zoom = np.where((f > 500) & (f < 4000))[0]
ax.plot(zoom_f, np.rad2deg(phi_m[idx_zoom]), lw=2.5, color=colors["Mid"], label="Mid path (HP 200 BW4 ×2 + LP 1100 LR4 ×2)")
ax.plot(zoom_f, np.rad2deg(phi_t[idx_zoom]), lw=2.5, color=colors["Tweeter"], label="Tweeter path (HP 1100 LR4 ×2 + 120 µs delay)")
ax.plot(zoom_f, np.rad2deg(phi_sum[idx_zoom]), lw=3, color=colors["System"], label="System sum")
ax.axvline(1100, color="0.5", ls=":", lw=1.5, alpha=0.7)
# Annotate phase difference
tx = 1100
ty_mid = np.rad2deg(phi_m[idx_1100])
ty_tw = np.rad2deg(phi_t[idx_1100])
ax.annotate(f"Δφ = {phase_diff_mt_1100:.1f}°",
            xy=(tx, (ty_mid+ty_tw)/2),
            xytext=(tx*0.65, ty_mid-200),
            fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="0.4", lw=1.5))
ax.set_ylabel("Phase [°]")
ax.set_xlabel("Frequency [Hz]")
ax.set_title(f"Mid-Tweeter Crossover Zoom — Phase Coherence @ 1100 Hz (Δ={phase_diff_mt_1100:.1f}°)",
             fontsize=13, fontweight="bold")
ax.legend(fontsize=8, loc="lower left")
ax.grid(True, which="both", alpha=0.2)
ax.set_xlim(500, 4000)
ax.set_xticks([500, 700, 1000, 1500, 2000, 3000, 4000])
ax.set_xticklabels(["500", "700", "1k", "1.5k", "2k", "3k", "4k"])

fig.tight_layout()
script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'phase_analysis.png')
fig.savefig(out_png, dpi=150)
print(f"\nwrote {out_png}")
