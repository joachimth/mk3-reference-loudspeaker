"""
Mk3 Reference Loudspeaker - bass alignment & max-SPL estimate
=============================================================

ASSUMPTIONS (simplified physics, NOT measured data)
- 2 x GRS 12SW-4HE per loudspeaker, sealed, shared chamber, push-push.
- N-driver sealed relation: Vas_total = N * Vas_single,
  Qtc = Qts*sqrt(1 + Vas_total/Vb), Fc = Fs*sqrt(1 + Vas_total/Vb).
- Max SPL is the EXCURSION-limited ceiling (anechoic, half-space, 1 m),
  two drivers summing in phase: SPL = 20*log10(k*f^2), capped at a thermal estimate.
- Driver T/S from GRS 12SW-4HE datasheet (Klippel verified Xmax).

Output: simulations/plots/bass_alignment_maxspl.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rho = 1.18  # kg/m^3

GRS12 = dict(name="GRS 12SW-4HE (2x)", Fs=22.0, Qts=0.43, Vas=80.4,
             Sd=504e-4, Xmax=12.5e-3, sens=84.5, Pmax=250, imp=4)

# Previous design reference (for comparison)
GRS8 = dict(name="GRS 8SW-4HE-8 (2x, previous)", Fs=48.0, Qts=0.38, Vas=28.0,
            Sd=220e-4, Xmax=4.5e-3, sens=85.0, Pmax=100, imp=8)

def sealed(d, Vb):
    a = 2 * d["Vas"] / Vb
    root = np.sqrt(1 + a)
    return d["Qts"] * root, d["Fs"] * root

def k_excursion(d):
    Vd = 2 * d["Sd"] * d["Xmax"]              # peak one-way, both drivers
    return rho * 2 * np.pi * Vd / np.sqrt(2) / 2e-5

def thermal_ceiling(d):
    # sens is dB @ 2.83V/1m. For 4 ohm, 2.83V = 2W -> 1W is sens-3.
    base = d["sens"] - 3 if d["imp"] <= 4 else d["sens"]
    return base + 10 * np.log10(d["Pmax"]) + 6   # +6 dB for two drivers

def hp2(f, Fc, Q):
    s2 = (f / Fc) ** 2
    return s2 / np.sqrt((1 - s2) ** 2 + (f / (Fc * Q)) ** 2)

# ---- alignment table ----
print("Sealed alignment (2 x GRS 12SW-4HE):")
for Vb in (69, 75, 80, 85):
    Qtc, Fc = sealed(GRS12, Vb)
    print(f"  Vb = {Vb:>3} L net  ->  Qtc {Qtc:.2f}   Fc {Fc:.1f} Hz")

print("\nPrevious design (2 x GRS 8SW-4HE-8) for comparison:")
for Vb in (69,):
    Qtc, Fc = sealed(GRS8, Vb)
    print(f"  Vb = {Vb:>3} L net  ->  Qtc {Qtc:.2f}   Fc {Fc:.1f} Hz")

Vb = 75  # target bass volume (under divider plate)
Qtc12, Fc12 = sealed(GRS12, Vb)
Qtc8, Fc8 = sealed(GRS8, 69)
k12, k8 = k_excursion(GRS12), k_excursion(GRS8)
th12, th8 = thermal_ceiling(GRS12), thermal_ceiling(GRS8)

for tag, k in (("GRS 12SW", k12), ("GRS 8SW (prev)", k8)):
    print(f"  Max SPL {tag}:  30Hz {20*np.log10(k*30**2):.1f} dB | "
          f"40Hz {20*np.log10(k*40**2):.1f} dB")

# ---- Linkwitz Transform target ----
Fc_target = 28.0   # Hz
Qt_target = 0.707
print(f"\nLinkwitz Transform target: Fc={Fc_target} Hz, Qt={Qt_target}")
print(f"  GRS 12SW raw: Fc={Fc12:.1f} Hz, Qtc={Qtc12:.2f}")
print(f"  GRS 8SW raw:  Fc={Fc8:.1f} Hz, Qtc={Qtc8:.2f}")

# ---- plot ----
f = np.logspace(np.log10(10), np.log10(500), 500)
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Top: sealed response
ax = axes[0]
ax.set_title(f"Bass alignment: 2× GRS 12SW-4HE (sealed {Vb}L) vs 2× GRS 8SW-4HE-8 (sealed 69L)",
             fontsize=13, fontweight="bold")
for d, Vb_d, col, ls in [(GRS12, Vb, "tab:blue", "-"),
                          (GRS8, 69, "tab:orange", "--")]:
    Qtc, Fc = sealed(d, Vb_d)
    H = hp2(f, Fc, Qtc)
    sens = d["sens"] + 3  # +3 dB push-push
    ax.plot(f, 20*np.log10(H) + sens, col, ls=ls, lw=2,
            label=f'{d["name"]}: Qtc={Qtc:.2f}, Fc={Fc:.1f} Hz')
    # With Linkwitz Transform
    H_lt = hp2(f, Fc_target, Qt_target)
    ax.plot(f, 20*np.log10(H_lt) + sens, col, ls=":", lw=1.5, alpha=0.7,
            label=f'{d["name"]} + LT (Fc={Fc_target} Hz)')
ax.set_ylabel("SPL (dB @ 2.83V/1m)")
ax.set_ylim(50, 100)
ax.set_xlim(10, 500)
ax.set_xscale("log")
ax.axhline(sens, color="0.5", ls=":", lw=0.5)
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.3)

# Bottom: max SPL
ax = axes[1]
ax.set_title("Excursion-limited max SPL (half-space, 1m)", fontsize=13, fontweight="bold")
for d, col, ls, lbl in [(GRS12, "tab:blue", "-", "GRS 12SW-4HE"),
                         (GRS8, "tab:orange", "--", "GRS 8SW-4HE-8 (prev)")]:
    k = k_excursion(d)
    th = thermal_ceiling(d)
    spl = np.minimum(20*np.log10(k * f**2), th)
    ax.plot(f, spl, col, ls=ls, lw=2, label=f'{lbl} ({2*d["Sd"]*1e4:.0f} cm² Sd, {d["Xmax"]*1e3:.1f} mm Xmax)')
    ax.axhline(th, color=col, ls=":", lw=0.8, alpha=0.5)
ax.set_ylabel("Max SPL (dB)")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylim(80, 120)
ax.set_xlim(10, 500)
ax.set_xscale("log")
ax.legend(fontsize=9)
ax.grid(True, which="both", alpha=0.3)

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), "plots", "bass_alignment_maxspl.png")
fig.savefig(out, dpi=150)
print(f"\nwrote {out}")
