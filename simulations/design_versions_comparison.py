"""
Mk2 Reference Loudspeaker - design versions comparison table
============================================================

Generates a summary comparison of all design versions (v1 through v6b) in
both CSV and Markdown formats, covering the key acoustic and physical parameters
that changed between versions.

This is a data-entry script: the numbers come directly from the repo's design
history (ROADMAP.md, DESIGN_DECISIONS.md, docs/).  No physics is calculated here
— the table is a condensed record of decisions made at each stage.

Output:
  simulations/csv/design_versions.csv
  simulations/design_versions.md   (Markdown table for docs/README)
"""
import os

# ---------------------------------------------------------------------------
#  Version data
#  Fields:
#    version, status, cabinet_w, cabinet_h, cabinet_d, wall,
#    front_roundover_R, woofer, woofer_qty, mid, tweeter, waveguide,
#    xover_bass_hz, xover_mid_hz, cc_mm, bass_vol_L, mid_vol_L,
#    Qtc, Fc_hz, notes
# ---------------------------------------------------------------------------
VERSIONS = [
    {
        "version": "v1",
        "status": "concept",
        "cabinet_W_mm": 300, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 50,
        "woofer": "SB23NRXS45-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1600,
        "cc_mid_tw_mm": 150,
        "bass_vol_L": 69.0, "mid_vol_L": 5.7,
        "Qtc": 0.56, "Fc_Hz": 31.9,
        "notes": "Initial concept with SB23 woofer; directivity investigation started"
    },
    {
        "version": "v2",
        "status": "concept",
        "cabinet_W_mm": 300, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 50,
        "woofer": "SB23NRXS45-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1500,
        "cc_mid_tw_mm": 150,
        "bass_vol_L": 69.0, "mid_vol_L": 5.7,
        "Qtc": 0.56, "Fc_Hz": 31.9,
        "notes": "Cabinet geometry defined; side-mounted push-push woofer layout introduced"
    },
    {
        "version": "v3",
        "status": "investigation",
        "cabinet_W_mm": 300, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 50,
        "woofer": "GRS 8SW-4HE-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1500,
        "cc_mid_tw_mm": 150,
        "bass_vol_L": 69.0, "mid_vol_L": 5.7,
        "Qtc": 0.62, "Fc_Hz": 34.5,
        "notes": "GRS 8SW-4HE-8 introduced as woofer candidate; strong sealed alignment fit"
    },
    {
        "version": "v4",
        "status": "exploration",
        "cabinet_W_mm": 280, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 40,
        "woofer": "GRS 8SW-4HE-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1400,
        "cc_mid_tw_mm": 150,
        "bass_vol_L": 65.0, "mid_vol_L": 5.7,
        "Qtc": 0.65, "Fc_Hz": 35.8,
        "notes": "Narrower 280 mm front explored; R40 roundover useful but mechanically constrained"
    },
    {
        "version": "v5",
        "status": "candidate",
        "cabinet_W_mm": 300, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 50,
        "woofer": "GRS 8SW-4HE-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1300,
        "cc_mid_tw_mm": 150,
        "bass_vol_L": 68.0, "mid_vol_L": 5.7,
        "Qtc": 0.63, "Fc_Hz": 34.8,
        "notes": "300 mm / R50 selected; 68 L bass volume"
    },
    {
        "version": "v6",
        "status": "candidate",
        "cabinet_W_mm": 300, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 50,
        "woofer": "GRS 8SW-4HE-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1250,
        "cc_mid_tw_mm": 140,
        "bass_vol_L": 69.0, "mid_vol_L": 5.7,
        "Qtc": 0.62, "Fc_Hz": 34.5,
        "notes": "Directivity optimization; c-c 140 mm target; WG212–WG240 compared"
    },
    {
        "version": "v6b",
        "status": "CURRENT REFERENCE",
        "cabinet_W_mm": 300, "cabinet_H_mm": 370, "cabinet_D_mm": 1080,
        "wall_mm": 22, "front_roundover_R_mm": 50,
        "woofer": "GRS 8SW-4HE-8", "woofer_qty": 2,
        "mid": "ScanSpeak 15W/4434G00",
        "tweeter": "ScanSpeak H2606/920000",
        "waveguide": "WG212",
        "xover_bass_Hz": 150, "xover_mid_Hz": 1250,
        "cc_mid_tw_mm": 150,
        "bass_vol_L": 69.0, "mid_vol_L": 5.7,
        "Qtc": 0.62, "Fc_Hz": 34.5,
        "notes": ("c-c 150 mm practical minimum (15W frame). WG212 CAD + cabinet CAD complete. "
                  "1250 Hz target subject to WG212 distortion test (tweeter Fs 1030 Hz). "
                  "Fallback: 1350-1450 Hz if 1250 Hz fails.")
    },
]

# ---------------------------------------------------------------------------
#  CSV
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(out_dir, exist_ok=True)
csv_path = os.path.join(out_dir, "design_versions.csv")

fields = list(VERSIONS[0].keys())
rows = [",".join(fields)]
for v in VERSIONS:
    rows.append(",".join(str(v[k]).replace(",", ";") for k in fields))
with open(csv_path, "w") as fh:
    fh.write("\n".join(rows) + "\n")
print("wrote", csv_path)

# ---------------------------------------------------------------------------
#  Markdown table
# ---------------------------------------------------------------------------
md_path = os.path.join(os.path.dirname(__file__), "design_versions.md")

def row(cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"

md = [
    "# Mk2 Reference Loudspeaker — Design Versions Comparison",
    "",
    ("Auto-generated by `simulations/design_versions_comparison.py`. "
     "Numbers from ROADMAP.md and design decision log."),
    "",
    "## Physical",
    "",
    row(["Version", "Status", "Cabinet (W×H×D mm)", "Wall", "R-front", "Bass vol (L)", "Mid vol (L)"]),
    row(["---"] * 7),
]
for v in VERSIONS:
    cab = f"{v['cabinet_W_mm']}×{v['cabinet_H_mm']}×{v['cabinet_D_mm']}"
    md.append(row([
        f"**{v['version']}**", v["status"],
        cab, f"{v['wall_mm']} mm", f"R{v['front_roundover_R_mm']}",
        v["bass_vol_L"], v["mid_vol_L"]
    ]))

md += [
    "",
    "## Drivers & crossovers",
    "",
    row(["Version", "Woofer", "Qty", "Midrange", "Tweeter", "Waveguide",
         "Xover bass", "Xover mid/tw", "c-c (mm)"]),
    row(["---"] * 9),
]
for v in VERSIONS:
    md.append(row([
        f"**{v['version']}**",
        v["woofer"], v["woofer_qty"],
        v["mid"], v["tweeter"], v["waveguide"],
        f"{v['xover_bass_Hz']} Hz LR4",
        f"{v['xover_mid_Hz']} Hz LR4",
        v["cc_mid_tw_mm"],
    ]))

md += [
    "",
    "## Bass alignment (2× driver, sealed)",
    "",
    row(["Version", "Qtc", "Fc (Hz)", "Notes"]),
    row(["---"] * 4),
]
for v in VERSIONS:
    md.append(row([f"**{v['version']}**", v["Qtc"], v["Fc_Hz"], v["notes"]]))

md += [
    "",
    ("---"),
    "",
    ("*Measurements will be added to this table once the prototype is built. "
     "Until then all values are design targets, not validated data.*"),
]

with open(md_path, "w") as fh:
    fh.write("\n".join(md) + "\n")
print("wrote", md_path)
