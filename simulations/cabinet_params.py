"""
Cabinet parameters — parsed from cad/cabinet.scad (single source of truth).

This module extracts key cabinet dimensions from the OpenSCAD model and
provides derived values for simulations. All simulation scripts must import
from here instead of hardcoding dimensions.

Cabinet.scad is the authoritative source for ALL physical dimensions.
If a dimension changes in cabinet.scad, this module picks it up automatically.
The CI check (check_cabinet_params) verifies the parse is consistent.

Baffle step model:
  - Woofers are SIDE-mounted on the cabinet side panels (D x H).
    Effective baffle radius = D/2 (half the depth, the nearest edge).
  - Mid and tweeter are FRONT-mounted on the front baffle (W x H).
    Effective baffle radius = W/2 (half the width, the nearest edge).
  - The front baffle has rounded vertical edges (round_r) which reduce
    edge diffraction but do not significantly change the baffle step
    frequency — we use the full width W for the effective radius.

Layout (from cabinet.scad):
  - Woofer pair: side panels, push-push, z = woofer_z mm
  - Midrange:    front baffle,  z = mid_z mm (top)
  - Tweeter/WG:  front baffle,  z = tw_z = mid_z - cc mm (below mid)
"""
import os
import re
import numpy as np

# Speed of sound (must match other simulation scripts)
C_SPEED = 343.0

# ============================================================
#  Parse cabinet.scad
# ============================================================
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
_CABINET_SCAD = os.path.join(_REPO_ROOT, "cad", "cabinet.scad")


def _parse_scad_variable(text, var_name):
    """Extract a numeric variable from OpenSCAD source.

    Handles patterns like:
        W       = 300;   // comment
        woofer_z = 520;  // comment
    """
    pattern = rf"^\s*{re.escape(var_name)}\s*=\s*([0-9.]+)\s*;"
    for line in text.splitlines():
        m = re.match(pattern, line)
        if m:
            return float(m.group(1))
    return None


def _load_cabinet_params():
    """Parse cabinet.scad and return a dict of key dimensions."""
    with open(_CABINET_SCAD) as f:
        scad_text = f.read()

    params = {}
    variables = [
        "W", "D", "H", "wall", "round_r",
        "woofer_z", "mid_z", "cc",
        "woofer_cut_d", "woofer_depth",
        "woofer_Fs", "woofer_Qts", "woofer_Vas_L",
        "woofer_displ_L",
    ]
    for var in variables:
        val = _parse_scad_variable(scad_text, var)
        if val is None:
            raise ValueError(
                f"Could not parse '{var}' from cabinet.scad — "
                f"check that it is a simple numeric assignment."
            )
        params[var] = val

    # Derived dimensions
    params["tw_z"] = params["mid_z"] - params["cc"]
    params["w_in"] = params["W"] - 2 * params["wall"]
    params["d_in"] = params["D"] - 2 * params["wall"]
    params["h_in"] = params["H"] - 2 * params["wall"]
    params["flat_front_w"] = params["W"] - 2 * params["round_r"]

    # Effective baffle radii [meters] for baffle step calculation
    # Side-mounted woofers: nearest edge is front/rear of side panel = D/2
    # Front-mounted mid/tweeter: nearest edge is left/right of front baffle = W/2
    params["a_side_m"] = params["D"] / 2.0 / 1000.0   # → 0.190 m
    params["a_front_m"] = params["W"] / 2.0 / 1000.0  # → 0.160 m

    # Baffle step frequencies [Hz]
    params["f_bs_side"] = C_SPEED / (2 * np.pi * params["a_side_m"])
    params["f_bs_front"] = C_SPEED / (2 * np.pi * params["a_front_m"])

    return params


# Load at import time — fails fast if cabinet.scad is missing or broken
PARAMS = _load_cabinet_params()

