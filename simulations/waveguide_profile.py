"""
Mk2 Reference Loudspeaker - WG212 mouth-to-baffle termination study
===================================================================

Why: the current waveguide model (cad/mk2_waveguide_os.scad) rolls the bore to a
flush tangent at z = D_tot, but then adds the mounting flange *forward* of that
plane and cuts the mouth as a straight prism through it. The last `flange_thick`
mm are therefore a straight, axial "lip" that ends in a sharp 90 deg edge at the
baffle surface -> mouth diffraction, audible as off-axis / spinorama ripple.

This script draws the waveguide wall in the r-z plane (horizontal plane,
theta_h) for:
  (a) CURRENT   : OS + roll + forward straight lip (sharp edge at the baffle)
  (b) FLUSH     : same roll, flange moved *behind* the mouth plane -> no lip
  (c) BLENDED   : flush + a baffle roundover (secondary radius) that lets the
                  mouth flow into the flat baffle with continuous curvature.

ASSUMPTIONS: purely geometric (matches the OpenSCAD profile math). Diffraction
severity is argued qualitatively; the real proof is a measurement of the printed
part. Numbers are estimates, not measured.

Output: simulations/plots/waveguide_termination.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- geometry from cad/mk2_waveguide_os.scad (horizontal plane) ---
r_t       = 28/2.0
theta     = 50.0           # theta_h [deg]
D_os      = 65.0
Lr        = 10.0           # current roundover forward depth
flange_t  = 9.0
flange_hw = 252/2.0        # flange half-width (horizontal)

tan, sin, cos = (lambda d: np.tan(np.radians(d)),
                 lambda d: np.sin(np.radians(d)),
                 lambda d: np.cos(np.radians(d)))

r_e = np.sqrt(r_t**2 + (D_os*tan(theta))**2)
a0  = np.degrees(np.arctan(D_os*tan(theta)**2 / r_e))      # wall angle at OS end

def roll(z, Lroll):
    Rroll = Lroll / (1 - sin(a0))
    return r_e + Rroll*(cos(a0) - np.cos(np.arcsin(sin(a0) + (z - D_os)/Rroll)))

# OS section
z_os = np.linspace(0, D_os, 200)
r_os = np.sqrt(r_t**2 + (z_os*tan(theta))**2)

# roll section (current Lr)
D_tot = D_os + Lr
z_roll = np.linspace(D_os, D_tot, 80)
r_roll = roll(z_roll, Lr)
mouth_r = roll(D_tot, Lr)

fig, ax = plt.subplots(figsize=(10, 6.2))

# ---- (a) CURRENT: roll then forward straight lip + flat flange face ----
ax.plot(np.r_[z_os, z_roll], np.r_[r_os, r_roll], color="tab:red", lw=2.6)
ax.plot([D_tot, D_tot+flange_t], [mouth_r, mouth_r], color="tab:red", lw=2.6)      # axial lip
ax.plot([D_tot+flange_t, D_tot+flange_t], [mouth_r, flange_hw], color="tab:red",
        lw=2.6, label="(a) current: forward lip -> sharp edge")
ax.scatter([D_tot+flange_t], [mouth_r], color="tab:red", zorder=6, s=55)
ax.annotate("sharp 90 deg edge\nat the baffle", (D_tot+flange_t, mouth_r),
            xytext=(D_tot+flange_t+9, mouth_r-26), color="tab:red", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="tab:red"))

# ---- (b) FLUSH: flange behind, roll reaches flush at the baffle plane ----
baffle_z = D_tot
ax.plot([baffle_z, baffle_z], [mouth_r, flange_hw], color="tab:green", lw=2.0,
        ls="--", label="(b) flush: flange behind, no lip")

# ---- (c) BLENDED: a larger termination radius into the baffle ----
Lr2 = 26.0
z_roll2 = np.linspace(D_os, D_os+Lr2, 120)
r_roll2 = roll(z_roll2, Lr2)
ax.plot(z_roll2, r_roll2, color="tab:blue", lw=2.2, label="(c) blended: larger roll -> tangent baffle")
mb = roll(D_os+Lr2, Lr2)
ax.plot([D_os+Lr2, D_os+Lr2], [mb, flange_hw], color="tab:blue", lw=1.4, ls=":")

ax.axhline(mouth_r, color="0.8", lw=0.8)
ax.text(2, mouth_r+2, "mouth radius (horizontal)", color="0.5", fontsize=8)
ax.set_xlabel("depth z  [mm]  (throat at 0, baffle at right)")
ax.set_ylabel("wall radius r  [mm]")
ax.set_title("WG212 mouth-to-baffle termination (horizontal plane)")
ax.set_xlim(0, D_tot+flange_t+22); ax.set_ylim(0, flange_hw+6)
ax.grid(True, alpha=0.25); ax.legend(loc="lower right", fontsize=9)
ax.text(2, 6,
        "The current lip protrudes forward of the flush plane and ends in a sharp edge\n"
        "at the baffle. Moving the flange behind the mouth plane (b), or rolling into a\n"
        "baffle blend (c), removes the edge and the diffraction it causes.",
        fontsize=8.5, color="0.3")

out = os.path.join(os.path.dirname(__file__), "plots", "waveguide_termination.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.tight_layout(); fig.savefig(out, dpi=135)
print(f"a0={a0:.1f} deg  mouth_r={mouth_r:.1f} mm  (horizontal)")
print("wrote", out)
