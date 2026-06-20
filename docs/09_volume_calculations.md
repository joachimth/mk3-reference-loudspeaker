# Chapter 9 - Volume Calculations

---

## Overview

The cabinet contains two distinct acoustically separate volumes:

1. **Bass chamber** - main sealed enclosure for the two GRS woofers
2. **Mid chamber** - sealed sub-enclosure for the ScanSpeak 15W midrange

These two volumes must be designed independently. The mid chamber is fully sealed from the bass chamber.

---

## Bass chamber

### Target

- Net bass volume: approximately 69 L
- Sealed alignment: Fc ~34.5 Hz, Qtc ~0.62

### Driver parameters (two GRS 8SW-4HE-8)

| Parameter | Per driver | Combined |
|---|---|---|
| Fs | ~24.9 Hz | ~24.9 Hz (unchanged) |
| Vas | ~31.7 L | Equivalent pair: see below |
| Qts | ~0.45 | ~0.45 (unchanged) |

For two identical sealed drivers in the same enclosure, the system behavior is equivalent to a single driver with double the moving mass and double the Sd, and the Vas of the equivalent driver is half the individual Vas per driver (because Vas scales with Sd and compliance).

However, in practice the sealed-box alignment is often calculated using the simple relation:

```
Qtc = Qts × sqrt(1 + Vas_effective / Vb)
```

Where Vas_effective accounts for both drivers sharing the enclosure.

For two drivers in a shared enclosure, the effective system Vas is approximately equal to the individual driver Vas (since both drivers share the same air volume and the air spring they see is halved per driver but they each experience the full enclosure).

The simulation used Qts = 0.45 and targeted a Qtc of approximately 0.62 in a ~69 L enclosure. This result was obtained from simulation software (VituixCAD / WinISD equivalent) and should be verified before construction.

### Gross vs. net volume

The gross internal bass chamber volume must exceed 69 L by the volume displaced by:

- Driver motor assemblies extending into the cabinet (woofer displacement)
- Bracing material inside the cabinet
- Damping material
- Mid chamber walls

Typical deductions per 8-inch woofer: approximately 0.5-1.0 L displacement.
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
- Driver displacement (2 woofers): ~1.5 L estimated
- Bracing: ~4-6 L estimated
- Damping material: minor

Approximate remaining bass net volume: ~86.5 - 5.7 - 6 - 1.5 = ~73 L

This suggests the current external dimensions can support a ~69 L net bass volume with reasonable bracing. The exact figure must be calculated from the final CAD model.

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
| Bass chamber | ~69 L | Estimated from external dimensions, pending CAD |
| Mid chamber | ~5.7 L | Pending CAD |

Both volumes are to be verified in the final 3D CAD model before construction.
