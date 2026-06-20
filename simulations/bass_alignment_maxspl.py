"""
Mk2 Reference Loudspeaker - bass alignment & max-SPL estimate
=============================================================

ASSUMPTIONS (simplified physics, NOT measured data)
- 2 x GRS 8SW-4HE per loudspeaker, sealed, shared chamber, push-push.
- N-driver sealed relation: Vas_total = N * Vas_single,
  Qtc = Qts*sqrt(1 + Vas_total/Vb), Fc = Fs*sqrt(1 + Vas_total/Vb).
- Max SPL is the EXCURSION-limited ceiling (anechoic, half-space, 1 m),
  two drivers summing in phase: SPL = 20*log10(k*f^2), capped at a thermal estimate.
- Driver T/S from the SoundImports datasheet; verify against the official GRS sheet.
  (Repo doc 03 lists the conservative Xmax 10.8 mm / Sd 227 cm2, matching the
   datasheet values used here.)

Output: simulations/plots/bass_alignment_maxspl.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rho = 1.18  # kg/m^3

GRS = dict(name="GRS 8SW-4HE (2x)", Fs=24.9, Qts=0.45, Vas=31.7,
           Sd=227e-4, Xmax=10.8e-3, sens=85.0, Pmax=150, imp=4)
SB23 = dict(name="SB23NRXS45-8 (2x)", Fs=27.0, Qts=0.38, Vas=94.0,
            Sd=216e-4, Xmax=6.5e-3, sens=88.5, Pmax=60, imp=8)

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
print("Sealed alignment (2 x GRS 8SW-4HE):")
for Vb in (62, 69, 73):
    Qtc, Fc = sealed(GRS, Vb)
    print(f"  Vb = {Vb:>3} L net  ->  Qtc {Qtc:.2f}   Fc {Fc:.1f} Hz")
Vb = 69
QtcG, FcG = sealed(GRS, Vb)
QtcS, FcS = sealed(SB23, Vb)
kG, kS = k_excursion(GRS), k_excursion(SB23)
thG, thS = thermal_ceiling(GRS), thermal_ceiling(SB23)
for tag, k in (("GRS", kG), ("SB23", kS)):
    print(f"  Max SPL {tag}:  30Hz {20*np.log10(k*30**2):.1f} dB | "
          f"40Hz {20*np.log10(k*40**2):.1f} dB")

# ---- plots ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4))

fb = np.linspace(20, 120, 200)
ax1.plot(fb, np.minimum(20*np.log10(kG*fb**2), thG), color="tab:red", lw=2.4, label=GRS["name"])
ax1.plot(fb, np.minimum(20*np.log10(kS*fb**2), thS), color="tab:blue", lw=2.0, label=SB23["name"])
ax1.axhline(thG, color="tab:red", ls=":", lw=1, alpha=0.6)
ax1.text(118, thG-1.4, "GRS thermal cap", ha="right", fontsize=7, color="tab:red")
ax1.set_xscale("log"); ax1.set_xlim(20, 120); ax1.set_ylim(88, 114)
ax1.set_xticks([20,30,40,50,70,100]); ax1.set_xticklabels(["20","30","40","50","70","100"])
ax1.minorticks_off()
ax1.set_xlabel("Frequency [Hz]"); ax1.set_ylabel("Max SPL @1m [dB] (anechoic, half-space)")
ax1.set_title("Max clean SPL (excursion-limited)")
ax1.grid(True, which="both", alpha=0.25); ax1.legend(fontsize=8, loc="lower right")

f = np.logspace(np.log10(18), np.log10(200), 400)
ax2.plot(f, 20*np.log10(hp2(f, FcG, QtcG)), color="tab:red", lw=2.4,
         label=f"GRS in {Vb} L (Qtc {QtcG:.2f}, Fc {FcG:.0f})")
ax2.plot(f, 20*np.log10(hp2(f, 28, 0.707)), color="tab:red", lw=1.6, ls="--",
         label="GRS + Linkwitz Transform (Fc 28, Q0.71)")
ax2.plot(f, 20*np.log10(hp2(f, FcS, QtcS)), color="tab:blue", lw=1.8,
         label=f"SB23 in {Vb} L (Qtc {QtcS:.2f}, Fc {FcS:.0f})")
ax2.axhline(-3, color="0.6", ls=":", lw=1); ax2.text(190, -2.6, "-3 dB", ha="right", fontsize=7, color="0.5")
ax2.set_xscale("log"); ax2.set_xlim(18, 200); ax2.set_ylim(-15, 4)
ax2.set_xticks([20,30,50,70,100,150]); ax2.set_xticklabels(["20","30","50","70","100","150"])
ax2.minorticks_off()
ax2.set_xlabel("Frequency [Hz]"); ax2.set_ylabel("Relative [dB]")
ax2.set_title("Sealed bass response (anechoic)")
ax2.grid(True, which="both", alpha=0.25); ax2.legend(fontsize=7.5, loc="lower right")

fig.suptitle("Mk2 bass: 2x GRS 8SW-4HE sealed (~%d L) - simplified estimate" % Vb, fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.95])
out = os.path.join(os.path.dirname(__file__), "plots", "bass_alignment_maxspl.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=135)
print("wrote", out)
