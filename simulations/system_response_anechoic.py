"""
Anechoic system response with per-driver dB adjustments (pre-EQ, pre-room)
==========================================================================

Shows individual driver curves with their DSP level adjustments and the
coherent sum, so you can see exactly how the three drivers combine through
the LR4 crossovers before any room gain or EQ.

Drivers (v9):
  - 2× GRS 12SW-4HE (woofer, sealed + LT, DSP gain 0.0 dB unity)
  - ScanSpeak 18W/4424G00 (midrange, DSP gain -4.0 dB)
  - SB Acoustics SB26STAC-C000-4 (tweeter, DSP gain -9.0 dB)

Crossovers: BW4 at 200 Hz + LR4 at 1100 Hz
Baffle step: cabinet.scad via cabinet_params.py (side D/2=190mm, front W/2=160mm)
Waveguide loading: +2.5 dB above control limit

No room gain, no Harman target, no PEQ — just the raw anechoic sum.

Output: simulations/plots/system_response_anechoic.png
        simulations/csv/system_response_anechoic.csv
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv

from cabinet_params import baffle_step_db_side, baffle_step_db_front

c_speed = 343.0

# ============================================================
#  Load digitized datasheet curves
# ============================================================
def load_freq_response_csv(filepath, col_name="spl_db"):
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
w18_freq, w18_spl = load_freq_response_csv("assets/datasheets/18W-4424G00_freq_response.csv")

# ============================================================
#  Filters
# ============================================================
def lr4_lp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2) + 1e-12)

def lr4_hp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2) + 1e-12)

def bw4_lp_db(f, fc):
    """4th-order Butterworth lowpass: two cascaded sections Q=0.5412, Q=1.3066."""
    s = 1j * f / fc
    H1 = 1.0 / (s**2 + s/0.5412 + 1)
    H2 = 1.0 / (s**2 + s/1.3066 + 1)
    return 20*np.log10(np.abs(H1 * H2) + 1e-12)

def bw4_hp_db(f, fc):
    """4th-order Butterworth highpass: two cascaded sections Q=0.5412, Q=1.3066."""
    s = 1j * f / fc
    H1 = s**2 / (s**2 + s/0.5412 + 1)
    H2 = s**2 / (s**2 + s/1.3066 + 1)
    return 20*np.log10(np.abs(H1 * H2) + 1e-12)

def lr2_hp_db(f, fc):
    s = 1j * f / fc
    H = s**2 / (s**2 + s/0.707 + 1)
    return 20*np.log10(np.abs(H) + 1e-12)

# ============================================================
#  Baffle step (from cabinet.scad via cabinet_params.py)
#  Side woofers: a = D/2 = 0.190 m → f_bs = 287 Hz
#  Front mid/tweeter: a = W/2 = 0.160 m → f_bs = 341 Hz
#  bs_side / bs_front computed after frequency array f is defined below
# ============================================================

# ============================================================
#  Waveguide loading
# ============================================================
def wg_loading_db(f, gain_db, f_low=1000, f_high=2000):
    f_mid = np.sqrt(f_low * f_high)
    spread = (np.log10(f_high) - np.log10(f_low)) * 0.3
    t = 0.5 * (1.0 + np.tanh((np.log10(f) - np.log10(f_mid)) / spread))
    return gain_db * t

# ============================================================
#  Woofer model: 2x GRS 12SW-4HE sealed + LT
# ============================================================
Fc_w = 28.0; Qtc_w = 0.707; sens_w = 84.5  # per driver, 2 drivers +3 dB

def woofer_response(f):
    s = 1j * f / Fc_w
    H_sealed = s**2 / (s**2 + s/Qtc_w + 1)
    mag = 20*np.log10(np.abs(H_sealed) + 1e-12) + (sens_w + 3.0)
    return mag

# ============================================================
#  Parameters — v9 actual settings
# ============================================================
dsp_w_gain = 0.0     # woofer DSP gain (dB) — optimized for in-room Harman target
dsp_m_gain = -4.0    # mid DSP gain (dB)
dsp_t_gain = -9.0    # tweeter DSP gain (dB)
fc_woofer = 200.0
fc_tweeter = 1100.0
wg_gain = 2.5

f = np.logspace(np.log10(20), np.log10(22000), 2000)
bs_side = baffle_step_db_side(f)     # woofer (side panel, D/2 = 0.190m)
bs_front = baffle_step_db_front(f)   # mid + tweeter (front baffle, W/2 = 0.160m)

def interp_curve(freq_data, spl_data, f_target, fill_below=None, fill_above=None):
    spl = np.interp(f_target, freq_data, spl_data)
    if fill_below is not None:
        spl[f_target < freq_data[0]] = fill_below
    if fill_above is not None:
        spl[f_target > freq_data[-1]] = fill_above
    return spl

# ============================================================
#  Per-driver responses (with DSP level adjustments)
# ============================================================

# Woofer: 2x GRS 12SW-4HE sealed + LT + baffle step + LP@150 + subsonic + DSP gain
mag_w_raw = woofer_response(f)
mag_w = mag_w_raw + bs_side + bw4_lp_db(f, fc_woofer) + lr2_hp_db(f, 18.0) + dsp_w_gain

# Mid: 18W/4424G00 real curve + baffle step + HP@150 + LP@1100 + DSP gain
mag_m_raw = interp_curve(w18_freq, w18_spl, f, fill_below=92.5, fill_above=80.0)
mag_m = mag_m_raw + bs_front + bw4_hp_db(f, fc_woofer) + lr4_lp_db(f, fc_tweeter) + dsp_m_gain

# Tweeter: SB26STAC real curve + WG loading + HP@1100 + DSP gain
mag_t_raw = interp_curve(sb26_freq, sb26_spl, f,
                         fill_below=sb26_spl[0] - 20,
                         fill_above=sb26_spl[-1] - 20)
wg_gain_curve = wg_loading_db(f, wg_gain, f_low=fc_tweeter, f_high=2000)
mag_t = mag_t_raw + wg_gain_curve + lr4_hp_db(f, fc_tweeter) + dsp_t_gain

# Coherent sum
w_lin = 10**(mag_w / 20.0)
m_lin = 10**(mag_m / 20.0)
t_lin = 10**(mag_t / 20.0)
mag_sum = 20*np.log10(w_lin + m_lin + t_lin + 1e-12)

# Normalize to 500 Hz
ref_idx = np.argmin(np.abs(f - 500))
ref = mag_sum[ref_idx]
mag_sum_n = mag_sum - ref
mag_w_n = mag_w - ref
mag_m_n = mag_m - ref
mag_t_n = mag_t - ref

# ============================================================
#  Print metrics
# ============================================================
pb = (f > 200) & (f < 15000)
pb_mid = (f > 500) & (f < 10000)
ripple = np.max(mag_sum_n[pb]) - np.min(mag_sum_n[pb])
ripple_mid = np.max(mag_sum_n[pb_mid]) - np.min(mag_sum_n[pb_mid])

print(f"\nAnechoic system response (v9, pre-EQ, pre-room)")
print(f"  Woofer DSP gain: {dsp_w_gain:+.1f} dB")
print(f"  Mid DSP gain:    {dsp_m_gain:+.1f} dB")
print(f"  Tweeter DSP gain:{dsp_t_gain:+.1f} dB")
print(f"  Crossovers: LR4 {fc_woofer:.0f} Hz + {fc_tweeter:.0f} Hz")
print(f"  Waveguide loading: +{wg_gain:.1f} dB")
print(f"\n  Sum @100Hz:  {np.interp(100, f, mag_sum_n):.1f} dB")
print(f"  Sum @500Hz:  {np.interp(500, f, mag_sum_n):.1f} dB (reference)")
print(f"  Sum @1k:     {np.interp(1000, f, mag_sum_n):.1f} dB")
print(f"  Sum @2k:     {np.interp(2000, f, mag_sum_n):.1f} dB")
print(f"  Sum @10k:    {np.interp(10000, f, mag_sum_n):.1f} dB")
print(f"  Ripple 200-15k: {ripple:.1f} dB")
print(f"  Ripple 500-10k: {ripple_mid:.1f} dB")

# ============================================================
#  PLOT
# ============================================================
fig, ax = plt.subplots(figsize=(16, 9))

colors = {
    "woofer": "#dc2626",   # red
    "mid":    "#059669",   # green
    "tweeter":"#7c3aed",   # purple
    "sum":    "#2563eb",   # blue
}

# Individual drivers (dashed, thinner)
ax.semilogx(f, mag_w_n, lw=1.8, color=colors["woofer"], ls="--", alpha=0.7,
            label=f"Woofer  2×GRS 12SW-4HE  ({dsp_w_gain:+.1f} dB, LP {fc_woofer:.0f} Hz BW4)")
ax.semilogx(f, mag_m_n, lw=1.8, color=colors["mid"], ls="--", alpha=0.7,
            label=f"Mid     ScanSpeak 18W/4424G00  ({dsp_m_gain:+.1f} dB, HP {fc_woofer:.0f} BW4 / LP {fc_tweeter:.0f} Hz)")
ax.semilogx(f, mag_t_n, lw=1.8, color=colors["tweeter"], ls="--", alpha=0.7,
            label=f"Tweeter SB26STAC-C000-4  ({dsp_t_gain:+.1f} dB, HP {fc_tweeter:.0f} Hz, WG +{wg_gain:.1f} dB)")

# System sum (solid, thick)
ax.semilogx(f, mag_sum_n, lw=3.5, color=colors["sum"],
            label="System sum (coherent, normalized @500 Hz)")

# ±3 dB window
ax.axhspan(-3, 3, color="0.85", alpha=0.3, label="±3 dB window")
ax.axhline(0, color="0.4", ls=":", lw=0.8)

# Crossover markers
for fc, label in [(fc_woofer, f"{fc_woofer:.0f} Hz"), (fc_tweeter, f"{fc_tweeter:.0f} Hz")]:
    ax.axvline(fc, color="0.5", ls=":", lw=1.0, alpha=0.5)
    ax.text(fc * 1.03, -18, label, fontsize=8, color="0.4")

ax.set_xlim(20, 22000)
ax.set_ylim(-25, 15)
ax.set_xlabel("Frequency [Hz]", fontsize=12)
ax.set_ylabel("dB (normalized @500 Hz)", fontsize=12)
ax.set_title("Mk3 v9 — Anechoic System Response (pre-EQ, pre-room)\n"
             "Individual drivers with DSP level adjustments + coherent sum  |  "
             "XO: 200 Hz BW4 / 1100 Hz LR4  |  Baffle step + WG loading included",
             fontsize=13, fontweight="bold")
ax.legend(fontsize=10, loc="lower left", framealpha=0.9)
ax.grid(True, which="both", alpha=0.25)
ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])

fig.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'system_response_anechoic.png')
fig.savefig(out_png, dpi=150)
print(f"\nwrote {out_png}")

# ============================================================
#  CSV
# ============================================================
csv_out = os.path.join(script_dir, 'csv', 'system_response_anechoic.csv')
header = "freq_Hz,woofer_dB,mid_dB,tweeter_dB,sum_dB"
rows = [header]
for i in range(len(f)):
    rows.append(f"{f[i]:.2f},{mag_w_n[i]:.4f},{mag_m_n[i]:.4f},{mag_t_n[i]:.4f},{mag_sum_n[i]:.4f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")
