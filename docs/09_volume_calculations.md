# Chapter 9 - Volume Calculations

---

## Overview

The cabinet contains two distinct acoustically separate volumes:

1. **Bass chamber** - main sealed enclosure for the two GRS 12SW-4HE woofers (volume under the divider plate)
2. **Mid chamber** - sealed sub-enclosure for the ScanSpeak 15W midrange

These two volumes must be designed independently. The mid chamber is fully sealed from the bass chamber.

---

## Bass chamber

### Target

- Net bass volume: approximately 75 L (volume under the divider plate)
- Sealed alignment: Fc ~39 Hz, Qtc ~0.76 → 28 Hz / 0.707 via Linkwitz Transform

### Driver parameters (two GRS 12SW-4HE)

| Parameter | Per driver | Combined |
|---|---|---|
| Fs | 22 Hz | 22 Hz (unchanged) |
| Vas | 80.4 L | Equivalent pair: see below |
| Qts | 0.43 | 0.43 (unchanged) |
| Sd | 504 cm² | 1008 cm² |
| Xmax | 12.5 mm (Klippel) | — |

For **N** identical drivers sharing one sealed enclosure, the system behaves like
a single equivalent driver with N times the Sd and **N times the Vas**:

```
Vas_total = N × Vas_single
Qtc = Qts × sqrt(1 + Vas_total / Vb)
Fc  = Fs  × sqrt(1 + Vas_total / Vb)
```

For two GRS 12SW-4HE (Vas 80.4 L each), `Vas_total = 2 × 80.4 = 160.8 L`. In a
~75 L net enclosure:

```
Qtc = 0.43 × sqrt(1 + 160.8/75) ≈ 0.76
Fc  = 22.0 × sqrt(1 + 160.8/75) ≈ 39.0 Hz
```

This gives a sealed Fc of ~39 Hz with Qtc ~0.76, which is then transformed via a
Linkwitz Transform to Fc 28 Hz / Qtc 0.707 in the DSP. The figures are simplified
estimates — reproduced by
[../simulations/bass_alignment_maxspl.py](../simulations/bass_alignment_maxspl.py)
and [../simulations/bass_volume_compare.py](../simulations/bass_volume_compare.py)
— and should still be confirmed before construction.

### Gross vs. net volume

The gross internal bass chamber volume must exceed 75 L by the volume displaced by:

- Driver motor assemblies extending into the cabinet (woofer displacement)
- Bracing material inside the cabinet
- Damping material
- Mid chamber walls

Deductions per 12-inch woofer depend strongly on motor depth. The GRS 12SW-4HE is
a deep driver (~136 mm overall depth, large magnet), so each displaces roughly
3-5 L inside the cabinet — budget ~8-10 L for the pair rather than the ~5 L for
the previous 8SW pair.
Bracing: estimate 2-5% of gross volume depending on brace density.

The gross external volume of the main cabinet (minus walls and mid chamber) will need to be calculated from the final cabinet drawings.

### External dimensions and gross volume estimate

Using the external dimensions 300 × 370 × 1080 mm and 22 mm walls on all six sides:

```
Internal width:  300 - 2×22 = 256 mm
Internal depth:  370 - 2×22 = 326 mm
Internal height: 1080 - 2×22 = 1036 mm

Total gross internal volume = 256 × 326 × 1036 / 1,000,000 = ~86.5 L
```

Deductions from gross total:
- Mid chamber: ~5.7 L (net) + walls
- Driver displacement (2 woofers): ~8-10 L estimated (deep 12SW magnets, ~3-5 L each)
- Bracing: ~4-6 L estimated
- Damping material: minor

Approximate remaining bass net volume: ~86.5 - 5.7 - 6 - 9 = ~66 L

This is below the 75 L target, so the divider plate position must be set to
allocate enough volume under it for the bass chamber. The exact figure must be
calculated from the final CAD model — the divider plate height is the primary
control for bass vs. the upper cabinet volume.

---

## Mid chamber

### Target

- Net mid chamber volume: approximately 5.7 L

### Purpose

The ScanSpeak 15W midrange operates in a sealed chamber to:
- Provide controlled acoustic loading below the crossover frequency
- Isolate the midrange from the bass chamber (prevents bass energy from entering the midrange from behind)
- Allow independent damping optimization

### Chamber location

The mid chamber is positioned at the top of the cabinet interior, behind the midrange driver cutout on the front baffle.

### Construction

The mid chamber walls will be constructed from 22 mm plywood panels inside the main cabinet, sealing the midrange driver's rear from the bass chamber. All seams must be fully sealed.

### Volume calculation

5.7 L net volume, allowing for:
- 15W driver displacement: approximately 0.3-0.5 L
- Chamber wall material: accounted for in gross dimensions

The chamber will be dimensioned from the CAD model once driver dimensions are confirmed.

### Damping

The mid chamber should be:
- Lined on all walls with absorptive material (e.g. acoustic foam, open-cell foam, or long-fiber wool)
- Not overstuffed - over-damping reduces the effective volume and can change the acoustic rolloff behavior
- Sealed completely before assembly

---

## Summary

| Volume | Target (net) | Status |
|---|---|---|
| Bass chamber | ~75 L (under divider plate) | Estimated from external dimensions + divider plate, pending CAD |
| Mid chamber | ~5.7 L | Pending CAD |

Both volumes are to be verified in the final 3D CAD model before construction.
