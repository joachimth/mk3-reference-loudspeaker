"""
Mk2 Reference Loudspeaker - vertical lobing at the mid/tweeter crossover
=======================================================================

ASSUMPTIONS (simplified, two in-phase point sources)
- First vertical interference null for two sources separated by c-c distance d:
      theta_null(f) = arcsin( c / (2 * d * f) )   [only valid where c/(2 d f) <= 1]
  i.e. below f = c/(2d) there is no null within +-90 deg.
- This is the geometric worst case; LR4 slopes and driver roll-off reduce the real
  severity. It is meant to compare c-c / crossover options, not predict absolute level.

Conclusion it supports (see REVIEW.md C2): even c-c 160 mm crossed at 1600 Hz keeps the
first vertical null near 42 deg - far outside the +-15..30 deg listening window - so a
buildable ~160 mm c-c does NOT force a 1100 Hz crossover.

Output: simulations/plots/vertical_lobing.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c = 344.0
f = np.linspace(900, 4000, 600)

def null_angle(f, d):
    x = c / (2 * d * f)
    out = np.full_like(f, np.nan)
    ok = x <= 1.0
    out[ok] = np.degrees(np.arcsin(x[ok]))
    return out

cc_options = {"c-c 140 mm": 0.140, "c-c 160 mm": 0.160}
xovers = {"1100 Hz": 1100, "1500 Hz": 1500, "1600 Hz": 1600}

print("First vertical null angle [deg]:")
for name, d in cc_options.items():
    for xn, fx in xovers.items():
        x = c / (2 * d * fx)
        a = "no null <90" if x > 1 else f"{np.degrees(np.arcsin(x)):.0f}"
        print(f"  {name}, xover {xn}: {a}")

fig, ax = plt.subplots(figsize=(9, 5.6))
for (name, d), col in zip(cc_options.items(), ["tab:red", "tab:blue"]):
    ax.plot(f, null_angle(f, d), lw=2.2, color=col, label=name)
for xn, fx in xovers.items():
    ax.axvline(fx, color="0.6", ls=":", lw=1)
    ax.text(fx, 88, xn, rotation=90, va="top", ha="right", fontsize=7, color="0.4")
ax.axhspan(0, 15, color="tab:green", alpha=0.10)
ax.axhspan(15, 30, color="tab:orange", alpha=0.08)
ax.text(3850, 13, "+-15 deg window", ha="right", fontsize=8, color="tab:green")
ax.text(3850, 28, "+-30 deg", ha="right", fontsize=8, color="tab:orange")
ax.set_xlim(900, 4000); ax.set_ylim(0, 90)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("First vertical null angle [deg off-axis]")
ax.set_title("Vertical lobing: first null vs frequency (lower = null nearer the axis)")
ax.grid(True, alpha=0.25); ax.legend(loc="upper right", fontsize=9)
ax.text(920, 4, "Curves stay well above the listening window in the crossover region\n"
                "-> c-c ~160 mm is clean; 140 mm is not required.",
        fontsize=8, color="0.3", va="bottom")

out = os.path.join(os.path.dirname(__file__), "plots", "vertical_lobing.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.tight_layout()
fig.savefig(out, dpi=135)
print("wrote", out)
