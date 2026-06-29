#!/usr/bin/env python3
"""
Generate full 16-view gallery locally.
Run: python3 scripts/render_all_views.py
"""
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

VIEWS = [
    # Waveguide (6 views)
    ("cad/mk2_waveguide_os.scad", "assets/renders/waveguide_mouth.png", 
     "--camera=0,0,45,0,0,0,600 --projection=ortho", []),
    ("cad/mk2_waveguide_os.scad", "assets/renders/waveguide_rear.png",
     "--camera=0,0,45,180,0,0,600 --projection=ortho", []),
    ("cad/mk2_waveguide_os.scad", "assets/renders/waveguide_side.png",
     "--camera=0,0,45,90,0,90,600 --projection=ortho", []),
    ("cad/mk2_waveguide_os.scad", "assets/renders/waveguide_top.png",
     "--camera=0,0,45,0,0,180,600 --projection=ortho", []),
    ("cad/mk2_waveguide_os.scad", "assets/renders/waveguide_iso.png",
     "--camera=200,-200,120,55,0,35,700", []),
    ("cad/mk2_waveguide_os.scad", "assets/renders/waveguide_cutaway.png",
     "--camera=0,0,45,90,0,90,600 --projection=ortho", ["show_cutaway=true"]),
    
    # Cabinet (10 views)
    ("cad/cabinet.scad", "assets/renders/cabinet_front.png",
     "--camera=0,200,540,0,0,0,1800 --projection=ortho", ["show_drivers=true"]),
    ("cad/cabinet.scad", "assets/renders/cabinet_rear.png",
     "--camera=0,-200,540,180,0,0,1800 --projection=ortho", []),
    ("cad/cabinet.scad", "assets/renders/cabinet_left.png",
     "--camera=0,90,540,0,-90,0,1400 --projection=ortho", ["show_drivers=true"]),
    ("cad/cabinet.scad", "assets/renders/cabinet_right.png",
     "--camera=0,90,540,0,90,0,1400 --projection=ortho", ["show_drivers=true"]),
    ("cad/cabinet.scad", "assets/renders/cabinet_top.png",
     "--camera=0,90,540,0,0,180,1800 --projection=ortho", []),
    ("cad/cabinet.scad", "assets/renders/cabinet_bottom.png",
     "--camera=0,90,540,0,180,0,1800 --projection=ortho", []),
    ("cad/cabinet.scad", "assets/renders/cabinet_exterior.png",
     "--camera=500,500,900,60,0,45,2000", ["show_drivers=true"]),
    ("cad/cabinet.scad", "assets/renders/cabinet_cutaway.png",
     "--camera=0,90,540,70,0,0,1600", ["show_internals=true", "show_drivers=true"]),
    ("cad/cabinet.scad", "assets/renders/cabinet_assembly.png",
     "--camera=400,500,700,70,0,20,1800", ["show_drivers=true", "show_waveguide=true"]),
    ("cad/cabinet.scad", "assets/renders/cabinet_full_cutaway.png",
     "--camera=400,400,700,65,0,35,1800", ["show_internals=true", "show_waveguide=true", "show_drivers=true"]),
]

def render(args):
    scad, output, camera, defs = args
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = f"openscad --render {camera} --imgsize=1920,1080 --colorscheme=Cornfield -o {output}"
    for d in defs:
        cmd += f" -D '{d}'"
    cmd += f" {scad}"
    
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return (output.name, result.returncode == 0)

if __name__ == "__main__":
    print(f"Rendering {len(VIEWS)} views with 4 workers...")
    with ProcessPoolExecutor(4) as exe:
        results = list(exe.map(render, VIEWS))
    
    ok = sum(1 for _, s in results if s)
    print(f"Done: {ok}/{len(VIEWS)}")
    for name, ok in results:
        print(f"  {'✓' if ok else '✗'} {name}")
