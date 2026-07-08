"""
System frequency response with datasheet curves (mk3 — SB26STAC @ 1100 Hz)
==========================================================================

Uses ACTUAL frequency response curves extracted from the manufacturer
datasheets (digitized from the PDF graphs), combined with:

  1. Baffle step (Vanderkooy model, v9 cabinet baffle (from cabinet_params.py))
  2. Waveguide loading (WG212 acoustic gain above control limit)
  3. Sealed woofer alignment (2x GRS 12SW-4HE, Fc=28 Hz with LT, Qtc=0.707)
  4. LR4 crossover filters (150 Hz + 1100 Hz)
  5. DSP level matching (tweeter pad to match midrange)

Data sources:
  - SB26STAC-C000-4: assets/datasheets/SB26STAC-C000-4.pdf (digitized)
  - 15W/4434G00: ScanSpeak datasheet (digitized)
  - GRS 8SW-4HE-8: modeled from T/S params (sealed alignment)
  - Baffle step: Vanderkooy/Keele, v9 baffle
  - Waveguide loading: WG212 control limit ~1620 Hz, +2.5 dB gain

ASSUMPTIONS
  - Datasheet curves are measured on IEC baffle (31.6 cm mic distance,
    normalized to 2.83V/1m). On-axis curves used.
  - Baffle step is applied to ALL drivers (they're all on the same baffle).
    The step transition is ~365 Hz for the v9 baffle.
  - Waveguide loading adds acoustic gain above the control limit. The
    bare-dome tweeter response (from datasheet) is modified by the WG212
    loading: +2.5 dB above 1620 Hz, transitioning smoothly from 1100-1800 Hz.
  - The SB26STAC has NO horn — its datasheet curve is the bare dome on an
    IEC baffle. The WG212 provides ALL the loading.
  - Room gain not included (anechoic estimate).
  - DSP EQ not applied (raw response shown — DSP would flatten this).

Output: simulations/plots/system_response_realistic.png
        simulations/csv/system_response_realistic.csv
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

c_speed = 343.0

# ============================================================
#  Load digitized datasheet curves from CSV files
# ============================================================
import csv

def load_freq_response_csv(filepath, col_name="spl_db"):
    """Load a datasheet frequency response CSV and return freq, spl arrays."""
    freqs, spls = [], []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    full_path = os.path.join(repo_root, filepath)
    with open(full_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                freq = float(row["freq_hz"])
                spl_str = row.get(col_name, "")
                if spl_str and spl_str.strip():
                    spl = float(spl_str)
                    freqs.append(freq)
                    spls.append(spl)
            except (ValueError, KeyError):
                continue
    freqs = np.array(freqs)
    spls = np.array(spls)
    sort_idx = np.argsort(freqs)
    return freqs[sort_idx], spls[sort_idx]

sb26_freq, sb26_spl = load_freq_response_csv("assets/datasheets/SB26STAC-C000-4_freq_response.csv")
w15_freq, w15_spl = load_freq_response_csv("assets/datasheets/15W-4434G00_freq_response.csv")
print(f"  SB26STAC: {len(sb26_freq)} pts, {sb26_freq[0]:.0f}-{sb26_freq[-1]:.0f} Hz")
print(f"  15W/4434G00: {len(w15_freq)} pts, {w15_freq[0]:.0f}-{w15_freq[-1]:.0f} Hz")

# ============================================================
#  Filter helpers
# ============================================================
def lr4_lp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2) + 1e-12)

def lr4_hp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2) + 1e-12)

def lr4_lp_lin(f, fc):
    s = 1j * f / fc
    return np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2)

def lr4_hp_lin(f, fc):
    s = 1j * f / fc
    return np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2)

# ============================================================
#  Baffle step model (Vanderkooy / Keele)
# ============================================================
# Cabinet: 300mm wide, 420mm deep (v9, from cabinet.scad)
# Mean baffle-edge distance: a = sqrt((150^2 + 185^2)/2) = 168 mm
a_h = 0.150   # half-width (dominant edge)
a_d = 0.185   # half-depth
a_mean = np.sqrt((a_h**2 + a_d**2) / 2.0)  # 0.168 m
f_bs = c_speed / (2.0 * np.pi * a_mean)  # ~325 Hz

def baffle_step_db(f, a=0.168):
    """Vanderkooy single-pole baffle step. Returns dB relative to half-space.
    Low freq: -6 dB (4π radiation). High freq: 0 dB (2π radiation).
    H = (0.5 + j*f/fbs) / (1 + j*f/fbs) — step from 0.5 to 1.0"""
    fbs = c_speed / (2.0 * np.pi * a)
    x = 1j * f / fbs
    H = (0.5 + x) / (1.0 + x)
    return 20.0 * np.log10(np.abs(H))

print(f"Baffle step: f_bs = {f_bs:.0f} Hz (a={a_mean*1000:.0f} mm)")
print(f"  At 100 Hz: {baffle_step_db(np.array([100.0]))[0]:.1f} dB")
print(f"  At 500 Hz: {baffle_step_db(np.array([500.0]))[0]:.1f} dB")
print(f"  At 2000 Hz: {baffle_step_db(np.array([2000.0]))[0]:.1f} dB")

# ============================================================
#  Waveguide loading model
# ============================================================
# WG212 control limit: ~1620 Hz (above this, constant directivity)
# Below: bare dome behavior
# The waveguide provides acoustic loading gain above the control limit.
# For a bare-dome tweeter (SB26STAC): +2.5 dB gain above 1620 Hz
F_CTRL = 1620.0

def wg_loading_db(f, gain_db, f_low=1000, f_high=2000):
    """Waveguide loading gain: 0 dB below f_low, gain_db above f_high.
    Smooth transition using tanh over ~0.3 octaves centered between f_low and f_high."""
    f_mid = np.sqrt(f_low * f_high)  # geometric mean (log center)
    spread = (np.log10(f_high) - np.log10(f_low)) * 0.3  # ~0.3 octave half-width
    t = 0.5 * (1.0 + np.tanh((np.log10(f) - np.log10(f_mid)) / spread))
    return gain_db * t

# ============================================================
#  Woofer model: sealed alignment
# ============================================================
# 2x GRS 12SW-4HE in ~75L sealed (bass volume under divider plate)
# Fs=22, Qts=0.43, Vas=80.4L per driver -> Vas_total=160.8L
# In 75L: Qtc=0.76, Fc=39.0 Hz
# With Linkwitz Transform: Fc=28 Hz, Qtc=0.707
# Sensitivity 84.5 dB per driver, 2 in push-push = +3 dB = 87.5 dB half-space
Fc_w = 28.0; Qtc_w = 0.707; sens_w = 84.5  # per driver, 2 drivers ≈ +3 dB (with LT)

def woofer_response(f):
    """Sealed woofer pair response with Linkwitz Transform."""
    s = 1j * f / Fc_w
    H_sealed = s**2 / (s**2 + s/Qtc_w + 1)
    mag = 20*np.log10(np.abs(H_sealed) + 1e-12) + (sens_w + 3.0)  # +3 dB for 2 drivers
    return mag

# ============================================================
#  Build system response (mk3: SB26STAC @ 1100 Hz)
# ============================================================
f = np.logspace(np.log10(20), np.log10(22000), 2000)
bs = baffle_step_db(f)  # baffle step at each frequency

# Interpolate datasheet curves onto our frequency grid
def interp_curve(freq_data, spl_data, f_target, fill_below=None, fill_above=None):
    """Interpolate with optional fill values outside data range."""
    spl = np.interp(f_target, freq_data, spl_data)
    if fill_below is not None:
        spl[f_target < freq_data[0]] = fill_below
    if fill_above is not None:
        spl[f_target > freq_data[-1]] = fill_above
    return spl

# mk3 design parameters
fc_tw = 1100.0
tw_pad = 1.8       # dB attenuation to match midrange
wg_gain = 2.5      # SB26STAC bare dome, WG212 provides full loading

# --- Woofer ---
mag_w_raw = woofer_response(f)
mag_w = mag_w_raw + bs  # baffle step applies
mag_w += lr4_lp_db(f, 150.0)  # LP at 150 Hz

# --- Midrange: real datasheet curve ---
mag_m_raw = interp_curve(w15_freq, w15_spl, f, fill_below=89.7, fill_above=80.0)
# Apply baffle step to midrange (it's on the same baffle)
mag_m = mag_m_raw + bs
# Crossover: HP@150 + LP@1100
mag_m += lr4_hp_db(f, 150.0)
mag_m += lr4_lp_db(f, fc_tw)

# --- Tweeter: real datasheet curve + waveguide loading ---
mag_t_raw = interp_curve(sb26_freq, sb26_spl, f,
                          fill_below=sb26_spl[0] - 20,
                          fill_above=sb26_spl[-1] - 20)
# Baffle step: minimal effect above ~500 Hz, but apply for consistency
# Actually, for the tweeter range (>1 kHz), baffle step is ~0 dB, so skip
# Apply waveguide loading
wg_gain_curve = wg_loading_db(f, wg_gain, f_low=fc_tw, f_high=2000)
mag_t = mag_t_raw + wg_gain_curve
# Crossover: HP@1100
mag_t += lr4_hp_db(f, fc_tw)
# DSP pad to match midrange
mag_t_trimmed = mag_t - tw_pad

# --- System sum (linear domain for proper summation) ---
w_lin = 10**(mag_w / 20.0)
m_lin = 10**(mag_m / 20.0)
t_lin = 10**(mag_t_trimmed / 20.0)
mag_sum = 20*np.log10(w_lin + m_lin + t_lin + 1e-12)

# Print key metrics
fc_idx = np.argmin(np.abs(f - fc_tw))
# Use actual passband: 200 Hz - 15 kHz (above woofer rolloff)
pb = (f > 200) & (f < 15000)
ripple = np.max(mag_sum[pb]) - np.min(mag_sum[pb])
# Also measure 500-10k (midband flatness — what DSP targets)
pb_mid = (f > 500) & (f < 10000)
ripple_mid = np.max(mag_sum[pb_mid]) - np.min(mag_sum[pb_mid])
print(f"\nSystem response (SB26STAC @ 1100 Hz):")
print(f"  Tweeter pad: -{tw_pad:.1f} dB")
print(f"  WG gain: +{wg_gain:.1f} dB above {F_CTRL:.0f} Hz")
print(f"  Sum @ crossover ({fc_tw:.0f} Hz): {mag_sum[fc_idx]:.1f} dB")
print(f"  Passband ripple (200-15k): {ripple:.1f} dB")
print(f"  Midband ripple (500-10k): {ripple_mid:.1f} dB")
print(f"  Sum @ 100 Hz: {np.interp(100, f, mag_sum):.1f} dB")
print(f"  Sum @ 500 Hz: {np.interp(500, f, mag_sum):.1f} dB")
print(f"  Sum @ 2 kHz: {np.interp(2000, f, mag_sum):.1f} dB")
print(f"  Sum @ 10 kHz: {np.interp(10000, f, mag_sum):.1f} dB")

# ============================================================
#  PLOT: Realistic system response
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(15, 13), gridspec_kw={"height_ratios": [1.2, 1, 1]})

# --- Panel 1: Individual drivers + system sum ---
ax = axes[0]
ax.semilogx(f, mag_sum, lw=3.0, color="tab:blue", label="System sum")
ax.semilogx(f, mag_w, lw=1.2, color="tab:red", alpha=0.4, label="Woofer (2×GRS 12SW sealed + LT + baffle step)")
ax.semilogx(f, mag_m, lw=1.2, color="tab:green", alpha=0.4, label="Mid (15W real curve + baffle step + LR4)")
ax.semilogx(f, mag_t_trimmed, lw=1.2, color="tab:purple", alpha=0.4, label="Tweeter (SB26STAC real curve + WG loading + pad)")

# Baffle step curve
ax.semilogx(f, bs, lw=1.0, color="0.6", ls=":", alpha=0.5, label="Baffle step (-6 dB → 0 dB)")

ax.axvline(150, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.axvline(1100, color="tab:blue", ls=":", lw=1.0, alpha=0.3)
ax.text(150, 100, "150 Hz", ha="center", fontsize=8, color="0.4")
ax.text(1100, 100, "1100 Hz", ha="center", fontsize=8, color="tab:blue")
ax.set_xlim(20, 22000); ax.set_ylim(60, 105)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB]")
ax.set_title("Realistic system response — real datasheet curves + baffle step + waveguide loading (SB26STAC @ 1100 Hz)")
ax.legend(fontsize=7, loc="lower left", ncol=2)
ax.grid(True, which="both", alpha=0.25)

# --- Panel 2: Normalized sum ---
ax = axes[1]
ref_idx = np.argmin(np.abs(f - 500))
norm = mag_sum - mag_sum[ref_idx]
ax.semilogx(f, norm, lw=2.8, color="tab:blue", label="System sum (normalized @ 500 Hz)")
ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.axhline(3, color="0.4", ls=":", lw=0.5, alpha=0.2)
ax.axhline(-3, color="0.4", ls=":", lw=0.5, alpha=0.2)
ax.axvline(1100, color="tab:blue", ls=":", lw=0.8, alpha=0.2)
ax.set_xlim(20, 22000); ax.set_ylim(-20, 10)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB, norm @ 500 Hz]")
ax.set_title("Normalized system sum (0 dB @ 500 Hz) — pre-DSP")
ax.legend(fontsize=9)
ax.grid(True, which="both", alpha=0.25)

# --- Panel 3: Acoustic effects + DSP correction needed ---
ax = axes[2]
# Baffle step
ax.semilogx(f, bs, lw=2.0, color="tab:orange", label="Baffle step (v9 baffle)")
# WG loading
wg_curve = wg_loading_db(f, wg_gain, f_low=fc_tw, f_high=2000)
ax.semilogx(f, wg_curve, lw=1.8, color="tab:blue", ls="--", label=f"WG loading (+{wg_gain:.1f} dB)")

# DSP correction needed: inverse of sum deviation from target (flat @ 500 Hz)
ref_idx_dsp = np.argmin(np.abs(f - 500))
# Target: flat at the 500 Hz level, only in passband 200-15k
target = mag_sum[ref_idx_dsp]
correction = target - mag_sum  # positive = boost needed, negative = cut
# Only show in passband
corr_mask = (f > 100) & (f < 18000)
corr_display = np.where(corr_mask, correction, np.nan)
ax.semilogx(f, corr_display, lw=2.0, color="tab:green", alpha=0.7,
            label="DSP correction needed (boost/cut to flatten to 500 Hz)")

ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.axvline(f_bs, color="tab:orange", ls=":", lw=0.8, alpha=0.3)
ax.text(f_bs, -8, f"f_bs={f_bs:.0f} Hz", fontsize=8, color="tab:orange", ha="center")
ax.axvline(F_CTRL, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.text(F_CTRL, -8, f"WG={F_CTRL:.0f} Hz", fontsize=8, color="0.4", ha="center")
ax.set_xlim(20, 22000); ax.set_ylim(-12, 8)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Gain [dB]")
ax.set_title("Acoustic effects + DSP correction needed (boost/cut to flatten to 500 Hz reference)")
ax.legend(fontsize=7, loc="lower right", ncol=1)
ax.grid(True, which="both", alpha=0.25)

fig.suptitle("System response — SB26STAC-C000-4 @ 1100 Hz (real datasheet curves + baffle step + WG loading)\n"
             "Pre-DSP, anechoic. Curves digitized from manufacturer datasheets.",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.94])

script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '/workspace/mk3-reference-loudspeaker/simulations'
out = os.path.join(script_dir, 'plots', 'system_response_realistic.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=150)
print(f"\nwrote {out}")

# CSV export
csv_dir = os.path.join(os.path.dirname(out), '..', 'csv')
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, 'system_response_realistic.csv')
header = "freq_Hz,sum_dB,woofer_dB,mid_dB,tweeter_dB,baffle_step_dB,wg_loading_dB"
rows = [header]
for i in range(len(f)):
    rows.append(f"{f[i]:.2f},{mag_sum[i]:.4f},"
                f"{mag_w[i]:.4f},"
                f"{mag_m[i]:.4f},"
                f"{mag_t_trimmed[i]:.4f},"
                f"{bs[i]:.4f},{wg_curve[i]:.4f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")

# ============================================================
#  Summary
# ============================================================
print("\n" + "=" * 70)
print("REALISTIC SYSTEM RESPONSE SUMMARY (pre-DSP, anechoic)")
print("=" * 70)
ripple = np.max(mag_sum[pb]) - np.min(mag_sum[pb])
ripple_mid = np.max(mag_sum[pb_mid]) - np.min(mag_sum[pb_mid])
print(f"\nSystem response (SB26STAC @ 1100 Hz):")
print(f"  Passband ripple (200-15k, pre-DSP): {ripple:.1f} dB")
print(f"  Midband ripple (500-10k, pre-DSP): {ripple_mid:.1f} dB")
print(f"  Baffle step effect @ 300 Hz: {np.interp(300, f, bs):.1f} dB")
print(f"  WG loading @ 2 kHz: {np.interp(2000, f, wg_curve):.1f} dB")
print(f"  Sum @ 100 Hz: {np.interp(100, f, mag_sum):.1f} dB")
print(f"  Sum @ 500 Hz: {np.interp(500, f, mag_sum):.1f} dB")
print(f"  Sum @ 2 kHz: {np.interp(2000, f, mag_sum):.1f} dB")
print(f"  Sum @ 10 kHz: {np.interp(10000, f, mag_sum):.1f} dB")
# DSP correction in midband only
ref = np.interp(500, f, mag_sum)
devs_mid = (mag_sum - ref)[pb_mid]
max_corr_mid = np.max(np.abs(devs_mid))
devs_pb = (mag_sum - ref)[pb]
max_corr_pb = np.max(np.abs(devs_pb))
print(f"  DSP correction needed (midband 500-10k): ±{max_corr_mid:.1f} dB")
print(f"  DSP correction needed (passband 200-15k): ±{max_corr_pb:.1f} dB")
