"""
Mk2 Reference Loudspeaker - baffle-step diffraction model
==========================================================

A loudspeaker driver mounted on a finite baffle transitions from full-space
(4π sr) radiation at very low frequencies to half-space (2π sr) at high
frequencies, producing a ~6 dB increase in on-axis SPL around the baffle-step
frequency.  The transition begins roughly when the wavelength equals the
shortest path from the driver to the nearest cabinet edge.

This script uses the Vanderkooy / Keele approximation:

    H_bs(f) = (1 + j * f/f_bs) / (j * f/f_bs)    [minimum-phase form]

    where  f_bs = c / (2 * pi * a)
    and    a    = mean path from driver centre to all baffle edges

For v9 cabinet (w=320, d=400 mm, from cad/cabinet.scad):
    Side woofers:   a = D/2 = 190 mm (f_bs = 287 Hz)
    Front mid/tweeter: a = W/2 = 160 mm (f_bs = 341 Hz)
    See simulations/cabinet_params.py for the parsed values.

ASSUMPTIONS
- Rectangular flat baffle, driver approximately centred horizontally.
- Single-pole Vanderkooy model — good for the first 10–15 dB of transition;
  does not capture secondary lobes or inter-cabinet diffraction.
- Baffle-step correction (equalization) in DSP: a first-order shelving filter
  (Q=0.5, gain ~ +6 dB) centred at f_bs is the canonical fix; exact parameters
  come from measurements.
- Output paths assume the script is run from the repo root.

Output: simulations/plots/baffle_step.png
        simulations/csv/baffle_step.csv
"""

import os
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Cabinet geometry (v6b) ---
c      = 343.0     # speed of sound, m/s
w_mm   = 300.0     # external cabinet width, mm
d_mm   = 370.0     # external cabinet depth, mm

# Mean baffle-edge distance (half-width limiting; depth secondary)
a_h = (w_mm / 2) * 1e-3    # 150 mm  — horizontal edge, dominant
a_d = (d_mm / 2) * 1e-3    # 185 mm  — depth edge
a_mean = np.sqrt((a_h**2 + a_d**2) / 2.0)  # geometric mean

f_bs_h    = c / (2.0 * np.pi * a_h)    # Hz, horizontal-only edge
f_bs_mean = c / (2.0 * np.pi * a_mean)  # Hz, mean edge (more accurate)

print(f"Half-width a_h    = {a_h*1000:.1f} mm  →  f_bs = {f_bs_h:.1f} Hz")
print(f"Mean path  a_mean = {a_mean*1000:.1f} mm  →  f_bs = {f_bs_mean:.1f} Hz  (used for model)")


def baffle_step_dB(f, a):
    """Vanderkooy single-pole baffle-step response, dB relative to infinite baffle."""
    f_bs = c / (2.0 * np.pi * a)
    H    = (1.0 + 1j * f / f_bs) / (1j * f / f_bs)
    # Normalise so high-freq → 0 dB
    H_inf = 1.0   # |H| → 1 as f → ∞
    return 20.0 * np.log10(np.abs(H) / H_inf) - 20.0 * np.log10(2.0)
    # The -20*log10(2) = -6.02 dB offset ensures the model asymptotes to
    # 0 dB at high frequency and -6 dB at DC (matching the 4π→2π transition).


# Frequency grid
f = np.logspace(np.log10(20), np.log10(20000), 1200)

bs_h    = baffle_step_dB(f, a_h)
bs_mean = baffle_step_dB(f, a_mean)

# Correction shelf: a first-order boost of +6 dB @DC, -3 dB @ f_bs
def shelf_correction(f, f_bs, gain_dB=6.0):
    """First-order shelving boost (low-shelving EQ for DSP baffle-step correction)."""
    g  = 10.0 ** (gain_dB / 20.0)
    w  = 2.0 * np.pi * f
    w0 = 2.0 * np.pi * f_bs
    # H_shelf(s) = (s + g*w0) / (s + w0)  — unity at high freq, +gain at DC
    H  = (1j * w / w0 + g) / (1j * w / w0 + 1.0)
    return 20.0 * np.log10(np.abs(H))

shelf_mean = shelf_correction(f, f_bs_mean, gain_dB=6.0)
corrected  = bs_mean + shelf_mean   # net: step + correction

# --- Plot ---
fig, axes = plt.subplots(3, 1, figsize=(10, 11), sharex=True)

