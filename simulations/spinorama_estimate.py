"""
Spinorama & system frequency response estimate (mk3 — SB26STAC @ 1100 Hz)
=========================================================================

Estimated spinorama curves and system on-axis frequency response for the
mk3 design:

  mk3 (v7):  SB26STAC-C000-4, crossover 1100 Hz, Fs=750, Xmax=0.6mm, sens 91.5 dB

Uses the same cabinet, woofers, midrange, and WG212 coverage angles as the
rest of the design.

ASSUMPTIONS (simplified, NOT measured data — same as polar_response.py)
  - 2x GRS 8SW-4HE: circular pistons (d=200mm), omni below 150 Hz, sealed HP Fc=34.5 Q=0.62
  - 15W/4434G00: flat piston a=58.3mm, sens 89.7 dB
  - SB26STAC in WG212: dome r=13mm → CD horn (100°H × 64°V) transition ~1100-1800 Hz, sens 91.5 dB
  - Baffle/edge effects IGNORED. Room gain not included.
  - Spinorama is 2D horizontal-plane approximation, NOT full CEA-2034.

Output: simulations/plots/spinorama_estimate.png
        simulations/csv/spinorama_estimate.csv
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c_speed = 344.0

# ============================================================
#  Shared math
# ============================================================
def j1(x):
    x = np.asarray(x, dtype=float)
    ax = np.abs(x)
    out = np.empty_like(ax)
    s = ax <= 3.0
    y = (x[s] / 3.0)**2
    out[s] = x[s] * (0.5 - 0.56249985*y + 0.21093573*y**2 - 0.03954289*y**3
                     + 0.00443319*y**4 - 0.00031761*y**5 + 0.00001109*y**6)
    b = ~s
    z = 3.0 / ax[b]
    f1 = (0.79788456 + 0.00000156*z + 0.01659667*z**2 + 0.00017105*z**3
          - 0.00249511*z**4 + 0.00113653*z**5 - 0.00020033*z**6)
    t1 = (ax[b] - 2.35619449 + 0.12499612*z + 0.00005650*z**2 - 0.00637879*z**3
          + 0.00074348*z**4 + 0.00079824*z**5 - 0.00029166*z**6)
    out[b] = f1 * np.cos(t1) / np.sqrt(ax[b])
    out[b] = np.sign(x[b]) * out[b]
    return out

def piston_d(theta, a, f):
    ka = 2*np.pi*f/c_speed * a
    st = np.sin(np.radians(theta))
    arg = ka * st
    D = np.ones_like(theta)
    nz = arg != 0
    D[nz] = np.abs(2*j1(arg[nz]) / arg[nz])
    return D

def cd_d(theta, cov_deg):
    half = cov_deg / 2.0
    if half >= 90:
        return np.ones_like(theta)
    n = -6.0 / (20.0 * np.log10(np.cos(np.radians(half))))
    ct = np.cos(np.radians(theta))
    ct = np.maximum(ct, 0.0)
    return ct**n

def smoothstep(x, x0, x1):
    t = np.clip((x - x0) / (x1 - x0 + 1e-12), 0, 1)
    return t * t * (3 - 2*t)

def lr4_lp(f, fc):
    s = 1j * f / fc
    return np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2)

def lr4_hp(f, fc):
    s = 1j * f / fc
    return np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2)

def lr4_lp_db(f, fc):
    s = 1j * f / fc
    H1 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    H2 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    return 20*np.log10(np.abs(H1 * H2))

def lr4_hp_db(f, fc):
    s = 1j * f / fc
    H1 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    H2 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    return 20*np.log10(np.abs(H1 * H2))

# ============================================================
#  Configuration (mk3 only)
# ============================================================
cfg = {
    "xover_tw": 1100.0,
    "tw_sens": 91.5,
    "tw_fs": 750.0,
    "tw_roll_start": 700.0,
    "wg_transition": (1100.0, 1800.0),
    "color": "tab:blue",
    "label": "SB26STAC @ 1100 Hz",
}

# Shared parameters
a_w = 0.100      # woofer piston radius (200mm diameter)
a_m = 0.0583     # midrange piston radius
a_t_dome = 0.013 # tweeter dome radius
a_t_wg = 0.106   # waveguide effective mouth radius
F_ctrl = 1620.0  # WG212 control limit

theta = np.linspace(0, 180, 181)

# ============================================================
#  Compute spinorama
# ============================================================
f_spin = np.logspace(np.log10(200), np.log10(20000), 500)
idx_map = {deg: np.argmin(np.abs(theta - deg)) for deg in
           [0, 10, 20, 30, 60, 90, 120, 150, 180]}

fc_tw = cfg["xover_tw"]
wg_t0, wg_t1 = cfg["wg_transition"]

# Woofer directivity
H_w_lp = lr4_lp(f_spin, 150.0)[:, None]
D_w = np.ones((len(f_spin), len(theta)))
for i, fi in enumerate(f_spin):
    D_w[i, :] = piston_d(theta, a_w, fi)
for i, fi in enumerate(f_spin):
    if fi < 150:
        D_w[i, :] = 1.0
D_w *= H_w_lp

# Midrange directivity
H_m_hp = lr4_hp(f_spin, 150.0)[:, None]
H_m_lp = lr4_lp(f_spin, fc_tw)[:, None]
D_m = np.ones((len(f_spin), len(theta)))
for i, fi in enumerate(f_spin):
    D_m[i, :] = piston_d(theta, a_m, fi)
D_m *= H_m_hp * H_m_lp

# Tweeter directivity
H_t_hp = lr4_hp(f_spin, fc_tw)[:, None]
wg_weight = smoothstep(f_spin, wg_t0, wg_t1)[:, None]
D_t = np.ones((len(f_spin), len(theta)))
for i, fi in enumerate(f_spin):
    a_eff = (1 - wg_weight[i, 0]) * a_t_dome + wg_weight[i, 0] * a_t_wg
    if a_eff < a_t_dome + 1e-6:
        D_t[i, :] = piston_d(theta, a_eff, fi)
    else:
        cd_h = cd_d(theta, 100.0)
        cd_v = cd_d(theta, 64.0)
        cd = np.sqrt(cd_h * cd_v)
        dom = piston_d(theta, a_eff, fi)
        D_t[i, :] = dom + (cd - dom) * wg_weight[i, 0]
D_t *= H_t_hp

# Combined directivity
D_total = D_w + D_m + D_t

# Normalize on-axis to 0 dB (1.0 linear) — spinorama curves are relative
on_axis_lin = D_total[:, 0]
on_axis_lin = np.maximum(on_axis_lin, 1e-12)
D_norm = D_total / on_axis_lin[:, None]

# Spinorama curves (all relative to on-axis = 0 dB)
on_axis = np.zeros_like(f_spin)  # 0 dB by definition
lw = 20*np.log10(np.mean([D_norm[:, idx_map[10]], D_norm[:, idx_map[20]],
                           D_norm[:, idx_map[30]], D_norm[:, idx_map[10]],
                           D_norm[:, idx_map[20]], D_norm[:, idx_map[30]]], axis=0) + 1e-12)
er = 20*np.log10(np.mean([D_norm[:, idx_map[60]], D_norm[:, idx_map[90]],
                           D_norm[:, idx_map[120]], D_norm[:, idx_map[60]],
                           D_norm[:, idx_map[90]], D_norm[:, idx_map[120]]], axis=0) + 1e-12)
# Sound Power: energy average over sphere, sin(theta) weighted
D2 = D_norm**2
sin_w = np.sin(np.radians(theta))
sin_w = np.maximum(sin_w, 1e-12)
sp = 10*np.log10(np.sum(D2 * sin_w[None, :], axis=1) / np.sum(sin_w) + 1e-12)
DI = on_axis - sp  # = -sp since on_axis = 0
PIR = 10*np.log10(0.5*(10**(on_axis/10) + 10**(sp/10)) + 1e-12)

spin = {"on_axis": on_axis, "lw": lw, "er": er, "sp": sp, "DI": DI, "PIR": PIR}

print(f"\n{cfg['label']}:")
print(f"  DI at crossover ({fc_tw:.0f} Hz): {DI[np.argmin(np.abs(f_spin - fc_tw))]:.1f} dB")
print(f"  DI at 2 kHz:  {DI[np.argmin(np.abs(f_spin - 2000))]:.1f} dB")
print(f"  DI at 10 kHz: {DI[np.argmin(np.abs(f_spin - 10000))]:.1f} dB")

# ============================================================
#  System on-axis frequency response
# ============================================================
f_sys = np.logspace(np.log10(18), np.log10(22000), 1800)

tw_sens = cfg["tw_sens"]
roll_start = cfg["tw_roll_start"]

# Woofer: sealed + LR4 LP@150
Fc_w = 34.5; Qtc_w = 0.62
s_w = 1j * f_sys / Fc_w
H_sealed = s_w**2 / (s_w**2 + s_w/Qtc_w + 1)
mag_woofer = 20*np.log10(np.abs(H_sealed)) + 85.0
mag_woofer += lr4_lp_db(f_sys, 150.0)

# Midrange: flat + LR4 HP@150 + LP@1100
mag_mid = np.ones_like(f_sys) * 89.7
mag_mid += lr4_hp_db(f_sys, 150.0)
mag_mid += lr4_lp_db(f_sys, fc_tw)

# Tweeter: smooth roll-in from Fs region + LR4 HP@1100
step = 0.5 * (1.0 + np.tanh(np.log10(f_sys / (roll_start * 1.3)) / 0.30))
mag_tweeter = tw_sens + 20*np.log10(step + 1e-6)
mag_tweeter += lr4_hp_db(f_sys, fc_tw)

# Level-match tweeter to midrange (DSP pad): -1.8 dB
pad = tw_sens - 89.7
mag_tweeter_trimmed = mag_tweeter - pad

# System sum (level-matched)
w_lin = 10**(mag_woofer/20.0)
m_lin = 10**(mag_mid/20.0)
t_lin = 10**(mag_tweeter_trimmed/20.0)
mag_sum = 20*np.log10(w_lin + m_lin + t_lin)

print(f"\nSystem response ({cfg['label']}):")
print(f"  Tweeter DSP pad: -{pad:.1f} dB")
fc_idx = np.argmin(np.abs(f_sys - fc_tw))
print(f"  Sum at crossover ({fc_tw:.0f} Hz): {mag_sum[fc_idx]:.1f} dB")
passband = (f_sys > 80) & (f_sys < 15000)
pb_vals = mag_sum[passband]
ripple = np.max(pb_vals) - np.min(pb_vals)
print(f"  Passband ripple (80-15k): {ripple:.1f} dB")

# ============================================================
#  PLOT 1: Spinorama
# ============================================================
fig = plt.figure(figsize=(16, 10))

# --- Panel 1: Spinorama curves (on-axis, LW, ER, SP) ---
ax1 = fig.add_subplot(2, 2, 1)
ax1.semilogx(f_spin, spin["on_axis"], lw=2.4, color="0.15", label="On-axis")
ax1.semilogx(f_spin, spin["lw"], lw=1.8, color="tab:green", alpha=0.8, ls="--", label="Listening Window")
ax1.semilogx(f_spin, spin["er"], lw=1.8, color="tab:orange", alpha=0.8, label="Early Reflections")
ax1.semilogx(f_spin, spin["sp"], lw=1.8, color="tab:blue", alpha=0.7, ls=":", label="Sound Power")
ax1.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax1.set_xlim(200, 20000); ax1.set_ylim(-12, 6)
ax1.set_xlabel("Frequency [Hz]"); ax1.set_ylabel("SPL [dB rel on-axis]")
ax1.set_title("Spinorama: On-axis / Listening Window / Early Reflections / Sound Power")
ax1.legend(fontsize=7, loc="upper right", ncol=2)
ax1.grid(True, which="both", alpha=0.25)

# --- Panel 2: Directivity Index ---
ax2 = fig.add_subplot(2, 2, 2)
ax2.semilogx(f_spin, spin["DI"], lw=2.4, color="0.15", label="Directivity Index")
ax2.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax2.axvline(1100, color="tab:blue", ls=":", lw=1.0, alpha=0.4)
ax2.text(1100, 11.5, "1100 Hz", fontsize=8, color="tab:blue", ha="center")
ax2.set_xlim(200, 20000); ax2.set_ylim(-2, 13)
ax2.set_xlabel("Frequency [Hz]"); ax2.set_ylabel("Directivity Index [dB]")
ax2.set_title("Directivity Index (on-axis − sound power)")
ax2.legend(fontsize=8)
ax2.grid(True, which="both", alpha=0.25)

# --- Panel 3: Predicted In-Room Response ---
ax3 = fig.add_subplot(2, 2, 3)
ax3.semilogx(f_spin, spin["PIR"], lw=2.4, color="tab:purple", label="Predicted In-Room")
# Harman target slope (-1 dB/octave from 1k to 10k)
f_harman = np.logspace(np.log10(1000), np.log10(10000), 100)
harman_target = -1.0 * np.log2(f_harman / 1000)  # -1 dB/octave
ax3.semilogx(f_harman, harman_target, lw=1.5, color="0.5", ls="--", label="Harman target (-1 dB/oct)")
ax3.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax3.set_xlim(200, 20000); ax3.set_ylim(-12, 6)
ax3.set_xlabel("Frequency [Hz]"); ax3.set_ylabel("SPL [dB rel on-axis]")
ax3.set_title("Predicted In-Room Response (PIR)")
ax3.legend(fontsize=8)
ax3.grid(True, which="both", alpha=0.25)

# --- Panel 4: Early Reflections & ERDI ---
ax4 = fig.add_subplot(2, 2, 4)
ax4.semilogx(f_spin, spin["er"], lw=2.4, color="tab:orange", label="Early Reflections")
ax4.semilogx(f_spin, spin["lw"] - spin["er"], lw=1.6, color="tab:green", ls="--", alpha=0.8,
             label="ERDI (LW − ER)")
ax4.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax4.set_xlim(200, 20000); ax4.set_ylim(-4, 12)
ax4.set_xlabel("Frequency [Hz]"); ax4.set_ylabel("SPL [dB] / ERDI [dB]")
ax4.set_title("Early Reflections & ERDI (LW − ER)")
ax4.legend(fontsize=7, loc="upper left")
ax4.grid(True, which="both", alpha=0.25)

fig.suptitle("Spinorama estimate — SB26STAC-C000-4 @ 1100 Hz (mk3, simplified 2D model)",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
out1 = os.path.join(os.path.dirname(__file__), "plots", "spinorama_estimate.png")
fig.savefig(out1, dpi=150)
print(f"\nwrote {out1}")

# ============================================================
#  PLOT 2: System frequency response
# ============================================================
fig2, axes = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={"height_ratios": [1, 1]})

# --- Top: Individual driver curves + system sum ---
ax = axes[0]
ax.semilogx(f_sys, mag_sum, lw=2.8, color="tab:blue", label="System sum")
ax.semilogx(f_sys, mag_woofer, lw=1.2, color="tab:red", alpha=0.4, label="Woofer (2×GRS sealed)")
ax.semilogx(f_sys, mag_mid, lw=1.2, color="tab:green", alpha=0.4, label="Mid (15W, LP@1100)")
ax.semilogx(f_sys, mag_tweeter_trimmed, lw=1.2, color="tab:purple", alpha=0.4, label="Tweeter SB26STAC (trimmed)")
ax.axvline(150, color="0.4", ls=":", lw=0.8, alpha=0.4)
ax.axvline(1100, color="tab:blue", ls=":", lw=1.0, alpha=0.4)
ax.text(150, 103, "150 Hz", ha="center", fontsize=8, color="0.4")
ax.text(1100, 103, "1100 Hz", ha="center", fontsize=8, color="tab:blue")
ax.set_xlim(18, 22000); ax.set_ylim(70, 108)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB]")
ax.set_title("System on-axis response — individual drivers + sum")
ax.legend(fontsize=7, loc="lower left", ncol=2)
ax.grid(True, which="both", alpha=0.25)

# --- Bottom: Normalized sum ---
ax = axes[1]
ref_freq = 500.0
ref_idx = np.argmin(np.abs(f_sys - ref_freq))
ax.semilogx(f_sys, mag_sum - mag_sum[ref_idx], lw=2.8, color="tab:blue",
            label="System sum (normalized @ 500 Hz)")
ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.axhline(-3, color="0.4", ls=":", lw=0.6, alpha=0.3)
ax.axvline(1100, color="tab:blue", ls=":", lw=1.0, alpha=0.3)
ax.set_xlim(18, 22000); ax.set_ylim(-25, 8)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB, normalized @ 500 Hz]")
ax.set_title("Normalized system sum (0 dB @ 500 Hz)")
ax.legend(fontsize=9)
ax.grid(True, which="both", alpha=0.25)

fig2.suptitle("System frequency response — SB26STAC-C000-4 @ 1100 Hz (mk3)",
              fontsize=14, fontweight="bold")
fig2.tight_layout(rect=[0, 0, 1, 0.96])

# ============================================================
#  Console summary
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY: mk3 spinorama & system response (SB26STAC @ 1100 Hz)")
print("=" * 70)

fc_idx = np.argmin(np.abs(f_spin - fc_tw))
print(f"\n{cfg['label']}:")
print(f"  Crossover: {fc_tw:.0f} Hz")
print(f"  DI at crossover:  {spin['DI'][fc_idx]:.1f} dB")
print(f"  DI at 2 kHz:      {spin['DI'][np.argmin(np.abs(f_spin - 2000))]:.1f} dB")
print(f"  DI at 10 kHz:     {spin['DI'][np.argmin(np.abs(f_spin - 10000))]:.1f} dB")
print(f"  DI smoothness (max step 1-5 kHz): ", end="")
di_region = spin['DI'][(f_spin > 1000) & (f_spin < 5000)]
di_step = np.max(np.abs(np.diff(di_region)))
print(f"{di_step:.1f} dB")

# PIR slope from 1k to 10k
pir_1k = spin['PIR'][np.argmin(np.abs(f_spin - 1000))]
pir_10k = spin['PIR'][np.argmin(np.abs(f_spin - 10000))]
pir_slope = (pir_10k - pir_1k) / np.log2(10000/1000)
print(f"  PIR slope (1-10 kHz): {pir_slope:.1f} dB/octave (Harman target: -1.0)")

# System sum ripple
pb = (f_sys > 80) & (f_sys < 15000)
ripple = np.max(mag_sum[pb]) - np.min(mag_sum[pb])
print(f"  System sum ripple (80-15k): {ripple:.1f} dB")
print(f"  Tweeter DSP pad: -{pad:.1f} dB")

# CSV export
csv_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, "spinorama_estimate.csv")
header = "freq_Hz,on_axis,LW,ER,SP,DI,PIR"
rows = [header]
for i in range(len(f_spin)):
    rows.append(f"{f_spin[i]:.3f},{spin['on_axis'][i]:.4f},{spin['lw'][i]:.4f},"
                f"{spin['er'][i]:.4f},{spin['sp'][i]:.4f},{spin['DI'][i]:.4f},{spin['PIR'][i]:.4f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"\nwrote {csv_out}")
