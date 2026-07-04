"""
Mk2 Reference Loudspeaker - vertical polar map & crossover comparison
=====================================================================

2D heat-map of vertical polar SPL response vs frequency, and a direct
comparison of the first null angle across the 1100 / 1300 / 1500 Hz
crossover options for the mid/tweeter transition.

ASSUMPTIONS (simplified, NOT measured data)
- Two in-phase point sources separated by c-c distance d vertically.
- The vertical SPL pattern is |2 cos(π d/λ sin θ)| for two identical sources.
  (the first null occurs where cos(...) = 0, giving the classic lobing formula).
- LR4 crossover filters are applied to the two sources: the woofer is cut at 150 Hz
  (not relevant for the mid/tweeter vertical map), the mid is LP, the tweeter is HP.
- Crossover region: the two sources partially overlap — at the crossover frequency
  the amplitude from each is -6 dB (LR4), so the null depth is reduced compared to
  the unfiltered point-source model.  We model the sum of two LR4-weighted point
  sources at each crossover frequency to show the real null depth.
- The c-c distance used is 150 mm (the v6b design target; 140 mm is the ideal).
- 15W/4434G00 radiating diameter is ~124 mm, so 150 mm c-c is the practical
  minimum before the frames touch.  The map uses d = 150 mm.
- The vertical map is shown in the plane of the two drivers (worst-case).

Output: simulations/plots/vertical_polar_map.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
#  Two-source vertical pattern with LR4 crossover weighting
# ---------------------------------------------------------------------------
c = 344.0

def lr4_lp(f, fc):
    s = 1j * f / fc
    H1 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    H2 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    return np.abs(H1 * H2)

def lr4_hp(f, fc):
    s = 1j * f / fc
    H1 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    H2 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    return np.abs(H1 * H2)

def vertical_pattern(f, theta_deg, d, fc):
    """
    Vertical SPL (normalized) for two point sources separated by d vertically,
    with LR4 crossover at fc.  theta_deg = 0 is on-axis.
    Mid is source 0 (lower), tweeter is source 1 (upper).  Both radiate in phase.
    """
    theta = np.radians(theta_deg)
    # path difference
    delta = 2 * np.pi * f / c * d * np.sin(theta)
    # LR4 weights
    w_mid = lr4_lp(f, fc)
    w_twt = lr4_hp(f, fc)
    # Sum
    # complex amplitudes
    A_mid = w_mid * np.ones_like(theta)
    A_twt = w_twt * np.exp(1j * delta)
    sum_amp = A_mid + A_twt
    return np.abs(sum_amp)

# ---------------------------------------------------------------------------
#  Parameters
# ---------------------------------------------------------------------------
d_cc = 0.150   # 150 mm c-c
f = np.linspace(800, 4000, 600)
theta = np.linspace(-90, 90, 181)
F_mesh, TH_mesh = np.meshgrid(f, theta)

# ---------------------------------------------------------------------------
#  Build 2D maps for each crossover frequency
# ---------------------------------------------------------------------------
xovers = {"1100 Hz": 1100, "1300 Hz": 1300, "1500 Hz": 1500}
maps = {}
for name, fc in xovers.items():
    maps[name] = vertical_pattern(F_mesh, TH_mesh, d_cc, fc)
    # Normalize to on-axis (theta=0) at each frequency
    maps[name] = maps[name] / np.max(maps[name], axis=0)

# ---------------------------------------------------------------------------
#  Plotting: 2×2 map grid + null depth comparison
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(15, 10))

for idx, (name, fc) in enumerate(xovers.items()):
    ax = fig.add_subplot(2, 3, idx + 1)
    Z = 20*np.log10(maps[name])
    Z = np.clip(Z, -30, 0)
    im = ax.pcolormesh(F_mesh, TH_mesh, Z, shading="auto", cmap="inferno", vmin=-30, vmax=0)
    ax.axhline(0, color="white", lw=0.8, alpha=0.6)
    ax.axhline(15, color="tab:green", lw=0.8, alpha=0.4, ls="--")
    ax.axhline(-15, color="tab:green", lw=0.8, alpha=0.4, ls="--")
    ax.axhline(30, color="tab:orange", lw=0.8, alpha=0.3, ls="--")
    ax.axhline(-30, color="tab:orange", lw=0.8, alpha=0.3, ls="--")
    ax.axvline(fc, color="cyan", lw=1.2, alpha=0.7, ls=":")
    ax.text(fc + 30, 82, "crossover", fontsize=8, color="cyan", ha="left")
    ax.set_xlim(800, 4000); ax.set_ylim(-90, 90)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Vertical angle [deg]")
    ax.set_title(f"c-c {d_cc*1000:.0f} mm, LR4 @{name}", fontsize=10)
    ax.set_facecolor("0.1")
    cbar = plt.colorbar(im, ax=ax, shrink=0.6, label="SPL [dB]")

# --- Null depth comparison at each crossover frequency ---
ax = fig.add_subplot(2, 3, 5)
for name, fc in xovers.items():
    # evaluate null depth vs angle at the crossover frequency
    # Find the first null angle (positive)
    theta_fine = np.linspace(0.1, 90, 500)
    pattern = vertical_pattern(fc, theta_fine, d_cc, fc)
    pattern = pattern / np.max(pattern)
    # first minimum above 0 deg
    dB = 20*np.log10(pattern)
    # find local minima
    minima = np.where((dB[1:-1] < dB[:-2]) & (dB[1:-1] < dB[2:]))[0] + 1
    if len(minima) > 0:
        first_null = theta_fine[minima[0]]
        null_depth = dB[minima[0]]
    else:
        first_null = 90
        null_depth = dB[-1]
    ax.bar(name, null_depth, color="tab:orange", alpha=0.8, edgecolor="0.2")
    ax.text(name, null_depth + 0.8, f"{null_depth:.1f} dB\n@ {first_null:.0f}°", ha="center", fontsize=8, color="0.2")

ax.axhline(0, color="0.4", ls=":", lw=0.8)
ax.set_ylabel("First null depth [dB]  (deeper = worse)")
ax.set_title("Null depth at crossover frequency (c-c 150 mm)")
ax.set_ylim(-30, 5)
ax.grid(True, axis="y", alpha=0.25)

# --- On-axis sum (0°) vs frequency for each crossover ---
ax = fig.add_subplot(2, 3, 6)
for name, fc in xovers.items():
    on_axis = vertical_pattern(f, 0, d_cc, fc)
    on_axis = on_axis / np.max(on_axis)
    ax.semilogx(f, 20*np.log10(on_axis), lw=2.2, label=name)
ax.axhline(0, color="0.4", ls=":", lw=0.8, alpha=0.5)
ax.axhline(-3, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.set_xlim(800, 4000); ax.set_ylim(-6, 2)
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("On-axis SPL [dB]")
ax.set_title("On-axis sum (0°) through crossover region")
ax.legend(fontsize=8, loc="lower left")
ax.grid(True, which="both", alpha=0.25)

fig.suptitle(
    "Mk3 Reference Loudspeaker – Vertical polar map & crossover comparison (simplified 2-point-source model)",
    fontsize=13
)
fig.tight_layout(rect=[0, 0, 1, 0.96])

out = os.path.join(os.path.dirname(__file__), "plots", "vertical_polar_map.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=135)
print("wrote", out)

# ---------------------------------------------------------------------------
#  Console summary
# ---------------------------------------------------------------------------
print("\nVertical lobing summary (c-c 150 mm, LR4 crossover, first null depth):")
for name, fc in xovers.items():
    theta_fine = np.linspace(0.1, 90, 500)
    pattern = vertical_pattern(fc, theta_fine, d_cc, fc)
    pattern = pattern / np.max(pattern)
    dB = 20*np.log10(pattern)
    minima = np.where((dB[1:-1] < dB[:-2]) & (dB[1:-1] < dB[2:]))[0] + 1
    if len(minima) > 0:
        print(f"  {name}: first null @ {theta_fine[minima[0]]:.0f}°  depth = {dB[minima[0]]:.1f} dB")
    else:
        print(f"  {name}: no null found within 90° (on-axis ripple = {np.min(dB):.1f} dB)")

print("\nNote: At the crossover frequency LR4 gives -6 dB per driver, so the null")
print("      is partially filled.  A shallower null does NOT mean the crossover is")
print("      better — it means the two sources overlap more.  The real criterion is")
print("      the null position relative to the listening window (±15°).")

# ---------------------------------------------------------------------------
#  CSV export: vertical lobing data for all crossover options
# ---------------------------------------------------------------------------
csv_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, "vertical_polar_map.csv")

# theta rows, frequency columns, one table per crossover
# Write as a "long" format: crossover_Hz, freq_Hz, theta_deg, spl_dB
rows = ["crossover_Hz,freq_Hz,theta_deg,spl_norm_dB"]
for name, fc in xovers.items():
    for fi_idx, fi in enumerate(f[::4]):   # every 4th frequency for size
        fi_idx_full = fi_idx * 4
        for tj, tj_deg in enumerate(theta[::5]):   # every 5 deg
            tj_full = tj * 5
            val = 20*np.log10(maps[name][tj_full, fi_idx_full])
            rows.append(f"{fc},{fi:.2f},{tj_deg:.1f},{val:.4f}")

with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print("wrote", csv_out)
