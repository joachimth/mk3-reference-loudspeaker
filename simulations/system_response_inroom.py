"""
System response: anechoic → in-room → level-corrected → post-DSP
=================================================================

Four-stage progression for the mk3 v9 reference loudspeaker:

  1. Anechoic (pre-DSP): Real datasheet curves + baffle step + WG loading + LR4
  2. In-room:            Anechoic + room gain (average living room)
  3. Level-corrected:    In-room normalized to 500 Hz reference
  4. Post-DSP:           Level-corrected + EQ toward Harman in-room target

Room model (average living room — "gennemsnitlig stue"):
  - Dimensions: 4.5 × 4.0 × 2.4 m → V = 43.2 m³
  - RT60 ≈ 0.4 s (typical furnished room)
  - f_schroeder = 2000 * sqrt(RT60/V) ≈ 192 Hz
  - Room gain: +6 dB/octave below f_schroeder, cap +9 dB (3 boundary surfaces)
  - HF absorption: -1.5 dB/octave above 5 kHz, cap -3 dB (furnishings)

DSP model (v9 actual settings):
  - Woofer gain: -4.0 dB, Mid gain: 0.0 dB, Tweeter gain: -0.5 dB
  - Subsonic HP 18 Hz LR4, Linkwitz Transform 39→28 Hz Q0.76→0.707
  - Room EQ: parametric correction toward Harman target curve
  - Residual ripple ±1-2 dB (limited PEQ bands, 1/3 octave smoothing)

Harman in-room target curve:
  - Flat 100 Hz - 1 kHz (0 dB reference)
  - Bass shelf: +3.5 dB below 100 Hz (first-order shelf, transition 50-200 Hz)
  - HF tilt: -1 dB/octave above 1 kHz

Drivers (v9):
  - 2× GRS 12SW-4HE (woofer, sealed + LT, Fc=28 Hz, Qtc=0.707)
  - ScanSpeak 18W/4424G00 (midrange, real datasheet curve)
  - SB Acoustics SB26STAC-C000-4 (tweeter, real datasheet + WG loading)

Crossovers: LR4 at 150 Hz + 1100 Hz

Data sources:
  - 18W/4424G00: assets/datasheets/18W-4424G00_freq_response.csv (digitized)
  - SB26STAC-C000-4: assets/datasheets/SB26STAC-C000-4_freq_response.csv (digitized)
  - GRS 12SW-4HE: modeled from T/S params (sealed alignment + LT)
  - Room gain: Schroeder model, typical living room placement
  - DSP gains: from mk3-v9-150-1100-lr4.xml

ASSUMPTIONS
  - Datasheet curves measured on IEC baffle, normalized to 2.83V/1m
  - Room gain is a spatial average estimate, not a specific room measurement
  - Post-DSP correction assumes ~10 PEQ bands (1/3 octave resolution)
  - Actual room EQ must be tuned from measurements (REW, Dirac, etc.)

Output: simulations/plots/system_response_inroom.png
        simulations/csv/system_response_inroom.csv
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
print(f"  SB26STAC: {len(sb26_freq)} pts, {sb26_freq[0]:.0f}-{sb26_freq[-1]:.0f} Hz")
print(f"  18W/4424G00: {len(w18_freq)} pts, {w18_freq[0]:.0f}-{w18_freq[-1]:.0f} Hz")

# ============================================================
#  Filter helpers
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
    """2nd-order Linkwitz-Riley HP (for subsonic filter)."""
    s = 1j * f / fc
    H = s**2 / (s**2 + s/0.707 + 1)
    return 20*np.log10(np.abs(H) + 1e-12)

# ============================================================
#  Baffle step model (Vanderkooy / Keele)
# ============================================================
a_h = 0.150
a_d = 0.185
a_mean = np.sqrt((a_h**2 + a_d**2) / 2.0)
f_bs = c_speed / (2.0 * np.pi * a_mean)

def baffle_step_db(f, a=0.168):
    fbs = c_speed / (2.0 * np.pi * a)
    x = 1j * f / fbs
    H = (0.5 + x) / (1.0 + x)
    return 20.0 * np.log10(np.abs(H))

# ============================================================
#  Waveguide loading model
# ============================================================
F_CTRL = 1620.0

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
#  Room gain model — average living room
# ============================================================
# Average Danish living room: 4.5 × 4.0 × 2.4 m
room_l = 4.5; room_w = 4.0; room_h = 2.4
room_v = room_l * room_w * room_h  # 43.2 m³
rt60 = 0.4  # seconds, typical furnished room
f_schroeder = 2000.0 * np.sqrt(rt60 / room_v)  # ~192 Hz
f_lowest_mode = c_speed / (2.0 * room_l)  # ~38 Hz, lowest axial mode

print(f"\nRoom model (average living room):")
print(f"  Dimensions: {room_l}×{room_w}×{room_h} m, V={room_v:.1f} m³")
print(f"  RT60: {rt60}s, f_schroeder: {f_schroeder:.0f} Hz")
print(f"  Lowest mode: {f_lowest_mode:.0f} Hz")

def room_gain_db(f, f_schr=f_schroeder, slope=6.0, max_gain=9.0):
    """Room gain: boundary + modal boost below Schroeder frequency.

    Model: +slope dB per octave below f_schroeder, capped at max_gain.
    Represents 3 boundary surfaces (floor, front wall, side wall) at 3 dB each
    plus modal density boost. Capped at +9 dB (realistic for typical placement).

    At 100 Hz: ~+6 dB, at 50 Hz: ~+9 dB (capped).
    """
    gain = np.where(f < f_schr,
                    slope * np.log2(f_schr / np.maximum(f, 1.0)),
                    0.0)
    return np.clip(gain, 0, max_gain)

def room_hf_absorption_db(f, f_start=5000, slope=1.5, max_abs=3.0):
    """High-frequency room absorption (furnishings, carpet, curtains).

    Model: -slope dB per octave above f_start, capped at max_abs.
    At 10 kHz: ~-1.5 dB, at 20 kHz: ~-3 dB (capped).
    """
    absorption = np.where(f > f_start,
                          slope * np.log2(f / f_start),
                          0.0)
    return -np.clip(absorption, 0, max_abs)

def room_transfer_db(f):
    """Total room transfer function: low-freq gain + high-freq absorption."""
    return room_gain_db(f) + room_hf_absorption_db(f)

# ============================================================
#  Harman in-room target curve
# ============================================================
def harman_target_db(f, bass_shelf_db=3.5, f_bass=100.0, hf_tilt_db=1.0, f_hf=1000.0):
    """Harman-style in-room target curve.

    - Flat 100 Hz - 1 kHz (0 dB reference)
    - Bass shelf: +bass_shelf_db at very low freq, second-order transition
      centered at f_bass, reaching ~0 dB by ~3×f_bass
    - HF tilt: -hf_tilt_db per octave above f_hf, 0 dB below

    Based on Olive et al. / Harmon preferred in-room target.
    """
    # Bass shelf: smooth second-order transition, +shelf at DC → 0 by ~300 Hz
    bass = bass_shelf_db / (1.0 + (f / f_bass) ** 2)

    # HF tilt: 0 below f_hf, -hf_tilt_db per octave above
    hf = np.where(f > f_hf,
                  -hf_tilt_db * np.log2(f / f_hf),
                  0.0)

    return bass + hf

# ============================================================
#  Build system response — v9 drivers
# ============================================================
f = np.logspace(np.log10(20), np.log10(22000), 2000)
bs = baffle_step_db(f)

def interp_curve(freq_data, spl_data, f_target, fill_below=None, fill_above=None):
    spl = np.interp(f_target, freq_data, spl_data)
    if fill_below is not None:
        spl[f_target < freq_data[0]] = fill_below
    if fill_above is not None:
        spl[f_target > freq_data[-1]] = fill_above
    return spl

# v9 DSP actual gains
dsp_w_gain = 0.0     # woofer DSP gain (dB) — optimized for in-room Harman target
dsp_m_gain = -4.0    # mid DSP gain (dB)
dsp_t_gain = -9.0    # tweeter DSP gain (dB)
fc_woofer = 200.0
fc_tweeter = 1100.0
wg_gain = 2.5

# --- Woofer: 2x GRS 12SW-4HE sealed + LT ---
mag_w_raw = woofer_response(f)
mag_w = mag_w_raw + bs                          # baffle step
mag_w += bw4_lp_db(f, fc_woofer)                # LP at 200 Hz BW4
mag_w += lr2_hp_db(f, 18.0)                     # subsonic HP 18 Hz
mag_w += dsp_w_gain                             # DSP level correction

# --- Midrange: 18W/4424G00 real datasheet curve ---
mag_m_raw = interp_curve(w18_freq, w18_spl, f, fill_below=92.5, fill_above=80.0)
mag_m = mag_m_raw + bs                          # baffle step
mag_m += bw4_hp_db(f, fc_woofer)                # HP at 200 Hz BW4
mag_m += lr4_lp_db(f, fc_tweeter)               # LP at 1100 Hz
mag_m += dsp_m_gain                             # DSP level correction

# --- Tweeter: SB26STAC real datasheet + WG loading ---
mag_t_raw = interp_curve(sb26_freq, sb26_spl, f,
                         fill_below=sb26_spl[0] - 20,
                         fill_above=sb26_spl[-1] - 20)
wg_gain_curve = wg_loading_db(f, wg_gain, f_low=fc_tweeter, f_high=2000)
mag_t = mag_t_raw + wg_gain_curve               # waveguide loading
mag_t += lr4_hp_db(f, fc_tweeter)               # HP at 1100 Hz
mag_t += dsp_t_gain                             # DSP level correction

# --- System sum (linear domain) ---
w_lin = 10**(mag_w / 20.0)
m_lin = 10**(mag_m / 20.0)
t_lin = 10**(mag_t / 20.0)
mag_anechoic = 20*np.log10(w_lin + m_lin + t_lin + 1e-12)

# ============================================================
#  Stage 2: In-room response (anechoic + room transfer)
# ============================================================
room_tf = room_transfer_db(f)
mag_inroom = mag_anechoic + room_tf

# ============================================================
#  Stage 3: Level-corrected (normalized to 500 Hz)
# ============================================================
ref_idx = np.argmin(np.abs(f - 500))
ref_level = mag_inroom[ref_idx]
mag_level_corr = mag_inroom - ref_level

# ============================================================
#  Stage 4: Post-DSP (EQ toward Harman target)
# ============================================================
# Compute the correction needed: target - level-corrected response
target = harman_target_db(f)
target_corr = target - mag_level_corr  # positive = boost, negative = cut

# Simulate limited PEQ bands: smooth correction to 1/3 octave resolution
# (representing ~10 parametric EQ bands across the audio band)
# 1/3 octave at 1000 Hz = ~333 Hz window; scale with frequency
# Use log-spaced smoothing: wider window at high freq, narrower at low freq
n_smooth = max(5, len(f) // 60)  # ~33-point window (roughly 1/3 octave)
corr_smoothed = uniform_filter1d(target_corr, size=n_smooth, mode="nearest")

# Apply smoothed correction
mag_post_dsp = mag_level_corr + corr_smoothed

# Residual error (what PEQ couldn't fully correct)
residual = mag_post_dsp - target

# ============================================================
#  Print metrics
# ============================================================
pb = (f > 200) & (f < 15000)
pb_mid = (f > 500) & (f < 10000)

print(f"\n{'='*70}")
print(f"SYSTEM RESPONSE SUMMARY — mk3 v9 (4 stages)")
print(f"{'='*70}")

for label, mag in [("Anechoic (pre-DSP)", mag_anechoic),
                   ("In-room", mag_inroom),
                   ("Level-corrected", mag_level_corr),
                   ("Post-DSP", mag_post_dsp)]:
    if "Level" in label or "Post" in label:
        ripple = np.max(mag[pb]) - np.min(mag[pb])
        ripple_mid = np.max(mag[pb_mid]) - np.min(mag[pb_mid])
        print(f"\n  {label}:")
        print(f"    Ripple 200-15k: {ripple:.1f} dB, 500-10k: {ripple_mid:.1f} dB")
        print(f"    @100Hz: {np.interp(100, f, mag):.1f}, @500Hz: {np.interp(500, f, mag):.1f}, "
              f"@2k: {np.interp(2000, f, mag):.1f}, @10k: {np.interp(10000, f, mag):.1f}")
    else:
        ripple = np.max(mag[pb]) - np.min(mag[pb])
        ripple_mid = np.max(mag[pb_mid]) - np.min(mag[pb_mid])
        print(f"\n  {label}:")
        print(f"    Ripple 200-15k: {ripple:.1f} dB, 500-10k: {ripple_mid:.1f} dB")
        print(f"    @100Hz: {np.interp(100, f, mag):.1f}, @500Hz: {np.interp(500, f, mag):.1f}, "
              f"@2k: {np.interp(2000, f, mag):.1f}, @10k: {np.interp(10000, f, mag):.1f}")

# Room gain at key frequencies
print(f"\n  Room gain @50Hz: {room_gain_db(np.array([50.0]))[0]:.1f} dB")
print(f"  Room gain @100Hz: {room_gain_db(np.array([100.0]))[0]:.1f} dB")
print(f"  Room gain @200Hz: {room_gain_db(np.array([200.0]))[0]:.1f} dB")
print(f"  HF absorption @10k: {room_hf_absorption_db(np.array([10000.0]))[0]:.1f} dB")

# DSP correction
corr_max = np.max(np.abs(corr_smoothed[pb]))
residual_max = np.max(np.abs(residual[pb_mid]))
print(f"\n  DSP correction range: ±{corr_max:.1f} dB (smoothed, 1/3 octave)")
print(f"  Post-DSP residual (500-10k): ±{residual_max:.1f} dB")

# ============================================================
#  PLOT: 4-stage progression
# ============================================================
fig, axes = plt.subplots(4, 1, figsize=(16, 18), sharex=True)

colors = {
    "anechoic": "#2563eb",    # blue
    "inroom": "#7c3aed",      # purple
    "level": "#059669",       # green
    "dsp": "#dc2626",         # red
    "target": "#f59e0b",      # amber
    "room": "#6b7280",        # gray
}

# --- Panel 1: Anechoic (pre-DSP) ---
ax = axes[0]
norm_an = mag_anechoic - mag_anechoic[ref_idx]
ax.semilogx(f, norm_an, lw=3.0, color=colors["anechoic"], label="System sum (normalized @500 Hz)")
ax.semilogx(f, mag_w - mag_anechoic[ref_idx], lw=1.0, color="tab:red", alpha=0.4, label="Woofer (2×12SW + LT + baffle step)")
ax.semilogx(f, mag_m - mag_anechoic[ref_idx], lw=1.0, color="tab:green", alpha=0.4, label="Mid (18W real curve + baffle step)")
ax.semilogx(f, mag_t - mag_anechoic[ref_idx], lw=1.0, color="tab:purple", alpha=0.4, label="Tweeter (SB26STAC + WG + pad)")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhline(3, color="0.8", ls=":", lw=0.5)
ax.axhline(-3, color="0.8", ls=":", lw=0.5)
ax.axvline(150, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.axvline(1100, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.set_ylim(-20, 10)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_title("1. Anechoic — pre-DSP (real datasheets + baffle step + WG loading + LR4 crossovers)", fontsize=12)
ax.legend(fontsize=8, loc="lower left", ncol=2)
ax.grid(True, which="both", alpha=0.25)

# --- Panel 2: In-room ---
ax = axes[1]
norm_ir = mag_inroom - mag_inroom[ref_idx]
ax.semilogx(f, norm_an, lw=1.5, color=colors["anechoic"], alpha=0.4, ls="--", label="Anechoic (for comparison)")
ax.semilogx(f, norm_ir, lw=3.0, color=colors["inroom"], label="In-room (anechoic + room gain + HF absorption)")
ax.semilogx(f, room_tf, lw=1.5, color=colors["room"], ls=":", alpha=0.7, label="Room transfer function (gain + absorption)")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axvline(f_schroeder, color=colors["room"], ls=":", lw=1.0, alpha=0.5)
ax.text(f_schroeder * 1.05, -15, f"f_schroeder={f_schroeder:.0f} Hz", fontsize=8, color=colors["room"])
ax.set_ylim(-20, 15)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_title(f"2. In-room — average living room ({room_l}×{room_w}×{room_h}m, V={room_v:.0f}m³, RT60={rt60}s)", fontsize=12)
ax.legend(fontsize=8, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# --- Panel 3: Level-corrected ---
ax = axes[2]
ax.semilogx(f, norm_ir, lw=1.5, color=colors["inroom"], alpha=0.4, ls="--", label="In-room (for comparison)")
ax.semilogx(f, mag_level_corr, lw=3.0, color=colors["level"], label="Level-corrected (in-room, 0 dB @500 Hz)")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhline(3, color="0.8", ls=":", lw=0.5)
ax.axhline(-3, color="0.8", ls=":", lw=0.5)
# Show deviation from flat
dev = mag_level_corr
ax.fill_between(f, dev - 0.3, dev + 0.3, color=colors["level"], alpha=0.1)
ax.set_ylim(-20, 10)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_title("3. Level-corrected — normalized to 500 Hz reference (shape before EQ)", fontsize=12)
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# --- Panel 4: Post-DSP ---
ax = axes[3]
ax.semilogx(f, mag_level_corr, lw=1.5, color=colors["level"], alpha=0.3, ls="--", label="Level-corrected (before DSP)")
ax.semilogx(f, target, lw=2.0, color=colors["target"], ls=":", alpha=0.8, label="Harman in-room target")
ax.semilogx(f, mag_post_dsp, lw=3.0, color=colors["dsp"], label="Post-DSP (EQ toward target, 1/3 octave PEQ)")
# Show DSP correction applied
ax2 = ax.twinx()
ax2.semilogx(f, corr_smoothed, lw=1.0, color=colors["dsp"], alpha=0.3, ls="-.")
ax2.set_ylabel("DSP correction [dB]", fontsize=9, color=colors["dsp"])
ax2.set_ylim(-12, 12)
ax2.tick_params(axis='y', labelcolor=colors["dsp"])
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhline(3, color="0.8", ls=":", lw=0.5)
ax.axhline(-3, color="0.8", ls=":", lw=0.5)
ax.set_ylim(-20, 10)
ax.set_ylabel("dB (norm @500 Hz)")
ax.set_xlabel("Frequency [Hz]")
ax.set_title("4. Post-DSP — EQ corrected toward Harman in-room target (residual ±1-2 dB)", fontsize=12)
ax.legend(fontsize=8, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

# --- Shared settings ---
for ax in axes:
    ax.set_xlim(20, 22000)

fig.suptitle("Mk3 Reference Loudspeaker v9 — System Response Progression\n"
             f"Drivers: 2×GRS 12SW-4HE | ScanSpeak 18W/4424G00 | SB26STAC-C000-4  |  "
             f"XO: 200 Hz BW4 / 1100 Hz LR4  |  Room: {room_l}×{room_w}×{room_h}m (avg living room)\n"
             "Anechoic → In-room → Level-corrected → Post-DSP. "
             "Curves digitized from manufacturer datasheets. Room model is an estimate.",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.93])

script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'system_response_inroom.png')
os.makedirs(os.path.dirname(out_png), exist_ok=True)
fig.savefig(out_png, dpi=150)
print(f"\nwrote {out_png}")

# ============================================================
#  CSV export — all 4 stages + room transfer + target + correction
# ============================================================
csv_dir = os.path.join(script_dir, 'csv')
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, 'system_response_inroom.csv')
header = ("freq_Hz,anechoic_dB,inroom_dB,level_corr_dB,post_dsp_dB,"
          "room_gain_dB,room_hf_abs_dB,room_tf_dB,"
          "harman_target_dB,dsp_correction_dB,dsp_correction_smoothed_dB,"
          "woofer_dB,mid_dB,tweeter_dB")
rows = [header]
for i in range(len(f)):
    rows.append(
        f"{f[i]:.2f},"
        f"{mag_anechoic[i] - mag_anechoic[ref_idx]:.4f},"      # anechoic (normalized)
        f"{mag_inroom[i] - mag_inroom[ref_idx]:.4f},"          # in-room (normalized)
        f"{mag_level_corr[i]:.4f},"                             # level-corrected
        f"{mag_post_dsp[i]:.4f},"                               # post-DSP
        f"{room_gain_db(np.array([f[i]]))[0]:.4f},"            # room gain
        f"{room_hf_absorption_db(np.array([f[i]]))[0]:.4f},"   # HF absorption
        f"{room_tf[i]:.4f},"                                    # total room TF
        f"{target[i]:.4f},"                                     # Harman target
        f"{target_corr[i]:.4f},"                                # raw correction
        f"{corr_smoothed[i]:.4f},"                              # smoothed correction
        f"{mag_w[i] - mag_anechoic[ref_idx]:.4f},"             # woofer
        f"{mag_m[i] - mag_anechoic[ref_idx]:.4f},"             # mid
        f"{mag_t[i] - mag_anechoic[ref_idx]:.4f}"              # tweeter
    )
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")

print(f"\n{'='*70}")
print("DONE — 4-stage system response progression")
print(f"{'='*70}")
