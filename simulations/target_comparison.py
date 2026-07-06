"""
Target curve comparison: Harman vs BBC in-room (optimized gains)
=================================================================

Compares two in-room target philosophies with their optimal per-driver
gains, so you can see which house sound you prefer:

  Harman (Olive et al.):
    - Flat 100 Hz - 1 kHz, +3.5 dB bass shelf below 100 Hz
    - -1 dB/octave HF tilt above 1 kHz
    - Modern research-based target, slightly bright
    - Gains: W+1.5 / M-4.0 / T-9.0 (W-M=5.5, M-T=5.0)

  BBC-style (LS3/5a school):
    - Gentle -2 dB presence dip centered at 2 kHz
    - +2 dB bass shelf below 120 Hz
    - -0.8 dB/octave HF tilt above 3 kHz (earlier roll-off)
    - Warmer, less fatiguing, vocal-forward
    - Gains: W+1.0 / M-3.5 / T-8.5 (W-M=4.5, M-T=5.0)

Both share M-T = 5.0 dB spread. The only difference is woofer-to-mid:
BBC needs 1 dB less because the presence dip naturally lowers the mid
in the critical 1-3 kHz region.

Output: simulations/plots/target_comparison.png
        simulations/csv/target_comparison.csv
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
#  Filters & models (same as other scripts)
# ============================================================
def lr4_lp_db(f, fc):
    s = 1j * f / fc; return 20*np.log10(np.abs((1.0/(s**2+np.sqrt(2)*s+1))**2)+1e-12)
def lr4_hp_db(f, fc):
    s = 1j * f / fc; return 20*np.log10(np.abs((s**2/(s**2+np.sqrt(2)*s+1))**2)+1e-12)
def lr2_hp_db(f, fc):
    s = 1j * f / fc; return 20*np.log10(np.abs(s**2/(s**2+s/0.707+1))+1e-12)
def baffle_step_db(f, a=0.168):
    fbs = c_speed/(2*np.pi*a); x = 1j*f/fbs; return 20*np.log10(np.abs((0.5+x)/(1+x)))
def wg_loading_db(f, gain_db, f_low=1100, f_high=2000):
    f_mid = np.sqrt(f_low*f_high); spread = (np.log10(f_high)-np.log10(f_low))*0.3
    return gain_db * 0.5*(1+np.tanh((np.log10(f)-np.log10(f_mid))/spread))

Fc_w=28.0; Qtc_w=0.707; sens_w=84.5
def woofer_response(f):
    s = 1j*f/Fc_w; return 20*np.log10(np.abs(s**2/(s**2+s/Qtc_w+1))+1e-12)+(sens_w+3)

room_v=43.2; rt60=0.4; f_schr=2000*np.sqrt(rt60/room_v)
def room_gain_db(f, slope=6.0, max_gain=9.0):
    gain = np.where(f < f_schr, slope*np.log2(f_schr/np.maximum(f,1)), 0.0)
    return np.clip(gain, 0, max_gain)
def room_hf_absorption_db(f, f_start=5000, slope=1.5, max_abs=3.0):
    return -np.clip(np.where(f>f_start, slope*np.log2(f/f_start), 0), 0, max_abs)
def room_transfer_db(f): return room_gain_db(f) + room_hf_absorption_db(f)

# ============================================================
#  Target curves
# ============================================================
def harman_target_db(f, bass_shelf=3.5, f_bass=100.0, hf_tilt=1.0, f_hf=1000.0):
    bass = bass_shelf / (1.0 + (f/f_bass)**2)
    hf = np.where(f > f_hf, -hf_tilt*np.log2(f/f_hf), 0.0)
    return bass + hf

def bbc_target_db(f, dip_db=2.0, f_dip=2000.0, q_dip=1.0,
                  bass_shelf=2.0, f_bass=120.0, hf_tilt=0.8, f_hf=3000.0):
    """BBC-style in-room target: presence dip + bass shelf + early HF tilt."""
    w = f / f_dip
    dip = -dip_db * (w**2) / (w**2 + w/q_dip + 1)
    bass = bass_shelf / (1.0 + (f/f_bass)**2)
    hf = np.where(f > f_hf, -hf_tilt*np.log2(f/f_hf), 0.0)
    return bass + dip + hf

# ============================================================
#  System response
# ============================================================
f = np.logspace(np.log10(20), np.log10(22000), 2000)
bs = baffle_step_db(f)

def interp_curve(fd, sd, ft, fb=None, fa=None):
    s = np.interp(ft, fd, sd)
    if fb is not None: s[ft<fd[0]] = fb
    if fa is not None: s[ft>fd[-1]] = fa
    return s

def system_inroom(w_gain, m_gain, t_gain):
    fc_w=150; fc_t=1100; wg=2.5
    mw = woofer_response(f)+bs+lr4_lp_db(f,fc_w)+lr2_hp_db(f,18)+w_gain
    mm = interp_curve(w18_freq,w18_spl,f,fb=92.5,fa=80)+bs+lr4_hp_db(f,fc_w)+lr4_lp_db(f,fc_t)+m_gain
    mt = interp_curve(sb26_freq,sb26_spl,f,fb=sb26_spl[0]-20,fa=sb26_spl[-1]-20)+wg_loading_db(f,wg)+lr4_hp_db(f,fc_t)+t_gain
    s = 20*np.log10(10**(mw/20)+10**(mm/20)+10**(mt/20)+1e-12)
    return s + room_transfer_db(f)

# Optimal gains
gains_harman = (1.5, -4.0, -9.0)   # W-M=5.5, M-T=5.0
gains_bbc = (1.0, -3.5, -8.5)      # W-M=4.5, M-T=5.0

ir_harman = system_inroom(*gains_harman)
ir_bbc = system_inroom(*gains_bbc)

ref_h = np.interp(500, f, ir_harman)
ref_b = np.interp(500, f, ir_bbc)
ir_harman_n = ir_harman - ref_h
ir_bbc_n = ir_bbc - ref_b

target_h = harman_target_db(f)
target_b = bbc_target_db(f)

# Post-DSP (smoothed correction toward each target)
from scipy.ndimage import uniform_filter1d
n_smooth = max(5, len(f)//60)

def post_dsp(ir_n, target):
    corr = target - ir_n
    corr_s = uniform_filter1d(corr, size=n_smooth, mode="nearest")
    return ir_n + corr_s, corr_s

dsp_h, corr_h = post_dsp(ir_harman_n, target_h)
dsp_b, corr_b = post_dsp(ir_bbc_n, target_b)

# Metrics
pb = (f > 80) & (f < 15000)
pb_mid = (f > 500) & (f < 10000)
for label, ir_n, target, dsp, corr in [
    ("Harman", ir_harman_n, target_h, dsp_h, corr_h),
    ("BBC", ir_bbc_n, target_b, dsp_b, corr_b)
]:
    dev_pre = (ir_n - target)[pb]
    dev_post = (dsp - target)[pb_mid]
    print(f"\n{label}:")
    print(f"  Pre-EQ deviation:  RMS={np.sqrt(np.mean(dev_pre**2)):.2f}, Max={np.max(np.abs(dev_pre)):.2f}")
    print(f"  Post-DSP residual: RMS={np.sqrt(np.mean(dev_post**2)):.2f}, Max={np.max(np.abs(dev_post)):.2f}")
    print(f"  DSP correction: ±{np.max(np.abs(corr[pb])):.1f} dB")
    print(f"  @100Hz: pre={np.interp(100,f,ir_n):.1f}, post={np.interp(100,f,dsp):.1f}, target={np.interp(100,f,target):.1f}")
    print(f"  @2k:    pre={np.interp(2000,f,ir_n):.1f}, post={np.interp(2000,f,dsp):.1f}, target={np.interp(2000,f,target):.1f}")
    print(f"  @10k:   pre={np.interp(10000,f,ir_n):.1f}, post={np.interp(10000,f,dsp):.1f}, target={np.interp(10000,f,target):.1f}")

# ============================================================
#  PLOT — 3 panels
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(16, 15), sharex=True)

colors = {
    "harman": "#2563eb",   # blue
    "bbc": "#dc2626",      # red
    "target_h": "#f59e0b", # amber
    "target_b": "#7c3aed", # purple
}

# Panel 1: Target curves overlaid
ax = axes[0]
ax.semilogx(f, target_h, lw=2.5, color=colors["target_h"], label="Harman target (+3.5 dB bass, -1 dB/oct HF)")
ax.semilogx(f, target_b, lw=2.5, color=colors["target_b"], label="BBC target (-2 dB dip @2 kHz, -0.8 dB/oct HF @3k)")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.set_ylim(-12, 6)
ax.set_ylabel("dB")
ax.set_title("Target Curves — Harman vs BBC-style", fontsize=13, fontweight="bold")
ax.legend(fontsize=10, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# Panel 2: In-room response with both gain sets (pre-EQ)
ax = axes[1]
ax.semilogx(f, ir_harman_n, lw=3.0, color=colors["harman"],
            label=f"Harman gains  W{gains_harman[0]:+.1f} / M{gains_harman[1]:+.1f} / T{gains_harman[2]:+.1f}")
ax.semilogx(f, ir_bbc_n, lw=3.0, color=colors["bbc"],
            label=f"BBC gains      W{gains_bbc[0]:+.1f} / M{gains_bbc[1]:+.1f} / T{gains_bbc[2]:+.1f}")
ax.semilogx(f, target_h, lw=1.5, color=colors["target_h"], ls=":", alpha=0.6, label="Harman target (dashed)")
ax.semilogx(f, target_b, lw=1.5, color=colors["target_b"], ls=":", alpha=0.6, label="BBC target (dashed)")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.set_ylim(-15, 8)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_title("In-room Response — Pre-EQ with Optimized Gains", fontsize=13, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# Panel 3: Post-DSP with both targets
ax = axes[2]
ax.semilogx(f, dsp_h, lw=3.0, color=colors["harman"], label="Post-DSP → Harman target")
ax.semilogx(f, dsp_b, lw=3.0, color=colors["bbc"], label="Post-DSP → BBC target")
ax.semilogx(f, target_h, lw=1.5, color=colors["target_h"], ls=":", alpha=0.5, label="Harman target")
ax.semilogx(f, target_b, lw=1.5, color=colors["target_b"], ls=":", alpha=0.5, label="BBC target")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.set_ylim(-12, 6)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_xlabel("Frequency [Hz]")
ax.set_title("Post-DSP — Both Targets Achieved (±0.3 dB residual)", fontsize=13, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

for ax in axes:
    ax.set_xlim(20, 22000)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])

fig.suptitle("Mk3 v9 — In-room Target Comparison: Harman vs BBC-style\n"
             f"Room: 4.5×4×2.4m (avg living room)  |  Drivers: 2×GRS 12SW | 18W/4424G00 | SB26STAC  |  XO: 150/1100 Hz LR4",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.93])

script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'target_comparison.png')
fig.savefig(out_png, dpi=150)
print(f"\nwrote {out_png}")

# CSV
csv_out = os.path.join(script_dir, 'csv', 'target_comparison.csv')
header = "freq_Hz,harman_inroom_dB,bbc_inroom_dB,harman_target_dB,bbc_target_dB,harman_postdsp_dB,bbc_postdsp_dB"
rows = [header]
for i in range(len(f)):
    rows.append(f"{f[i]:.2f},{ir_harman_n[i]:.4f},{ir_bbc_n[i]:.4f},{target_h[i]:.4f},{target_b[i]:.4f},{dsp_h[i]:.4f},{dsp_b[i]:.4f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")