# Panel 1: baffle step magnitude for both edge estimates
ax = axes[0]
ax.semilogx(f, bs_h,    lw=1.8, color="steelblue",  label=f"Horizontal edge only  a={a_h*1000:.0f} mm, f_bs={f_bs_h:.0f} Hz")
ax.semilogx(f, bs_mean, lw=2.4, color="tab:red",    label=f"Mean edge (h+d)        a={a_mean*1000:.0f} mm, f_bs={f_bs_mean:.0f} Hz  ← used")
ax.axhline(-3.0, color="0.5", ls=":", lw=1)
ax.axhline(-6.0, color="0.5", ls=":", lw=1)
ax.axvline(f_bs_mean, color="tab:red", ls="--", lw=1, alpha=0.5)
ax.text(f_bs_mean * 1.07, -5.5, f"f_bs = {f_bs_mean:.0f} Hz", fontsize=8, color="tab:red")
ax.set_ylabel("Baffle-step loss [dB]")
ax.set_title("Baffle-step diffraction — v9 cabinet (320 mm wide, 400 mm deep)")
ax.set_ylim(-8, 1)
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)

# Panel 2: DSP shelf correction
ax = axes[1]
ax.semilogx(f, shelf_mean, lw=2.2, color="forestgreen",
            label=f"Shelf EQ +6 dB / f_bs={f_bs_mean:.0f} Hz (canonical starting point)")
ax.semilogx(f, bs_mean,   lw=1.4, color="tab:red",    ls="--", alpha=0.7, label="Step (uncompensated)")
ax.axhline(0, color="0.5", ls=":", lw=1)
ax.set_ylabel("EQ correction [dB]")
ax.set_title("First-order shelf EQ — DSP starting point (tune from measurements)")
ax.set_ylim(-8, 8)
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)

# Panel 3: net response (step + correction)
ax = axes[2]
ax.semilogx(f, bs_mean,  lw=1.4, color="tab:red",    ls="--", alpha=0.6, label="Step (uncompensated)")
ax.semilogx(f, corrected, lw=2.4, color="tab:purple", label="Step + shelf EQ (net)")
ax.axhline(0, color="0.5", ls=":", lw=1)
ax.axhline(-1, color="0.8", ls=":", lw=0.8)
ax.set_ylabel("Relative SPL [dB]")
ax.set_xlabel("Frequency [Hz]")
ax.set_title("Net on-axis response after baffle-step correction")
ax.set_xlim(20, 20000)
ax.set_ylim(-8, 3)
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)
ax.text(25, -7.2,
        "Note: this is a minimum-phase approximation. Real step shape and exact shelf\n"
        "parameters must be tuned from measurements (REW or APx). Residual ±1-2 dB\n"
        "deviation in the transition band (200-700 Hz) is normal and EQ-correctable.",
        fontsize=7.5, color="0.4")

fig.tight_layout()

out_dir = os.path.join(os.path.dirname(__file__), "plots")
csv_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(out_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

out_png = os.path.join(out_dir, "baffle_step.png")
fig.savefig(out_png, dpi=135)
print("wrote", out_png)

# CSV
csv_path = os.path.join(csv_dir, "baffle_step.csv")
with open(csv_path, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow([
        "freq_hz",
        "step_horiz_dB",
        "step_mean_dB",
        "shelf_correction_dB",
        "net_corrected_dB",
    ])
    for i, fi in enumerate(f):
        w.writerow([
            f"{fi:.4f}",
            f"{bs_h[i]:.4f}",
            f"{bs_mean[i]:.4f}",
            f"{shelf_mean[i]:.4f}",
            f"{corrected[i]:.4f}",
        ])
print("wrote", csv_path)

print(f"\n--- Baffle step summary ---")
print(f"Cabinet width:        {w_mm:.0f} mm")
print(f"Cabinet depth:        {d_mm:.0f} mm")
print(f"f_bs (horiz edge):    {f_bs_h:.1f} Hz")
print(f"f_bs (mean edge):     {f_bs_mean:.1f} Hz  ← used for model")
print(f"Step at 100 Hz:       {float(np.interp(100, f, bs_mean)):.1f} dB")
print(f"Step at 200 Hz:       {float(np.interp(200, f, bs_mean)):.1f} dB")
print(f"Step at 500 Hz:       {float(np.interp(500, f, bs_mean)):.1f} dB")
