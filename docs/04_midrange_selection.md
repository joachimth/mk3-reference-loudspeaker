# Chapter 4 - Midrange Investigations

---

## Requirements

The midrange driver must:

- Cover the range from approximately 150 Hz to 1100 Hz
- Be a 15 cm (6-inch class) driver with good off-axis response in the midrange
- Have low distortion at normal listening levels in the 200-1000 Hz range
- Fit within a 300 mm wide baffle with the waveguide above it at 140 mm c-c
- Operate in a dedicated sealed chamber of approximately 5.7 L net

A 15 cm driver size is preferred over smaller drivers for this range because:
- It can reach down to 150 Hz without excessive excursion or rolloff
- It remains small enough that its directivity begins narrowing (in free-field) above approximately 1200-1500 Hz, which matches the target crossover frequency
- The radiating diameter is compatible with achieving the 140 mm c-c spacing to the waveguide

---

## Investigated driver

### ScanSpeak 15W/4434G00 (selected)

The ScanSpeak Illuminator 15W/4434G00 is the midrange driver selected for this project.

**Key characteristics:**

| Parameter | Value |
|---|---|
| Nominal diameter | 15 cm (6 inch) |
| Re | ~5.6 Ω |
| Fs | ~55 Hz |
| Sensitivity | ~89.7 dB / 2.83V / 1m |
| Xmax | ~7 mm |
| Sd | ~107 cm² |

**Why the ScanSpeak 15W:**

- The Illuminator series is known for low distortion and smooth frequency response
- The 15W cone area provides sufficient output from 150 Hz without requiring excessive amplifier power
- The upper frequency limit in a baffle is well-suited to a 1100 Hz crossover with LR4 slopes
- ScanSpeak has detailed datasheet and measured data available, supporting simulation work
- Good availability through European suppliers

**Sealed mid chamber:**

The 15W operates in a dedicated sealed chamber of approximately 5.7 L net. The chamber isolates the midrange from the bass chamber acoustically and provides a controlled rear loading.

The chamber must be:
- Lined with absorptive material (not overstuffed)
- Sealed from the bass chamber
- Designed so the midrange mounting depth fits within the cabinet internal dimensions

---

## Crossover integration

The midrange is crossed:

- High-pass at 150 Hz (LR4) from the bass system
- Low-pass at 1100 Hz (LR4) to the tweeter/waveguide

The 150 Hz crossover point is low enough that the 15W does not need to produce significant bass output. The 1100 Hz crossover point is within the normal operating range of this driver with the cabinet geometry.

**Vertical lobing:** The 140 mm c-c spacing between the 15W midrange and the WG212 tweeter determines the vertical lobing pattern at the mid/tweeter crossover. See Chapter 11 (Crossovers) and Chapter 12 (Directivity) for detail.

---

## Open items

- Verify exact mounting depth to confirm fit with mid chamber dimensions
- Verify off-axis response at 1100 Hz from measurements in finished cabinet
- Confirm that 1100 Hz LR4 does not require excessive excursion from the 15W below the crossover
