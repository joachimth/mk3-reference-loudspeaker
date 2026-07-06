"""
Anechoic system response with per-driver dB adjustments (pre-EQ, pre-room)
==========================================================================

Shows individual driver curves with their DSP level adjustments and the
coherent sum, so you can see exactly how the three drivers combine through
the LR4 crossovers before any room gain or EQ.

Drivers (v9):
  - 2× GRS 12SW-4HE (woofer, sealed + LT, DSP gain -4.0 dB)
  - ScanSpeak 18W/4424G00 (midrange, DSP gain 0.0 dB)
  - SB Acoustics SB26STAC-C000-4 (tweeter, DSP gain -0.5 dB)

Crossovers: LR4 at 150 Hz + 1100 Hz
Baffle step: Vandercooy model, 300mm cabinet
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

def lr2_hp_db(f, fc):
    s = 1j * f / fc
    H = s**2 / (s**2 + s/0.707 + 1)
    return 20*np.log10(np.abs(H) + 1e-12)

# ============================================================
#  Baffle step (Vanderkooy)
# ============================================================
a_h = 0.150; a_d = 0.185
a_mean = np.sqrt((a_h**2 + a_d**2) / 2.0)

def baffle_step_db(f, a=0.168):
    fbs = c_speed / (2.0 * np.pi * a)
    x = 1j * f / fbs
    H = (0.5 + x) / (1.0 + x)
    return 20.0 * np.log10(np.abs(H))

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
dsp_w_gain = 0.0     # woofer DSP gain (dB)
dsp_m_gain = -4.5    # mid DSP gain (dB)
dsp_t_gain = -7.5    # tweeter DSP gain (dB)
fc_woofer = 150.0
fc_tweeter = 1100.0
wg_gain = 2.5

f = np.logspace(np.log10(20), np.log10(22000), 2000)
bs = baffle_step_db(f)

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
mag_w = mag_w_raw + bs + lr4_lp_db(f, fc_woofer) + lr2_hp_db(f, 18.0) + dsp_w_gain

# Mid: 18W/4424G00 real curve + baffle step + HP@150 + LP@1100 + DSP gain
mag_m_raw = interp_curve(w18_freq, w18_spl, f, fill_below=92.5, fill_above=80.0)
mag_m = mag_m_raw + bs + lr4_hp_db(f, fc_woofer) + lr4_lp_db(f, fc_tweeter) + dsp_m_gain

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
            label=f"Woofer  2×GRS 12SW-4HE  ({dsp_w_gain:+.1f} dB, LP {fc_woofer:.0f} Hz LR4)")
ax.semilogx(f, mag_m_n, lw=1.8, color=colors["mid"], ls="--", alpha=0.7,
            label=f"Mid     ScanSpeak 18W/4424G00  ({dsp_m_gain:+.1f} dB, HP {fc_woofer:.0f} / LP {fc_tweeter:.0f} Hz)")
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
             "XO: 150/1100 Hz LR4  |  Baffle step + WG loading included",
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
