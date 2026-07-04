# H2606 Distortion Test — 1250 Hz Crossover Viability

This is **the first gate** for the Mk2 build. The sim says 1250 Hz LR4 should work —
we need real data to confirm. If H2606 passes, we proceed. If not, switch to
SB26STAC branch (mk3-sb26stac, 1100 Hz).

**Estimated time:** 30 min including setup.

---

## Required Equipment

| Item | Notes |
|------|-------|
| H2606 tweeter | One driver, any condition |
| WG212 waveguide | 3D printed, mounted to test baffle |
| Measurement mic | UMIK-1 or calibrated XLR |
| Power amp | 20-50W clean, rated for 4Ω |
| Audio interface | Mic preamp (USB or standalone) |
| REW (free) | Latest version: roomeqwizard.com |
| Laptop/tablet | With REW installed |

**Optional but useful:**
- H2606 in free-air (no waveguide) for reference comparison
- Known-good tweeter (e.g. SB26STAC) as sanity check later

---

## Signal Chain

```
Laptop → USB → Audio Interface → Line Out → Power Amp → H2606 (in WG212)
                                              ↑
                                        Measurement Mic
                                              ↑
                                         Mic Preamp
                                              ↑
                                        USB → Laptop
```

**Level diagram (96 dB target at 1 m):**
- H2606 sensitivity: ~91 dB / 2.83 V / 1 m
- To reach 96 dB at 1 m: ~3 V RMS ≈ 2.2 W into 4Ω
- At 1250 Hz, add waveguide efficiency gain (~3-6 dB): need **~1.5 V RMS ≈ 1 W**
- **Start at 1 V RMS, measure SPL, adjust to hit 96 dB**

---

## Setup Procedure

### 1. Mount Tweeter + Waveguide
- Mount H2606 to WG212 with screws + sealing gasket (no air leaks)
- Mount the waveguide on a test baffle (≈60×60 cm minimum, or the actual Mk2 baffle)
- Baffle should be vertical, tweeter at ear height if possible

### 2. Place Mic
- **On-axis:** pointed directly at tweeter dome, behind waveguide exit
- **Distance:** EXACTLY 1 m from waveguide mouth
- Avoid reflections: 1 m from nearest wall/floor/ceiling
- If room is small (under 4×4 m): use **gated measurement** (REW gating, see below)

### 3. Calibration
- Open REW → Preferences → Soundcard → select your interface
- If using UMIK-1: load its calibration file (REW → Mic/Meter → Calibrate)
- Set SPL reference: REW → Check Levels → use SPL meter or UMIK-1's sensitivity value
- Verify levels: play a 1250 Hz tone at your target voltage, confirm REW reads ~96 dB

### 4. Connect Output
- REW default output → interface line out → amp → tweeter
- **VERIFY POLARITY:** pop test or click test before sweeps
- **START WITH AMP VOLUME AT MINIMUM** — tweeters die fast

---

## Measurement — REW Settings

### Sweep Setup
```
Measurement Type:  Frequency Response
Timing:            Use acoustic timing reference (or loopback)
Sweep Level:       -12 dBFS (adjust to reach 96 dB at 1 m)
Sweep Length:      256k (about 5 seconds at 48 kHz)
Smoothing:         1/12 octave (for display only, keep raw data)
Noise Floor:       Enable — capture before sweep
Averages:          3 sweeps, averaged
```

### Sweep Parameters Tab
```
Start Freq:         100 Hz
End Freq:           20,000 Hz
Steps per Octave:   48 (for distortion harmonics)
Weighing:           None (keep linear)
Cycles:             Use max (standard for distortion)
```

### Distortion Tab (in Measurement results)
After the sweep, look at:
- **THD vs Frequency** — the main chart
- **H2 (2nd harmonic)** — dominant distortion type for dome tweeters
- **H3 (3rd harmonic)** — indicates suspension/nonlinearity issues
- **HD at 1250 Hz** — the crossover frequency

---

## Pass / Fail Criteria

### Pass — Green light for Mk2 at 1250 Hz

All of the following must be true:

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| THD at 1250 Hz, 96 dB | ≤ 2.0 % | REW Distortion tab |
| THD at 1250 Hz, 90 dB | ≤ 1.0 % | Lower-level sweep |
| H2 at 1250 Hz, 96 dB | ≤ 1.5 % | REW harmonics table |
| No audible breakup | Clean, no buzz/rattle | Listen to sine sweep |
| No resonance peak within 1 octave of XO | Within ±3 dB of average | Freq response at 1250 Hz ±300 Hz |

