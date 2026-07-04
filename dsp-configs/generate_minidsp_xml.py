#!/usr/bin/env python3
"""
MiniDSP 4×10 HD XML Config Generator

Generates a complete plug-in XML config from a speaker crossover specification.
The XML can be imported directly into the MiniDSP 4×10 HD plugin via File → Import.

Usage:
    # Generate the mk2 crossover config
    python generate_minidsp_xml.py > mk2-150-1250-lr4.xml

    # Custom crossover
    python generate_minidsp_xml.py \
        --sample-rate 96000 \
        --woofer-lp 150 --woofer-lp-type lr4 \
        --mid-hp 150 --mid-hp-type lr4 --mid-lp 1250 --mid-lp-type lr4 \
        --tweeter-hp 1250 --tweeter-hp-type lr4 \
        --tweeter-trim -5.5 \
        --subsonic-hp 18
"""

import argparse
import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Biquad computation (96 kHz reference unless overridden)
# ---------------------------------------------------------------------------

def butterworth_lowpass(fc: float, fs: float) -> tuple[float, float, float, float, float]:
    """2nd-order Butterworth lowpass biquad coefficients."""
    Q = 1 / math.sqrt(2)
    w0 = 2 * math.pi * fc / fs
    alpha = math.sin(w0) / (2 * Q)
    cosw0 = math.cos(w0)

    b0 = (1 - cosw0) / 2
    b1 = 1 - cosw0
    b2 = (1 - cosw0) / 2
    a0 = 1 + alpha
    a1 = -2 * cosw0
    a2 = 1 - alpha

    return (b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def butterworth_highpass(fc: float, fs: float) -> tuple[float, float, float, float, float]:
    """2nd-order Butterworth highpass biquad coefficients."""
    Q = 1 / math.sqrt(2)
    w0 = 2 * math.pi * fc / fs
    alpha = math.sin(w0) / (2 * Q)
    cosw0 = math.cos(w0)

    b0 = (1 + cosw0) / 2
    b1 = -(1 + cosw0)
    b2 = (1 + cosw0) / 2
    a0 = 1 + alpha
    a1 = -2 * cosw0
    a2 = 1 - alpha

    return (b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def build_lr4_lowpass(fc: float, fs: float) -> list[tuple[float, float, float, float, float]]:
    """LR4 lowpass = two cascaded BW2 sections."""
    s = butterworth_lowpass(fc, fs)
    return [s, s]


def build_lr4_highpass(fc: float, fs: float) -> list[tuple[float, float, float, float, float]]:
    """LR4 highpass = two cascaded BW2 sections."""
    s = butterworth_highpass(fc, fs)
    return [s, s]


def build_linkwitz_transform(
    fc: float, Qc: float, fs_target: float, Q_target: float, sample_rate: float
) -> tuple[float, float, float, float, float]:
    """
    Linkwitz Transform biquad.
    Peforms Fc/Qc → Fs/Qc transformation for baffle-step / bass alignment.

    Coefficients from: https://www.linkwitzlab.com/filters.htm
    """
    w0 = 2 * math.pi * fc / sample_rate
    cosw0 = math.cos(w0)
    sinw0 = math.sin(w0)
    alpha_act = sinw0 / (2 * Qc)
    alpha_target = sinw0 / (2 * Q_target)

    b0 = (1 + alpha_target * (fs_target / fc))
    b1 = -2 * cosw0
    b2 = (1 - alpha_target * (fs_target / fc))
    a0 = (1 + alpha_act)
    a1 = -2 * cosw0
    a2 = (1 - alpha_act)

    return (b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


# ---------------------------------------------------------------------------
# MiniDSP XML generation
# ---------------------------------------------------------------------------

@dataclass
class BiquadFilter:
    """A single biquad filter section with its metadata."""
    label: str
    coeffs: tuple[float, float, float, float, float]  # b0, b1, b2, a1, a2


@dataclass
class OutputChannel:
    """One output channel with its filter chain."""
    label: str
    gain_db: float = 0.0
    delay_ms: float = 0.0
    invert_polarity: bool = False
    biquads: list[BiquadFilter] = field(default_factory=list)


def build_mk2_config(
    sample_rate: int = 96000,
    woofer_lp: float = 150,
    woofer_lp_type: str = "lr4",
    mid_hp: float = 150,
    mid_hp_type: str = "lr4",
    mid_lp: float = 1250,
    mid_lp_type: str = "lr4",
    tweeter_hp: float = 1250,
    tweeter_hp_type: str = "lr4",
    tweeter_trim: float = -5.5,
    subsonic_hp: float = 18,
    subsonic_hp_type: str = "lr4",
    woofer_lt_fc: Optional[float] = 47.2,
    woofer_lt_fs: Optional[float] = 28.0,
    woofer_lt_qc: Optional[float] = 0.63,
    woofer_lt_qs: Optional[float] = 0.707,
) -> list[OutputChannel]:
    """Build the complete channel configuration for the Mk2 3-way + push-push woofer."""

    def wkz(label, coeffs):
        return BiquadFilter(label=label, coeffs=coeffs)

    # Build the biquad chains
    # Woofer chain: subsonic HP (LR4) + Linkwitz Transform + LP (LR4)
    woofer_biquads: list[BiquadFilter] = []

    if subsonic_hp and subsonic_hp > 0:
        if subsonic_hp_type == "lr4":
            for coeffs in build_lr4_highpass(subsonic_hp, sample_rate):
                woofer_biquads.append(wkz(f"Sub HP {subsonic_hp} LR4", coeffs))

    if woofer_lt_fc and woofer_lt_fs:
        coeffs = build_linkwitz_transform(
            fc=woofer_lt_fc, Qc=woofer_lt_qc or 0.63,
            fs_target=woofer_lt_fs, Q_target=woofer_lt_qs or 0.707,
            sample_rate=sample_rate,
        )
        woofer_biquads.append(wkz(f"LT {woofer_lt_fc}→{woofer_lt_fs}Hz Q{woofer_lt_qc}→{woofer_lt_qs}", coeffs))

    if woofer_lp and woofer_lp > 0:
        if woofer_lp_type == "lr4":
            for coeffs in build_lr4_lowpass(woofer_lp, sample_rate):
                woofer_biquads.append(wkz(f"LP {woofer_lp} LR4", coeffs))

    # Mid chain: HP (LR4) + LP (LR4)
    mid_biquads: list[BiquadFilter] = []
    if mid_hp and mid_hp > 0:
        if mid_hp_type == "lr4":
            for coeffs in build_lr4_highpass(mid_hp, sample_rate):
                mid_biquads.append(wkz(f"HP {mid_hp} LR4", coeffs))
    if mid_lp and mid_lp > 0:
        if mid_lp_type == "lr4":
            for coeffs in build_lr4_lowpass(mid_lp, sample_rate):
                mid_biquads.append(wkz(f"LP {mid_lp} LR4", coeffs))

    # Tweeter chain: HP (LR4) only
    tweeter_biquads: list[BiquadFilter] = []
    if tweeter_hp and tweeter_hp > 0:
        if tweeter_hp_type == "lr4":
            for coeffs in build_lr4_highpass(tweeter_hp, sample_rate):
                tweeter_biquads.append(wkz(f"HP {tweeter_hp} LR4", coeffs))

    # Delay estimation: ~0.12 ms for tweeter (acoustic offset, typical WG212 depth)
    # Woofer and mid share the same delay reference (0)
    # Tweeter is physically shallower → needs delayed by ~0.12 ms to align

    return [
        OutputChannel(label="GRS Woofer L Top",  gain_db=0.0,  delay_ms=0.0,    biquads=woofer_biquads),
        OutputChannel(label="GRS Woofer L Bot",  gain_db=0.0,  delay_ms=0.0,    biquads=woofer_biquads),
        OutputChannel(label="15W/4434G00 Mid L", gain_db=0.0,  delay_ms=0.0,    biquads=mid_biquads),
        OutputChannel(label="H2606 Tweeter L",   gain_db=tweeter_trim, delay_ms=0.12, biquads=tweeter_biquads),
        OutputChannel(label="(Spare input)",     gain_db=0.0,  delay_ms=0.0,    biquads=[]),
        OutputChannel(label="GRS Woofer R Top",  gain_db=0.0,  delay_ms=0.0,    biquads=woofer_biquads),
        OutputChannel(label="GRS Woofer R Bot",  gain_db=0.0,  delay_ms=0.0,    biquads=woofer_biquads),
        OutputChannel(label="15W/4434G00 Mid R", gain_db=0.0,  delay_ms=0.0,    biquads=mid_biquads),
        OutputChannel(label="H2606 Tweeter R",   gain_db=tweeter_trim, delay_ms=0.12, biquads=tweeter_biquads),
        OutputChannel(label="(Spare output)",    gain_db=0.0,  delay_ms=0.0,    biquads=[]),
    ]


def build_2way_config(
    sample_rate: int = 48000,
    woofer_hp: float = 0,
    woofer_hp_type: str = "lr4",
    woofer_lp: float = 2500,
    woofer_lp_type: str = "lr4",
    tweeter_hp: float = 2500,
    tweeter_hp_type: str = "lr4",
    tweeter_hp_slope: str = "lr4",
    tweeter_trim: float = -3.0,
) -> list[OutputChannel]:
    """Build a simple 2-way config."""
    woofer_biquads: list[BiquadFilter] = []
    if woofer_hp and woofer_hp > 0:
        if woofer_hp_type == "lr4":
            for c in build_lr4_highpass(woofer_hp, sample_rate):
                woofer_biquads.append(BiquadFilter(label=f"HP {woofer_hp} LR4", coeffs=c))
    if woofer_lp and woofer_lp > 0:
        if woofer_lp_type == "lr4":
            for c in build_lr4_lowpass(woofer_lp, sample_rate):
                woofer_biquads.append(BiquadFilter(label=f"LP {woofer_lp} LR4", coeffs=c))

    tweeter_biquads: list[BiquadFilter] = []
    if tweeter_hp and tweeter_hp > 0:
        if tweeter_hp_slope == "lr4":
            for c in build_lr4_highpass(tweeter_hp, sample_rate):
                tweeter_biquads.append(BiquadFilter(label=f"HP {tweeter_hp} LR4", coeffs=c))

    return [
        OutputChannel(label="Woofer L",  gain_db=0.0,          biquads=woofer_biquads),
        OutputChannel(label="Tweeter L", gain_db=tweeter_trim, biquads=tweeter_biquads),
        OutputChannel(label="Woofer R",  gain_db=0.0,          biquads=woofer_biquads),
        OutputChannel(label="Tweeter R", gain_db=tweeter_trim, biquads=tweeter_biquads),
    ]


# ---------------------------------------------------------------------------
# XML output (MiniDSP 4×10 HD plugin format)
# ---------------------------------------------------------------------------

def channel_to_xml(ch: OutputChannel, index: int) -> ET.Element:
    """Convert an OutputChannel to MiniDSP XML format."""
    out = ET.Element("output", attrib={"i": str(index)})

    # Basic settings
    mute = ET.SubElement(out, "mute")
    mute.text = "false"

    label = ET.SubElement(out, "label")
    label.text = ch.label

    gain = ET.SubElement(out, "gain")
    gain.text = f"{ch.gain_db:.1f}"

    delay = ET.SubElement(out, "delay")
    delay.text = f"{ch.delay_ms * 1000:.2f}"  # MiniDSP uses µs

    invert = ET.SubElement(out, "invert")
    invert.text = "true" if ch.invert_polarity else "false"

    # Biquad PEQ sections
    for biq_idx, bq in enumerate(ch.biquads):
        peq = ET.SubElement(out, "peq", attrib={
            "i": str(biq_idx),
            "type": "biquad",
            "enabled": "true",
        })

        # Label
        label_el = ET.SubElement(peq, "label")
        label_el.text = bq.label

        # Coefficients in MiniDSP order: b0 b1 b2 a1 a2
        b0, b1, b2, a1, a2 = bq.coeffs
        for coeff_name, coeff_val in [("b0", b0), ("b1", b1), ("b2", b2),
                                       ("a1", a1), ("a2", a2)]:
            el = ET.SubElement(peq, coeff_name)
            el.text = f"{coeff_val:.15f}"

    return out


def generate_xml(
    channels: list[OutputChannel],
    sample_rate: int = 96000,
    woofer_lp: float = 150,
    mid_hp: float = 150,
    mid_lp: float = 1250,
    tweeter_hp: float = 1250,
    subsonic_hp: float = 18,
    woofer_lt_fc: Optional[float] = 47.2,
    woofer_lt_fs: Optional[float] = 28.0,
) -> str:
    """Generate complete MiniDSP plugin XML from channel config."""
    root = ET.Element("minidsp")

    # Determine tweeter based on crossover frequency
    tweeter_name = "SB26STAC-C000-4" if tweeter_hp == 1100 else "ScanSpeak H2606 (WG212)"

    # Header
    header = ET.SubElement(root, "header")
    ET.SubElement(header, "name").text = "Mk2 Reference Loudspeaker"
    lt_str = f"LT {woofer_lt_fc}->{woofer_lt_fs}" if woofer_lt_fc and woofer_lt_fs else "no LT"
    desc_parts = [
        f"3-way + push-push woofer.",
        f"GRS 8SW-4HE-8 ×2 | ScanSpeak 15W/4434G00 | {tweeter_name}.",
        f"XO: {woofer_lp}/{mid_hp}-{mid_lp}/{tweeter_hp} Hz LR4.",
        f"Sub HP {subsonic_hp} Hz {lt_str}.",
        f"Sample rate: {sample_rate} Hz.",
        "Generated by generate_minidsp_xml.py",
    ]
    ET.SubElement(header, "description").text = " ".join(desc_parts)
    ET.SubElement(header, "plugin").text = "4x10HD"
    ET.SubElement(header, "version").text = "1"

    # Config info
    config = ET.SubElement(root, "config")
    ET.SubElement(config, "sample_rate").text = str(sample_rate)
    ET.SubElement(config, "input_routing").text = "stereo"  # stereo input
    ET.SubElement(config, "input_gain").text = "0.0"
    ET.SubElement(config, "output_config").text = "10ch"

    # Inputs (stereo)
    for inp_idx in range(2):
        inp = ET.SubElement(root, "input", attrib={"i": str(inp_idx)})
        ET.SubElement(inp, "mute").text = "false"
        ET.SubElement(inp, "label").text = f"Input {'L' if inp_idx == 0 else 'R'}"
        ET.SubElement(inp, "gain").text = "0.0"
        # Simple routing: input 0 → outputs 0-4, input 1 → outputs 5-9
        routing = ET.SubElement(inp, "routing")
        for out_idx in range(5):
            dest = ET.SubElement(routing, "dest")
            offset = inp_idx * 5 + out_idx
            ET.SubElement(dest, "output", attrib={"i": str(offset)}).text = str(offset)
            ET.SubElement(dest, "level").text = "0.0"

    # Outputs
    for idx, ch in enumerate(channels):
        if idx < 10:  # Max 10 outputs on 4x10 HD
            root.append(channel_to_xml(ch, idx))

    # Pretty print
    rough = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(rough.encode())
    return dom.toprettyxml(indent="  ")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate MiniDSP 4×10 HD XML config from crossover spec",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mk2 reference (default)
  python generate_minidsp_xml.py > mk2-150-1250-lr4.xml

  # Custom 2-way
  python generate_minidsp_xml.py --two-way --woofer-lp 2500 --tweeter-hp 2500 --tweeter-trim -3

  # Custom 3-way with SB26STAC (mk3 fallback)
  python generate_minidsp_xml.py \\
    --woofer-lp 150 \\
    --mid-hp 150 --mid-lp 1100 \\
    --tweeter-hp 1100 --tweeter-trim -1.0 \\
    --no-subsonic --no-lt
"""
    )

    parser.add_argument("--sample-rate", type=int, default=96000, help="Sample rate (Hz, default: 96000)")

    # Way configuration
    parser.add_argument("--two-way", action="store_true", dest="two_way", help="2-way config (default: 3-way)")

    # Woofer filters
    parser.add_argument("--woofer-lp", type=float, default=150, help="Woofer lowpass freq (Hz)")
    parser.add_argument("--woofer-lp-type", default="lr4", choices=["lr4", "lr2", "bw2", "bw4"])
    parser.add_argument("--subsonic-hp", type=float, default=18, help="Subsonic highpass freq (Hz)")
    parser.add_argument("--subsonic-hp-type", default="lr4", choices=["lr4", "lr2"])
    parser.add_argument("--no-subsonic", action="store_true", help="Skip subsonic filter")
    parser.add_argument("--no-lt", action="store_true", help="Skip Linkwitz Transform")

    # Mid filters (3-way only)
    parser.add_argument("--mid-hp", type=float, default=150, help="Mid highpass freq (Hz)")
    parser.add_argument("--mid-hp-type", default="lr4", choices=["lr4", "lr2", "bw2", "bw4"])
    parser.add_argument("--mid-lp", type=float, default=1250, help="Mid lowpass freq (Hz)")
    parser.add_argument("--mid-lp-type", default="lr4", choices=["lr4", "lr2", "bw2", "bw4"])

    # Tweeter filters
    parser.add_argument("--tweeter-hp", type=float, default=1250, help="Tweeter highpass freq (Hz)")
    parser.add_argument("--tweeter-hp-type", default="lr4", choices=["lr4", "lr2", "bw2", "bw4"])
    parser.add_argument("--tweeter-trim", type=float, default=-5.5, help="Tweeter gain trim (dB)")

    args = parser.parse_args()

    sr = args.sample_rate

    if args.no_subsonic:
        sub_hp = 0
    else:
        sub_hp = args.subsonic_hp

    if args.two_way:
        channels = build_2way_config(
            sample_rate=sr,
            woofer_lp=args.woofer_lp,
            woofer_lp_type=args.woofer_lp_type,
            tweeter_hp=args.tweeter_hp,
            tweeter_hp_slope=args.tweeter_hp_type,
            tweeter_trim=args.tweeter_trim,
        )
    else:
        channels = build_mk2_config(
            sample_rate=sr,
            woofer_lp=args.woofer_lp,
            woofer_lp_type=args.woofer_lp_type,
            mid_hp=args.mid_hp,
            mid_hp_type=args.mid_hp_type,
            mid_lp=args.mid_lp,
            mid_lp_type=args.mid_lp_type,
            tweeter_hp=args.tweeter_hp,
            tweeter_hp_type=args.tweeter_hp_type,
            tweeter_trim=args.tweeter_trim,
            subsonic_hp=sub_hp,
            woofer_lt_fc=None if args.no_lt else 47.2,
            woofer_lt_fs=None if args.no_lt else 28.0,
        )

    # Pass the actual filter values used for the description
    woofer_lp_val = args.woofer_lp
    mid_hp_val = args.mid_hp if not args.two_way else 0
    mid_lp_val = args.mid_lp if not args.two_way else 0
    tweeter_hp_val = args.tweeter_hp
    sub_hp_val = 0 if args.no_subsonic else args.subsonic_hp
    lt_fc_val = None if args.no_lt else 47.2
    lt_fs_val = None if args.no_lt else 28.0

    xml = generate_xml(channels, sr,
                       woofer_lp=woofer_lp_val,
                       mid_hp=mid_hp_val,
                       mid_lp=mid_lp_val,
                       tweeter_hp=tweeter_hp_val,
                       subsonic_hp=sub_hp_val,
                       woofer_lt_fc=lt_fc_val,
                       woofer_lt_fs=lt_fs_val)
    print(xml)


if __name__ == "__main__":
    main()
