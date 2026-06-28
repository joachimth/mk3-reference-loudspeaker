#!/usr/bin/env python3
"""
CAD render orchestrator for Mk2 Reference Loudspeaker.
Uses OpenSCAD with reusable process pools for faster batch rendering.
"""
import subprocess
import sys
import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse

# Camera definitions: (name, tx, ty, tz, rx, ry, rz, distance, projection, extra_defs)
WAVEGUIDE_VIEWS = [
    ("mouth", 0, 0, 45, 0, 0, 0, 600, "ortho", []),
    ("rear", 0, 0, 45, 180, 0, 0, 600, "ortho", []),
    ("side", 0, 0, 45, 90, 0, 90, 600, "ortho", []),
    ("top", 0, 0, 45, 0, 0, 180, 600, "ortho", []),
    ("iso", 200, -200, 120, 55, 0, 35, 700, "perspective", []),
    ("cutaway", 0, 0, 45, 90, 0, 90, 600, "ortho", ["show_cutaway=true"]),
]

CABINET_VIEWS = [
    ("front", 0, 200, 540, 0, 0, 0, 1800, "ortho", ["show_drivers=true"]),
    ("rear", 0, -200, 540, 180, 0, 0, 1800, "ortho", []),
    ("left", 0, 90, 540, 0, -90, 0, 1400, "ortho", ["show_drivers=true"]),
    ("right", 0, 90, 540, 0, 90, 0, 1400, "ortho", ["show_drivers=true"]),
    ("top", 0, 90, 540, 0, 0, 180, 1800, "ortho", []),
    ("bottom", 0, 90, 540, 0, 180, 0, 1800, "ortho", []),
    ("exterior", 500, 500, 900, 60, 0, 45, 2000, "perspective", ["show_drivers=true"]),
    ("cutaway", 0, 90, 540, 70, 0, 0, 1600, "perspective", ["show_internals=true", "show_drivers=true"]),
    ("assembly", 400, 500, 700, 70, 0, 20, 1800, "perspective", ["show_drivers=true", "show_waveguide=true"]),
    ("full_cutaway", 400, 400, 700, 65, 0, 35, 1800, "perspective", ["show_internals=true", "show_waveguide=true", "show_drivers=true"]),
]


def render_single(args):
    """Render a single view. Designed to be run in parallel processes."""
    scad_file, output_dir, name, tx, ty, tz, rx, ry, rz, dist, projection, extra_defs = args
    
    output_file = Path(output_dir) / f"{name}.png"
    
    # Build command
    cmd = [
        "xvfb-run", "-a",  # virtual display for headless
        "openscad",
        "--render",
        "--camera", f"{tx},{ty},{tz},{rx},{ry},{rz},{dist}",
        "--imgsize", "1920,1080",
        "--colorscheme", "Cornfield",
        "--projection", projection,
        "-o", str(output_file),
    ]
    
    # Add variable definitions
    for d in extra_defs:
        cmd.extend(["-D", d])
    
    cmd.append(scad_file)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 min timeout per render
        )
        if result.returncode == 0:
            return (name, True, str(output_file), None)
        else:
            return (name, False, None, result.stderr)
    except subprocess.TimeoutExpired:
        return (name, False, None, "Timeout after 300s")
    except Exception as e:
        return (name, False, None, str(e))


def render_batch(scad_file, output_dir, views, max_workers=4):
    """Render a batch of views in parallel."""
    scad_file = Path(scad_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build argument tuples for each render
    render_args = [
        (scad_file, output_dir, name, tx, ty, tz, rx, ry, rz, dist, proj, defs)
        for name, tx, ty, tz, rx, ry, rz, dist, proj, defs in views
    ]
    
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(render_single, arg): arg for arg in render_args}
        
        for future in as_completed(futures):
            name, success, path, error = future.result()
            if success:
                print(f"✓ {name}")
                results.append((name, path))
            else:
                print(f"✗ {name}: {error}")
                results.append((name, None))
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Batch CAD renderer for Mk2")
    parser.add_argument("--waveguide-only", action="store_true", help="Render only waveguide")
    parser.add_argument("--cabinet-only", action="store_true", help="Render only cabinet")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers (default: 4)")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    cad_dir = base_dir / "cad"
    output_dir = base_dir / "assets" / "renders"
    
    all_results = []
    
    if not args.cabinet_only:
        print("Rendering waveguide views (6 images)...")
        wg_file = cad_dir / "mk2_waveguide_os.scad"
        if wg_file.exists():
            results = render_batch(wg_file, output_dir, WAVEGUIDE_VIEWS, args.workers)
            all_results.extend(results)
        else:
            print(f"Waveguide file not found: {wg_file}")
    
    if not args.waveguide_only:
        print("Rendering cabinet views (10 images)...")
        cab_file = cad_dir / "cabinet.scad"
        if cab_file.exists():
            results = render_batch(cab_file, output_dir, CABINET_VIEWS, args.workers)
            all_results.extend(results)
        else:
            print(f"Cabinet file not found: {cab_file}")
    
    # Summary
    success = sum(1 for _, r in all_results if r is not None)
    total = len(all_results)
    print(f"\nDone: {success}/{total} renders successful")
    
    return 0 if success == total else 1


if __name__ == "__main__":
    sys.exit(main())
