# Technical Review — Mk2 Reference Loudspeaker

External review of the repository documentation and the "simulations" (the numbers and
physics claims in the docs). Goal: flag anything incorrect, anything worth optimising,
and confirm which numbers hold up.

**Headline:** the core bass alignment is **correct** (reproduced independently below).
The design framing (sealed, active, push-push, spinorama-driven, "estimates not
measurements") is sound and honestly stated. The issues are a handful of **documentation
errors in the physics explanations** and **two design targets (1250 Hz crossover, 140 mm
c-c) that are questionable and probably not buildable as written**.

Severity: 🔴 fix (wrong), 🟠 revisit (questionable judgement), 🟡 minor/polish.

---

## A. Bass alignment — verified correct ✅

Independent recomputation, two GRS 8SW-4HE in a shared sealed box, standard N-driver
relation `Vas_total = N · Vas_single`, `Qtc = Qts·√(1 + Vas_total/Vb)`:

| Vb (net) | Qtc | Fc |
|---|---|---|
| 62 L | 0.64 | 35.4 Hz |
| 69 L | 0.62 | 34.5 Hz |
| 73 L | 0.62 | 34.0 Hz |

This matches the repo's stated **Qtc ≈ 0.62 / Fc ≈ 34.5 Hz** in ~69 L. Good low-Q sealed
alignment, ideal for DSP extension. No change needed to the *numbers*.

---

## B. Documentation errors to fix 🔴

### B1. `docs/09_volume_calculations.md` — the Vas explanation is wrong
The text says *"the effective system Vas is approximately equal to the individual driver
Vas."* That is incorrect, and if you actually used it you'd get the wrong answer:
`Vas=31.7, Vb=69 → Qtc 0.54 / Fc 30`, **not** the 0.62/34.5 you (correctly) report.

The correct statement, and the one that reproduces your own result:
> For N identical drivers sharing one sealed box, the system behaves like one driver with
> `Sd_total = N·Sd` and **`Vas_total = N · Vas_single`**. For two GRS: `Vas_total = 2 × 31.7 = 63.4 L`.
> `Qtc = Qts·√(1 + Vas_total/Vb) = 0.45·√(1 + 63.4/69) = 0.62`, `Fc = 24.9·√(…) = 34.5 Hz`.

Note `docs/03_woofer_selection.md` already states the correct `63.4 L` — so 09 currently
contradicts 03. Align 09 to 03.

### B2. `docs/03_woofer_selection.md` — inverted formula + spec mismatches
- The formula is printed inverted: *"Qtc = Qts × sqrt(1 + Vb/Vas per driver pair)"*.
  It should be `Qtc = Qts × sqrt(1 + Vas_total / Vb)`.
- Spec table lists **Xmax ~13 mm** and **Sd ~214 cm²**. The SoundImports datasheet for
  8SW-4HE gives **Xmax 10.8 mm** and **Sd 227 cm²** (Re 3.8 Ω, not 3.4). The 13 mm figure
  is likely an Xmech/peak number, not Xmax. Use the conservative datasheet Xmax (10.8 mm)
  for any SPL/excursion estimate, and verify all three against the official GRS sheet.

### B3. `docs/11_crossovers.md` — LR4 phase claim is wrong
The doc says *"both drivers are 180° out of phase at Fc, but this is corrected by time
delay."* That describes **LR2**, not LR4. For **LR4** the two acoustic outputs are
**in phase (0°)** at Fc, each at −6 dB, and they sum flat **without** polarity inversion.
What time-alignment (delay) corrects is the **physical acoustic-centre offset** between
drivers — not a 180° crossover phase. Suggested wording:
> LR4 outputs are in phase at the crossover frequency (each −6 dB) and sum flat with no
> polarity inversion. DSP delay is used to align the drivers' acoustic centres so the
> summation is correct off-axis as well as on-axis.

---

## C. Design targets to revisit 🟠

### C1. 140 mm c-c (DD-011) is probably not buildable as written
Geometric minimum c-c ≈ `(mid_frame/2) + (WG_flange_height/2)`. The 15W frame is Ø149,
so its half is 74.5 mm. A WG212 (mouth ~121 mm tall + a rolled mouth termination) needs a
flange roughly 140–150 mm tall → half ≈ 70–75 mm. That puts the **geometric minimum c-c
at ~145–160 mm**. 140 mm is only achievable with a deliberately compact / bottom-trimmed
("D-shaped") flange. Recommendation: treat **c-c ≈ 150–160 mm** as the realistic target,
set it from the actual WG flange + mid recess once the WG is in CAD, and don't over-commit
to 140 in the decision log.

Importantly, you don't *need* 140 for lobing — see C2.

### C2. 1250 Hz crossover (DD-010) — the rationale is only half-right
The repo says lowering the crossover "improves directivity matching." It improves
**lobing**, but it can **hurt constant directivity**, because a 212 mm-mouth waveguide only
controls its pattern down to ~1500–1700 Hz. Crossing at **1250 Hz** sits ~300–450 Hz
**below** where the WG controls, so in that octave the tweeter pattern is still broad (no
match benefit), and you ask the H2606 (Fs 1030 Hz) to work at only **1.2 × Fs** — aggressive
for an LR4 high-pass and a distortion/excursion risk.

Lobing does **not** force 1250 Hz. First vertical null angle `θ = asin(c / (2·d·fx))`:

| c-c | 1250 Hz | 1500 Hz | 1600 Hz |
|---|---|---|---|
| 140 mm | 79° | 55° | 50° |
| 160 mm | 59° | 46° | 42° |

Even at **c-c 160 mm and 1600 Hz** the first null is at **42°** — far outside the ±15–30°
window. So a buildable **c-c ≈ 160 mm crossed near the WG control limit (~1500 Hz)** is
clean for lobing *and* gives the WG something to actually do. Suggested target: **acoustic
LR4 ~1500 Hz, c-c ~155–160 mm**, final value set by measured H2606-in-WG distortion
(expect the usable range 1400–1700 Hz). (`simulations/vertical_lobing.py` reproduces the
table above.)

### C3. `docs/08_push_push_bass.md` — self-contradictory, and the stagger is excessive
The chapter says "centres aligned at the same height" and then "vertically stacked … lower
350 mm / upper 700 mm." A 350 mm vertical offset destroys most of the force-cancelling
couple (large rocking moment) — it is *not* a minor compromise.

It is also unnecessary. The GRS overall depth is ~117 mm; in a 256 mm internal width two
opposed magnets leave `256 − 2×117 = 22 mm` of **static** gap (the magnets are fixed to the
baskets/walls and don't move). So **same-height opposed push-push fits**, and a short rigid
**coupling block bonded across that 22 mm** is actually the ideal force-cancelling
arrangement. Recommendation: drop the 350/700 stagger; specify **same height, opposed, with
a coupling block**. Only stagger or widen the cabinet if you want more working clearance.

---

## D. Minor / polish 🟡

- **`docs/09`** driver-displacement deduction "~1.5 L for two woofers" is low for the deep
  GRS (117 mm, ~1.6 kg magnet) — budget ~2–3 L each (~5 L pair). It barely moves Qtc
  (still ~0.62), but fix the figure.
- **`docs/14` / DD-006** mid sensitivity is quoted ~88 dB; the 15W/4434G00 is ~89.7 dB.
  Tweeter pad will land around −5 to −7 dB; finalise from measurement (already noted).
- **Impedance labelling:** the SoundImports listing shows 4 Ω under the "-8" SKU
  (Re 3.8). Confirm whether your drivers are 4 Ω (series → 8 Ω, as the docs assume) or
  8 Ω before wiring.
- **Naming:** consider stating once, prominently, that all spinorama/DI curves are
  *simplified power-response estimates*, not CEA-2034 from measurement — the docs say it,
  but a one-line banner at the top of `13_spinorama.md` would prevent misreading.

---

## E. What's genuinely good (so it isn't lost in the edits)

- Sealed-alignment maths and the low-Q DSP rationale are correct.
- The "estimates, not measurements; finalise from REW/VituixCAD" discipline is exactly
  right and consistently repeated.
- The CEA-2034 / Toole–Olive framing in `02_theory.md` and `13_spinorama.md` is accurate.
- Cabinet width / roundover reasoning (300 mm + R50) is sound and well-justified.
- Documentation structure (numbered chapters + a decision log with DD-IDs) is excellent and
  easy to review.

---

## F. Suggested additions in this PR

To start closing the "recreate simulations as version-controlled scripts" TODO
(`SIMULATIONS.md`), this review ships two runnable, assumption-headed scripts:

- `simulations/bass_alignment_maxspl.py` — sealed alignment table + excursion-limited max
  SPL (GRS pair vs SB23 reference) + sealed response with a Linkwitz-Transform target.
  Writes `simulations/plots/bass_alignment_maxspl.png`.
- `simulations/vertical_lobing.py` — first vertical-null angle vs frequency for c-c and
  crossover options (backs up §C2). Writes `simulations/plots/vertical_lobing.png`.

Run: `python3 simulations/bass_alignment_maxspl.py` (needs numpy + matplotlib).

All figures are simplified physics estimates and must be validated against measurements of
the finished cabinet.
