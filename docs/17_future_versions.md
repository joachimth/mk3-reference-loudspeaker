# Chapter 17 - Future Versions

---

## Version roadmap

The Mk3 Reference Loudspeaker is designed to be an evolving platform. The v9 design (GRS 12SW-4HE woofer upgrade, ScanSpeak 18W/4424G00 midrange, SB26STAC-C000-4 tweeter at 1100 Hz, 200 Hz BW4 bass/mid crossover, 320 mm cabinet) is the current prototype candidate. Future versions will address remaining limitations and explore more advanced techniques.

---

## v8 - GRS 12SW-4HE woofer upgrade

Woofer upgraded from GRS 8SW-4HE-8 (8") to GRS 12SW-4HE (12" high excursion).

**Changes:**
- 2 × GRS 12SW-4HE push-push woofers (Fs 22 Hz, Xmax 12.5 mm, Sd 504 cm²)
- Bass volume ~75 L under divider plate
- Linkwitz Transform: Fc 39→28 Hz, Qtc 0.76→0.707
- Max SPL @ 30 Hz: +16 dB over v7
- See DD-015

---

## v9 - Midrange upgrade + crossover optimization

The v9 design upgrades the midrange and optimizes the bass/mid crossover.

**Changes from v8:**
- Midrange replaced: ScanSpeak 15W/4434G00 → **18W/4424G00** (Discovery, 18 cm, 91 dB)
- Layout flipped: midrange on top, waveguide/tweeter below, full-width tilted divider between
- Bass/mid crossover: 150 Hz LR4 → **200 Hz BW4** (fills woofer rolloff dip)
- Cabinet width: 300 mm → **320 mm** (12SW magnet clearance), depth 380 mm, height 1180 mm
- Front roundovers: R50 → **R19**
- Mid/tweeter c-c: 150 mm → **165 mm** (physical minimum with 18W faceplate)
- DSP gains rebalanced: **W0/M-4/T-9** (woofer at unity, pad others down)
- DSP correction reduced: ±6 → ±1.3 dB
- See DD-016, DD-017

**Remaining goals (prototype validation):**
- Build prototype cabinet
- Measure all drivers in cabinet
- Import measurements into VituixCAD
- Validate or revise the 1100 Hz crossover for 18 cm cone directivity
- Validate the vertical listening window at 165 mm c-c
- Finalize DSP crossover settings
- Document all measurements

**Success criteria:**
- On-axis response ±1.5 dB after DSP
- DI smooth and rising
- No lobing artifacts in ±15° vertical listening window
- SB26STAC distortion acceptable at 1100 Hz (expected)

---

## v10 - CAD and package refinement

After the prototype is validated acoustically, refine the physical design for a higher-quality final version.

**Goals:**
- Create complete 2D cabinet drawings for CNC or hand cutting
- Finalize waveguide CAD (OpenSCAD or Fusion360/FreeCAD)
- Export STEP/STL files for waveguide printing or machining
- Generate final front baffle layout drawing with exact hole positions
- Refine exterior finish (veneer, solid wood edge, paint)

---

## v11 - DSP implementation

Finalize the DSP implementation for long-term use.

**Goals:**
- Finalize MiniDSP or FusionAmp presets
- Create preset files for three house curves (flat, Harman, bass lift)
- Document all DSP settings with backup files in repository
- Test with multiple sources and listening conditions
- Document startup/shutdown procedure for the active system

---

## v12 - FIR filters

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

## v13 - Integrated active electronics

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

### Cardioid bass (separate experiment)

Cardioid bass uses a rear-facing woofer with a delay and polarity inversion to produce partial cancellation of the rear wave. This can reduce room excitation by the bass system and improve the in-room bass response.

Inspired by Dutch & Dutch 8C. Requires additional amplifier channel and DSP filters.

### Purifi midrange

The Purifi PTT6.5W04-NFA-01 is a 6.5-inch midrange driver with exceptionally low distortion. It would be a candidate to replace the ScanSpeak 15W in a higher-performance version.

### Klippel NFS measurements

A Klippel NFS (Near Field Scanner) provides a complete spinorama dataset from near-field measurements, without requiring a large outdoor measurement area. Available at some universities and professional labs.

### Public website / GitHub Pages

A GitHub Pages static site with the design documentation, measurement results, and build photos, for sharing the project with the DIY audio community.

---

## Version history

See [ROADMAP.md](../ROADMAP.md) for the full version history.
See [CHANGELOG.md](../CHANGELOG.md) for detailed design changes per version.
