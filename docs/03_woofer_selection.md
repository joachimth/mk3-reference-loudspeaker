# Chapter 3 - Woofer Investigations

---

## Requirements

The woofer system must:

- Cover the bass range from approximately 20-25 Hz to 200 Hz
- Be suitable for a sealed alignment with Qtc around 0.6-0.65
- Produce useful output below 30 Hz with DSP assistance
- Fit two drivers side-mounted in a 320 mm wide cabinet
- Have sufficient excursion for realistic SPL at low frequencies
- Have an acceptable cost/performance ratio for a DIY project

A 12-inch driver size was selected as the target, as it provides high excursion and large radiating surface area for deep bass output in a moderate sealed cabinet. (An earlier 8-inch target — GRS 8SW-4HE-8 — was used through v7 and is retained below as a historical comparison.)

---

## Investigated drivers

### SB Acoustics SB23 (initial concept, v1)

The SB23 family was the starting point in the earliest concept phase (v1). The SB23 is a well-regarded driver with good T/S parameters, but it was replaced as the project evolved and the bass volume requirements became clearer.

**Outcome:** Not selected. Used as the starting reference point only.

---

### GRS 8SW-4HE-8 (historical — v3 through v7, superseded by 12SW)

The GRS 8SW-4HE-8 was introduced in v3 and served as the woofer through v7. It has
been superseded by the GRS 12SW-4HE (see below) for the v8 bass upgrade. It is
retained here as a historical comparison.

**Key T/S parameters (manufacturer data):**

| Parameter | Value |
|---|---|
| Fs | ~24.9 Hz |
| Vas | ~31.7 L |
| Qts | ~0.45 |
| Re | ~3.8 Ω |
| Xmax | ~10.8 mm |
| Sd | ~227 cm² |

T/S values are from the SoundImports datasheet and must be verified against the
official GRS sheet before construction. Use the conservative datasheet **Xmax
~10.8 mm** for any excursion/SPL estimate; the ~13 mm figure quoted elsewhere is
likely an Xmech/peak number, not Xmax.

**Two drivers in series:**
- Total impedance: ~8 Ω nominal
- Combined Vas: approximately 2 × 31.7 L = 63.4 L equivalent (for one equivalent driver)
- Combined Sd: approximately 2 × 227 cm² = 454 cm²

**Sealed alignment — two drivers in 69 L net (historical, v7):**

Two identical drivers sharing one sealed box behave like a single equivalent
driver with `Sd_total = 2 × Sd` and `Vas_total = 2 × Vas_single = 63.4 L`. The
sealed alignment is then:

```
Qtc = Qts × sqrt(1 + Vas_total / Vb) = 0.45 × sqrt(1 + 63.4/69) ≈ 0.62
Fc  = Fs  × sqrt(1 + Vas_total / Vb) = 24.9 × sqrt(1 + 63.4/69) ≈ 34.5 Hz
```

So for two GRS 8SW-4HE-8 in a sealed cabinet (historical v7 simulation target):

- Net bass volume: ~69 L
- Fc: ~34.5 Hz
- Qtc: ~0.62

This is a low-Q sealed alignment that:
- Has a well-controlled rolloff
- Responds well to DSP bass extension (Linkwitz Transform or shelf boost)
- Produces low group delay compared with heavily tuned ported designs

**Strengths:**

- Low Fs suitable for deep bass in a moderate cabinet
- Good excursion for the price
- 4-ohm nominal impedance allows series wiring to 8 Ω (suitable for most amplifiers)
- Fits the cabinet geometry and mounting requirements

**Weaknesses / open items:**

- Verify exact cutout and frame dimensions before cabinet construction
- Verify push-push wiring phase: the rear-mounted woofer must be wired in reversed polarity to maintain acoustic push-push cancellation of cabinet reaction forces

### GRS 12SW-4HE (selected — v8)

