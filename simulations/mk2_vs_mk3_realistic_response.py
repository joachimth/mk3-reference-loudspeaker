"""
Mk2 vs Mk3 — Realistic system frequency response with datasheet curves
=======================================================================

Uses ACTUAL frequency response curves extracted from the manufacturer
datasheets (digitized from the PDF graphs), combined with:

  1. Baffle step (Vanderkooy model, 300mm cabinet baffle)
  2. Waveguide loading (WG212 acoustic gain above control limit)
  3. Sealed woofer alignment (2x GRS 8SW-4HE, Fc=34.5 Hz, Qtc=0.62)
  4. LR4 crossover filters (150 Hz + 1100/1250 Hz)
  5. DSP level matching (tweeter pad to match midrange)

Data sources:
  - SB26STAC-C000-4: assets/datasheets/SB26STAC-C000-4.pdf (digitized)
  - H2606/920000: assets/datasheets/H2606-920000.pdf (digitized)
  - 15W/4434G00: ScanSpeak datasheet (digitized)
  - GRS 8SW-4HE-8: modeled from T/S params (sealed alignment)
  - Baffle step: Vanderkooy/Keele, 300mm baffle
  - Waveguide loading: WG212 control limit ~1620 Hz, +2.5 dB gain

ASSUMPTIONS
  - Datasheet curves are measured on IEC baffle (31.6 cm mic distance,
    normalized to 2.83V/1m). On-axis curves used.
  - Baffle step is applied to ALL drivers (they're all on the same baffle).
    The step transition is ~365 Hz for the 300mm baffle.
  - Waveguide loading adds acoustic gain above the control limit. The
    bare-dome tweeter response (from datasheet) is modified by the WG212
    loading: +2.5 dB above 1620 Hz, transitioning smoothly from 1100-1800 Hz.
  - The H2606 already has a built-in horn, so its datasheet curve already
    includes horn loading. The WG212 adds ADDITIONAL loading on top.
  - The SB26STAC has NO horn — its datasheet curve is the bare dome on an
    IEC baffle. The WG212 provides ALL the loading.
  - Room gain not included (anechoic estimate).
  - DSP EQ not applied (raw response shown — DSP would flatten this).

Output: simulations/plots/mk2_vs_mk3_realistic_response.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

c_speed = 343.0

# ============================================================
#  Load digitized datasheet curves
# ============================================================
data = np.load('/workspace/scratch/datasheet_curves.npz')
sb26_freq = data['sb26_freq']; sb26_spl = data['sb26_spl']
h2606_freq = data['h2606_freq']; h2606_spl = data['h2606_spl']
w15_freq = data['w15_freq']; w15_spl = data['w15_spl']

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
# Cabinet: 300mm wide, 370mm deep
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
# For a horn tweeter (H2606): +1.0 dB additional gain (already has horn)
F_CTRL = 1620.0

def wg_loading_db(f, gain_db, f_low=1000, f_high=2000):
    """Waveguide loading gain: 0 dB below f_low, gain_db above f_high.
    Smooth transition using tanh over ~0.3 octaves centered between f_low and f_high."""
    f_mid = np.sqrt(f_low * f_high)  # geometric mean (log center)
    spread = (np.log10(f_high) - np.log10(f_low)) * 0.3  # ~0.3 octave half-width
    t = 0.5 * (1.0 + np.tanh((np.log10(f) - np.log10(f_mid)) / spread))
    return gain_db * t

# ============================================================
#  Woofer model: sealed alignment (same for mk2 and mk3)
# ============================================================
# 2x GRS 8SW-4HE-8 in ~69L sealed
# Fc = 34.5 Hz, Qtc = 0.62, sensitivity 85 dB (2 drivers + 3dB = 88 dB half-space)
Fc_w = 34.5; Qtc_w = 0.62; sens_w = 85.0  # per driver, 2 drivers ≈ +3 dB
# Note: datasheet sensitivity for GRS is ~85 dB, two in push-push = +3 dB = 88 dB

def woofer_response(f):
    """Sealed woofer pair response."""
    s = 1j * f / Fc_w
    H_sealed = s**2 / (s**2 + s/Qtc_w + 1)
    mag = 20*np.log10(np.abs(H_sealed) + 1e-12) + (sens_w + 3.0)  # +3 dB for 2 drivers
    return mag

# ============================================================
#  Build system response for each design
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

designs = {
    "mk2 (H2606 @ 1250 Hz)": {
        "xover_tw": 1250.0,
        "tw_pad": 5.5,  # dB attenuation to match midrange
        "tw_freq": h2606_freq,
        "tw_spl": h2606_spl,
        "wg_gain": 1.0,  # H2606 already has horn, WG212 adds modest gain
        "color": "tab:red",
    },
    "mk3 (SB26STAC @ 1100 Hz)": {
        "xover_tw": 1100.0,
        "tw_pad": 1.8,
        "tw_freq": sb26_freq,
        "tw_spl": sb26_spl,
        "wg_gain": 2.5,  # SB26STAC bare dome, WG212 provides full loading
        "color": "tab:blue",
    },
}

results = {}

for name, cfg in designs.items():
    fc_tw = cfg["xover_tw"]

    # --- Woofer (same for both) ---
    mag_w_raw = woofer_response(f)
    mag_w = mag_w_raw + bs  # baffle step applies
    mag_w += lr4_lp_db(f, 150.0)  # LP at 150 Hz

    # --- Midrange: real datasheet curve ---
    mag_m_raw = interp_curve(w15_freq, w15_spl, f, fill_below=89.7, fill_above=80.0)
    # Apply baffle step to midrange (it's on the same baffle)
    mag_m = mag_m_raw + bs
    # Crossover: HP@150 + LP@xover
    mag_m += lr4_hp_db(f, 150.0)
    mag_m += lr4_lp_db(f, fc_tw)

    # --- Tweeter: real datasheet curve + waveguide loading ---
    mag_t_raw = interp_curve(cfg["tw_freq"], cfg["tw_spl"], f,
                              fill_below=cfg["tw_spl"][0] - 20,
                              fill_above=cfg["tw_spl"][-1] - 20)
    # Baffle step: minimal effect above ~500 Hz, but apply for consistency
    # Actually, for the tweeter range (>1 kHz), baffle step is ~0 dB, so skip
    # Apply waveguide loading
    wg_gain = wg_loading_db(f, cfg["wg_gain"], f_low=fc_tw, f_high=2000)
    mag_t = mag_t_raw + wg_gain
    # Crossover: HP@xover
    mag_t += lr4_hp_db(f, fc_tw)
    # DSP pad to match midrange
    mag_t_trimmed = mag_t - cfg["tw_pad"]

    # --- System sum (linear domain for proper summation) ---
    w_lin = 10**(mag_w / 20.0)
    m_lin = 10**(mag_m / 20.0)
    t_lin = 10**(mag_t_trimmed / 20.0)
    mag_sum = 20*np.log10(w_lin + m_lin + t_lin + 1e-12)

    results[name] = {
        "woofer": mag_w, "mid": mag_m,
        "tweeter_raw": mag_t_raw, "tweeter_wg": mag_t,
        "tweeter_trimmed": mag_t_trimmed,
        "sum": mag_sum,
        "wg_gain_curve": wg_gain,
        "baffle_step": bs,
    }

    # Print key metrics
    fc_idx = np.argmin(np.abs(f - fc_tw))
    # Use actual passband: 200 Hz - 15 kHz (above woofer rolloff)
    pb = (f > 200) & (f < 15000)
    ripple = np.max(mag_sum[pb]) - np.min(mag_sum[pb])
    # Also measure 500-10k (midband flatness — what DSP targets)
    pb_mid = (f > 500) & (f < 10000)
    ripple_mid = np.max(mag_sum[pb_mid]) - np.min(mag_sum[pb_mid])
    print(f"\n{name}:")
    print(f"  Tweeter pad: -{cfg['tw_pad']:.1f} dB")
    print(f"  WG gain: +{cfg['wg_gain']:.1f} dB above {F_CTRL:.0f} Hz")
    print(f"  Sum @ crossover ({fc_tw:.0f} Hz): {mag_sum[fc_idx]:.1f} dB")
    print(f"  Passband ripple (200-15k): {ripple:.1f} dB")
    print(f"  Midband ripple (500-10k): {ripple_mid:.1f} dB")
    print(f"  Sum @ 100 Hz: {np.interp(100, f, mag_sum):.1f} dB")
    print(f"  Sum @ 500 Hz: {np.interp(500, f, mag_sum):.1f} dB")
    print(f"  Sum @ 2 kHz: {np.interp(2000, f, mag_sum):.1f} dB")
    print(f"  Sum @ 10 kHz: {np.interp(10000, f, mag_sum):.1f} dB")

# ============================================================
#  PLOT: Realistic system response comparison
# ============================================================
fig, axes = plt.subplots(4, 1, figsize=(15, 16), gridspec_kw={"height_ratios": [1.2, 1, 0.6, 0.8]})

# --- Panel 1: Individual drivers + system sum ---
ax = axes[0]
for name, cfg in designs.items():
    r = results[name]
    col = cfg["color"]
    ls = "-" if "mk3" in name else "--"
    ax.semilogx(f, r["sum"], lw=3.0, color=col, ls=ls, label=f'{name} — system sum')

# Show individual drivers for mk3
r3 = results["mk3 (SB26STAC @ 1100 Hz)"]
ax.semilogx(f, r3["woofer"], lw=1.2, color="tab:red", alpha=0.3, label="Woofer (2×GRS sealed + baffle step)")
ax.semilogx(f, r3["mid"], lw=1.2, color="tab:green", alpha=0.3, label="Mid (15W real curve + baffle step + LR4)")
ax.semilogx(f, r3["tweeter_trimmed"], lw=1.2, color="tab:blue", alpha=0.3, label="Tweeter (SB26STAC real curve + WG loading + pad)")

# Baffle step curve
ax.semilogx(f, r3["baffle_step"], lw=1.0, color="0.6", ls=":", alpha=0.5, label="Baffle step (-6 dB → 0 dB)")

ax.axvline(150, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.axvline(1100, color="tab:blue", ls=":", lw=1.0, alpha=0.3)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
ax.text(150, 100, "150 Hz", ha="center", fontsize=8, color="0.4")
ax.text(1100, 100, "1100", ha="center", fontsize=7, color="tab:blue")
ax.text(1250, 97, "1250", ha="center", fontsize=7, color="tab:red")
ax.set_xlim(20, 22000); ax.set_ylim(60, 105)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB]")
ax.set_title("Realistic system response — real datasheet curves + baffle step + waveguide loading")
ax.legend(fontsize=7, loc="lower left", ncol=2)
ax.grid(True, which="both", alpha=0.25)

# --- Panel 2: Normalized sum comparison ---
ax = axes[1]
ref_idx = np.argmin(np.abs(f - 500))
for name, cfg in designs.items():
    r = results[name]
    col = cfg["color"]
    ls = "-" if "mk3" in name else "--"
    norm = r["sum"] - r["sum"][ref_idx]
    ax.semilogx(f, norm, lw=2.8, color=col, ls=ls, label=name)
ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.axhline(3, color="0.4", ls=":", lw=0.5, alpha=0.2)
ax.axhline(-3, color="0.4", ls=":", lw=0.5, alpha=0.2)
ax.axvline(1100, color="tab:blue", ls=":", lw=0.8, alpha=0.2)
ax.axvline(1250, color="tab:red", ls=":", lw=0.8, alpha=0.2)
ax.set_xlim(20, 22000); ax.set_ylim(-20, 10)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB, norm @ 500 Hz]")
ax.set_title("Normalized system sum (0 dB @ 500 Hz) — pre-DSP")
ax.legend(fontsize=9)
ax.grid(True, which="both", alpha=0.25)

# --- Panel 3: Difference (mk3 - mk2) ---
ax = axes[2]
mk2_norm = results["mk2 (H2606 @ 1250 Hz)"]["sum"] - results["mk2 (H2606 @ 1250 Hz)"]["sum"][ref_idx]
mk3_norm = results["mk3 (SB26STAC @ 1100 Hz)"]["sum"] - results["mk3 (SB26STAC @ 1100 Hz)"]["sum"][ref_idx]
diff = mk3_norm - mk2_norm
ax.semilogx(f, diff, lw=2.4, color="0.15")
ax.axhline(0, color="0.5", ls="-", lw=0.8, alpha=0.5)
ax.fill_between(f, 0, diff, where=diff > 0, alpha=0.15, color="tab:blue", label="mk3 > mk2")
ax.fill_between(f, 0, diff, where=diff < 0, alpha=0.15, color="tab:red", label="mk2 > mk3")
ax.axvline(1100, color="tab:blue", ls=":", lw=0.8, alpha=0.2)
ax.axvline(1250, color="tab:red", ls=":", lw=0.8, alpha=0.2)
ax.set_xlim(20, 22000); ax.set_ylim(-8, 8)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Δ SPL [dB]")
ax.set_title("Difference: mk3 (SB26STAC @ 1100) − mk2 (H2606 @ 1250), normalized @ 500 Hz")
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)
# Annotate max differences
for region_name, f_lo, f_hi in [("bass", 50, 150), ("xover", 900, 1800), ("treble", 5000, 15000)]:
    mask = (f > f_lo) & (f < f_hi)
    if np.any(mask):
        idx = np.argmax(np.abs(diff[mask]))
        f_max = f[mask][idx]
        v_max = diff[mask][idx]
        ax.annotate(f"{region_name}: {v_max:+.1f} dB @ {f_max:.0f} Hz",
                    xy=(f_max, v_max), xytext=(f_max*2, v_max + np.sign(v_max)*1.5),
                    fontsize=7, arrowprops=dict(arrowstyle="->", color="0.4"))

# --- Panel 4: Acoustic effects + DSP correction needed ---
ax = axes[3]
# Baffle step
ax.semilogx(f, bs, lw=2.0, color="tab:orange", label="Baffle step (300mm baffle)")
# WG loading
wg_mk2 = wg_loading_db(f, 1.0, f_low=1250, f_high=2000)
wg_mk3 = wg_loading_db(f, 2.5, f_low=1100, f_high=2000)
ax.semilogx(f, wg_mk2, lw=1.8, color="tab:red", ls="--", label="WG loading mk2 (+1.0 dB)")
ax.semilogx(f, wg_mk3, lw=1.8, color="tab:blue", ls="--", label="WG loading mk3 (+2.5 dB)")

# DSP correction needed: inverse of sum deviation from target (flat @ 500 Hz)
ref_idx_dsp = np.argmin(np.abs(f - 500))
for name, cfg in designs.items():
    r = results[name]
    col = cfg["color"]
    ls = "-" if "mk3" in name else "--"
    # Target: flat at the 500 Hz level, only in passband 200-15k
    target = r["sum"][ref_idx_dsp]
    correction = target - r["sum"]  # positive = boost needed, negative = cut
    # Only show in passband
    corr_mask = (f > 100) & (f < 18000)
    corr_display = np.where(corr_mask, correction, np.nan)
    ax.semilogx(f, corr_display, lw=2.0, color=col, ls=ls, alpha=0.6,
                label=f"DSP correction {name.split('(')[0].strip()}")

ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.axvline(f_bs, color="tab:orange", ls=":", lw=0.8, alpha=0.3)
ax.text(f_bs, -8, f"f_bs={f_bs:.0f} Hz", fontsize=8, color="tab:orange", ha="center")
ax.axvline(F_CTRL, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.text(F_CTRL, -8, f"WG={F_CTRL:.0f} Hz", fontsize=8, color="0.4", ha="center")
ax.set_xlim(20, 22000); ax.set_ylim(-12, 8)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Gain [dB]")
ax.set_title("Acoustic effects + DSP correction needed (boost/cut to flatten to 500 Hz reference)")
ax.legend(fontsize=7, loc="lower right", ncol=2)
ax.grid(True, which="both", alpha=0.25)

fig.suptitle("Mk2 vs Mk3 — Realistic system response (real datasheet curves + baffle step + WG loading)\n"
             "Pre-DSP, anechoic. Curves digitized from manufacturer datasheets.",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.94])

out = os.path.join(os.path.dirname(__file__) if '__file__' in dir() else 'mk2-reference-loudspeaker/simulations',
                   'plots', 'mk2_vs_mk3_realistic_response.png')
# Fix path
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '/workspace/mk2-reference-loudspeaker/simulations'
out = os.path.join(script_dir, 'plots', 'mk2_vs_mk3_realistic_response.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=150)
print(f"\nwrote {out}")

# CSV export
csv_dir = os.path.join(os.path.dirname(out), '..', 'csv')
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, 'mk2_vs_mk3_realistic_response.csv')
header = "freq_Hz,mk2_sum_dB,mk3_sum_dB,mk2_woof_dB,mk3_mid_dB,mk3_tweeter_dB,baffle_step_dB,wg_loading_mk2_dB,wg_loading_mk3_dB"
rows = [header]
for i in range(len(f)):
    rows.append(f"{f[i]:.2f},{results['mk2 (H2606 @ 1250 Hz)']['sum'][i]:.4f},"
                f"{results['mk3 (SB26STAC @ 1100 Hz)']['sum'][i]:.4f},"
                f"{results['mk3 (SB26STAC @ 1100 Hz)']['woofer'][i]:.4f},"
                f"{results['mk3 (SB26STAC @ 1100 Hz)']['mid'][i]:.4f},"
                f"{results['mk3 (SB26STAC @ 1100 Hz)']['tweeter_trimmed'][i]:.4f},"
                f"{bs[i]:.4f},{wg_mk2[i]:.4f},{wg_mk3[i]:.4f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")

# ============================================================
#  Summary
# ============================================================
print("\n" + "=" * 70)
print("REALISTIC SYSTEM RESPONSE SUMMARY (pre-DSP, anechoic)")
print("=" * 70)
for name, cfg in designs.items():
    r = results[name]
    pb = (f > 200) & (f < 15000)
    pb_mid = (f > 500) & (f < 10000)
    ripple = np.max(r["sum"][pb]) - np.min(r["sum"][pb])
    ripple_mid = np.max(r["sum"][pb_mid]) - np.min(r["sum"][pb_mid])
    print(f"\n{name}:")
    print(f"  Passband ripple (200-15k, pre-DSP): {ripple:.1f} dB")
    print(f"  Midband ripple (500-10k, pre-DSP): {ripple_mid:.1f} dB")
    print(f"  Baffle step effect @ 300 Hz: {np.interp(300, f, bs):.1f} dB")
    print(f"  WG loading @ 2 kHz: {np.interp(2000, f, wg_loading_db(f, cfg['wg_gain'], cfg['xover_tw'], 2000)):.1f} dB")
    print(f"  Sum @ 100 Hz: {np.interp(100, f, r['sum']):.1f} dB")
    print(f"  Sum @ 500 Hz: {np.interp(500, f, r['sum']):.1f} dB")
    print(f"  Sum @ 2 kHz: {np.interp(2000, f, r['sum']):.1f} dB")
    print(f"  Sum @ 10 kHz: {np.interp(10000, f, r['sum']):.1f} dB")
    # DSP correction in midband only
    ref = np.interp(500, f, r["sum"])
    devs_mid = (r["sum"] - ref)[pb_mid]
    max_corr_mid = np.max(np.abs(devs_mid))
    devs_pb = (r["sum"] - ref)[pb]
    max_corr_pb = np.max(np.abs(devs_pb))
    print(f"  DSP correction needed (midband 500-10k): ±{max_corr_mid:.1f} dB")
    print(f"  DSP correction needed (passband 200-15k): ±{max_corr_pb:.1f} dB")
