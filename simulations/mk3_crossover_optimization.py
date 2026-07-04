"""
Mk3 crossover optimization — systematic sweep for SB26STAC-C000-4
==================================================================

Sweeps mid/tweeter crossover frequencies from 800 to 1600 Hz and scores
each option against five criteria:

  1. Fs margin: crossover − Fs (750 Hz). Higher = safer, less distortion.
  2. Excursion headroom: relative max SPL at crossover before distortion.
     Proportional to Xmax × Sd × fc². Higher = more headroom.
  3. Directivity match: DI mismatch between 15W midrange and WG212 tweeter
     at the crossover frequency. Lower = better match.
  4. Vertical lobing: SPL ripple at ±15° (listening window edge) and
     first null position/depth. Lower ripple = better.
  5. System sum flatness: ripple in the 80-15000 Hz passband after
     level-matching. Lower = flatter response.

Also computes the same metrics for mk2 (H2606 @ 1250 Hz) as baseline.

A composite score weights all criteria and identifies the optimal crossover.

Output: simulations/plots/mk3_crossover_optimization.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c_speed = 344.0

# ============================================================
#  Shared math (same as mk2_vs_mk3_spinorama.py)
# ============================================================
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

def piston_beamwidth_deg(f, a_mid=0.0583):
    ka = 2*np.pi*f/c_speed * a_mid
    theta = np.radians(np.linspace(0.5, 90, 600))
    arg = ka * np.sin(theta)
    D = np.ones_like(arg)
    nz = arg != 0
    D[nz] = np.abs(2*j1(arg[nz]) / arg[nz])
    below = np.where(D <= 0.5)[0]
    if below.size == 0:
        return 180.0
    return 2*np.degrees(theta[below[0]])

def di_from_coverage(th_h, th_v):
    return 10*np.log10(41253.0 / (th_h * th_v))

F_CTRL = 1620.0
def wg_coverage_deg(f):
    if f >= F_CTRL:
        return 100.0, 64.0
    g = (F_CTRL - f) / F_CTRL
    return 100.0 + g*(180.0 - 100.0), 64.0 + g*(140.0 - 64.0)

def lr4_lp(f, fc):
    s = 1j * f / fc
    return np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2)

def lr4_hp(f, fc):
    s = 1j * f / fc
    return np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2)

def lr4_lp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((1.0 / (s**2 + np.sqrt(2)*s + 1))**2))

def lr4_hp_db(f, fc):
    s = 1j * f / fc
    return 20*np.log10(np.abs((s**2 / (s**2 + np.sqrt(2)*s + 1))**2))

def vertical_pattern(f, theta_deg, d, fc):
    theta = np.radians(theta_deg)
    delta = 2 * np.pi * f / c_speed * d * np.sin(theta)
    w_mid = lr4_lp(f, fc)
    w_twt = lr4_hp(f, fc)
    return np.abs(w_mid * np.ones_like(theta) + w_twt * np.exp(1j * delta))

# ============================================================
#  Driver parameters
# ============================================================
drivers = {
    "SB26STAC": {"Fs": 750, "Xmax_mm": 0.6, "Sd_cm2": 6.2, "sens": 91.5, "Re": 3.2},
    "H2606":    {"Fs": 1030, "Xmax_mm": 0.2, "Sd_cm2": 5.7, "sens": 95.2, "Re": 4.7},
}

d_cc = 0.150  # 150mm c-c
mid_sens = 89.7  # 15W sensitivity

# ============================================================
#  Sweep crossover frequencies
# ============================================================
xover_freqs = np.arange(800, 1650, 50)  # 800, 850, ..., 1600

results = {}

for drv_name, drv in drivers.items():
    results[drv_name] = {}
    for fc in xover_freqs:
        # 1. Fs margin
        fs_margin = fc - drv["Fs"]

        # 2. Excursion headroom (relative to H2606 @ 1250 = 0 dB)
        rel_exc = 20 * np.log10(
            drv["Xmax_mm"] * drv["Sd_cm2"] * fc**2 /
            (drivers["H2606"]["Xmax_mm"] * drivers["H2606"]["Sd_cm2"] * 1250**2)
        )

        # 3. Directivity mismatch at crossover
        dm = max(di_from_coverage(piston_beamwidth_deg(fc), piston_beamwidth_deg(fc)), 0.0)
        th_h, th_v = wg_coverage_deg(fc)
        dt = di_from_coverage(th_h, th_v)
        di_mismatch = dt - dm

        # 4. Vertical lobing at ±15°
        theta_fine = np.linspace(0.1, 90, 500)
        pattern = vertical_pattern(fc, theta_fine, d_cc, fc)
        pattern = pattern / np.max(pattern)
        dB_pat = 20*np.log10(pattern)
        idx_15 = np.argmin(np.abs(theta_fine - 15))
        spl_15 = dB_pat[idx_15]
        # First null
        minima = np.where((dB_pat[1:-1] < dB_pat[:-2]) & (dB_pat[1:-1] < dB_pat[2:]))[0] + 1
        if len(minima) > 0:
            null_angle = theta_fine[minima[0]]
            null_depth = dB_pat[minima[0]]
        else:
            null_angle = 90
            null_depth = dB_pat[-1]
        # Broadside null frequency
        f_broadside = c_speed / (2 * d_cc)  # 1147 Hz
        # Is crossover below or above broadside null?
        below_broadside = fc < f_broadside

        # 5. System sum flatness
        f_sys = np.logspace(np.log10(18), np.log10(22000), 1000)
        # Woofer: sealed + LP@150
        s_w = 1j * f_sys / 34.5
        H_sealed = s_w**2 / (s_w**2 + s_w/0.62 + 1)
        mag_w = 20*np.log10(np.abs(H_sealed)) + 85.0 + lr4_lp_db(f_sys, 150.0)
        # Mid: flat + HP@150 + LP@fc
        mag_m = np.ones_like(f_sys) * 89.7 + lr4_hp_db(f_sys, 150.0) + lr4_lp_db(f_sys, fc)
        # Tweeter: roll-in + HP@fc
        roll_start = drv["Fs"] * 0.85
        step = 0.5 * (1.0 + np.tanh(np.log10(f_sys / (roll_start * 1.3)) / 0.30))
        mag_t = drv["sens"] + 20*np.log10(step + 1e-6) + lr4_hp_db(f_sys, fc)
        # Level-match
        pad = drv["sens"] - mid_sens
        mag_t_trim = mag_t - pad
        # Sum
        w_lin = 10**(mag_w/20.0)
        m_lin = 10**(mag_m/20.0)
        t_lin = 10**(mag_t_trim/20.0)
        mag_sum = 20*np.log10(w_lin + m_lin + t_lin)
        # Ripple in passband
        pb = (f_sys > 80) & (f_sys < 15000)
        ripple = np.max(mag_sum[pb]) - np.min(mag_sum[pb])

        # Store
        results[drv_name][fc] = {
            "fs_margin": fs_margin,
            "rel_excursion": rel_exc,
            "di_mismatch": di_mismatch,
            "spl_at_15": spl_15,
            "null_angle": null_angle,
            "null_depth": null_depth,
            "below_broadside": below_broadside,
            "ripple": ripple,
            "pad": pad,
            "sum": mag_sum,
            "f_sys": f_sys,
        }

# ============================================================
#  Composite scoring (SB26STAC only — we're optimizing for mk3)
# ============================================================
# Normalize each criterion to 0-10 (10 = best)
sb = results["SB26STAC"]
freqs = list(sb.keys())

# Get ranges for normalization
fs_margins = [sb[f]["fs_margin"] for f in freqs]
excursions = [sb[f]["rel_excursion"] for f in freqs]
di_mismatches = [sb[f]["di_mismatch"] for f in freqs]
spl_15s = [abs(sb[f]["spl_at_15"]) for f in freqs]  # absolute — closer to 0 = better
ripples = [sb[f]["ripple"] for f in freqs]

def norm(val, best, worst, higher_better=True):
    """Normalize to 0-10 scale. best→10, worst→0."""
    if higher_better:
        if best == worst: return 5.0
        return 10.0 * (val - worst) / (best - worst)
    else:
        if best == worst: return 5.0
        return 10.0 * (worst - val) / (worst - best)

# Weights: Fs margin 25%, excursion 20%, DI 15%, lobing 15%, ripple 25%
weights = {"fs_margin": 0.25, "excursion": 0.20, "di": 0.15, "lobing": 0.15, "ripple": 0.25}

# Fs margin: diminishing returns above 300 Hz — use sigmoid
# Below 200 Hz: bad. 200-300: improving. 300+: plateau (safe enough)
def fs_score(margin):
    if margin < 0: return 0.0
    # Sigmoid centered at 250 Hz, width 50 Hz
    return 10.0 / (1.0 + np.exp(-(margin - 250) / 50))

# Excursion: diminishing returns above +6 dB — use soft threshold
# Below 0 dB: bad. 0-6: improving. 6+: plateau
def exc_score(exc):
    # Sigmoid centered at +4 dB, width 2 dB
    return 10.0 / (1.0 + np.exp(-(exc - 4) / 2))

for f in freqs:
    s = sb[f]
    scores = {
        "fs_margin": fs_score(s["fs_margin"]),
        "excursion": exc_score(s["rel_excursion"]),
        "di": norm(s["di_mismatch"], min(di_mismatches), max(di_mismatches), False),
        "lobing": norm(abs(s["spl_at_15"]), min(spl_15s), max(spl_15s), False)
                  + (1.0 if s["below_broadside"] else 0.0),  # bonus: below broadside null
        "ripple": norm(s["ripple"], min(ripples), max(ripples), False),
    }
    composite = sum(weights[k] * scores[k] for k in weights)
    s["scores"] = scores
    s["composite"] = composite

# Find optimal
best_fc = max(freqs, key=lambda f: sb[f]["composite"])
print("=" * 80)
print("MK3 CROSSOVER OPTIMIZATION — SB26STAC-C000-4")
print("=" * 80)
print(f"\n{'Fc [Hz]':>8} {'Fs margin':>10} {'Exc+dB':>8} {'DI mis':>7} {'±15° dB':>8} "
      f"{'Ripple':>7} {'Score':>7}  Broadside")
print("-" * 80)
for f in freqs:
    s = sb[f]
    marker = " ◀ BEST" if f == best_fc else ""
    bs = "below" if s["below_broadside"] else "above"
    print(f"{f:>7}Hz {s['fs_margin']:>+8}Hz {s['rel_excursion']:>+7.1f} {s['di_mismatch']:>+6.1f} "
          f"{s['spl_at_15']:>+7.1f} {s['ripple']:>6.1f} {s['composite']:>6.1f}  {bs}{marker}")

print(f"\nOptimal crossover: {best_fc} Hz (composite score {sb[best_fc]['composite']:.1f}/10)")
print(f"  Fs margin:      {sb[best_fc]['fs_margin']} Hz")
print(f"  Excursion:      {sb[best_fc]['rel_excursion']:+.1f} dB vs H2606@1250")
print(f"  DI mismatch:    {sb[best_fc]['di_mismatch']:.1f} dB")
print(f"  ±15° ripple:    {sb[best_fc]['spl_at_15']:+.1f} dB")
print(f"  System ripple:  {sb[best_fc]['ripple']:.1f} dB (pre-DSP)")
print(f"  Broadside null: {'below' if sb[best_fc]['below_broadside'] else 'above'} crossover "
      f"({c_speed/(2*d_cc):.0f} Hz)")

# Also show mk2 baseline
print(f"\n{'='*80}")
print("MK2 BASELINE — H2606/920000 @ 1250 Hz")
print(f"{'='*80}")
mk2 = results["H2606"][1250]
print(f"  Fs margin:      {mk2['fs_margin']} Hz")
print(f"  Excursion:      {mk2['rel_excursion']:+.1f} dB (reference)")
print(f"  DI mismatch:    {mk2['di_mismatch']:.1f} dB")
print(f"  ±15° ripple:    {mk2['spl_at_15']:+.1f} dB")
print(f"  System ripple:  {mk2['ripple']:.1f} dB (pre-DSP)")

# ============================================================
#  PLOT 1: Optimization sweep (5 panels + composite score)
# ============================================================
fig = plt.figure(figsize=(16, 10))

fc_arr = np.array(freqs)

# Panel 1: Fs margin
ax = fig.add_subplot(2, 3, 1)
ax.plot(fc_arr, [sb[f]["fs_margin"] for f in freqs], "o-", lw=2, color="tab:green")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axhline(250, color="tab:orange", ls=":", lw=0.8, alpha=0.5)
ax.text(fc_arr[-1]+20, 250, "250 Hz\n(safe)", fontsize=7, color="tab:orange", va="center")
ax.axvline(best_fc, color="tab:blue", ls="--", lw=1.0, alpha=0.5)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
ax.set_xlabel("Crossover [Hz]"); ax.set_ylabel("Fs margin [Hz]")
ax.set_title("1. Fs Margin (higher = safer)")
ax.grid(True, alpha=0.25)

# Panel 2: Excursion headroom
ax = fig.add_subplot(2, 3, 2)
ax.plot(fc_arr, [sb[f]["rel_excursion"] for f in freqs], "o-", lw=2, color="tab:purple")
ax.axhline(0, color="0.5", ls=":", lw=0.8)
ax.axvline(best_fc, color="tab:blue", ls="--", lw=1.0, alpha=0.5)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
ax.set_xlabel("Crossover [Hz]"); ax.set_ylabel("Rel. max SPL [dB]")
ax.set_title("2. Excursion Headroom (vs H2606@1250=0)")
ax.grid(True, alpha=0.25)

# Panel 3: DI mismatch
ax = fig.add_subplot(2, 3, 3)
ax.plot(fc_arr, [sb[f]["di_mismatch"] for f in freqs], "o-", lw=2, color="tab:orange")
# Also show H2606 for reference
ax.axhline(mk2["di_mismatch"], color="tab:red", ls=":", lw=1.2, label="H2606 @ 1250")
ax.axvline(best_fc, color="tab:blue", ls="--", lw=1.0, alpha=0.5)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
ax.set_xlabel("Crossover [Hz]"); ax.set_ylabel("DI mismatch [dB]")
ax.set_title("3. Directivity Mismatch (lower = better)")
ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

# Panel 4: Vertical lobing at ±15°
ax = fig.add_subplot(2, 3, 4)
ax.plot(fc_arr, [abs(sb[f]["spl_at_15"]) for f in freqs], "o-", lw=2, color="tab:cyan")
ax.axhline(abs(mk2["spl_at_15"]), color="tab:red", ls=":", lw=1.2, label="H2606 @ 1250")
ax.axvline(best_fc, color="tab:blue", ls="--", lw=1.0, alpha=0.5)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
# Mark broadside null
ax.axvline(c_speed/(2*d_cc), color="0.4", ls=":", lw=0.8)
ax.text(c_speed/(2*d_cc)+10, 0.01, f"broadside\n{c_speed/(2*d_cc):.0f} Hz", fontsize=7, color="0.4")
ax.set_xlabel("Crossover [Hz]"); ax.set_ylabel("|SPL at ±15°| [dB]")
ax.set_title("4. Vertical Lobing at ±15° (lower = better)")
ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

# Panel 5: System sum ripple
ax = fig.add_subplot(2, 3, 5)
ax.plot(fc_arr, [sb[f]["ripple"] for f in freqs], "o-", lw=2, color="tab:gray")
ax.axhline(mk2["ripple"], color="tab:red", ls=":", lw=1.2, label="H2606 @ 1250")
ax.axvline(best_fc, color="tab:blue", ls="--", lw=1.0, alpha=0.5)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
ax.set_xlabel("Crossover [Hz]"); ax.set_ylabel("Ripple [dB]")
ax.set_title("5. System Sum Ripple 80-15k (lower = better)")
ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

# Panel 6: Composite score
ax = fig.add_subplot(2, 3, 6)
scores_arr = [sb[f]["composite"] for f in freqs]
colors = ["tab:blue" if f != best_fc else "gold" for f in freqs]
ax.bar(range(len(freqs)), scores_arr, color=colors, edgecolor="0.3")
ax.set_xticks(range(len(freqs)))
ax.set_xticklabels([str(f) for f in freqs], rotation=45, fontsize=8)
ax.set_ylabel("Composite score (0-10)")
ax.set_title(f"Composite Score (weights: Fs25% Exc20% DI15% Lob15% Rip25%)")
ax.axhline(sb[best_fc]["composite"], color="tab:blue", ls="--", lw=0.8)
ax.text(0.5, sb[best_fc]["composite"]+0.1, f"Best: {best_fc} Hz ({sb[best_fc]['composite']:.1f})",
        fontsize=9, color="tab:blue")
ax.grid(True, axis="y", alpha=0.25)

fig.suptitle(f"Mk3 Crossover Optimization — SB26STAC-C000-4 (Fs=750 Hz, Xmax=0.6mm)\n"
             f"Optimal: {best_fc} Hz | mk2 baseline: H2606 @ 1250 Hz (red dotted)",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.93])
out1 = os.path.join(os.path.dirname(__file__), "plots", "mk3_crossover_optimization.png")
fig.savefig(out1, dpi=150)
print(f"\nwrote {out1}")

# ============================================================
#  PLOT 2: System response at optimal vs mk2 baseline
# ============================================================
fig2, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={"height_ratios": [1, 1]})

# Top: system sum overlay
ax = axes[0]
f_sys = sb[best_fc]["f_sys"]
ax.semilogx(f_sys, sb[best_fc]["sum"], lw=2.8, color="tab:blue",
            label=f"mk3: SB26STAC @ {best_fc} Hz (pad -{sb[best_fc]['pad']:.1f} dB)")
ax.semilogx(f_sys, mk2["sum"], lw=2.8, color="tab:red", ls="--",
            label=f"mk2: H2606 @ 1250 Hz (pad -{mk2['pad']:.1f} dB)")
ax.axvline(best_fc, color="tab:blue", ls=":", lw=1.0, alpha=0.4)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.4)
ax.axvline(150, color="0.4", ls=":", lw=0.8, alpha=0.3)
ax.set_xlim(18, 22000); ax.set_ylim(70, 108)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB]")
ax.set_title(f"System on-axis response: mk3 optimal ({best_fc} Hz) vs mk2 (1250 Hz)")
ax.legend(fontsize=9); ax.grid(True, which="both", alpha=0.25)

# Bottom: difference (normalized @ 500 Hz)
ax = axes[1]
ref_idx = np.argmin(np.abs(f_sys - 500))
mk3_norm = sb[best_fc]["sum"] - sb[best_fc]["sum"][ref_idx]
mk2_norm = mk2["sum"] - mk2["sum"][ref_idx]
diff = mk3_norm - mk2_norm
ax.semilogx(f_sys, diff, lw=2.4, color="0.15")
ax.axhline(0, color="0.5", ls="-", lw=0.8, alpha=0.5)
ax.fill_between(f_sys, 0, diff, where=diff > 0, alpha=0.15, color="tab:blue", label="mk3 > mk2")
ax.fill_between(f_sys, 0, diff, where=diff < 0, alpha=0.15, color="tab:red", label="mk2 > mk3")
ax.axvline(best_fc, color="tab:blue", ls=":", lw=1.0, alpha=0.3)
ax.axvline(1250, color="tab:red", ls=":", lw=1.0, alpha=0.3)
ax.set_xlim(18, 22000); ax.set_ylim(-5, 5)
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Δ SPL [dB]")
ax.set_title(f"Difference: mk3 ({best_fc} Hz) − mk2 (1250 Hz), normalized @ 500 Hz")
ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.25)

# Annotate max difference
xover_region = (f_sys > 800) & (f_sys < 2000)
if np.any(xover_region):
    idx_max = np.argmax(np.abs(diff[xover_region]))
    f_max = f_sys[xover_region][idx_max]
    v_max = diff[xover_region][idx_max]
    ax.annotate(f"Max Δ: {v_max:+.1f} dB @ {f_max:.0f} Hz",
                xy=(f_max, v_max), xytext=(f_max*1.8, v_max+1),
                fontsize=8, arrowprops=dict(arrowstyle="->", color="0.4"))

fig2.suptitle(f"Mk3 Crossover Optimization — Optimal ({best_fc} Hz) vs Mk2 (1250 Hz) System Response",
              fontsize=13, fontweight="bold")
fig2.tight_layout(rect=[0, 0, 1, 0.95])
out2 = os.path.join(os.path.dirname(__file__), "plots", "mk3_optimal_vs_mk2_response.png")
fig2.savefig(out2, dpi=150)
print(f"wrote {out2}")

# ============================================================
#  CSV export
# ============================================================
csv_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(csv_dir, exist_ok=True)
csv_out = os.path.join(csv_dir, "mk3_crossover_optimization.csv")
header = "fc_Hz,fs_margin_Hz,rel_excursion_dB,di_mismatch_dB,spl_at_15_dB,null_angle_deg,null_depth_dB,ripple_dB,composite_score"
rows = [header]
for f in freqs:
    s = sb[f]
    rows.append(f"{f},{s['fs_margin']},{s['rel_excursion']:.2f},{s['di_mismatch']:.2f},"
                f"{s['spl_at_15']:.2f},{s['null_angle']:.0f},{s['null_depth']:.1f},"
                f"{s['ripple']:.2f},{s['composite']:.2f}")
with open(csv_out, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print(f"wrote {csv_out}")
