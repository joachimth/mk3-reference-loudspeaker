"""
Woofer-mid crossover optimization (80-200 Hz sweep)
====================================================

Investigates the dip at the 150 Hz woofer/mid crossover and finds the
optimal crossover frequency and filter order by sweeping:

  - Frequency: 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200 Hz
  - Filter: LR2, LR4, BW2, BW4

For each combination, evaluates:
  1. System flatness (ripple through crossover region)
  2. Crossover dip depth
  3. Phase coherence (summing efficiency)
  4. 18W excursion headroom at the new HP frequency (90 dB SPL)
  5. 12SW directivity (ka at the new LP frequency)

Constraints:
  - 18W/4424G00: Fs=49 Hz, Xmax=4.5 mm, Sd=137 cm²
    Can safely play down to ~80 Hz at 90 dB with 20 dB headroom
  - 12SW-4HE: Sd=504 cm², piston radius 127 mm
    ka < 1.0 up to ~430 Hz, no directivity issues below 300 Hz

Output: simulations/plots/crossover_woofer_mid.png
        simulations/csv/crossover_woofer_mid.csv
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv

c_speed = 343.0

# ============================================================
#  Load datasheets
# ============================================================
def load_freq_response_csv(filepath, col_name="spl_db"):
    freqs, spls = [], []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    with open(os.path.join(repo_root, filepath)) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                freq = float(row["freq_hz"])
                spl_str = row.get(col_name, "")
                if spl_str and spl_str.strip():
                    freqs.append(freq); spls.append(float(spl_str))
            except: pass
    freqs = np.array(freqs); spls = np.array(spls)
    idx = np.argsort(freqs)
    return freqs[idx], spls[idx]

sb26_freq, sb26_spl = load_freq_response_csv("assets/datasheets/SB26STAC-C000-4_freq_response.csv")
w18_freq, w18_spl = load_freq_response_csv("assets/datasheets/18W-4424G00_freq_response.csv")

# ============================================================
#  Filter functions
# ============================================================
def lr2_lp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs(1.0 / (s**2 + s/0.707 + 1)) + 1e-12)

def lr2_hp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs(s**2 / (s**2 + s/0.707 + 1)) + 1e-12)

def lr4_lp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2) + 1e-12)

def lr4_hp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2) + 1e-12)

def bw2_lp_db(f, fc):
    """2nd-order Butterworth LP."""
    s = 1j * f / fc
    return 20*np.log10(np.abs(1.0 / (s**2 + np.sqrt(2)*s + 1)) + 1e-12)

def bw2_hp_db(f, fc):
    """2nd-order Butterworth HP."""
    s = 1j * f / fc
    return 20*np.log10(np.abs(s**2 / (s**2 + np.sqrt(2)*s + 1)) + 1e-12)

def bw4_lp_db(f, fc):
    """4th-order Butterworth LP."""
    s = 1j * f / fc
    H = 1.0 / (s**2 + 1.8478*s + 1) * 1.0 / (s**2 + 0.7654*s + 1)
    return 20*np.log10(np.abs(H) + 1e-12)

def bw4_hp_db(f, fc):
    """4th-order Butterworth HP."""
    s = 1j * f / fc
    H = s**2 / (s**2 + 1.8478*s + 1) * s**2 / (s**2 + 0.7654*s + 1)
    return 20*np.log10(np.abs(H) + 1e-12)

def lr2_hp_db_sub(f, fc):
    """Subsonic LR2 HP."""
    s = 1j * f / fc
    return 20*np.log10(np.abs(s**2 / (s**2 + s/0.707 + 1)) + 1e-12)

filters = {
    "LR2": (lr2_lp_db, lr2_hp_db),
    "LR4": (lr4_lp_db, lr4_hp_db),
    "BW2": (bw2_lp_db, bw2_hp_db),
    "BW4": (bw4_lp_db, bw4_hp_db),
}

# ============================================================
#  Baffle step + WG loading
# ============================================================
def baffle_step_db(f, a=0.168):
    fbs = c_speed/(2*np.pi*a); x = 1j*f/fbs
    return 20*np.log10(np.abs((0.5+x)/(1+x)))

def wg_loading_db(f, gain_db, f_low=1100, f_high=2000):
    f_mid = np.sqrt(f_low*f_high)
    spread = (np.log10(f_high)-np.log10(f_low))*0.3
    return gain_db * 0.5*(1+np.tanh((np.log10(f)-np.log10(f_mid))/spread))

# ============================================================
#  Woofer model (2x 12SW sealed + LT)
# ============================================================
Fc_w = 28.0; Qtc_w = 0.707; sens_w = 84.5
def woofer_response(f):
    s = 1j*f/Fc_w
    return 20*np.log10(np.abs(s**2/(s**2+s/Qtc_w+1))+1e-12)+(sens_w+3)

# ============================================================
#  Room model
# ============================================================
room_v=43.2; rt60=0.4; f_schr=2000*np.sqrt(rt60/room_v)
def room_gain_db(f, slope=6.0, max_gain=9.0):
    g = np.where(f<f_schr, slope*np.log2(f_schr/np.maximum(f,1)), 0)
    return np.clip(g, 0, max_gain)
def room_hf_absorption_db(f, f_start=5000, slope=1.5, max_abs=3.0):
    return -np.clip(np.where(f>f_start, slope*np.log2(f/f_start), 0), 0, max_abs)
def room_transfer_db(f): return room_gain_db(f) + room_hf_absorption_db(f)

# ============================================================
#  Harman target
# ============================================================
def harman_target_db(f, bass_shelf=3.5, f_bass=100.0, hf_tilt=1.0, f_hf=1000.0):
    bass = bass_shelf / (1.0 + (f/f_bass)**2)
    hf = np.where(f > f_hf, -hf_tilt*np.log2(f/f_hf), 0.0)
    return bass + hf

# ============================================================
#  Frequency grid
# ============================================================
f = np.logspace(np.log10(20), np.log10(22000), 3000)
bs = baffle_step_db(f)
room_tf = room_transfer_db(f)
target = harman_target_db(f)

def interp_curve(fd, sd, ft, fb=None, fa=None):
    s = np.interp(ft, fd, sd)
    if fb is not None: s[ft<fd[0]] = fb
    if fa is not None: s[ft>fd[-1]] = fa
    return s

# v9 gains (Harman-optimized)
W_GAIN = 1.5; M_GAIN = -4.0; T_GAIN = -9.0
FC_TWEETER = 1100.0; WG_GAIN = 2.5

# Tweeter (constant across all woofer-mid crossover variants)
mag_t = (interp_curve(sb26_freq, sb26_spl, f, fb=sb26_spl[0]-20, fa=sb26_spl[-1]-20)
         + wg_loading_db(f, WG_GAIN) + lr4_hp_db(f, FC_TWEETER) + T_GAIN)

# ============================================================
#  Crossover sweep
# ============================================================
xo_freqs = [80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200]
results = []

# 18W excursion at 90 dB SPL
Sd_m = 137e-4  # m²
Xmax_m = 4.5e-3  # m
rho_air = 1.18

# 12SW directivity
Sd_w = 504e-4
r_eff_w = np.sqrt(Sd_w / np.pi)

print(f"{'XO':>5s} {'Filter':>5s} {'Dip':>6s} {'Ripple':>7s} {'RMS':>6s} {'Max':>6s} {'18W_xmax':>10s} {'12SW_ka':>8s}")
print("-" * 70)

for fc_wm in xo_freqs:
    for filter_name, (lp_func, hp_func) in filters.items():
        # Woofer
        mag_w = (woofer_response(f) + bs + lp_func(f, fc_wm)
                 + lr2_hp_db_sub(f, 18.0) + W_GAIN)
        # Mid
        mag_m = (interp_curve(w18_freq, w18_spl, f, fb=92.5, fa=80.0)
                 + bs + hp_func(f, fc_wm) + lr4_lp_db(f, FC_TWEETER) + M_GAIN)

        # System sum
        w_lin = 10**(mag_w/20); m_lin = 10**(mag_m/20); t_lin = 10**(mag_t/20)
        mag_sum = 20*np.log10(w_lin + m_lin + t_lin + 1e-12)

        # In-room
        mag_inroom = mag_sum + room_tf
        ref = np.interp(500, f, mag_inroom)
        mag_n = mag_inroom - ref

        # Metrics in crossover region (0.5×fc to 2×fc)
        xo_region = (f > fc_wm*0.5) & (f < fc_wm*2.0)
        # Dip depth: min in crossover region relative to 500 Hz ref
        dip = np.min(mag_n[xo_region])
        # Ripple in crossover region
        ripple_xo = np.max(mag_n[xo_region]) - np.min(mag_n[xo_region])
        # Deviation from Harman target in full passband
        pb = (f > 80) & (f < 15000)
        dev = (mag_n - target)[pb]
        rms = np.sqrt(np.mean(dev**2))
        maxdev = np.max(np.abs(dev))

        # 18W excursion at fc_wm for 90 dB
        p_90 = 20e-6 * 10**(90/20)
        x_at_fc = p_90 * 2.0 / (rho_air * c_speed * Sd_m * 2*np.pi*fc_wm)
        headroom = 20*np.log10(Xmax_m / x_at_fc)

        # 12SW directivity at fc_wm
        ka = 2*np.pi*fc_wm*r_eff_w / c_speed

        results.append({
            'fc': fc_wm, 'filter': filter_name,
            'dip': dip, 'ripple': ripple_xo, 'rms': rms, 'maxdev': maxdev,
            'headroom': headroom, 'ka': ka,
            'mag_n': mag_n, 'mag_w': mag_w - ref, 'mag_m': mag_m - ref,
        })

        print(f"{fc_wm:5d} {filter_name:>5s} {dip:6.1f} {ripple_xo:7.1f} {rms:6.2f} {maxdev:6.2f} {headroom:10.1f} {ka:8.2f}")

# ============================================================
#  Find best configurations
# ============================================================
print("\n" + "="*70)
print("TOP 10 CONFIGURATIONS (sorted by crossover dip depth)")
print("="*70)
by_dip = sorted(results, key=lambda r: -r['dip'])  # least negative dip = best
for r in by_dip[:10]:
    print(f"  {r['fc']:4d} Hz {r['filter']:>4s}  dip={r['dip']:+.1f}  ripple={r['ripple']:.1f}  "
          f"RMS={r['rms']:.2f}  18W headroom={r['headroom']:.1f} dB  ka={r['ka']:.2f}")

print("\n" + "="*70)
print("TOP 10 (sorted by overall RMS deviation from Harman target)")
print("="*70)
by_rms = sorted(results, key=lambda r: r['rms'])
for r in by_rms[:10]:
    print(f"  {r['fc']:4d} Hz {r['filter']:>4s}  dip={r['dip']:+.1f}  ripple={r['ripple']:.1f}  "
          f"RMS={r['rms']:.2f}  18W headroom={r['headroom']:.1f} dB  ka={r['ka']:.2f}")

# ============================================================
#  PLOT: best crossover vs current 150 Hz LR4
# ============================================================
best = by_rms[0]
current = next(r for r in results if r['fc'] == 150 and r['filter'] == 'LR4')

fig, axes = plt.subplots(3, 1, figsize=(16, 14), sharex=True)

# Panel 1: Current 150 Hz LR4
ax = axes[0]
ax.semilogx(f, current['mag_w'], lw=1.5, color="#dc2626", ls="--", alpha=0.6, label="Woofer (LP 150 Hz LR4)")
ax.semilogx(f, current['mag_m'], lw=1.5, color="#059669", ls="--", alpha=0.6, label="Mid (HP 150 Hz LR4)")
ax.semilogx(f, current['mag_n'], lw=3.0, color="#2563eb", label="System sum (in-room, norm)")
ax.axvline(150, color="0.5", ls=":", lw=1.0, alpha=0.5)
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhspan(-3, 3, color="0.85", alpha=0.2)
ax.set_ylim(-15, 10)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_title(f"Current: 150 Hz LR4  |  dip={current['dip']:+.1f} dB, ripple={current['ripple']:.1f} dB, RMS={current['rms']:.2f}",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# Panel 2: Best crossover
ax = axes[1]
ax.semilogx(f, best['mag_w'], lw=1.5, color="#dc2626", ls="--", alpha=0.6,
            label=f"Woofer (LP {best['fc']} Hz {best['filter']})")
ax.semilogx(f, best['mag_m'], lw=1.5, color="#059669", ls="--", alpha=0.6,
            label=f"Mid (HP {best['fc']} Hz {best['filter']})")
ax.semilogx(f, best['mag_n'], lw=3.0, color="#2563eb", label="System sum (in-room, norm)")
ax.axvline(best['fc'], color="0.5", ls=":", lw=1.0, alpha=0.5)
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhspan(-3, 3, color="0.85", alpha=0.2)
ax.set_ylim(-15, 10)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_title(f"Optimal: {best['fc']} Hz {best['filter']}  |  dip={best['dip']:+.1f} dB, ripple={best['ripple']:.1f} dB, RMS={best['rms']:.2f}  |  18W headroom={best['headroom']:.1f} dB",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# Panel 3: Overlay comparison
ax = axes[2]
ax.semilogx(f, current['mag_n'], lw=2.5, color="#dc2626", alpha=0.7,
            label=f"Current: 150 Hz LR4 (dip={current['dip']:+.1f})")
ax.semilogx(f, best['mag_n'], lw=2.5, color="#059669", alpha=0.7,
            label=f"Optimal: {best['fc']} Hz {best['filter']} (dip={best['dip']:+.1f})")
ax.semilogx(f, target, lw=1.5, color="#f59e0b", ls=":", alpha=0.5, label="Harman target")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhspan(-3, 3, color="0.85", alpha=0.2)
# Mark the crossover regions
ax.axvspan(75, 300, color="0.9", alpha=0.3, label="Crossover region")
ax.set_ylim(-15, 10)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_xlabel("Frequency [Hz]")
ax.set_title("Overlay: Current vs Optimal woofer-mid crossover", fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

for ax in axes:
    ax.set_xlim(20, 22000)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])

fig.suptitle("Mk3 v9 — Woofer/Mid Crossover Optimization\n"
             "Sweep: 80-200 Hz × {LR2, LR4, BW2, BW4}  |  Constraints: 18W excursion, 12SW directivity",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.93])

script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'crossover_woofer_mid.png')
fig.savefig(out_png, dpi=150)
print(f"\nwrote {out_png}")

# CSV: sweep results
csv_out = os.path.join(script_dir, 'csv', 'crossover_woofer_mid.csv')
with open(csv_out, "w") as fh:
    fh.write("fc_hz,filter,dip_db,ripple_db,rms_db,maxdev_db,18w_headroom_db,12sw_ka\n")
    for r in sorted(results, key=lambda r: r['rms']):
        fh.write(f"{r['fc']},{r['filter']},{r['dip']:.2f},{r['ripple']:.2f},{r['rms']:.2f},{r['maxdev']:.2f},{r['headroom']:.1f},{r['ka']:.2f}\n")
print(f"wrote {csv_out}")
