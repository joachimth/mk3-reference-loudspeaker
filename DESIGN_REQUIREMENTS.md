# Design Requirements

## Acoustic Targets

- Approx. ±1.5 dB on-axis response
- Smooth directivity index
- Controlled horizontal radiation
- Useful ±15° vertical listening window
- Smooth predicted in-room response

## Driver Layout

- 2 × GRS 12SW-4HE (side-mounted push-push)
- ScanSpeak 18W/4424G00 midrange at the top of the front baffle
- SB Acoustics SB26STAC-C000-4 in the custom waveguide, below the midrange
- Custom waveguide (SB26STAC version, no horn loading)
- Full-width tilted divider plate between midrange and waveguide
  (sealed mid chamber above, bass volume below)

## Cabinet

- 320 × 370 × 1080 mm (width driven by the opposed 12" woofer depth)
- 22 mm birch plywood
- R19 front roundovers (R50 leaves no flat for the 242 mm waveguide flange)

## Alignment

- ~65 L net sealed bass chamber (below divider plate; 75 L remains the target)
- Qtc ≈ 0.707 (via Linkwitz Transform target)
- Sealed Fc ≈ 41 Hz → 28 Hz after LT
- Sealed mid chamber ~11 L net (18W/4424G00 datasheet closed-box rec.: 13 L)
- Woofer cutout: 284 mm (GRS 12SW-4HE)

## Crossovers

- 150 Hz LR4
- 1100 Hz LR4

## Geometry

- Mid/tweeter c-c spacing: **165 mm** — the physical minimum with the Ø179.2 mm 18W/4424G00 faceplate and the 143 mm waveguide flange both flush-recessed in the baffle (`cad/cabinet.scad` echoes the computed minimum). The earlier 140 mm target (DD-011) is not reachable with these parts. Confirm from physical parts before locking the cabinet model.
