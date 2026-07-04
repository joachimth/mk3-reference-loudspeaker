"""
Tweeter selection analysis — why SB26STAC-C000-4 was chosen (historical)
=======================================================================

Historical record of the tweeter selection for the mk3 design. This compares
the two candidate tweeters across the critical design parameters: crossover
margin, excursion headroom, directivity match, and vertical lobing.

The SB26STAC-C000-4 is the selected tweeter for the mk3 design (1100 Hz
crossover). The ScanSpeak H2606/920000 was the earlier candidate; it is
retained here only as the historical baseline that the selection was made
against — it is NOT a current design option.

Key physical differences:
  H2606/920000:   Fs=1030 Hz, Xmax=0.2mm, 95.2 dB, horn exit Ø33mm, 6Ω
  SB26STAC-C000-4: Fs=750 Hz, Xmax=0.6mm, 91.5 dB, bare dome Ø26mm, 4Ω

Crossover scenarios examined:
  H2606 @ 1250 Hz:  220 Hz margin (earlier candidate — superseded)
  H2606 @ 1450 Hz:  420 Hz margin (earlier fallback — superseded)
  SB26STAC @ 1000 Hz: 250 Hz margin (aggressive, below broadside null)
  SB26STAC @ 1100 Hz: 350 Hz margin (balanced — SELECTED)
  SB26STAC @ 1250 Hz: 500 Hz margin (same crossover, much safer)

Output: simulations/plots/tweeter_comparison.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c = 344.0

# ============================================================
# 1. EXCURSION ANALYSIS
# ============================================================
# For a dome tweeter producing SPL at frequency f, the required
# displacement scales as 1/f^2 for constant SPL (piston regime).
# Xmax determines the max SPL before distortion rises sharply.
#
# Relative excursion at crossover frequency (normalized to H2606 @ 1250):
#   x ∝ Sd^-1 × f^-2 × 10^(SPL/20)
# For equal SPL output, excursion ratio between drivers:
#   x_ratio = (Sd_ref / Sd) × (f_ref / f)^2

# Driver parameters
drivers = {
    "H2606": {
        "Fs": 1030, "Xmax_mm": 0.2, "Sd_cm2": 5.7, "sens_dB": 95.2,
        "Re": 4.7, "imp": 6, "throat_d": 33, "faceplate": 104, "BCD": 95,
        "depth_mm": 44, "horn": True, "ferrofluid": True,
        "power_W": 100, "price_eur": 44, "color": "tab:red",
    },
    "SB26STAC": {
        "Fs": 750, "Xmax_mm": 0.6, "Sd_cm2": 6.2, "sens_dB": 91.5,
        "Re": 3.2, "imp": 4, "throat_d": 28, "faceplate": 100, "BCD": 88.5,
        "depth_mm": 39.7, "horn": False, "ferrofluid": False,
        "power_W": 120, "price_eur": 37, "color": "tab:blue",
    },
}

# Crossover scenarios
xover_scenarios = [
    ("H2606 @ 1250", "H2606", 1250, "tab:red", "--"),
    ("H2606 @ 1450", "H2606", 1450, "tab:red", ":"),
    ("SB26 @ 1000",  "SB26STAC", 1000, "tab:blue", "--"),
    ("SB26 @ 1100",  "SB26STAC", 1100, "tab:blue", "-."),
    ("SB26 @ 1250",  "SB26STAC", 1250, "tab:blue", "-"),
]

# Max SPL at crossover frequency (simplified):
# SPL_max = sens + 20*log10(Xmax / x_ref)
# where x_ref is the displacement needed for 1 Pascal at 1m at freq f
# For comparison we compute relative max SPL: 20*log10(Xmax * f^2 * Sd)
# Higher = more headroom before distortion

print("=" * 70)
print("EXCURSION HEADROOM AT CROSSOVER (relative max SPL before distortion)")
print("=" * 70)
print(f"{'Scenario':>16} {'Driver':>10} {'Fc':>6} {'Fs':>6} {'Margin':>7} {'Xmax':>6} {'Rel SPL':>8}")
print("-" * 70)
for name, drv_key, fc, _, _ in xover_scenarios:
    d = drivers[drv_key]
    margin = fc - d["Fs"]
    # Relative max SPL: proportional to Xmax × Sd × f^2
    # Normalize to H2606 @ 1250
    rel_spl = 20 * np.log10(d["Xmax_mm"] * d["Sd_cm2"] * fc**2 /
                             (drivers["H2606"]["Xmax_mm"] * drivers["H2606"]["Sd_cm2"] * 1250**2))
    print(f"{name:>16} {drv_key:>10} {fc:>5}Hz {d['Fs']:>5}Hz {margin:>5}Hz {d['Xmax_mm']:>5.1f}mm {rel_spl:>+7.1f}dB")

# ============================================================
# 2. DIRECTIVITY MATCH (same WG212 coverage for both)
# ============================================================
# Both waveguides use theta_h=50, theta_v=32 (identical coverage).
# The only difference is throat_d (28 vs 33) which produces a
# marginally different mouth size but the same coverage angles.
# So the directivity match with the 15W is essentially identical
# for both tweeters at the same crossover frequency.
#
# The advantage of SB26STAC is that it CAN cross lower (1000-1100 Hz)
# where the 15W is closer to omni, reducing the DI step.

# 15W piston beamwidth
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

a_mid = np.sqrt(107e-4 / np.pi)  # 15W effective radius ~58.3mm
theta = np.radians(np.linspace(0.5, 90, 600))

def piston_beamwidth_deg(f):
    ka = 2*np.pi*f/c * a_mid
    arg = ka * np.sin(theta)
    D = np.ones_like(arg)
    nz = arg != 0
    D[nz] = np.abs(2*j1(arg[nz]) / arg[nz])
    below = np.where(D <= 0.5)[0]
    if below.size == 0:
        return 180.0
    return 2*np.degrees(theta[below[0]])

def di_from_coverage(th_h, th_v):
    return 10*np.log10(41253.0 / (th_h * th_v))

F_CTRL = 1620.0
def wg_coverage_deg(f):
    if f >= F_CTRL:
        return 100.0, 64.0
    g = (F_CTRL - f) / F_CTRL
    return 100.0 + g*(180.0 - 100.0), 64.0 + g*(140.0 - 64.0)

print("\n" + "=" * 70)
print("DIRECTIVITY MATCH (DI mismatch between 15W and WG212 tweeter)")
print("=" * 70)
print(f"{'Crossover':>10} {'DI_mid':>8} {'DI_tweeter':>10} {'Mismatch':>10}")
print("-" * 70)
for fc in [1000, 1100, 1250, 1450, 1600]:
    dm = max(di_from_coverage(piston_beamwidth_deg(fc), piston_beamwidth_deg(fc)), 0.0)
    th_h, th_v = wg_coverage_deg(fc)
    dt = di_from_coverage(th_h, th_v)
    print(f"{fc:>9}Hz {dm:>7.1f}dB {dt:>9.1f}dB {dt-dm:>+9.1f}dB")

# ============================================================
# 3. VERTICAL LOBING (c-c = 150mm, LR4)
# ============================================================
def lr4_lp(f, fc):
    s = 1j * f / fc
    return np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2)

def lr4_hp(f, fc):
    s = 1j * f / fc
    return np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2)

def vertical_pattern(f, theta_deg, d, fc):
    theta = np.radians(theta_deg)
    delta = 2 * np.pi * f / c * d * np.sin(theta)
    w_mid = lr4_lp(f, fc)
    w_twt = lr4_hp(f, fc)
    return np.abs(w_mid * np.ones_like(theta) + w_twt * np.exp(1j * delta))

d_cc = 0.150
theta_fine = np.linspace(0.1, 90, 500)

print("\n" + "=" * 70)
print("VERTICAL LOBING (c-c=150mm, LR4, first null)")
print("=" * 70)
print(f"{'Crossover':>10} {'Null angle':>11} {'Null depth':>11} {'At ±15°':>10}")
print("-" * 70)
for fc in [1000, 1100, 1250, 1450]:
    pattern = vertical_pattern(fc, theta_fine, d_cc, fc)
    pattern = pattern / np.max(pattern)
    dB = 20*np.log10(pattern)
    minima = np.where((dB[1:-1] < dB[:-2]) & (dB[1:-1] < dB[2:]))[0] + 1
    if len(minima) > 0:
        null_angle = theta_fine[minima[0]]
        null_depth = dB[minima[0]]
    else:
        null_angle = 90
        null_depth = dB[-1]
    # SPL at ±15° (listening window edge)
    idx_15 = np.argmin(np.abs(theta_fine - 15))
    spl_15 = dB[idx_15]
    print(f"{fc:>9}Hz {null_angle:>9.0f}° {null_depth:>+9.1f}dB {spl_15:>+8.1f}dB")

# Broadside null position for c-c=150mm: f_null = c/(2*d) = 1147 Hz
f_broadside = c / (2 * d_cc)
print(f"\nBroadside null at {f_broadside:.0f} Hz for c-c={d_cc*1000:.0f}mm")
print(f"  Crossover below {f_broadside:.0f} Hz → null is ABOVE the crossover (better)")
print(f"  Crossover above {f_broadside:.0f} Hz → null is BELOW the crossover (worse)")

# ============================================================
# 4. COMPREHENSIVE COMPARISON PLOT
# ============================================================
fig = plt.figure(figsize=(16, 12))

# --- Plot 1: Excursion headroom ---
ax1 = fig.add_subplot(2, 2, 1)
freqs = np.linspace(500, 2000, 200)
for drv_key, d in drivers.items():
    # Max SPL relative to 1W/1m, limited by Xmax
    # SPL_max(f) = sens + 20*log10(Xmax * f^2 / (x_ref * f_ref^2))
    # Simplified: relative to driver's own sensitivity
    rel_max = 20 * np.log10(d["Xmax_mm"] * d["Sd_cm2"] * freqs**2 /
                            (drivers["H2606"]["Xmax_mm"] * drivers["H2606"]["Sd_cm2"] * 1250**2))
    ax1.plot(freqs, rel_max, lw=2.2, color=d["color"], label=f"{drv_key} (Xmax={d['Xmax_mm']}mm)")
    ax1.axvline(d["Fs"], color=d["color"], ls=":", lw=1.2, alpha=0.7)
    ax1.text(d["Fs"]+10, rel_max[0]+1, f"Fs={d['Fs']}", color=d["color"], fontsize=8)

for name, drv_key, fc, col, ls in xover_scenarios:
    ax1.axvline(fc, color=col, ls=ls, lw=1.0, alpha=0.5)
ax1.axvline(1250, color="tab:purple", ls="--", lw=1.5, alpha=0.6)
ax1.text(1255, 10, "1250 Hz\n(superseded)", color="tab:purple", fontsize=7, ha="left")
ax1.set_xlabel("Frequency [Hz]")
ax1.set_ylabel("Relative max SPL before distortion [dB]")
ax1.set_title("Excursion Headroom (H2606 @ 1250 = 0 dB reference)")
ax1.set_xlim(500, 2000); ax1.set_ylim(-5, 15)
ax1.grid(True, alpha=0.25); ax1.legend(fontsize=8)

# --- Plot 2: Directivity match ---
ax2 = fig.add_subplot(2, 2, 2)
f = np.logspace(np.log10(200), np.log10(20000), 400)
di_mid = np.array([max(di_from_coverage(piston_beamwidth_deg(fi), piston_beamwidth_deg(fi)), 0.0) for fi in f])
wg = np.array([wg_coverage_deg(fi) for fi in f])
di_tw = di_from_coverage(wg[:,0], wg[:,1])
ax2.semilogx(f, di_mid, lw=2.2, color="tab:blue", label="15W midrange (piston)")
ax2.semilogx(f, di_tw, lw=2.2, color="tab:red", label="WG212 tweeter (coverage)")
for fc, col, ls, lbl in [(1000, "tab:blue", "--", "SB26@1000"),
                          (1100, "tab:blue", "-.", "SB26@1100"),
                          (1250, "tab:purple", "--", "H2606@1250"),
                          (1450, "tab:red", ":", "H2606@1450")]:
    ax2.axvline(fc, color=col, ls=ls, lw=1.4, alpha=0.6)
    dm = max(di_from_coverage(piston_beamwidth_deg(fc), piston_beamwidth_deg(fc)), 0.0)
    th_h, th_v = wg_coverage_deg(fc)
    dt = di_from_coverage(th_h, th_v)
    ax2.text(fc, 10.5, f"{lbl}\nΔ{dt-dm:.1f}", color=col, fontsize=6.5, ha="center")
ax2.set_xlim(200, 20000); ax2.set_ylim(0, 12)
ax2.set_xlabel("Frequency [Hz]"); ax2.set_ylabel("Directivity index DI [dB]")
ax2.set_title("Directivity Match (smaller Δ = better)")
ax2.grid(True, which="both", alpha=0.25); ax2.legend(fontsize=8, loc="upper left")

# --- Plot 3: Vertical lobing at different crossovers ---
ax3 = fig.add_subplot(2, 2, 3)
theta_plot = np.linspace(-60, 60, 300)
for fc, col, ls, lbl in [(1000, "tab:blue", "-", "1000 Hz (SB26 aggressive)"),
                          (1100, "tab:blue", "-.", "1100 Hz (SB26 — SELECTED)"),
                          (1250, "tab:purple", "--", "1250 Hz (H2606 superseded)"),
                          (1450, "tab:red", ":", "1450 Hz (H2606 superseded)")]:
    pattern = vertical_pattern(fc, theta_plot, d_cc, fc)
    pattern = pattern / np.max(pattern)
    ax3.plot(theta_plot, 20*np.log10(pattern), lw=2.0, color=col, ls=ls, label=lbl)
ax3.axhline(-3, color="0.5", ls=":", lw=0.8)
ax3.axvspan(-15, 15, alpha=0.1, color="green", label="Listening window ±15°")
ax3.set_xlim(-60, 60); ax3.set_ylim(-30, 3)
ax3.set_xlabel("Vertical angle [deg]"); ax3.set_ylabel("SPL [dB]")
ax3.set_title("Vertical Pattern at Crossover (c-c=150mm, LR4)")
ax3.grid(True, alpha=0.25); ax3.legend(fontsize=7, loc="lower right")

# --- Plot 4: Spec comparison radar/bar chart ---
ax4 = fig.add_subplot(2, 2, 4)
categories = ["Fs margin\n@1250 (Hz)", "Xmax\n(×0.1mm)", "Sens match\nto 15W (dB)", "Power\n(W÷10)", "Price\n(inv)", "CAD data\navail"]
# Normalize each category to 0-10 scale (higher = better)
h2606_vals = [220, 2.0, 5.5, 10.0, 44, 10]  # STEP available = 10
sb26_vals = [500, 6.0, 1.8, 12.0, 37, 3]    # No STEP = 3

# Normalize
max_vals = [max(h, s) for h, s in zip(h2606_vals, sb26_vals)]
h_norm = [h/m*10 for h, m in zip(h2606_vals, max_vals)]
s_norm = [s/m*10 for s, m in zip(sb26_vals, max_vals)]

x = np.arange(len(categories))
width = 0.35
ax4.barh(x - width/2, h_norm, width, color="tab:red", label="H2606/920000", alpha=0.85)
ax4.barh(x + width/2, s_norm, width, color="tab:blue", label="SB26STAC-C000-4", alpha=0.85)
ax4.set_yticks(x); ax4.set_yticklabels(categories, fontsize=8)
ax4.set_xlim(0, 12); ax4.set_xlabel("Relative score (10 = best of pair)")
ax4.set_title("Feature Comparison (higher = better)")
ax4.legend(fontsize=8, loc="lower right")
# Annotate raw values
for i, (h, s) in enumerate(zip(h2606_vals, sb26_vals)):
    ax4.text(h_norm[i]+0.3, i-width/2, str(h), fontsize=7, va="center", color="tab:red")
    ax4.text(s_norm[i]+0.3, i+width/2, str(s), fontsize=7, va="center", color="tab:blue")

fig.suptitle("Tweeter selection analysis — SB26STAC-C000-4 (selected) vs H2606/920000 (superseded baseline)",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])

out = os.path.join(os.path.dirname(__file__), "plots", "tweeter_comparison.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=150)
print(f"\nwrote {out}")
