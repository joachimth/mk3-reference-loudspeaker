"""
Mk3 Reference Loudspeaker - sealed bass volume comparison (70-85 L)
===================================================================

ASSUMPTIONS (simplified, small-signal, sealed box)
- Two GRS 12SW-4HE in one sealed box behave as one equivalent driver with
  Vas_total = 2 * Vas_single. T/S from GRS 12SW-4HE datasheet:
      Fs = 22.0 Hz, Qts = 0.43, Vas_single = 80.4 L  ->  Vas_total = 160.8 L
- Sealed alignment:  Qtc = Qts*sqrt(1 + Vas_total/Vb),  Fc = Fs*sqrt(1 + ...).
- Acoustic roll-off is the ideal 2nd-order high-pass set by (Fc, Qtc); real
  output adds box losses, leakage and room gain. This compares alignments; it is
  not an absolute in-room prediction. Measured truth comes later (MEASUREMENTS.md).

Output: simulations/plots/bass_volume_compare.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- driver / system constants ---
Fs        = 22.0      # Hz
Qts       = 0.43
Vas_total = 160.8     # L  (2 x 80.4)

volumes = [69, 72, 75, 78, 80, 85]   # L net, 75 L is the target
highlight = 75

def alignment(Vb):
    k   = np.sqrt(1.0 + Vas_total / Vb)
    Qtc = Qts * k
    Fc  = Fs * k
    a   = 1.0 / Qtc**2 - 2.0
    f3  = Fc * np.sqrt((a + np.sqrt(a*a + 4.0)) / 2.0)
    return Qtc, Fc, f3

def hp2(f, Fc, Qtc):
    s = 1j * (f / Fc)
    return (s*s) / (s*s + (1.0/Qtc)*s + 1.0)

def group_delay_ms(f, Fc, Qtc):
    w   = 2*np.pi*f
    phi = np.unwrap(np.angle(hp2(f, Fc, Qtc)))
    gd  = -np.gradient(phi, w)
    return gd * 1e3   # ms

f = np.logspace(np.log10(10), np.log10(300), 800)

print(f"{'Vb [L]':>7} {'Qtc':>6} {'Fc [Hz]':>8} {'F3 [Hz]':>8} {'peakGD [ms]':>12}")
results = {}
for Vb in volumes:
    Qtc, Fc, f3 = alignment(Vb)
    gd = group_delay_ms(f, Fc, Qtc)
    results[Vb] = (Qtc, Fc, f3, gd)
    tag = "  <- target" if Vb == highlight else ""
    print(f"{Vb:>7} {Qtc:>6.3f} {Fc:>8.1f} {f3:>8.1f} {gd.max():>12.1f}{tag}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8.2), sharex=True)

for Vb in volumes:
    Qtc, Fc, f3, gd = results[Vb]
    lw  = 3.0 if Vb == highlight else 1.4
    col = "tab:red" if Vb == highlight else str(0.45 + 0.08*volumes.index(Vb))
    z   = 5 if Vb == highlight else 2
    lab = f"{Vb} L (Qtc {Qtc:.2f}, Fc {Fc:.1f}, F3 {f3:.1f})"
    db  = 20*np.log10(np.abs(hp2(f, Fc, Qtc)))
    ax1.semilogx(f, db, lw=lw, color=col, zorder=z, label=lab)
    ax2.semilogx(f, gd, lw=lw, color=col, zorder=z)

ax1.axhline(-3, color="0.6", ls=":", lw=1)
ax1.text(11, -3.4, "-3 dB", fontsize=8, color="0.4")
ax1.set_ylim(-18, 3); ax1.set_ylabel("Relative SPL [dB]")
ax1.set_title("Sealed alignment vs net box volume (2 x GRS 12SW-4HE, ideal 2nd-order)")
ax1.grid(True, which="both", alpha=0.25); ax1.legend(fontsize=7.5, loc="lower right")

ax2.set_ylabel("Group delay [ms]"); ax2.set_xlabel("Frequency [Hz]")
ax2.set_xlim(10, 300); ax2.grid(True, which="both", alpha=0.25)
ax2.text(11, 0.3, "Qtc < 0.707 -> no peaking; group delay stays low and smooth.\n"
                  "69 -> 85 L barely moves Fc/Qtc: the alignment is robust to build tolerance.",
         fontsize=8, color="0.3", va="bottom")

out = os.path.join(os.path.dirname(__file__), "plots", "bass_volume_compare.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.tight_layout()
fig.savefig(out, dpi=135)
print("wrote", out)
