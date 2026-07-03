"""
Mk3 Reference Loudspeaker - crossover simulation (LR4 filters + sum curve)
==========================================================================

Plots the theoretical amplitude and phase response of the two LR4 crossover
sections used in the v7 (mk3) design, plus the combined on-axis sum.

ASSUMPTIONS (theoretical filters, NOT measured data)
- Low-pass  : 150 Hz LR4, applied to the woofer pair (2x GRS 8SW-4HE).
- High-pass : 1100 Hz LR4, applied to the midrange (15W/4434G00).
- High-pass2: 1100 Hz LR4, applied to the tweeter (SB26STAC-C000-4 in WG212).
- All drivers are treated as ideal flat-bandwidth sources on their own.
  Real acoustic response (cone breakup, waveguide loading, baffle step)
  is NOT included — this is the electrical/acoustic filter topology only.
- 0 dB reference = the summed level when all three drivers are in phase.
- 180 deg phase inversion at the high-pass side is the standard LR4 implementation
  (Linkwitz-Riley requires high-pass = low-pass with 180 deg phase flip).

Output: simulations/plots/crossover_simulation.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
#  LR4 filter math (4th-order Linkwitz-Riley = two cascaded 2nd-order Butterworth)
# ---------------------------------------------------------------------------
def lr4_lp(f, fc):
    """LR4 low-pass: magnitude [dB] and phase [deg] at frequencies f."""
    s = 1j * f / fc
    # two identical Butterworth Q=0.707 stages
    H1 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    H2 = 1.0 / (s**2 + np.sqrt(2)*s + 1)
    H = H1 * H2
    return 20*np.log10(np.abs(H)), np.degrees(np.angle(H))

def lr4_hp(f, fc):
    """LR4 high-pass: magnitude [dB] and phase [deg] at frequencies f."""
    s = 1j * f / fc
    H1 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    H2 = s**2 / (s**2 + np.sqrt(2)*s + 1)
    H = H1 * H2
    # 180 deg phase inversion for LR4 crossover (high-pass = low-pass with 180 flip)
    return 20*np.log10(np.abs(H)), np.degrees(np.angle(H)) + 180

# ---------------------------------------------------------------------------
#  Parameters
# ---------------------------------------------------------------------------
f = np.logspace(np.log10(15), np.log10(20000), 1200)

fc_bass = 150.0     # Hz  LR4 low-pass to mid
fc_mid  = 1100.0    # Hz  LR4 high-pass to mid / low-pass to tweeter

# ---------------------------------------------------------------------------
#  Compute per section
# ---------------------------------------------------------------------------
# Woofer: LP @ 150 Hz
mag_w, ph_w = lr4_lp(f, fc_bass)
# Midrange: HP @ 150 Hz + LP @ 1100 Hz
mag_m_lp, ph_m_lp = lr4_lp(f, fc_mid)
mag_m_hp, ph_m_hp = lr4_hp(f, fc_bass)
# Combined mid = HP(150) * LP(1100)  -> add magnitudes in dB, phases in complex
mag_mid = mag_m_hp + mag_m_lp
ph_mid = ph_m_hp + ph_m_lp
# Tweeter: HP @ 1100 Hz
mag_t, ph_t = lr4_hp(f, fc_mid)

# On-axis sum: coherent addition (all in phase at crossover points for LR4)
# Convert to linear complex, sum, convert back to dB
w_lin = 10**(mag_w/20.0) * np.exp(1j*np.radians(ph_w))
m_lin = 10**(mag_mid/20.0) * np.exp(1j*np.radians(ph_mid))
t_lin = 10**(mag_t/20.0) * np.exp(1j*np.radians(ph_t))

sum_lin = w_lin + m_lin + t_lin
mag_sum = 20*np.log10(np.abs(sum_lin))
ph_sum = np.degrees(np.angle(sum_lin))

# ---------------------------------------------------------------------------
#  Plotting
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 9.5))

# --- Amplitude per section ---
ax = axes[0, 0]
ax.semilogx(f, mag_w, lw=2.2, color="tab:red", label="Woofer (2x GRS) – LP 150 Hz")
ax.semilogx(f, mag_mid, lw=2.2, color="tab:green", label="Midrange (15W) – HP 150 + LP 1100 Hz")
ax.semilogx(f, mag_t, lw=2.2, color="tab:blue", label="Tweeter (SB26STAC) – HP 1100 Hz")
ax.semilogx(f, mag_sum, lw=2.6, color="0.15", ls="--", label="Sum (coherent)")
ax.axhline(-3, color="0.5", ls=":", lw=0.8, alpha=0.6)
ax.axhline(-6, color="0.5", ls=":", lw=0.8, alpha=0.6)
ax.set_xlim(15, 20000); ax.set_ylim(-45, 6)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Magnitude [dB]")
ax.set_title("Per-section LR4 magnitude (ideal drivers)")
ax.legend(fontsize=8, loc="upper right")
ax.grid(True, which="both", alpha=0.25)

# --- Phase per section ---
ax = axes[0, 1]
ax.semilogx(f, ph_w, lw=2.2, color="tab:red", label="Woofer")
ax.semilogx(f, ph_mid, lw=2.2, color="tab:green", label="Midrange")
ax.semilogx(f, ph_t, lw=2.2, color="tab:blue", label="Tweeter")
ax.semilogx(f, ph_sum, lw=2.6, color="0.15", ls="--", label="Sum")
ax.axhline(0, color="0.4", ls="-", lw=0.5)
ax.axhline(180, color="0.4", ls="-", lw=0.5)
ax.axhline(-180, color="0.4", ls="-", lw=0.5)
ax.set_xlim(15, 20000); ax.set_ylim(-270, 270)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Phase [deg]")
ax.set_title("Per-section phase (LR4 high-pass = LP + 180°)")
ax.legend(fontsize=8, loc="upper right")
ax.grid(True, which="both", alpha=0.25)

# --- Zoom: 150 Hz crossover region ---
ax = axes[1, 0]
zoom = (f >= 50) & (f <= 500)
ax.semilogx(f[zoom], mag_w[zoom], lw=2.4, color="tab:red", label="Woofer LP 150")
ax.semilogx(f[zoom], mag_m_hp[zoom], lw=2.4, color="tab:green", label="Mid HP 150")
ax.semilogx(f[zoom], (mag_w[zoom] + mag_m_hp[zoom]), lw=2.6, color="0.15", ls="--", label="Sum")
ax.axvline(150, color="0.4", ls=":", lw=1.2)
ax.text(150, 5.5, "150 Hz", ha="center", fontsize=9, color="0.4")
ax.axhline(-3, color="0.5", ls=":", lw=0.8, alpha=0.6)
ax.set_xlim(50, 500); ax.set_ylim(-20, 7)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Magnitude [dB]")
ax.set_title("150 Hz LR4 crossover (bass → mid)")
ax.legend(fontsize=8, loc="upper right")
ax.grid(True, which="both", alpha=0.25)

# --- Zoom: 1100 Hz crossover region ---
ax = axes[1, 1]
zoom = (f >= 400) & (f <= 4000)
ax.semilogx(f[zoom], mag_m_lp[zoom], lw=2.4, color="tab:green", label="Mid LP 1100")
ax.semilogx(f[zoom], mag_t[zoom], lw=2.4, color="tab:blue", label="Tweeter HP 1100")
ax.semilogx(f[zoom], (mag_m_lp[zoom] + mag_t[zoom]), lw=2.6, color="0.15", ls="--", label="Sum")
ax.axvline(1100, color="0.4", ls=":", lw=1.2)
ax.text(1100, 5.5, "1100 Hz", ha="center", fontsize=9, color="0.4")
ax.axhline(-3, color="0.5", ls=":", lw=0.8, alpha=0.6)
ax.set_xlim(400, 4000); ax.set_ylim(-20, 7)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Magnitude [dB]")
ax.set_title("1100 Hz LR4 crossover (mid → tweeter)")
ax.legend(fontsize=8, loc="upper right")
ax.grid(True, which="both", alpha=0.25)

fig.suptitle(
    "Mk3 Reference Loudspeaker – LR4 crossover simulation (150 Hz + 1100 Hz, ideal sources)",
    fontsize=13
)
fig.tight_layout(rect=[0, 0, 1, 0.96])

out = os.path.join(os.path.dirname(__file__), "plots", "crossover_simulation.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=135)
print("wrote", out)

# ---------------------------------------------------------------------------
#  CSV export
# ---------------------------------------------------------------------------
csv_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, "crossover_simulation.csv")
header = ("freq_Hz,woofer_mag_dB,woofer_phase_deg,"
          "mid_mag_dB,mid_phase_deg,"
          "tweeter_mag_dB,tweeter_phase_deg,"
          "sum_mag_dB,sum_phase_deg")
rows = [header]
for i in range(len(f)):
    rows.append(
        f"{f[i]:.3f},"
        f"{mag_w[i]:.4f},{ph_w[i]:.4f},"
        f"{mag_mid[i]:.4f},{ph_mid[i]:.4f},"
        f"{mag_t[i]:.4f},{ph_t[i]:.4f},"
        f"{mag_sum[i]:.4f},{ph_sum[i]:.4f}"
    )
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print("wrote", csv_out)
