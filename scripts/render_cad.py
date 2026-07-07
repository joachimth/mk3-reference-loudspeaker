#!/usr/bin/env python3
"""
CAD render orchestrator for Mk3 Reference Loudspeaker.
Groups STL + PNG renders per model for efficient parallelization.
"""
import subprocess
import sys
import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class RenderJob:
    name: str
    scad_file: Path
    output_file: Path
    is_stl: bool
    camera: Optional[Tuple] = None
    projection: str = "ortho"
    extra_defs: List[str] = None
    
    def __post_init__(self):
        if self.extra_defs is None:
            self.extra_defs = []


def build_job_list(cad_dir: Path, output_dir: Path, exports_dir: Path) -> List[RenderJob]:
    """Build complete job list: STL exports + PNG renders for both models."""
    jobs = []
    
    # Waveguide model
    wg_scad = cad_dir / "waveguide.scad"
    wg_stl = exports_dir / "waveguide.stl"
    
    # Waveguide STL
    jobs.append(RenderJob(
        name="wg_stl",
        scad_file=wg_scad,
        output_file=wg_stl,
        is_stl=True
    ))
    
    # Waveguide PNGs: (name, tx, ty, tz, rx, ry, rz, distance, projection, extra_defs)
    wg_views = [
        ("waveguide_mouth", 0, 0, 45, 0, 0, 0, 600, "ortho", []),
        ("waveguide_rear", 0, 0, 45, 180, 0, 0, 600, "ortho", []),
        ("waveguide_side", 0, 0, 45, 90, 0, 90, 600, "ortho", []),
        ("waveguide_top", 0, 0, 45, 0, 0, 180, 600, "ortho", []),
        ("waveguide_iso", 200, -200, 120, 55, 0, 35, 700, "perspective", []),
        ("waveguide_cutaway", 0, 0, 45, 90, 0, 90, 600, "ortho", ["show_cutaway=true"]),
    ]
    
    for name, tx, ty, tz, rx, ry, rz, dist, proj, defs in wg_views:
        jobs.append(RenderJob(
            name=name,
            scad_file=wg_scad,
            output_file=output_dir / f"{name}.png",
            is_stl=False,
            camera=(tx, ty, tz, rx, ry, rz, dist),
            projection=proj,
            extra_defs=defs
        ))
    
    # Cabinet model
    cab_scad = cad_dir / "cabinet.scad"
    cab_stl = exports_dir / "cabinet.stl"
    
    # Cabinet STL
    jobs.append(RenderJob(
        name="cab_stl",
        scad_file=cab_scad,
        output_file=cab_stl,
        is_stl=True
    ))
    
    # Cabinet PNGs
    cab_views = [
        ("cabinet_front", 0, 200, 540, 0, 0, 0, 1800, "ortho", ["show_drivers=true"]),
        ("cabinet_rear", 0, -200, 540, 180, 0, 0, 1800, "ortho", []),
        ("cabinet_left", 0, 90, 540, 0, -90, 0, 1400, "ortho", ["show_drivers=true"]),
        ("cabinet_right", 0, 90, 540, 0, 90, 0, 1400, "ortho", ["show_drivers=true"]),
        ("cabinet_top", 0, 90, 540, 0, 0, 180, 1800, "ortho", []),
        ("cabinet_bottom", 0, 90, 540, 0, 180, 0, 1800, "ortho", []),
        ("cabinet_exterior", 500, 500, 900, 60, 0, 45, 2000, "perspective", ["show_drivers=true"]),
        ("cabinet_cutaway", 0, 90, 540, 70, 0, 0, 1600, "perspective", ["show_internals=true", "show_drivers=true"]),
        ("cabinet_assembly", 400, 500, 700, 70, 0, 20, 1800, "perspective", ["show_drivers=true", "show_waveguide=true"]),
        ("cabinet_full_cutaway", 400, 400, 700, 65, 0, 35, 1800, "perspective", ["show_internals=true", "show_waveguide=true", "show_drivers=true"]),
    ]
    
    for name, tx, ty, tz, rx, ry, rz, dist, proj, defs in cab_views:
        jobs.append(RenderJob(
            name=name,
            scad_file=cab_scad,
            output_file=output_dir / f"{name}.png",
            is_stl=False,
            camera=(tx, ty, tz, rx, ry, rz, dist),
            projection=proj,
            extra_defs=defs
        ))
    
    return jobs


def execute_job(job: RenderJob) -> Tuple[str, bool, Optional[str]]:
    """Execute a single render job (STL or PNG)."""
    
    if job.is_stl:
        # STL export
        cmd = [
            "openscad",
            "-o", str(job.output_file),
            str(job.scad_file)
        ]
    else:
        # PNG render
        tx, ty, tz, rx, ry, rz, dist = job.camera
        cmd = [
            "xvfb-run", "-a",
            "openscad",
            "--render",
            "--camera", f"{tx},{ty},{tz},{rx},{ry},{rz},{dist}",
            "--imgsize", "1920,1080",
            "--colorscheme", "Cornfield",
            "--projection", job.projection,
            "-o", str(job.output_file),
        ]
        for d in job.extra_defs:
            cmd.extend(["-D", d])
        cmd.append(str(job.scad_file))
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return (job.name, True, None)
        else:
            return (job.name, False, result.stderr[:200])
    except subprocess.TimeoutExpired:
        return (job.name, False, "Timeout after 300s")
    except Exception as e:
        return (job.name, False, str(e)[:200])


def main():
    parser = argparse.ArgumentParser(description="Batch CAD renderer for Mk3")
    parser.add_argument("--waveguide-only", action="store_true")
    parser.add_argument("--cabinet-only", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true", help="List jobs without running")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    cad_dir = base_dir / "cad"
    output_dir = base_dir / "assets" / "renders"
    exports_dir = cad_dir / "exports"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # Build job list
    all_jobs = build_job_list(cad_dir, output_dir, exports_dir)
    
    # Filter if requested
    if args.waveguide_only:
        jobs = [j for j in all_jobs if "wg_" in j.name or "waveguide_" in j.name]
    elif args.cabinet_only:
        jobs = [j for j in all_jobs if "cab_" in j.name or "cabinet_" in j.name]
    else:
        jobs = all_jobs
    
    stl_jobs = [j for j in jobs if j.is_stl]
    png_jobs = [j for j in jobs if not j.is_stl]
    
    print(f"Render plan: {len(stl_jobs)} STL + {len(png_jobs)} PNG = {len(jobs)} total jobs")
    print(f"Workers: {args.workers}\n")
    
    if args.dry_run:
        for job in jobs:
            type_str = "STL" if job.is_stl else "PNG"
            print(f"  [{type_str}] {job.name} -> {job.output_file.name}")
        return 0
    
    # Execute all jobs in parallel
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(execute_job, job): job for job in jobs}
        
        for future in as_completed(futures):
            name, success, error = future.result()
            prefix = "✓" if success else "✗"
            suffix = "" if success else f": {error}"
            print(f"{prefix} {name}{suffix}")
            results.append((name, success))
    
    # Summary
    success_count = sum(1 for _, s in results if s)
    print(f"\nDone: {success_count}/{len(jobs)} jobs successful")
    
    # List outputs
    if success_count > 0:
        print("\nOutputs:")
        if stl_jobs:
            print(f"  STL: {exports_dir}/")
        if png_jobs:
            print(f"  PNG: {output_dir}/")
    
    return 0 if success_count == len(jobs) else 1


if __name__ == "__main__":
    sys.exit(main())
