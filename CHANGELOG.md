# Changelog

All notable design changes for Mk2 Reference Loudspeaker are documented here.

## v6b - Current reference candidate

### Added

- WG212 selected as current waveguide direction.
- 1250 Hz LR4 acoustic mid/tweeter crossover selected as current target.
- 140 mm mid/tweeter c-c spacing selected as target.
- 300 mm front baffle retained.
- R50 vertical front roundovers retained.
- Approx. 69 L sealed bass chamber target retained.

### Notes

The latest simplified spinorama/directivity simulations suggest that lowering the mid/tweeter crossover and reducing the c-c spacing are more important than increasing waveguide mouth size.

### Refined and corrected (post-review)

- Push-push woofers specified as **opposed at the same height with a rigid
  coupling block**, replacing the earlier 350 mm / 700 mm vertical stagger (the
  stagger re-introduced a rocking moment; same-height opposed cancels cleanly and
  fits the ~22 mm magnet gap). See Chapter 8.
- DD-010 (1250 Hz) and DD-011 (140 mm c-c) annotated with the review caveats:
  1250 Hz sits below the WG212 control band, and ~150-160 mm is the realistic
  buildable c-c. The nominal targets are retained pending measurement.
- Corrected physics-doc errors flagged in `REVIEW.md`: the sealed-box formula and
  T/S data (Chapter 3), the N-driver Vas relation (Chapter 9), and the LR4 phase
  description (Chapter 11). Design numbers (Qtc ~0.62 / Fc ~34.5 Hz) are unchanged.
- Registered the **SB23 line** as a parallel alternative variant (see `ROADMAP.md`
  and `assets/`). The v6b GRS spec is unchanged.
- Minor data polish (REVIEW §D): midrange sensitivity corrected ~88 → ~89.7 dB
  with the tweeter pad widened to ~5-7 dB (measurement-dependent); deep-GRS driver
  displacement raised ~1.5 → ~5 L for the pair (net bass still ~70 L); added a
  4 Ω-vs-8 Ω impedance-confirmation note (Chapter 3) and a "simulated, not
  CEA-2034" banner to Chapter 13.

## v6 - Directivity optimization

### Added

- Compared WG212, WG220, WG230 and WG240.
- Compared 1300, 1400, 1500 and 1600 Hz mid/tweeter crossover targets.
- Compared 140, 145, 150 and 157 mm c-c spacing.

### Result

The best candidates were concentrated around low crossover frequency and short c-c spacing.

## v5b - Volume and placement refinement

### Added

- Refined woofer centers to 350 mm and 700 mm from cabinet bottom.
- Refined mid chamber to approx. 5.7 L net.
- Estimated net bass volume around 70 L.
- Estimated sealed alignment around Fc 34-35 Hz and Qtc 0.62.

## v5 - 300 mm / R50 cabinet

### Added

- Selected 300 mm cabinet width.
- Selected R50 vertical front roundovers.
- Retained 370 mm depth and approx. 1080 mm height.

### Result

300/R50 was selected as a better practical compromise than 280/R40 or wider variants.

## v4 - 280 mm cabinet exploration

### Added

- Explored 280 mm wide cabinet.
- Compared R20, R30, R40 and R50 roundovers.

### Result

R40 was promising, but 280 mm width was considered more mechanically constrained.

## v3 - GRS woofer introduced

### Added

- Investigated GRS 8SW-4HE-8 as replacement woofer.
- Simulated sealed box volumes around 55-75 L.

### Result

2 x GRS 8SW-4HE-8 in approx. 64-70 L sealed volume gave a low-Q alignment suitable for DSP.

## v2 - Cabinet concept

### Added

- Active 3-way cabinet concept.
- Push-push side woofers.
- Dedicated sealed mid chamber.
- H2606 waveguide tweeter.

## v1 - Initial concept

### Added

- Initial Mk2 active reference loudspeaker direction.
- SB23-based starting point.
