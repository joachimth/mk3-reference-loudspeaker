# Chapter 17 - Future Versions

---

## Version roadmap

The Mk2/Mk3 Reference Loudspeaker is designed to be an evolving platform. The v6b design (mk2) is the current prototype candidate on the `main` branch. The v7 (mk3) design on the `mk3-sb26stac` branch uses the SB26STAC-C000-4 tweeter at 1100 Hz. Future versions will address remaining limitations and explore more advanced techniques.

---

## v7 - Mk3 (SB26STAC-C000-4, 1100 Hz crossover)

> **mk3-sb26stac branch.** This is the current branch's design direction.
> Parallel design variant, created July 3 2026.

The mk3 variant swaps the tweeter to the SB Acoustics SB26STAC-C000-4 and lowers the mid/tweeter crossover to 1100 Hz, removing the H2606 distortion-test gate. See DD-013 and DD-014.

**Changes from v6b (mk2):**
- Tweeter: SB Acoustics SB26STAC-C000-4 (replaces ScanSpeak H2606/920000)
- Crossover: 1100 Hz LR4 (lower than mk2's 1250 Hz)
- Waveguide: custom non-horn-loaded (`cad/mk2_waveguide_sb26stac.scad`)
- +8.1 dB excursion headroom at crossover vs H2606
- No distortion-test gate required (Fs 750 Hz, 350 Hz margin)

**Goals:**
- Build prototype cabinet (mk3 spec)
- Measure SB26STAC in waveguide response/directivity at 1100 Hz
- Import measurements into VituixCAD
- Validate the 1100 Hz crossover (expected comfortable — 350 Hz Fs margin, no distortion gate)
- Validate the vertical listening window
- Finalize DSP crossover settings
- Document all measurements

**Success criteria:**
- On-axis response ±1.5 dB after DSP
- DI smooth and rising
- No lobing artifacts in ±15° vertical listening window
- SB26STAC distortion acceptable at 1100 Hz (expected)

---

## v8 - Mk2 measurement-validated design (main branch)

> **main branch (mk2).** The original v6b-based prototype using the ScanSpeak
> H2606/920000 at 1250 Hz. Retained on main as the mk2 fallback.

The first physical prototype of the mk2 design.

**Goals:**
- Build prototype v6b cabinet
- Measure all drivers in cabinet
- Import measurements into VituixCAD
- Validate or revise the 1250 Hz crossover based on H2606 distortion
- Validate the vertical listening window
- Finalize DSP crossover settings
- Document all measurements

**Success criteria:**
- On-axis response ±1.5 dB after DSP
- DI smooth and rising
- No lobing artifacts in ±15° vertical listening window
- H2606 distortion acceptable at crossover frequency

---

## v9 - CAD and package refinement

After the prototype is validated acoustically, refine the physical design for a higher-quality final version.

**Goals:**
- Create complete 2D cabinet drawings for CNC or hand cutting
- Finalize waveguide CAD (OpenSCAD or Fusion360/FreeCAD)
- Export STEP/STL files for waveguide printing or machining
- Generate final front baffle layout drawing with exact hole positions
- Refine exterior finish (veneer, solid wood edge, paint)

---

## v10 - DSP implementation

Finalize the DSP implementation for long-term use.

**Goals:**
- Finalize MiniDSP or FusionAmp presets
- Create preset files for three house curves (flat, Harman, bass lift)
- Document all DSP settings with backup files in repository
- Test with multiple sources and listening conditions
- Document startup/shutdown procedure for the active system

---

## v11 - FIR filters

Upgrade the DSP from IIR (Linkwitz-Riley) to FIR (linear phase) crossovers.

**Goals:**
- Implement FIR crossover filters (requires a DSP platform with sufficient tap count)
- Achieve linear phase crossover behavior
- Measure before/after comparison
- Evaluate audibility of the change

**Platform options:**
- miniDSP SHD (Dirac Live, FIR capable)
- ADAU1701/1452 with FIR support
- Linux-based DSP (e.g. Camilla DSP on Raspberry Pi)

---

## v12 - Integrated active electronics

Design and build an integrated amplifier module that fits inside the cabinet.

**Goals:**
- Internal 3- or 4-channel Class D amplifier
- Internal DSP
- Power supply
- Single IEC power input on the rear panel
- Balanced XLR or RCA line-level input
- Clean cable management

**Platform candidates:**
- Hypex FusionAmp (plug-in module)
- Purifi-based custom amplifier
- ADAU1452 custom DSP + separate ICEpower or Purifi amplifier channels

---

## Advanced investigations (Nice To Have)

### Cardioid bass (v7 / separate experiment)

Cardioid bass uses a rear-facing woofer with a delay and polarity inversion to produce partial cancellation of the rear wave. This can reduce room excitation by the bass system and improve the in-room bass response.

Inspired by Dutch & Dutch 8C. Requires additional amplifier channel and DSP filters.

### Purifi midrange

The Purifi PTT6.5W04-NFA-01 is a 6.5-inch midrange driver with exceptionally low distortion. It would be a candidate to replace the ScanSpeak 15W in a higher-performance version.

### Bliesma tweeter

The Bliesma T25B or T34A are high-performance dome tweeters with very low distortion and extended frequency response. A potential replacement for the ScanSpeak H2606/920000 in a higher-performance version.

### Klippel NFS measurements

A Klippel NFS (Near Field Scanner) provides a complete spinorama dataset from near-field measurements, without requiring a large outdoor measurement area. Available at some universities and professional labs.

### Public website / GitHub Pages

A GitHub Pages static site with the design documentation, measurement results, and build photos, for sharing the project with the DIY audio community.

---

## Version history

See [ROADMAP.md](../ROADMAP.md) for the full version history from v1 to v6b.
See [CHANGELOG.md](../CHANGELOG.md) for detailed design changes per version.
