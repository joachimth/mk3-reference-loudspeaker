"""
Mk2 Reference Loudspeaker - estimated polar response & spinorama curves
=======================================================================

Simplified model of the polar directivity pattern across the full bandwidth,
plus the derived spinorama curves (on-axis, listening window, early reflections,
sound power, directivity index, and predicted in-room).

ASSUMPTIONS (theoretical, NOT measured data)
- 2x GRS 8SW-4HE: modelled as circular pistons (d=200 mm) for directivity above
  their 150 Hz crossover.  Below 150 Hz they are omnidirectional (sealed box,
  wavelength >> driver diameter).  Push-push geometry does not change directivity
  because the two sources radiate in the same direction from opposite sides.
- 15W/4434G00: flat circular piston, a=58.3 mm (from Sd=107 cm^2).  Directivity
  from |2 J1(ka sinθ)/(ka sinθ)|.  This is valid roughly to the cone breakup region
  (~2 kHz).  Crossed at 1100 Hz, so the mid dominates below that and the tweeter
  above.
- SB26STAC-C000-4 in WG212: above the control limit (~1620 Hz) modelled as a
  constant-directivity source with coverage 100°H × 64°V.  The transition from
  omni-dome to CD-horn is approximated by a smooth crossover function from the
  bare dome radius (~13 mm) to the waveguide mouth (~106×60 mm).  This is a very
  rough geometric model; the real pattern is measured, not predicted.
- Baffle / edge effects are IGNORED.  The 300 mm baffle would create significant
  baffle step and edge diffraction at the lower midrange.  This model gives the
  driver-directivity only.
- Frequencies are evaluated every 1/24 octave from 200 Hz to 20 kHz.

Output: simulations/plots/polar_response.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
#  J1 via Abramowitz & Stegun 9.4 (no scipy needed, same as directivity_estimate.py)
# ---------------------------------------------------------------------------
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
    """Circular piston directivity: |2 J1(ka sinθ)/(ka sinθ)|. theta in deg."""
    c = 344.0
    ka = 2*np.pi*f/c * a
    st = np.sin(np.radians(theta))
    arg = ka * st
    D = np.ones_like(theta)
    nz = arg != 0
    D[nz] = np.abs(2*j1(arg[nz]) / arg[nz])
    return D

def cd_d(theta, cov_deg):
    """Constant-directivity approximation: cosine raised to power for beamwidth."""
    # simple: (cos theta)^n where n chosen so -6 dB at cov_deg/2
    # cov_deg is the full beamwidth (e.g. 100° means -6 dB at 50°)
    half = cov_deg / 2.0
    if half >= 90:  # omnidirectional
        return np.ones_like(theta)
    # power law: (cos theta)^p gives -6 dB at half -> p = -log10(0.5)/log10(cos(half_rad))
    p = -np.log10(0.5) / np.log10(np.cos(np.radians(half)))
    return np.cos(np.radians(theta))**p

def smoothstep(x, x0, x1):
    """Smooth transition 0@x0 to 1@x1."""
    t = np.clip((x - x0) / (x1 - x0 + 1e-12), 0, 1)
    return t * t * (3 - 2*t)

# ---------------------------------------------------------------------------
#  Driver / crossover model
# ---------------------------------------------------------------------------
c = 344.0
f = np.logspace(np.log10(200), np.log10(20000), 500)
theta = np.linspace(0, 180, 181)   # degrees

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

# Woofer: LP@150, diameter 200 mm -> a=0.1m, omni below 150
a_w = 0.100   # 200 mm diameter
# Mid: 15W, a=58.3 mm, HP@150 + LP@1100
a_m = 0.0583
# Tweeter: dome radius ~13 mm, transitions to waveguide mouth ~106 mm at ~1620 Hz
a_t_dome = 0.013
a_t_wg = 0.106
F_ctrl = 1620.0

# Build 2D frequency×theta directivity arrays
# Woofer directivity: omni below 150, piston above
H_w_lp = lr4_lp(f, 150.0)[:, None]  # (Nf, 1)
D_w = np.ones((len(f), len(theta)))
for i, fi in enumerate(f):
    D_w[i, :] = piston_d(theta, a_w, fi)
# Below 150 Hz, force omnidirectional (sealed bass, wavelength >> diameter)
for i, fi in enumerate(f):
    if fi < 150:
        D_w[i, :] = 1.0
D_w *= H_w_lp

# Midrange directivity: HP@150, piston
H_m_hp = lr4_hp(f, 150.0)[:, None]
D_m = np.ones((len(f), len(theta)))
for i, fi in enumerate(f):
    D_m[i, :] = piston_d(theta, a_m, fi)
D_m *= H_m_hp

# Tweeter directivity: HP@1100, transition dome→waveguide
H_t_hp = lr4_hp(f, 1100.0)[:, None]
# transition: at 1100 Hz it's still dome-like, at 2000 Hz it's CD
wg_weight = smoothstep(f, 1100.0, 2000.0)[:, None]
D_t = np.ones((len(f), len(theta)))
for i, fi in enumerate(f):
    a_eff = (1 - wg_weight[i,0]) * a_t_dome + wg_weight[i,0] * a_t_wg
    if a_eff < a_t_dome + 1e-6:
        D_t[i, :] = piston_d(theta, a_eff, fi)
    else:
        # blend: piston_dome + waveguide CD, with weight on CD
        cd_h = cd_d(theta, 100.0)
        cd_v = cd_d(theta, 64.0)
        # on-axis = horizontal, assume vertical is averaged over listening window
        cd = np.sqrt(cd_h * cd_v)   # geometric mean of H and V coverage
        dom = piston_d(theta, a_eff, fi)
        D_t[i, :] = dom + (cd - dom) * wg_weight[i, 0]
D_t *= H_t_hp

# Combined directivity (normalized to on-axis)
D_total = D_w + D_m + D_t
# Normalize to on-axis (theta=0)
D_total_norm = D_total / D_total[:, 0:1]

# ---------------------------------------------------------------------------
#  Spinorama curves
# ---------------------------------------------------------------------------
# On-axis = D_total[:,0]
# Listening window: average of 0°, ±10°, ±20°, ±30° horizontally (keep vertical 0°)
# Early reflections: average of floor/ceiling (±60°) + side walls (±90°)
# Sound power: integral over full sphere (approximate with spherical mean)
# Here we use simple angular integration in the horizontal plane (2D approximation)
# for a first-order estimate.  Real spinorama requires the full 3D polar data.

# Angular indices
idx = {deg: np.argmin(np.abs(theta - deg)) for deg in
       [0, 10, 20, 30, 60, 90, 120, 150, 180]}

# On-axis
on_axis = 20*np.log10(D_total[:, 0])

# Listening Window (horizontal, ±10, ±20, ±30)
lw = 20*np.log10(np.mean([D_total[:, idx[10]], D_total[:, idx[20]], D_total[:, idx[30]],
                          D_total[:, idx[10]], D_total[:, idx[20]], D_total[:, idx[30]]], axis=0))

# Early Reflections (simplified): mean of ±60°, ±90°, ±120°
er = 20*np.log10(np.mean([D_total[:, idx[60]], D_total[:, idx[90]], D_total[:, idx[120]],
                          D_total[:, idx[60]], D_total[:, idx[90]], D_total[:, idx[120]]], axis=0))

# Sound Power (2D approximation: integrate over horizontal circle)
# Simpson rule in 1D, weighted by sinθ in 3D -> use spherical mean approximation
# Here just use the average over all angles (very rough)
sp = 20*np.log10(np.mean(D_total, axis=1))

# Directivity Index: DI = on_axis - sound_power
DI = on_axis - sp

# Predicted In-Room (PIR): average of listening window + sound power (1:1)
PIR = 10*np.log10(0.5*(10**(on_axis/10) + 10**(sp/10)))

# ---------------------------------------------------------------------------
#  Plotting
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(15, 10.5))

# --- Polar map ---
ax = fig.add_subplot(2, 2, 1, polar=True)
F_mesh, TH_mesh = np.meshgrid(f, theta)
# Plot normalized SPL (dB relative to on-axis at each frequency)
SPL_map = 20*np.log10(D_total_norm.T)
# clip below -40 dB for display
SPL_map_clipped = np.clip(SPL_map, -40, 0)
# use log frequency axis for polar mesh: convert to polar coordinates
# angle = theta (converted to radians), radius = log10(f)
logf = np.log10(f)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
c = ax.pcolormesh(np.radians(TH_mesh), np.tile(logf, (len(theta), 1)), SPL_map_clipped,
                  shading="auto", cmap="viridis")
ax.set_ylim(2.0, 4.3)  # 100 Hz to 20 kHz
ax.set_yticks([2.0, 2.3, 2.6, 2.9, 3.2, 3.5, 3.8, 4.1, 4.3])
ax.set_yticklabels(["100", "200", "500", "1k", "2k", "5k", "10k", "15k", "20k"], fontsize=7)
ax.set_thetagrids([0, 30, 60, 90, 120, 150, 180], labels=["0°", "30°", "60°", "90°", "120°", "150°", "180°"])
plt.colorbar(c, ax=ax, shrink=0.6, label="SPL [dB rel on-axis]")
ax.set_title("Polar map (normalized, 2D estimate)", fontsize=10, pad=15)

# --- Spinorama curves ---
ax = fig.add_subplot(2, 2, 2)
ax.semilogx(f, on_axis, lw=2.4, color="0.15", label="On-axis")
ax.semilogx(f, lw, lw=2.0, color="tab:green", label="Listening Window")
ax.semilogx(f, er, lw=2.0, color="tab:orange", label="Early Reflections")
ax.semilogx(f, sp, lw=2.0, color="tab:blue", label="Sound Power")
ax.semilogx(f, PIR, lw=2.0, color="tab:purple", ls="--", label="Predicted In-Room")
ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.set_xlim(200, 20000); ax.set_ylim(-12, 6)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB rel on-axis]")
ax.set_title("Spinorama curves (simplified 2D estimate)")
ax.legend(fontsize=8, loc="upper right")
ax.grid(True, which="both", alpha=0.25)

# --- Directivity Index ---
ax = fig.add_subplot(2, 2, 3)
ax.semilogx(f, DI, lw=2.4, color="0.15")
ax.axhline(0, color="0.5", ls=":", lw=0.8, alpha=0.5)
ax.set_xlim(200, 20000); ax.set_ylim(-2, 12)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Directivity Index [dB]")
ax.set_title("Estimated Directivity Index (on-axis – sound power)")
ax.grid(True, which="both", alpha=0.25)
# annotations
ax.axvline(150, color="0.4", ls=":", lw=0.8, alpha=0.5)
ax.axvline(1100, color="0.4", ls=":", lw=0.8, alpha=0.5)
ax.text(150, 11, "150 Hz", fontsize=8, color="0.4")
ax.text(1100, 11, "1100 Hz", fontsize=8, color="0.4")

# --- Horizontal polar cuts at key frequencies ---
ax = fig.add_subplot(2, 2, 4, polar=True)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
colors = plt.cm.viridis(np.linspace(0, 0.9, 7))
for (freq, col) in zip([250, 500, 1000, 2000, 4000, 8000, 16000], colors):
    idx_f = np.argmin(np.abs(f - freq))
    # only 0-180 (plot symmetrically)
    dB = 20*np.log10(D_total_norm[idx_f, :])
    dB = np.clip(dB, -40, 0)
    ax.plot(np.radians(theta), dB, lw=1.8, color=col, label="%d Hz" % freq)
ax.set_ylim(-40, 0)
ax.set_yticks([-40, -30, -20, -10, 0])
ax.set_yticklabels(["-40", "-30", "-20", "-10", "0"], fontsize=7, color="0.4")
ax.set_thetagrids([0, 30, 60, 90, 120, 150, 180], labels=["0°", "30°", "60°", "90°", "120°", "150°", "180°"])
ax.set_title("Horizontal polar cuts (normalized)", fontsize=10, pad=15)
ax.legend(fontsize=7, loc="lower left", bbox_to_anchor=(0.85, -0.05))

fig.suptitle(
    "Mk2 Reference Loudspeaker – Estimated polar response & spinorama (simplified model, NOT measured)",
    fontsize=13
)
fig.tight_layout(rect=[0, 0, 1, 0.96])

out = os.path.join(os.path.dirname(__file__), "plots", "polar_response.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=135)
print("wrote", out)

# ---------------------------------------------------------------------------
#  CSV exports
# ---------------------------------------------------------------------------
csv_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(csv_dir, exist_ok=True)

# Spinorama curves
spin_out = os.path.join(csv_dir, "spinorama.csv")
header = "freq_Hz,on_axis_dB,listening_window_dB,early_reflections_dB,sound_power_dB,DI_dB,PIR_dB"
rows = [header]
for i in range(len(f)):
    rows.append(
        f"{f[i]:.3f},{on_axis[i]:.4f},{lw[i]:.4f},"
        f"{er[i]:.4f},{sp[i]:.4f},{DI[i]:.4f},{PIR[i]:.4f}"
    )
with open(spin_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print("wrote", spin_out)

# Polar data (angles × frequencies)  - sampled at 10-deg intervals
polar_out = os.path.join(csv_dir, "polar_horizontal.csv")
theta_sample = np.arange(0, 181, 10)
f_sample_idx = [np.argmin(np.abs(f - fx)) for fx in [200, 500, 1000, 2000, 4000, 8000, 16000]]
header_parts = ["theta_deg"] + [f"f{f[i]:.0f}Hz_dB" for i in f_sample_idx]
rows = [",".join(header_parts)]
for t_deg in theta_sample:
    t_idx = np.argmin(np.abs(theta - t_deg))
    vals = [f"{t_deg:.0f}"]
    for fi in f_sample_idx:
        vals.append(f"{20*np.log10(D_total_norm[fi, t_idx]):.4f}")
    rows.append(",".join(vals))
with open(polar_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print("wrote", polar_out)
