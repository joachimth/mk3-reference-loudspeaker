# Chapter 3 - Woofer Investigations

---

## Requirements

The woofer system must:

- Cover the bass range from approximately 20-25 Hz to 150 Hz
- Be suitable for a sealed alignment with Qtc around 0.6-0.65
- Produce useful output below 30 Hz with DSP assistance
- Fit two drivers side-mounted in a 300 mm wide cabinet
- Have sufficient excursion for realistic SPL at low frequencies
- Have an acceptable cost/performance ratio for a DIY project

An 8-inch driver size was selected as the target, as it provides a useful balance between excursion, surface area, and physical fit in the cabinet.

---

## Investigated drivers

### SB Acoustics SB23 (initial concept, v1)

The SB23 family was the starting point in the earliest concept phase (v1). The SB23 is a well-regarded driver with good T/S parameters, but it was replaced as the project evolved and the bass volume requirements became clearer.

**Outcome:** Not selected. Used as the starting reference point only.

---

### GRS 8SW-4HE-8 (selected)

The GRS 8SW-4HE-8 was introduced in v3 and became the woofer candidate for all subsequent versions.

**Key T/S parameters (manufacturer data):**

| Parameter | Value |
|---|---|
| Fs | ~24.9 Hz |
| Vas | ~31.7 L |
| Qts | ~0.45 |
| Re | 3.4 Ω |
| Xmax | ~13 mm |
| Sd | ~214 cm² |

**Two drivers in series:**
- Total impedance: ~8 Ω nominal
- Combined Vas: approximately 2 × 31.7 L = 63.4 L equivalent (for one equivalent driver)
- Combined Sd: approximately 2 × 214 cm² = 428 cm²

**Sealed alignment - two drivers in 69 L net:**

Using the relation Qtc = Qts × sqrt(1 + Vb/Vas per driver pair):

For two GRS 8SW-4HE-8 in a sealed cabinet, the effective system can be treated as an equivalent single driver with the combined moving mass and Sd. The simulation target:

- Net bass volume: ~69 L
- Fc: ~34-35 Hz
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

---

## Configuration: push-push

Two woofers, one front-mounted and one rear-mounted (or both side-mounted facing outward), wired so that as one cone moves outward the other cone also moves outward into free air. This means the reaction forces on the cabinet are equal and opposite, cancelling rather than summing.

See Chapter 8 (Push-push bass) for full detail.

---

## Wiring

Two 4-ohm woofers wired in series: nominal 8 Ω total load.

Parallel wiring (2 Ω total) is possible if the amplifier channel is rated for 2-ohm loads, but series wiring is safer for most DSP/amplifier hardware.

---

## Current status

GRS 8SW-4HE-8 selected. Exact mechanical dimensions (cutout, frame width, mounting depth) to be verified before cabinet CAD is finalized.
