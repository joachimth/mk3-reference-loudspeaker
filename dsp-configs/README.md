# MiniDSP 4×10 HD Configurations for Mk3 Reference Loudspeaker

This directory holds MiniDSP 4×10 HD XML configuration files for active DSP
crossover / EQ on the Mk3 loudspeaker. Each XML file is a complete plugin
configuration that can be loaded via MiniDSP's plugin software.

## Current Configs

| File | Crossover | Status |
|---|---|---|
| `mk3-sb26stac-1100hz.xml` | 150 Hz LR4 + 1100 Hz LR4 | ✅ Design target |
| ... | (add more as measurements refine) | |

A reusable generator is provided: `generate_minidsp_xml.py` (3-way + push-push
woofer, 2-way, subsonic HP, Linkwitz Transform, variable sample rate, per-channel
gain/delay). Biquad coefficients can be generated with `generate_biquads.py`.

## Input → Output Mapping

MiniDSP 4×10 HD has 1 stereo input (2 channels) and 10 outputs. Per-speaker
biamp setup (one MiniDSP per speaker pair, or a single MiniDSP with 5 channels
per side):

### Left Speaker
| Input | Output | Driver | Filter |
|---|---|---|---|
| CH1 (Left) | Out 1 → Woofer L+ | GRS 12SW-4HE (first) | Subsonic HP 18 Hz LR4, Linkwitz Transform (39→28 Hz, Q 0.76→0.707), LP 150 Hz LR4 |
| CH1 (Left) | Out 2 → Woofer L- | GRS 12SW-4HE (second) | Same as Out 1 (wired in series = 8Ω) |
| CH1 (Left) | Out 3 → Mid L | 15W/4434G00 | HP 150 Hz LR4, LP 1100 Hz LR4 |
| CH1 (Left) | Out 4 → Tweeter L | SB26STAC in waveguide | HP 1100 Hz LR4, level trim ~-1.8 dB |
| CH1 (Left) | Out 5 → Tweeter L (#2) | — | Spare / biamp |

### Right Speaker
| CH2 (Right) | Out 6 → Woofer R+ | (same as left) |
|---|---|---|
| CH2 (Right) | Out 7 → Woofer R- | (same as left) |
| CH2 (Right) | Out 8 → Mid R | (same as left) |
| CH2 (Right) | Out 9 → Tweeter R | (same as left) |
| CH2 (Right) | Out 10 | Spare |

## Wiring Notes

- Two GRS 12SW-4HE woofers per speaker, wired in **series** → 8 Ω load.
- Each woofer gets its own output channel for individual EQ/delay if needed,
  or they can share a channel and be wired in parallel (2 Ω — verify amp stability).
- **Default config: series wiring, individual channels with identical filters.**
  This allows DSP-based polarity flip or individual excursion limiting later.

## To Load

1. Open MiniDSP 4×10 HD plugin
2. Connect to device
3. File → Import → choose XML
4. Upload to device
5. Verify with pink noise + REW measurement
