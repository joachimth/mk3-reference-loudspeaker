"""
Mk3 v9 — Polar Radiation Pattern Visualization
================================================

Generates polar radiation plots showing the mk3's output in horizontal
and vertical planes at key frequencies. Accounts for:

- Driver positions on the cabinet (side woofers vs front mid/tweeter)
- Baffle diffraction effects
- Waveguide directivity (SB26STAC + elliptical WG212)
- Array interference between dual side woofers
- Room transition effects

This shows WHY the mk3's radiation pattern changes with frequency
and how the push-push woofer and front-mid/waveguide interact.

Output: simulations/plots/radiation_pattern.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

c_speed = 343.0

# ============================================================
#  Cabinet geometry (from cad/cabinet.scad)
# ============================================================
W = 0.300      # cabinet width [m]
D = 0.420      # cabinet depth [m]
H = 1.180      # cabinet height [m]

# Driver positions (millimetres from CAD → metres)
woofer_z = 0.520       # woofer pair centre height
woofer_y = D/2          # side-mounted: at the side panel midpoint in depth
woofer_x_off = W/2      # each woofer is at the side panel centre

mid_z = 1.065           # midrange centre height
mid_x = 0               # front baffle centre
mid_y = 0               # front baffle face

tw_z = mid_z - 0.164    # waveguide/tweeter centre height (cc=164 mm)
tw_x = 0                # front baffle centre
tw_y = 0                # front baffle face

cc_tw_mid = tw_z - mid_z  # centre-to-centre = -164 mm (tweeter below mid)

# ============================================================
#  Directivity models
# ============================================================

def piston_directivity(theta_deg, ka):
    """
    Directivity of a piston in an infinite baffle.
    theta_deg: off-axis angle [degrees], 0 = on-axis
    ka: wave number × piston radius
    Returns: dB relative to on-axis
    """
    from scipy.special import j1 as j1_scipy
    
    theta = np.deg2rad(theta_deg)
    x = ka * np.sin(theta)
    
    # J1(x)/x for a circular piston
    # Use scipy's j1 which handles x→0 correctly
    with np.errstate(invalid='ignore', divide='ignore'):
        di = np.where(np.abs(x) > 1e-10,
                      2 * j1_scipy(np.where(np.abs(x) > 1e-10, x, 1e-10)) / np.where(np.abs(x) > 1e-10, x, 1e-10),
                      1.0)
    
    return 20 * np.log10(np.abs(di) + 1e-12)


def baffle_diffraction(theta_deg, freq, dim, axis='h'):
    """
    Simple baffle diffraction model.
    Accounts for the cabinet width (horizontal) or height (vertical)
    as a finite baffle causing edge diffraction.
    
    Uses the Vanderkooy approximation: H(θ) ∝ |sinc(k·d·cosθ/2)|
    where d is the baffle dimension along the axis.
    """
    k = 2 * np.pi * freq / c_speed
    theta = np.deg2rad(theta_deg)
    
    if axis == 'h':
        d = W
        # Front baffle width causes horizontal diffraction
        # The edge closest to the driver creates the first dip
        H = np.sinc(k * d * np.sin(theta) / (2 * np.pi))
    else:
        d = H
        # Cabinet height causes vertical diffraction
        H = np.sinc(k * d * np.cos(theta) / (2 * np.pi))
    
    return 20 * np.log10(np.abs(H) + 1e-12)


def array_interference(theta_deg, freq, d, phase_deg=0):
    """
    Two-source array interference.
    theta_deg: observation angle
    d: source spacing [m] (centre-to-centre)
    phase_deg: relative phase between sources [degrees]
    
    The push-push woofers are on opposite sides, so at the listening
    position one is closer and one is further. At low frequencies
    (d << λ) they sum coherently; at higher frequencies they create
    a lobing pattern.
    """
    theta = np.deg2rad(theta_deg)
    k = 2 * np.pi * freq / c_speed
    phi = np.deg2rad(phase_deg)
    
    # Path length difference for two sources separated by d along x-axis
    # For side-mounted woofers: path difference depends on horizontal angle
    # At θ=90° (directly to the side), one woofer is d/2 closer
    delta = d * np.sin(theta)
    
    H = np.cos(k * delta / 2 + phi / 2)
    return 20 * np.log10(np.abs(H) + 1e-12)


def waveguide_directivity(theta_deg, freq):
    """
    Simplified elliptical waveguide directivity model.
    The SB26STAC in the custom elliptical waveguide creates
    controlled directivity above ~1100 Hz.
    
    Models waveguide as a circular horn with effective mouth
    diameter determined by the waveguide dimensions.
    """
    # Waveguide mouth: ~88.5 mm × broad dimension ~130 mm
    # Effective mouth diameter ~120 mm in horizontal, ~95 mm in vertical
    BCD = 0.0885  # narrow axis (vertical for this waveguide)
    
    theta = np.deg2rad(theta_deg)
    k = 2 * np.pi * freq / c_speed
    
    # Exponential horn directivity approximation
    # H(θ) ≈ 1/(1 + (k·a·sinθ)²) where a is throat radius
    a = 0.014  # throat radius [m] (28 mm throat)
    
    # Below cutoff, the waveguide doesn't control directivity
    fc = c_speed / (2 * BCD)  # ~1940 Hz
    
    if freq < fc * 0.7:
        # Below waveguide cutoff: behaves like dome tweeter in baffle
        return piston_directivity(theta_deg, k * 0.013)  # 13 mm voice coil
    else:
        # Above cutoff: waveguide narrows the beam
        # Sum of dome + waveguide effects
        dome = piston_directivity(theta_deg, k * 0.013)
        wg_db = -6 * (np.sin(theta) * freq / fc) ** 2
        return np.maximum(dome, wg_db)  # whichever dominates (more directional)


def woofer_directivity_vertical(theta_deg, freq):
    """
    Vertical directivity for the side-mounted 12SW pair.
    The woofers are at the same height (z=520 mm) on opposite sides.
    
    In the vertical plane, the two woofers are coincident (same Z),
    so they behave like a single piston in vertical direction.
    """
    Sd = 504e-4  # m² per driver
    r_eff = np.sqrt(Sd / np.pi)
    k = 2 * np.pi * freq / c_speed
    ka = k * r_eff
    return piston_directivity(theta_deg, ka)


def woofer_directivity_horizontal(theta_deg, freq):
    """
    Horizontal directivity for side-mounted 12SW pair.
    Since they're on opposite sides of the cabinet:
    - Left-right asymmetry at close range
    - At far field (>> W), they look like a single source at cabinet centre
    - The W=300 mm spacing causes comb filtering at higher frequencies
    """
    Sd = 504e-4
    r_eff = np.sqrt(Sd / np.pi)
    k = 2 * np.pi * freq / c_speed
    ka = k * r_eff
    
    # Individual piston directivity
    piston = piston_directivity(theta_deg, ka)
    
    # Array interference from the push-push spacing
    # The woofers are separated by W = 300 mm across the cabinet
    if freq < 200:  # only above 200 Hz does the spacing matter
        array = array_interference(theta_deg, freq, W)
        return piston + array
    else:
        # Below 200 Hz, W << λ (λ at 200 Hz = 1.7 m), no significant lobing
        return piston


# ============================================================
#  Combined radiation pattern
# ============================================================

def total_directivity(theta_deg, freq, plane='h'):
    """
    Total directivity of the mk3 at a given frequency and observation angle.
    
    Sums contributions from:
    - 2× side-mounted 12SW woofers (push-push)
    - 1× front-mounted 18W/4424G00 midrange
    - 1× SB26STAC tweeter in waveguide
    
    With appropriate crossover filters applied.
    """
    theta = np.deg2rad(theta_deg)
    
    # Crossover filters (simplified magnitude-only for radiation purposes)
    f_wm = 200.0  # woofer-mid crossover (BW4)
    f_mt = 1100.0  # mid-tweeter crossover (LR4)
    
    def bw4_lp_mag(f, fc):
        s = 1j * f / fc
        H = 1.0 / (s**2 + 1.8478*s + 1) * 1.0 / (s**2 + 0.7654*s + 1)
        return np.abs(H)
    
    def bw4_hp_mag(f, fc):
        s = 1j * f / fc
        H = s**2 / (s**2 + 1.8478*s + 1) * s**2 / (s**2 + 0.7654*s + 1)
        return np.abs(H)
    
    def lr4_lp_mag(f, fc):
        s = 1j * f / fc
        return np.abs(1.0 / (s**2 + s/0.707 + 1.0)) ** 2
    
    def lr4_hp_mag(f, fc):
        s = 1j * f / fc
        return np.abs(s**2 / (s**2 + s/0.707 + 1.0)) ** 2
    
    # Driver contributions (linear SPL, not dB)
    if plane == 'h':
        # Horizontal: woofers create interference pattern
        w_dir = woofer_directivity_horizontal(theta_deg, freq)
    else:
        # Vertical: woofers are coincident
        w_dir = woofer_directivity_vertical(theta_deg, freq)
    
    # Midrange directivity
    Sd_m = 137e-4
    r_m = np.sqrt(Sd_m / np.pi)
    k_m = 2 * np.pi * freq / c_speed
    m_dir = piston_directivity(theta_deg, k_m * r_m)
    
    # Tweeter + waveguide
    t_dir = waveguide_directivity(theta_deg, freq)
    
    # Gains (from DSP config)
    w_gain_lin = 10**(0.0 / 20)    # W = 0 dB
    m_gain_lin = 10**(-4.0 / 20)   # M = -4 dB
    t_gain_lin = 10**(-9.0 / 20)   # T = -9 dB
    
    # Crossover filters
    w_xo = bw4_lp_mag(freq, f_wm)
    m_xo_w = bw4_hp_mag(freq, f_wm)    # HP from woofer-mid
    m_xo_t = lr4_lp_mag(freq, f_mt)    # LP from mid-tweeter
    mid_xo = m_xo_w * m_xo_t
    t_xo = lr4_hp_mag(freq, f_mt)
    
    # Sum in linear domain
    w_lin = 10**((w_dir + 20*np.log10(w_gain_lin * w_xo)) / 20)
    m_lin = 10**((m_dir + 20*np.log10(m_gain_lin * mid_xo)) / 20)
    t_lin = 10**((t_dir + 20*np.log10(t_gain_lin * t_xo)) / 20)
    
    total_lin = w_lin + m_lin + t_lin
    total_db = 20 * np.log10(total_lin + 1e-12)
    
    # Normalize to on-axis (theta=0 is always in our linspace)
    on_axis = np.interp(0, theta_deg, total_db)
    return total_db - on_axis


# ============================================================
#  Generate plots
# ============================================================
frequencies = [80, 200, 500, 1100, 2500, 5000]
freq_labels = ["80 Hz", "200 Hz", "500 Hz", "1.1 kHz", "2.5 kHz", "5 kHz"]
colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(frequencies)))

theta = np.linspace(-180, 180, 361)

fig = plt.figure(figsize=(24, 12), constrained_layout=True)
gs = GridSpec(2, 6, figure=fig, hspace=0.25, wspace=0.20)

# --- Horizontal radiation (top row) ---
for idx, freq in enumerate(frequencies):
    ax = fig.add_subplot(gs[0, idx], projection='polar')
    
    # Convert theta from degrees in speaker coordinates to polar plot
    # 0° = front (on-axis), 90° = right side, -90° = left side
    for i in range(len(frequencies)):
        if i == idx:
            continue
        freq2 = frequencies[i]
        db2 = total_directivity(theta, freq2, plane='h')
        # Clip to meaningful range
        db2_clip = np.clip(db2, -40, 0) + 40  # shift to 0-40 for polar
        theta_rad = np.deg2rad(theta)
        color2 = colors[i]
        ax.plot(theta_rad, db2_clip, color=color2, lw=0.5, alpha=0.15)
    
    # Current frequency
    db_h = total_directivity(theta, freq, plane='h')
    db_h_clip = np.clip(db_h, -40, 0) + 40
    
    theta_rad = np.deg2rad(theta)
    ax.plot(theta_rad, db_h_clip, color=colors[idx], lw=2.5, label=f"{freq_labels[idx]}")
    
    # Fill
    ax.fill(theta_rad, db_h_clip, color=colors[idx], alpha=0.12)
    
    # Annotations
    ax.set_title(f"{freq_labels[idx]}", fontsize=11, fontweight="bold", pad=15)
    ax.set_ylim(0, 45)
    ax.set_yticks([10, 20, 30, 40])
    ax.set_yticklabels(["-30", "-20", "-10", "0 dB"])
    ax.set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(["Front", "", "R Side", "", "Rear", "", "L Side", ""], fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Mark -6 dB ring
    ax.plot(np.deg2rad(np.linspace(0, 360, 361)), np.full(361, 34), 
            color=colors[idx], lw=0.8, ls="--", alpha=0.3)

# --- Vertical radiation (bottom row) ---
for idx, freq in enumerate(frequencies):
    ax = fig.add_subplot(gs[1, idx], projection='polar')
    
    for i in range(len(frequencies)):
        if i == idx:
            continue
        freq2 = frequencies[i]
        db2 = total_directivity(theta, freq2, plane='v')
        db2_clip = np.clip(db2, -40, 0) + 40
        theta_rad = np.deg2rad(theta)
        color2 = colors[i]
        ax.plot(theta_rad, db2_clip, color=color2, lw=0.5, alpha=0.15)
    
    db_v = total_directivity(theta, freq, plane='v')
    db_v_clip = np.clip(db_v, -40, 0) + 40
    
    theta_rad = np.deg2rad(theta)
    ax.plot(theta_rad, db_v_clip, color=colors[idx], lw=2.5, label=f"{freq_labels[idx]}")
    ax.fill(theta_rad, db_v_clip, color=colors[idx], alpha=0.12)
    
    # Highlight the waveguide narrowing
    if frequencies[idx] >= 1100:
        ax.annotate("WG active",
                    xy=(np.deg2rad(45), 25), fontsize=7, color=colors[idx],
                    ha='left', style='italic')
    
    ax.set_title(f"{freq_labels[idx]}", fontsize=11, fontweight="bold", pad=15)
    ax.set_ylim(0, 45)
    ax.set_yticks([10, 20, 30, 40])
    ax.set_yticklabels(["-30", "-20", "-10", "0 dB"])
    ax.set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(["Up ↗", "", "Back", "", "Down ↙", "", "Front", ""], fontsize=7)
    ax.grid(True, alpha=0.3)

# Row labels
fig.text(0.01, 0.75, "Horizontal", fontsize=13, fontweight="bold", rotation=90, va='center')
fig.text(0.01, 0.25, "Vertical", fontsize=13, fontweight="bold", rotation=90, va='center')

fig.suptitle("Mk3 v9 — Radiation Pattern by Frequency\n"
             "Horizontal: side woofers create asymmetry | Vertical: mid+WG control pattern",
             fontsize=14, fontweight="bold")

# Annotate key features
fig.text(0.5, -0.02,
         "Above 200 Hz: woofers become directional → front radiation narrows\n"
         "1100 Hz: waveguide takes over → controlled directivity through midrange crossover\n"
         "2500-5000 Hz: waveguide narrows → listening window becomes critical",
         fontsize=9, ha='center', va='bottom', style='italic',
         bbox=dict(boxstyle="round,pad=0.3", facecolor="0.95"))

# constrained_layout enabled above — no tight_layout call needed
script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'radiation_pattern.png')
fig.savefig(out_png, dpi=150)
print(f"wrote {out_png}")