**If all pass:** 🟢 Proceed with Mk2 build. H2606 in WG212 at 1250 Hz LR4 is viable.
The MiniDSP config at `dsp-configs/mk2-150-1250-lr4.md` is your starting point.

### Fail — Switch to Mk3 / SB26STAC

Any ONE of these triggers the fallback:

| Criterion | Threshold | Action |
|-----------|-----------|--------|
| THD at 1250 Hz, 96 dB | > 3.0 % | H2606 exceeds safe excursion at XO |
| H2 at 1250 Hz, 96 dB | > 2.5 % | Nonlinear distortion too high |
| Audible distortion / buzzing | Any at XO power level | Mechanical issue (excursion, suspension) |
| Large resonance peak near XO | > 6 dB deviation at 1250 ± 300 Hz | Waveguide interaction or driver resonance |

**If any fail:** 🔴 Switch to SB26STAC-C000-4 fallback.
1. Check out branch: `git checkout mk3-sb26stac`
2. The waveguide and crossover are designed for 1100 Hz LR4
3. No changes to cabinet or woofer section needed
4. MiniDSP config: adjust Out 4/9 HP from 1250 Hz → 1100 Hz LR4
5. Rerun the distortion test with SB26STAC at 1100 Hz

### Borderline (2-3% THD at 1250 Hz)

You have options:

| Option | Trade-off |
|--------|-----------|
| Raise XO to 1400-1500 Hz | Reduces tweeter excursion, still safe for 15W mid |
| Reduce XO level by -1 to -2 dB | Lowers SPL, reduces excursion; may need EQ compensation |
| Add notch filter at resonance Fs (~1030 Hz) in DSP | Cleans up the resonance peak, helps THD |

Make a judgment call based on the full distortion curve, not just the 1250 Hz point.
If THD rises rapidly below 1250 Hz, you're excursion-limited — raise the XO.
If THD is flat across the band, the 1250 Hz XO is fine with minor EQ.

---

## What To Do With Results

### If Pass 🟢

1. Save the REW measurement as `measurements/h2606_wg212_onaxis_96db.mdat`
2. Iterate: measure at lower levels (90, 85 dB) and off-axis (10, 15, 20 deg)
3. Proceed to cabinet build
4. The MiniDSP config is ready — load and verify with pink noise

### If Fail 🔴

1. Save the REW measurement as `measurements/h2606_wg212_fail_96db.mdat` (data is still useful)
2. Switch to mk3-sb26stac branch: `measurements/sb26stac_wg433_onaxis_96db.mdat`
3. Run the same test procedure for SB26STAC at 1100 Hz
4. Update MiniDSP config accordingly — or use the generator script

### If Borderline

1. Make a decision based on your target SPL and listening distance
2. Nearfield / desktop use (< 1.5 m, < 90 dB) — borderline is fine
3. Living room / hi-fi (> 2 m, > 95 dB peaks) — pass is preferred
4. Document the decision in `MEASUREMENTS.md` with the measurement file

---

## Quick Reference — REW Workflow

```
1. REW → Measure → Start (with chosen settings)
2. Wait for sweep to complete (5-10 sec)
3. Check: SPL window → read 96 dB
4. Check: Distortion window → THD at 1250 Hz
5. Check: Harmonics tab → H2, H3 at 1250 Hz
6. Check: Graph → any anomalies near XO region
7. Save: File → Save Measurement As → descriptive name
8. If multiple sweeps: REW → Average → select measurements
9. Export: File → Export Text → for Python/Excel post-processing
```

**Gated measurement (for small rooms):**
- Set IR Window → Left Window: 0 ms, Right Window: 3-5 ms
- This cuts off reflections but limits resolution below ~300-500 Hz
- Fine for tweeter testing — we care about 800-5000 Hz

---

## Notes

- **Room temperature:** No special requirements. Normal listening temp (18-25 °C) is
  fine for this test.
- **Break-in:** H2606 doesn't need break-in for a distortion test. 5 minutes of
  pink noise at moderate level is sufficient.
- **Safety:** Never run the tweeter unloaded (no waveguide) at full power. The
  waveguide provides acoustic loading and protects the diaphragm.
- **Multiple samples:** If you have two H2606 drivers, test both. Sample variation
  in Fs can affect distortion at XO frequency.
