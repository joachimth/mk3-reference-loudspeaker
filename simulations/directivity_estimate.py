"""
Reference Loudspeaker - directivity (DI) estimate through the mid/tweeter xover
================================================================================

Supports the directivity discussion in docs/06, docs/12 and REVIEW.md C2:
does crossing the WG212 + 15W near the waveguide's ~1620 Hz control limit give a
better directivity match than the 1100 Hz design crossover?

ASSUMPTIONS (simplified estimate, NOT a measured spinorama)
  - Midrange 15W/4434G00 modelled as a flat circular piston, effective radius
    a = sqrt(Sd/pi) with Sd = 107 cm^2  ->  a ~ 58.3 mm. -6 dB beamwidth from the
    piston directivity  D(theta) = |2*J1(k a sin theta)/(k a sin theta)|.
  - Tweeter (SB26STAC-C000-4) in WG212 modelled as a constant-directivity source
    above the control limit (~100 deg H / ~64 deg V) that broadens below it
    toward the bare-dome pattern.
  - Directivity index from coverage angles:  Q ~ 41253 / (theta_h * theta_v)
    [deg], DI = 10 log10(Q). This is the standard horn rule-of-thumb; it ignores
    rear radiation / baffle effects, so absolute dB are approximate. The point is
    the *match* between the two sources, not the absolute level.

J1 via the Abramowitz & Stegun 9.4 polynomial approximation (no scipy needed).

Output: simulations/plots/directivity_estimate.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c = 344.0

# ---- Bessel J1 (A&S 9.4.4 / 9.4.6) ----------------------------------
def j1(x):
    x = np.asarray(x, dtype=float)
    ax = np.abs(x)
    out = np.empty_like(ax)
    # |x| <= 3
    s = ax <= 3.0
    y = (x[s] / 3.0)**2
    out[s] = x[s] * (0.5 - 0.56249985*y + 0.21093573*y**2 - 0.03954289*y**3
                     + 0.00443319*y**4 - 0.00031761*y**5 + 0.00001109*y**6)
    # |x| > 3
    b = ~s
    z = 3.0 / ax[b]
    f1 = (0.79788456 + 0.00000156*z + 0.01659667*z**2 + 0.00017105*z**3
          - 0.00249511*z**4 + 0.00113653*z**5 - 0.00020033*z**6)
    t1 = (ax[b] - 2.35619449 + 0.12499612*z + 0.00005650*z**2 - 0.00637879*z**3
          + 0.00074348*z**4 + 0.00079824*z**5 - 0.00029166*z**6)
    out[b] = f1 * np.cos(t1) / np.sqrt(ax[b])
    out[b] = np.sign(x[b]) * out[b]
    return out

# ---- midrange piston -6 dB full beamwidth ---------------------------
a_mid = np.sqrt(107e-4 / np.pi)     # m  (~0.0583)
theta = np.radians(np.linspace(0.5, 90, 600))

def piston_beamwidth_deg(f):
    ka = 2*np.pi*f/c * a_mid
    arg = ka * np.sin(theta)
    D = np.ones_like(arg)
    nz = arg != 0
    D[nz] = np.abs(2*j1(arg[nz]) / arg[nz])
    below = np.where(D <= 0.5)[0]
    if below.size == 0:
        return 180.0                 # never -6 dB within 90 deg -> very wide
    return 2*np.degrees(theta[below[0]])

# ---- WG212 tweeter coverage model -----------------------------------
F_CTRL = 1620.0
def wg_coverage_deg(f):
    # constant above the control limit, broadening below it
    if f >= F_CTRL:
        return 100.0, 64.0
    g = (F_CTRL - f) / F_CTRL
    return 100.0 + g*(180.0 - 100.0), 64.0 + g*(140.0 - 64.0)

def di_from_coverage(th_h, th_v):
    return 10*np.log10(41253.0 / (th_h * th_v))

# ---- sweep ----------------------------------------------------------
f = np.logspace(np.log10(200), np.log10(20000), 400)
di_mid = np.array([di_from_coverage(piston_beamwidth_deg(fi), piston_beamwidth_deg(fi)) for fi in f])
di_mid = np.maximum(di_mid, 0.0)
wg = np.array([wg_coverage_deg(fi) for fi in f])
di_tw = di_from_coverage(wg[:,0], wg[:,1])

print(f"{'f [Hz]':>8} {'DI_mid':>8} {'DI_tw':>8} {'mismatch':>9}")
for fx in [1100, 1620, 2000]:
    dm = di_from_coverage(piston_beamwidth_deg(fx), piston_beamwidth_deg(fx)); dm = max(dm, 0.0)
    th_h, th_v = wg_coverage_deg(fx); dt = di_from_coverage(th_h, th_v)
    print(f"{fx:>8} {dm:>8.1f} {dt:>8.1f} {dt-dm:>9.1f}")

fig, ax = plt.subplots(figsize=(9.2, 5.8))
ax.semilogx(f, di_mid, lw=2.2, color="tab:blue", label="15W midrange (piston estimate)")
ax.semilogx(f, di_tw, lw=2.2, color="tab:red", label="SB26STAC in WG212 (coverage estimate)")
ax.axvline(1100, color="tab:blue", ls="--", lw=1.4)
ax.text(1100, 10.4, "1100 Hz\n(design)", color="tab:blue", fontsize=8, ha="center")
ax.axvline(F_CTRL, color="0.5", ls=":", lw=1.4)
ax.text(F_CTRL, 11.2, "WG212 control\nlimit ~1620 Hz", color="0.4", fontsize=8, ha="left")
ax.set_xlim(200, 20000); ax.set_ylim(0, 12)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Directivity index DI [dB] (estimate)")
ax.set_title("Estimated directivity match across the mid/tweeter crossover (1100 Hz)")
ax.grid(True, which="both", alpha=0.25); ax.legend(loc="upper left", fontsize=9)
ax.text(210, 0.3,
        "The small 15W stays near-omni until ~2.5 kHz, so the WG tweeter is always more\n"
        "directional at the crossover -> an unavoidable DI step. The step is SMALLER at a\n"
        "lower crossover (~5 dB at 1100 Hz vs ~7 dB at 1620) -> the directivity argument\n"
        "behind DD-010. Countering it (REVIEW C2): below ~1620 Hz the WG is not yet pattern-\n"
        "controlling and the tweeter must have the excursion headroom to cross low. The\n"
        "SB26STAC (Fs 750, Xmax 0.6mm) has the margin to cross at 1100 Hz safely.",
        fontsize=7.5, color="0.3", va="bottom")

out = os.path.join(os.path.dirname(__file__), "plots", "directivity_estimate.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.tight_layout()
fig.savefig(out, dpi=135)
print("wrote", out)
