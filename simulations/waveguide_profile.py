"""
Mk3 Reference Loudspeaker - WG212 mouth-to-baffle termination study
===================================================================

Why: the waveguide termination at the baffle matters for diffraction.
The current waveguide model (cad/waveguide.scad) seats the flange *behind*
the flush mouth plane — the bore rolls to a flush tangent at z = D_tot
with no forward lip.

This script draws the waveguide wall in the r-z plane (horizontal plane,
theta_h) comparing three approaches:
  (a) OLD LIP  : forward straight lip (sharp 90 deg edge at the baffle)
  (b) FLUSH    : flush mouth plane, flange behind (CURRENT design)
  (c) BLENDED  : larger roll (Lr=26) for continuous baffle curvature

NOTE: Lr was increased from 10 to 25 on Joachim's request (commit d807ab0)
to match the H2606 waveguide depth and improve baffle blend. The Python
values are now synced to the SCAD source-of-truth.

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

# --- geometry from cad/waveguide.scad (horizontal plane) ---
r_t       = 28/2.0
theta     = 50.0           # theta_h [deg]
D_os      = 65.0
Lr        = 25.0           # current roundover forward depth
flange_t  = 5.0           # SCAD: flange_thick (cad/waveguide.scad)
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
        lw=2.6, label="(a) old lip: forward lip -> sharp edge")
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
        "(a) shows the old design with a forward lip and sharp edge at the baffle.\n"
        "The current design (b, flush) seats the flange behind the mouth plane.\n"
        "Option (c, blended) uses a larger roll (Lr=26) for continuous curvature.",
        fontsize=8.5, color="0.3")

out = os.path.join(os.path.dirname(__file__), "plots", "waveguide_termination.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.tight_layout(); fig.savefig(out, dpi=135)
print(f"a0={a0:.1f} deg  mouth_r={mouth_r:.1f} mm  (horizontal)")
print("wrote", out)
