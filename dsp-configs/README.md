# MiniDSP 4×10 HD Configurations for Mk3 Reference Loudspeaker

This directory holds MiniDSP 4×10 HD XML configuration files for active DSP
crossover / EQ on the Mk3 loudspeaker. Each XML file is a complete plugin
configuration that can be loaded via MiniDSP's plugin software (File → Import).

## Current Configs

| File | Crossover | Drivers | Status |
|------|-----------|---------|--------|
| `mk3-v9-200-1100-bw4-lr4.xml` | 200 Hz BW4 + 1100 Hz LR4 | 2×GRS 12SW-4HE → 18W/4424G00 → SB26STAC-C000-4 | ✅ **v9 design target** |
| `mk2-mk3-transition-150-1100-lr4.xml` | 150 Hz LR4 + 1100 Hz LR4 | 2×GRS 12SW-4HE → 15W/4434G00 → SB26STAC-C000-4 | 🗄️ Transition config (pre-v9) |
| *(add more as measurements refine)* | | | |

## Generator

`generate_minidsp_xml.py` is a reusable generator supporting:

- **3-way + push-push woofer** (mk3 v9 default)
- **2-way** configs (--two-way)
- Subsonic HP, Linkwitz Transform, variable sample rate
- Per-channel gain/delay
- Full MiniDSP 4×10 HD XML output (File → Import ready)

Usage:
```bash
# Mk3 v9 (default)
python generate_minidsp_xml.py > mk3-v9-custom.xml

# Custom 3-way
python generate_minidsp_xml.py \
  --woofer-lp 200 --mid-hp 200 --mid-lp 1100 \
  --tweeter-hp 1100 --tweeter-trim -9.0 \
  --woofer-trim 0.0 --mid-trim -4.0

# All options
python generate_minidsp_xml.py --help
```

Biquad coefficients can also be generated stand-alone with `generate_biquads.py`.

## v9 Sensitivity Balance

| Driver | Sensitivity | DSP Trim | Net SPL |
|--------|------------|----------|---------|
| 2×GRS 12SW-4HE (push-push) | ~95 dB | 0.0 dB | **95 dB** |
| ScanSpeak 18W/4424G00 | 91 dB | -4.0 dB | **87 dB** |
| SB26STAC-C000-4 (waveguide) | 91.5 dB | -9.0 dB | **82.5 dB** |

Gains are W0/M-4/T-9 (woofer at unity, mid and tweeter padded down). Net SPL
values are pre-measurement estimates; final trims set from in-cabinet measurement.
DSP correction is approximately ±1.3 dB.

## Input → Output Mapping

MiniDSP 4×10 HD has 2 input channels and 10 outputs. The config maps
Input L → Out 0-4 (left speaker) and Input R → Out 5-9 (right speaker).

### Left Speaker

| Input | Output | Driver | Filters |
|-------|--------|--------|---------|
| CH1 (Left) | Out 0 → Woofer Top | GRS 12SW-4HE (series, 8Ω pair) | Sub HP 18 Hz LR4, LT 39→28 Hz Q0.76→0.707, LP 200 Hz BW4 |
| CH1 (Left) | Out 1 → Woofer Bot | GRS 12SW-4HE (series, 8Ω pair) | Same as Out 0 |
| CH1 (Left) | Out 2 → Mid | ScanSpeak 18W/4424G00 | HP 200 Hz BW4, LP 1100 Hz LR4 |
| CH1 (Left) | Out 3 → Tweeter | SB26STAC-C000-4 (waveguide WG212) | HP 1100 Hz LR4, delay 120 µs |
| CH1 (Left) | Out 4 | Spare | — |

### Right Speaker

| Input | Output | Driver | Filters |
|-------|--------|--------|---------|
| CH2 (Right) | Out 5 → Woofer Top | GRS 12SW-4HE | Same as Out 0 |
| CH2 (Right) | Out 6 → Woofer Bot | GRS 12SW-4HE | Same as Out 1 |
| CH2 (Right) | Out 7 → Mid | ScanSpeak 18W/4424G00 | Same as Out 2 |
| CH2 (Right) | Out 8 → Tweeter | SB26STAC-C000-4 (waveguide WG212) | Same as Out 3 |
| CH2 (Right) | Out 9 | Spare | — |

## Wiring Notes

- Two GRS 12SW-4HE woofers per speaker, wired in **series** → 8 Ω load.
- Each woofer gets its own output channel with identical filters.
  This allows DSP-based polarity flip or individual excursion limiting later.
- Mid and tweeter are single drivers per channel (4 Ω each).
- Delay on tweeter: 120 µs (~0.12 ms) to align acoustic centers with the
  deeper woofer/mid cone plane. The WG212 waveguide recesses the tweeter
  dome behind the baffle surface, requiring this delay for time alignment.

## To Load on MiniDSP

1. Open MiniDSP 4×10 HD plugin
2. Connect to device
3. File → Import → choose XML
4. Upload to device
5. Verify with pink noise + REW measurement
6. Fine-tune delay and gain based on measured response
