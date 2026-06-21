"""
Mk2 Reference Loudspeaker - estimated system on-axis frequency response
========================================================================

Combines the simplified driver response models with the LR4 crossover
filters to show a full-bandwidth on-axis estimate from 20 Hz to 20 kHz.

ASSUMPTIONS (simplified physics, NOT measured data)
- 2x GRS 8SW-4HE-8 in sealed ~69 L: Qtc 0.62, Fc 34.5 Hz, sensitivity 85 dB/W/m
  (two drivers in phase + 3 dB, half-space + 3 dB, but sealed losses and 4 ohm
  wiring mean the nominal sensitivity stays close to 85 dB).  The model uses
  a standard 2nd-order sealed high-pass with Fc = 34.5 Hz and Q = 0.62.
- 15W/4434G00 midrange: flat to 150 Hz cutoff, sensitvity 89.7 dB/W/m.
  No cone breakup modelled (piston model valid ~to 2 kHz, crossing at 1250 Hz).
- H2606/920000 in WG212: sensitivity ~95 dB above ~2 kHz, roll-in from Fs=1030 Hz
  to 2 kHz approximated by a smooth high-pass step.  Waveguide loading above
  control limit (~1620 Hz) is modelled as a slight flat boost (directivity gain).
- Baffle step not modelled (it interacts with the crossover and is handled by
  the final DSP target curve, not the driver model).
- Room gain below ~80 Hz not included — this is an anechoic estimate.
- A flat 0 dB reference means the curves are relative to the woofer pair SPL
  at the 150 Hz crossover point; the tweeter is ~7 dB hotter and is shown
  raw, then with a level-match trim to show the system sum shape.

Output: simulations/plots/system_response.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
#  Shared filter helper
# ---------------------------------------------------------------------------
def hp2(f, fc, q):
    """2nd-order high-pass: magnitude [dB]"""
    s2 = (f / fc) ** 2
    return 20*np.log10(s2 / np.sqrt((1 - s2)**2 + (f / (fc * q))**2))

def lp2(f, fc, q):
    """2nd-order low-pass: magnitude [dB]"""
    s2 = (f / fc) ** 2
    return 20*np.log10(1.0 / np.sqrt((1 - s2)**2 + (f / (fc * q))**2))

def lr4_lp(f, fc):
    """LR4 low-pass: two cascaded Butterworth Q=0.707"""
    H = lp2(f, fc, 0.707) / 2.0   # lp2 returns 2nd order; do twice
    # redo properly: two 2nd order stages in complex domain
    s = 1j * f / fc
    H1 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    H2 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    return 20*np.log10(np.abs(H1 * H2))

def lr4_hp(f, fc):
    """LR4 high-pass: two cascaded Butterworth Q=0.707"""
    s = 1j * f / fc
    H1 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    H2 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    return 20*np.log10(np.abs(H1 * H2))

# ---------------------------------------------------------------------------
#  Driver models (simplified)
# ---------------------------------------------------------------------------
f = np.logspace(np.log10(18), np.log10(22000), 1800)

# --- Woofer: sealed alignment + LR4 LP@150 ---
Fc_w = 34.5; Qtc_w = 0.62
# 2nd-order sealed high-pass response
s = 1j * f / Fc_w
H_sealed = s**2 / (s**2 + s/Qtc_w + 1)
mag_woofer = 20*np.log10(np.abs(H_sealed)) + 85.0   # sensitivity 85 dB
# LR4 low-pass at 150 Hz
mag_woofer += lr4_lp(f, 150.0)

# --- Midrange: flat piston, LR4 HP@150 + LP@1250, sens 89.7 ---
mag_mid = np.ones_like(f) * 89.7
mag_mid += lr4_hp(f, 150.0)
mag_mid += lr4_lp(f, 1250.0)

# --- Tweeter: H2606 in WG212 ---
# Sensitivity ~95 dB above WG loading, smooth roll-in from Fs=1030 Hz
# Approximate: 2nd-order HP at ~900 Hz (very rough model for Fs 1030 + baffle step)
# plus a gentle lift from ~1000 Hz to ~2000 Hz as the waveguide takes control
# then flat above 2 kHz.  This is intentionally crude — it only shows the shape.
# REAL: needs a measured FR of the driver-in-waveguide.
# Model: 1 + tanh((log10(f/1000))/0.3) gives a smooth step from ~0 to ~1 across 500-2000 Hz
step = 0.5 * (1.0 + np.tanh(np.log10(f/1000.0) / 0.30))
mag_tweeter = 95.0 + 20*np.log10(step + 1e-6)
mag_tweeter += lr4_hp(f, 1250.0)

# --- Trim level to match woofer at crossover points for sum ---
# At 150 Hz, woofer = 85 dB (flat there, LR4 -6 dB at crossover, but reference is 0)
# Actually, sum is 0 dB at crossover point for LR4.  Let's use raw relative curves.
ref = 0.0
# Relative to reference level, just show shape

# System sum (coherent, ideal drivers, no phase issues in simplified model)
w_lin = 10**(mag_woofer/20.0)
m_lin = 10**(mag_mid/20.0)
t_lin = 10**(mag_tweeter/20.0)
mag_sum = 20*np.log10(w_lin + m_lin + t_lin)

# --- Level-matched tweeter for sum ---
# Tweeter is ~7 dB hotter; add a trim to show a cleaner crossover sum
mag_tweeter_trimmed = mag_tweeter - 7.0
w_lin2 = 10**(mag_woofer/20.0)
m_lin2 = 10**(mag_mid/20.0)
t_lin2 = 10**(mag_tweeter_trimmed/20.0)
mag_sum_trimmed = 20*np.log10(w_lin2 + m_lin2 + t_lin2)

# ---------------------------------------------------------------------------
#  Plotting
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6.5))

ax.semilogx(f, mag_woofer, lw=2.0, color="tab:red", alpha=0.7, label="Woofer (2x GRS) – sealed + LR4 LP@150 Hz")
ax.semilogx(f, mag_mid, lw=2.0, color="tab:green", alpha=0.7, label="Midrange (15W) – LR4 HP@150 + LP@1250")
ax.semilogx(f, mag_tweeter, lw=2.0, color="tab:blue", alpha=0.7, label="Tweeter (H2606) – roll-in + LR4 HP@1250")
ax.semilogx(f, mag_tweeter_trimmed, lw=1.6, color="tab:blue", ls=":", alpha=0.5, label="Tweeter – level-matched -7 dB")
ax.semilogx(f, mag_sum, lw=2.6, color="0.15", ls="--", alpha=0.6, label="Raw sum (tweeter +7 dB hot)")
ax.semilogx(f, mag_sum_trimmed, lw=2.8, color="0.15", label="Estimated system response (level-matched)")

ax.axhline(0, color="0.4", ls=":", lw=0.8, alpha=0.6)
ax.axhline(-3, color="0.4", ls=":", lw=0.8, alpha=0.4)
ax.axhline(-6, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.axvline(150, color="0.3", ls=":", lw=1.0, alpha=0.5)
ax.axvline(1250, color="0.3", ls=":", lw=1.0, alpha=0.5)
ax.text(150, ax.get_ylim()[1] if False else 102, "150 Hz", ha="center", fontsize=9, color="0.4")
ax.text(1250, 102, "1250 Hz", ha="center", fontsize=9, color="0.4")

ax.set_xlim(18, 22000); ax.set_ylim(65, 105)
ax.set_xlabel("Frequency [Hz]", fontsize=11); ax.set_ylabel("SPL [dB] (anechoic, 2.83 V / 1 m, half-space)", fontsize=10)
ax.set_title("Mk2 estimated system on-axis response (simplified models, not measured)", fontsize=12)
ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
ax.grid(True, which="both", alpha=0.25)

# Inset notes
ax.text(20, 67,
        "Note: Tweeter model is a crude roll-in approximation.  The real response\n"
        "requires a measurement of the H2606/920000 in the WG212 waveguide.\n"
        "Baffle step and room gain are not included.",
        fontsize=7.5, color="0.35", va="bottom",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="0.95", edgecolor="0.7", linewidth=0.5))

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "plots", "system_response.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=135)
print("wrote", out)