# Expose as module-level constants for convenience
W = PARAMS["W"]               # external width [mm]
D = PARAMS["D"]               # external depth [mm]
H = PARAMS["H"]               # external height [mm]
WALL = PARAMS["wall"]         # panel thickness [mm]
ROUND_R = PARAMS["round_r"]   # front roundover radius [mm]
WOOFER_Z = PARAMS["woofer_z"] # woofer centre height [mm]
MID_Z = PARAMS["mid_z"]       # midrange centre height [mm]
TW_Z = PARAMS["tw_z"]         # tweeter/waveguide centre height [mm]
CC = PARAMS["cc"]             # mid-tweeter centre-to-centre [mm]
W_IN = PARAMS["w_in"]         # internal width [mm]
D_IN = PARAMS["d_in"]         # internal depth [mm]
H_IN = PARAMS["h_in"]         # internal height [mm]
FLAT_FRONT_W = PARAMS["flat_front_w"]  # flat front baffle width [mm]
A_SIDE_M = PARAMS["a_side_m"]     # side baffle effective radius [m]
A_FRONT_M = PARAMS["a_front_m"]   # front baffle effective radius [m]
F_BS_SIDE = PARAMS["f_bs_side"]   # side baffle step frequency [Hz]
F_BS_FRONT = PARAMS["f_bs_front"] # front baffle step frequency [Hz]


# ============================================================
#  Baffle step functions (Vanderkooy single-pole model)
# ============================================================
def baffle_step_db_side(f):
    """Baffle step for side-mounted woofers (D/2 effective radius).

    At low frequencies: -6 dB (4π radiation, full space).
    At high frequencies:  0 dB (2π radiation, half space into side).
    Transition at f_bs_side ≈ 259 Hz (D=420mm).
    """
    fbs = F_BS_SIDE
    x = 1j * f / fbs
    return 20 * np.log10(np.abs((0.5 + x) / (1 + x)) + 1e-12)


def baffle_step_db_front(f):
    """Baffle step for front-mounted mid/tweeter (W/2 effective radius).

    At low frequencies: -6 dB (4π radiation, full space).
    At high frequencies:  0 dB (2π radiation, half space toward listener).
    Transition at f_bs_front ≈ 364 Hz (W=300mm).
    """
    fbs = F_BS_FRONT
    x = 1j * f / fbs
    return 20 * np.log10(np.abs((0.5 + x) / (1 + x)) + 1e-12)


# Backward-compatible alias: baffle_step_db uses front baffle by default
# (most legacy scripts applied it to all drivers — new scripts should use
#  the specific side/front functions)
def baffle_step_db(f, a=0.160):
    """Generic baffle step with custom effective radius [meters].

    For new code, prefer baffle_step_db_side() or baffle_step_db_front().
    """
    fbs = C_SPEED / (2 * np.pi * a)
    x = 1j * f / fbs
    return 20 * np.log10(np.abs((0.5 + x) / (1 + x)) + 1e-12)


# ============================================================
#  Validation (called by CI check)
# ============================================================
def validate():
    """Re-parse cabinet.scad and verify all values are consistent.

    Returns a list of human-readable status lines.
    Raises AssertionError if any value is missing or implausible.
    """
    lines = []
    p = _load_cabinet_params()

    checks = [
        ("External width W", p["W"], 200, 500),
        ("External depth D", p["D"], 250, 600),
        ("External height H", p["H"], 500, 2000),
        ("Wall thickness", p["wall"], 15, 35),
        ("Roundover radius", p["round_r"], 5, 50),
        ("Woofer centre height", p["woofer_z"], 200, 1000),
        ("Midrange centre height", p["mid_z"], 500, 2000),
        ("Mid-tweeter C-C distance", p["cc"], 100, 300),
        ("Woofer cutout diameter", p["woofer_cut_d"], 200, 400),
    ]
    for label, val, lo, hi in checks:
        status = "OK" if lo <= val <= hi else "FAIL"
        lines.append(f"  {label}: {val} mm [{status}]")
        assert lo <= val <= hi, f"{label} = {val} is outside expected range [{lo}, {hi}]"

    lines.append(f"  Front baffle radius: {p['a_front_m']*1000:.1f} mm → f_bs = {p['f_bs_front']:.0f} Hz")
    lines.append(f"  Side baffle radius:  {p['a_side_m']*1000:.1f} mm → f_bs = {p['f_bs_side']:.0f} Hz")
    lines.append(f"  Front flat width: {p['flat_front_w']:.0f} mm (W - 2×round_r)")

    return lines


if __name__ == "__main__":
    print("=" * 60)
    print("Cabinet parameters from cad/cabinet.scad")
    print("=" * 60)
    for line in validate():
        print(line)
    print()
    print(f"  Internal: {W_IN:.0f} × {D_IN:.0f} × {H_IN:.0f} mm")
    print(f"  Mid z={MID_Z:.0f} mm, Tweeter z={TW_Z:.0f} mm, Woofer z={WOOFER_Z:.0f} mm")
    print()
    print("All values OK.")
