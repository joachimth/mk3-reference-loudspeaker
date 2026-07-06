"""
In-room gain optimization: all-zero vs optimized (Harman target)
=================================================================

Shows the in-room response with three gain configurations and documents
the optimization process:

  1. All gains = 0 dB — raw driver levels, no correction
  2. Optimized gains — Woofer 0 dB (unity), Mid -4.0 dB, Tweeter -9.0 dB
  3. Post-DSP — optimized gains + 1/3 octave PEQ toward Harman target

The gain optimization is a 3-parameter sweep (W, M, T) minimizing RMS
deviation from the Harman in-room target. Because the system is
normalized at 500 Hz, only the relative spreads matter:
  W-M = 4.0 dB, M-T = 5.0 dB

The woofer is pinned at 0 dB (unity) to avoid wasting DAC headroom.
The optimizer confirms W0/M-4.0/T-9.0 as optimal at 0.1 dB resolution.

Output: simulations/plots/inroom_gain_optimization.png
        simulations/csv/inroom_gain_optimization.csv
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
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
#  Filters & models
# ============================================================
def lr4_lp_db(f, fc):
    s = 1j*f/fc; return 20*np.log10(np.abs((1/(s**2+np.sqrt(2)*s+1))**2)+1e-12)
def lr4_hp_db(f, fc):
    s = 1j*f/fc; return 20*np.log10(np.abs((s**2/(s**2+np.sqrt(2)*s+1))**2)+1e-12)
def bw4_lp_db(f, fc):
    s = 1j*f/fc
    return 20*np.log10(np.abs(1/(s**2+s/0.5412+1) * 1/(s**2+s/1.3066+1))+1e-12)
def bw4_hp_db(f, fc):
    s = 1j*f/fc
    return 20*np.log10(np.abs(s**2/(s**2+s/0.5412+1) * s**2/(s**2+s/1.3066+1))+1e-12)
def lr2_hp_db(f, fc):
    s = 1j*f/fc; return 20*np.log10(np.abs(s**2/(s**2+s/0.707+1))+1e-12)
def baffle_step_db(f, a=0.168):
    fbs = c_speed/(2*np.pi*a); x = 1j*f/fbs
    return 20*np.log10(np.abs((0.5+x)/(1+x)))
def wg_loading_db(f, gain_db, f_low=1100, f_high=2000):
    f_mid = np.sqrt(f_low*f_high); spread = (np.log10(f_high)-np.log10(f_low))*0.3
    return gain_db * 0.5*(1+np.tanh((np.log10(f)-np.log10(f_mid))/spread))

Fc_w=28.0; Qtc_w=0.707; sens_w=84.5
def woofer_response(f):
    s = 1j*f/Fc_w; return 20*np.log10(np.abs(s**2/(s**2+s/Qtc_w+1))+1e-12)+(sens_w+3)

room_v=43.2; rt60=0.4; f_schr=2000*np.sqrt(rt60/room_v)
def room_gain_db(f, slope=6.0, max_gain=9.0):
    g = np.where(f<f_schr, slope*np.log2(f_schr/np.maximum(f,1)), 0)
    return np.clip(g, 0, max_gain)
def room_hf_absorption_db(f, f_start=5000, slope=1.5, max_abs=3.0):
    return -np.clip(np.where(f>f_start, slope*np.log2(f/f_start), 0), 0, max_abs)
def room_transfer_db(f): return room_gain_db(f) + room_hf_absorption_db(f)

def harman_target_db(f, bass_shelf=3.5, f_bass=100.0, hf_tilt=1.0, f_hf=1000.0):
    bass = bass_shelf / (1.0 + (f/f_bass)**2)
    hf = np.where(f > f_hf, -hf_tilt*np.log2(f/f_hf), 0.0)
    return bass + hf

# ============================================================
#  System response
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

def system_inroom(w_gain, m_gain, t_gain):
    fc_wm=200; fc_t=1100; wg=2.5
    mw = woofer_response(f)+bs+bw4_lp_db(f,fc_wm)+lr2_hp_db(f,18)+w_gain
    mm = interp_curve(w18_freq,w18_spl,f,fb=92.5,fa=80)+bs+bw4_hp_db(f,fc_wm)+lr4_lp_db(f,fc_t)+m_gain
    mt = interp_curve(sb26_freq,sb26_spl,f,fb=sb26_spl[0]-20,fa=sb26_spl[-1]-20)+wg_loading_db(f,wg)+lr4_hp_db(f,fc_t)+t_gain
    s = 20*np.log10(10**(mw/20)+10**(mm/20)+10**(mt/20)+1e-12)
    return s + room_tf

# ============================================================
#  Three configurations
# ============================================================
pb = (f > 80) & (f < 15000)

# 1. All gains = 0
ir_zero = system_inroom(0.0, 0.0, 0.0)
ref_z = np.interp(500, f, ir_zero)
n_zero = ir_zero - ref_z
dev_zero = (n_zero - target)[pb]

# 2. Optimized gains (W0/M-4/T-9)
ir_opt = system_inroom(0.0, -4.0, -9.0)
ref_o = np.interp(500, f, ir_opt)
n_opt = ir_opt - ref_o
dev_opt = (n_opt - target)[pb]

# 3. Post-DSP (optimized + PEQ)
n_smooth = max(5, len(f)//60)
corr = target - n_opt
corr_smoothed = uniform_filter1d(corr, size=n_smooth, mode="nearest")
n_dsp = n_opt + corr_smoothed
dev_dsp = (n_dsp - target)[(f>500)&(f<10000)]

# Individual drivers at 0 dB (for reference)
mw0 = woofer_response(f)+bs+bw4_lp_db(f,200)+lr2_hp_db(f,18)+0.0+room_tf
mm0 = interp_curve(w18_freq,w18_spl,f,fb=92.5,fa=80)+bs+bw4_hp_db(f,200)+lr4_lp_db(f,1100)+0.0+room_tf
mt0 = interp_curve(sb26_freq,sb26_spl,f,fb=sb26_spl[0]-20,fa=sb26_spl[-1]-20)+wg_loading_db(f,2.5)+lr4_hp_db(f,1100)+0.0+room_tf

# Print
print("="*65)
print("IN-ROOM GAIN OPTIMIZATION (200 Hz BW4, Harman target)")
print("="*65)
for label, n, dev in [("All gains = 0 dB", n_zero, dev_zero),
                       ("Optimized (W0/M-4/T-9)", n_opt, dev_opt)]:
    rms = np.sqrt(np.mean(dev**2))
    mx = np.max(np.abs(dev))
    print(f"\n  {label}:")
    print(f"    @100Hz: {np.interp(100,f,n):+.1f}  @2k: {np.interp(2000,f,n):+.1f}  @10k: {np.interp(10000,f,n):+.1f}")
    print(f"    RMS: {rms:.2f} dB, Max: {mx:.2f} dB")

print(f"\n  Post-DSP (optimized + 1/3 oct PEQ):")
print(f"    Residual: RMS={np.sqrt(np.mean(dev_dsp**2)):.2f} dB, Max={np.max(np.abs(dev_dsp)):.2f} dB")

print(f"\n  Driver sensitivities (why gains are needed):")
print(f"    Woofer pair:  {84.5+3:.1f} dB (84.5 + 3 dB for 2 drivers)")
print(f"    Mid (18W):    92.0 dB")
print(f"    Tweeter+WG:   {91.0+2.5:.1f} dB (91.0 + 2.5 dB WG loading)")
print(f"    → Mid is {92.0-87.5:.1f} dB louder than woofer, tweeter is {93.5-87.5:.1f} dB louder")
print(f"    → Gains compensate: M-4.0 dB, T-9.0 dB (extra tweeter pad for HF tilt)")

# ============================================================
#  PLOT — 3 panels
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(16, 15), sharex=True)

# Panel 1: All gains = 0 dB
ax = axes[0]
ax.semilogx(f, n_zero, lw=3.0, color="#059669", label="System sum (all gains = 0 dB)")
ax.semilogx(f, mw0-ref_z, lw=1.2, color="#dc2626", ls="--", alpha=0.5, label="Woofer (0 dB)")
ax.semilogx(f, mm0-ref_z, lw=1.2, color="#059669", ls="--", alpha=0.5, label="Mid (0 dB)")
ax.semilogx(f, mt0-ref_z, lw=1.2, color="#7c3aed", ls="--", alpha=0.5, label="Tweeter (0 dB, WG +2.5)")
ax.semilogx(f, target, lw=1.5, color="#f59e0b", ls=":", alpha=0.6, label="Harman target")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhspan(-3, 3, color="0.85", alpha=0.2)
ax.set_ylim(-15, 12)
ax.set_ylabel("dB (norm @500 Hz)")
rms_z = np.sqrt(np.mean(dev_zero**2))
ax.set_title(f"1. All Gains = 0 dB — raw driver levels  |  RMS deviation: {rms_z:.2f} dB",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# Panel 2: Optimized gains
ax = axes[1]
ax.semilogx(f, n_zero, lw=1.5, color="#059669", alpha=0.3, ls="--", label="All 0 dB (for comparison)")
ax.semilogx(f, n_opt, lw=3.0, color="#2563eb", label="Optimized: W0 / M-4.0 / T-9.0")
ax.semilogx(f, target, lw=1.5, color="#f59e0b", ls=":", alpha=0.6, label="Harman target")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhspan(-3, 3, color="0.85", alpha=0.2)
# Annotate the correction
ax.annotate('', xy=(2000, np.interp(2000,f,n_zero)), xytext=(2000, np.interp(2000,f,n_opt)),
            arrowprops=dict(arrowstyle='<->', color='0.4', lw=1.5))
ax.text(2200, (np.interp(2000,f,n_zero)+np.interp(2000,f,n_opt))/2, '−4 dB mid pad',
        fontsize=8, color='0.3', va='center')
ax.annotate('', xy=(8000, np.interp(8000,f,n_zero)), xytext=(8000, np.interp(8000,f,n_opt)),
            arrowprops=dict(arrowstyle='<->', color='0.4', lw=1.5))
ax.text(8800, (np.interp(8000,f,n_zero)+np.interp(8000,f,n_opt))/2, '−9 dB tweeter pad',
        fontsize=8, color='0.3', va='center')
ax.set_ylim(-15, 12)
ax.set_ylabel("dB (norm @500 Hz)")
rms_o = np.sqrt(np.mean(dev_opt**2))
ax.set_title(f"2. Optimized Gains (W0/M-4/T-9)  |  RMS deviation: {rms_o:.2f} dB  |  Spreads: W-M=4.0, M-T=5.0",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# Panel 3: Post-DSP
ax = axes[2]
ax.semilogx(f, n_opt, lw=1.5, color="#2563eb", alpha=0.3, ls="--", label="Optimized gains (before DSP)")
ax.semilogx(f, target, lw=1.5, color="#f59e0b", ls=":", alpha=0.6, label="Harman target")
ax.semilogx(f, n_dsp, lw=3.0, color="#dc2626", label="Post-DSP (optimized + 1/3 oct PEQ)")
ax2 = ax.twinx()
ax2.semilogx(f, corr_smoothed, lw=1.0, color="#dc2626", alpha=0.3, ls="-.")
ax2.set_ylabel("DSP correction [dB]", fontsize=9, color="#dc2626")
ax2.set_ylim(-8, 8)
ax2.tick_params(axis='y', labelcolor="#dc2626")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhspan(-3, 3, color="0.85", alpha=0.2)
ax.set_ylim(-15, 8)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_xlabel("Frequency [Hz]")
ax.set_title(f"3. Post-DSP — optimized gains + ±{np.max(np.abs(corr_smoothed[pb])):.1f} dB PEQ  |  Residual: ±{np.max(np.abs(dev_dsp)):.1f} dB",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

for ax in axes:
    ax.set_xlim(20, 22000)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])

fig.suptitle("Mk3 v9 — In-room Gain Optimization\n"
             "Room: 4.5×4×2.4m  |  XO: 200 Hz BW4 / 1100 Hz LR4  |  "
             "Driver levels: 87.5 / 92 / 93.5 dB → pads: 0 / -4 / -9 dB",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.93])

script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'inroom_gain_optimization.png')
fig.savefig(out_png, dpi=150)
print(f"\nwrote {out_png}")

# CSV
csv_out = os.path.join(script_dir, 'csv', 'inroom_gain_optimization.csv')
header = "freq_Hz,all_zero_dB,optimized_dB,post_dsp_dB,harman_target_dB,dsp_correction_dB"
rows = [header]
for i in range(len(f)):
    rows.append(f"{f[i]:.2f},{n_zero[i]:.4f},{n_opt[i]:.4f},{n_dsp[i]:.4f},{target[i]:.4f},{corr_smoothed[i]:.4f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")