The GRS 12SW-4HE is a 12-inch high-excursion woofer selected for the v8 bass
upgrade, replacing the 8SW. The push-push configuration and sealed alignment are
retained.

**Key T/S parameters (manufacturer data, Klippel-verified Xmax):**

| Parameter | Value |
|---|---|
| Fs | 22 Hz |
| Vas | 80.4 L |
| Qts | 0.43 |
| Sd | 504 cm² |
| Xmax | 12.5 mm (Klippel verified) |
| Bl | 16.2 Tm |
| Sensitivity | 84.5 dB |
| Power | 250 W |
| Impedance | 4 Ω |
| Cutout diameter | 284 mm |

**Two drivers in series:**
- Total impedance: ~8 Ω nominal
- Combined Vas: 2 × 80.4 = 160.8 L equivalent
- Combined Sd: 2 × 504 = 1008 cm²

**Sealed alignment — two drivers in ~75 L net (under divider plate):**

```
Qtc = Qts × sqrt(1 + Vas_total / Vb) = 0.43 × sqrt(1 + 160.8/75) ≈ 0.76
Fc  = Fs  × sqrt(1 + Vas_total / Vb) = 22.0 × sqrt(1 + 160.8/75) ≈ 39.0 Hz
```

So for two GRS 12SW-4HE in a sealed cabinet (v8 target):

- Net bass volume: ~75 L (under the divider plate)
- Sealed Fc: ~39 Hz, Qtc: ~0.76
- Linkwitz Transform target: Fc 39.0 → 28 Hz, Qtc 0.76 → 0.707

**Displacement and max SPL:**
- Peak displacement (2 drivers): 2 × Sd × Xmax = 2 × 504 cm² × 12.5 mm = 12.6 cm³
- vs 8SW pair: 2.0 cm³ — a 6.3× increase
- Max SPL @ 30 Hz: **+16 dB** over the previous 8SW design

**Strengths:**

- Very low Fs (22 Hz) — deep bass extension in a moderate sealed cabinet
- High excursion (12.5 mm Xmax, Klippel verified) for low-distortion SPL
- Large Sd (504 cm²) for efficient air displacement
- Good cost/performance ratio (~€75 per driver)
- Qts 0.43 works well with a Linkwitz Transform to a 0.707 target

**Weaknesses / open items:**

- Large frame (~332 mm overall) and 284 mm cutout — verify fit on 370 mm deep
  side panels
- Basket depth ~136 mm — opposed magnets have only ~4 mm clearance in the
  276 mm internal width (vs ~22 mm for the old 8SW). Coupling block must be sized
  accordingly.
- Lower sensitivity (84.5 dB) than the 8SW — more amplifier power needed, but the
  6.3× displacement advantage dominates at low frequencies
- Verify push-push wiring phase and coupling block fit before finalizing CAD

---

## Configuration: push-push

Two woofers, one front-mounted and one rear-mounted (or both side-mounted facing outward), wired so that as one cone moves outward the other cone also moves outward into free air. This means the reaction forces on the cabinet are equal and opposite, cancelling rather than summing.

See Chapter 8 (Push-push bass) for full detail.

---

## Wiring

Two 4-ohm woofers wired in series: nominal 8 Ω total load.

Parallel wiring (2 Ω total) is possible if the amplifier channel is rated for 2-ohm loads, but series wiring is safer for most DSP/amplifier hardware.

**Confirm impedance before wiring.** The GRS 12SW-4HE is a 4 Ω driver; two in
series gives the intended 8 Ω load. Verify the actual DCR of the delivered drivers
before committing the wiring.

---

## Current status

GRS 12SW-4HE selected (v8). The previous GRS 8SW-4HE-8 is retained as a historical
comparison. Exact mechanical dimensions (cutout 284 mm, frame ~332 mm, mounting
depth ~136 mm, opposed magnet clearance ~4 mm) must be verified before cabinet CAD
is finalized.
