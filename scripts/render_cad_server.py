#!/usr/bin/env python3
"""
CAD render using OpenSCAD server mode for single-load multi-export.
Experimental - falls back to batch mode if server fails.
"""
import subprocess
import sys
import os
import json
import time
from pathlib import Path
from typing import List, Tuple, Optional


# Views: (name, camera, projection, extra_defs)
ViewConfig = Tuple[str, str, str, List[str]]

WAVEGUIDE_VIEWS: List[ViewConfig] = [
    ("mouth", "--camera=0,0,45,0,0,0,600", "ortho", []),
    ("rear", "--camera=0,0,45,180,0,0,600", "ortho", []),
    ("side", "--camera=0,0,45,90,0,90,600", "ortho", []),
    ("top", "--camera=0,0,45,0,0,180,600", "ortho", []),
    ("iso", "--camera=200,-200,120,55,0,35,700", "perspective", []),
    ("cutaway", "--camera=0,0,45,90,0,90,600", "ortho", ["show_cutaway=true"]),
]

CABINET_VIEWS: List[ViewConfig] = [
    ("front", "--camera=0,200,540,0,0,0,1800", "ortho", ["show_drivers=true"]),
    ("rear", "--camera=0,-200,540,180,0,0,1800", "ortho", []),
    ("left", "--camera=0,90,540,0,-90,0,1400", "ortho", ["show_drivers=true"]),
    ("right", "--camera=0,90,540,0,90,0,1400", "ortho", ["show_drivers=true"]),
    ("top", "--camera=0,90,540,0,0,180,1800", "ortho", []),
    ("bottom", "--camera=0,90,540,0,180,0,1800", "ortho", []),
    ("exterior", "--camera=500,500,900,60,0,45,2000", "perspective", ["show_drivers=true"]),
    ("cutaway", "--camera=0,90,540,70,0,0,1600", "perspective", ["show_internals=true", "show_drivers=true"]),
    ("assembly", "--camera=400,500,700,70,0,20,1800", "perspective", ["show_drivers=true", "show_waveguide=true"]),
    ("full_cutaway", "--camera=400,400,700,65,0,35,1800", "perspective", ["show_internals=true", "show_waveguide=true", "show_drivers=true"]),
]


class OpenSCADServer:
    """Wrapper for OpenSCAD server mode (experimental)."""
    
    def __init__(self, scad_file: Path, exports_dir: Path, renders_dir: Path):
        self.scad_file = scad_file
        self.exports_dir = exports_dir
        self.renders_dir = renders_dir
        self.process: Optional[subprocess.Popen] = None
        self.available = False
        
    def start(self) -> bool:
        """Start OpenSCAD in server mode. Returns True if successful."""
        try:
            # Try to start server mode
            cmd = [
                "xvfb-run", "-a",
                "openscad",
                "--server",  # Experimental server mode
                str(self.scad_file)
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if process started
            time.sleep(0.5)
            if self.process.poll() is not None:
                # Process died immediately - server mode not supported
                stderr = self.process.stderr.read() if self.process.stderr else ""
                print(f"Server mode not available: {stderr[:200]}")
                return False
                
            self.available = True
            return True
            
        except Exception as e:
            print(f"Failed to start server mode: {e}")
            return False
    
    def export_stl(self, output: Path) -> bool:
        """Export STL (server command)."""
        if not self.available:
            return False
        
        cmd = f"export-stl {output}\n"
        try:
            self.process.stdin.write(cmd)
            self.process.stdin.flush()
            
            # Wait for completion signal
            response = self._wait_for_response(timeout=60)
            return response and "ok" in response.lower()
        except Exception as e:
            print(f"STL export failed: {e}")
            return False
    
    def export_png(self, output: Path, camera: str, projection: str, 
                   extra_defs: List[str]) -> bool:
        """Export PNG with camera settings (server command)."""
        if not self.available:
            return False
        
        # Build command
        defs_str = " ".join(f"-D {d}" for d in extra_defs)
        cmd = f"export-png {output} {camera} --imgsize=1920,1080 --colorscheme=Cornfield --projection={projection} {defs_str}\n"
        
        try:
            self.process.stdin.write(cmd)
            self.process.stdin.flush()
            
            response = self._wait_for_response(timeout=120)
            return response and "ok" in response.lower()
        except Exception as e:
            print(f"PNG export failed: {e}")
            return False
    
    def _wait_for_response(self, timeout: float) -> Optional[str]:
        """Wait for response from server with timeout."""
        import select
        
        if not self.process or not self.process.stdout:
            return None
            
        end_time = time.time() + timeout
        response = []
        
        while time.time() < end_time:
            # Check if process died
            if self.process.poll() is not None:
                break
                
            # Non-blocking read
            if select.select([self.process.stdout], [], [], 0.1)[0]:
                line = self.process.stdout.readline()
                if line:
                    response.append(line)
                    if "done" in line.lower() or "ok" in line.lower():
                        break
                        
        return "".join(response) if response else None
    
    def stop(self):
        """Stop server."""
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("quit\n")
                self.process.stdin.flush()
                self.process.wait(timeout=5)
            except:
                self.process.terminate()


def render_with_fallback(scad_file: Path, name: str, exports_dir: Path, 
                         renders_dir: Path, views: List[ViewConfig],
                         max_workers: int = 4) -> List[Tuple[str, bool]]:
    """Try server mode, fall back to parallel batch if unavailable."""
    
    # Try server mode
    server = OpenSCADServer(scad_file, exports_dir, renders_dir)
    
    if server.start():
        print(f"Using server mode for {name}...")
        results = []
        
        # Export STL
        stl_path = exports_dir / f"{name}.stl"
        if server.export_stl(stl_path):
            print(f"✓ {name}.stl")
            results.append((f"{name}_stl", True))
        else:
            print(f"✗ {name}.stl")
            results.append((f"{name}_stl", False))
        
        # Export PNGs
        for view_name, camera, proj, defs in views:
            png_path = renders_dir / f"{view_name}.png"
            if server.export_png(png_path, camera, proj, defs):
                print(f"✓ {view_name}.png")
                results.append((view_name, True))
            else:
                print(f"✗ {view_name}.png")
                results.append((view_name, False))
        
        server.stop()
        return results
        
    else:
        # Fall back to batch mode
        print(f"Server mode unavailable for {name}, using batch mode...")
        return render_batch(scad_file, name, exports_dir, renders_dir, views, max_workers)


def render_batch(scad_file: Path, name: str, exports_dir: Path,
                 renders_dir: Path, views: List[ViewConfig],
                 max_workers: int) -> List[Tuple[str, bool]]:
    """Fallback: parallel batch rendering."""
    from concurrent.futures import ProcessPoolExecutor, as_completed
    
    jobs = []
    # STL job
    stl_path = exports_dir / f"{name}.stl"
    jobs.append(("stl", scad_file, stl_path, None, None, []))
    
    # PNG jobs
    for view_name, camera, proj, defs in views:
        png_path = renders_dir / f"{view_name}.png"
        jobs.append((view_name, scad_file, png_path, camera, proj, defs))
    
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(render_job, job): job[0] for job in jobs}
        
        for future in as_completed(futures):
            job_name = futures[future]
            success = future.result()
            prefix = "✓" if success else "✗"
            print(f"{prefix} {job_name}")
            results.append((job_name, success))
    
    return results


def render_job(args) -> bool:
    """Single render job."""
    job_name, scad_file, output, camera, proj, defs = args
    
    if camera is None:
        # STL export
        cmd = ["openscad", "-o", str(output), str(scad_file)]
    else:
        # PNG render
        cmd = [
            "xvfb-run", "-a",
            "openscad",
            "--render",
            camera,
            "--imgsize", "1920,1080",
            "--colorscheme", "Cornfield",
            "--projection", proj,
            "-o", str(output),
        ]
        for d in defs:
            cmd.extend(["-D", d])
        cmd.append(str(scad_file))
    
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        return result.returncode == 0
    except:
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--waveguide-only", action="store_true")
    parser.add_argument("--cabinet-only", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--force-batch", action="store_true", help="Skip server mode")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    cad_dir = base_dir / "cad"
    exports_dir = cad_dir / "exports"
    renders_dir = base_dir / "assets" / "renders"
    
    exports_dir.mkdir(exist_ok=True)
    renders_dir.mkdir(exist_ok=True)
    
    all_results = []
    
    if not args.cabinet_only:
        wg_file = cad_dir / "mk2_waveguide_os.scad"
        if wg_file.exists():
            results = render_with_fallback(
                wg_file, "mk2_waveguide_os", exports_dir, renders_dir,
                WAVEGUIDE_VIEWS, args.workers
            )
            all_results.extend(results)
    
    if not args.waveguide_only:
        cab_file = cad_dir / "cabinet.scad"
        if cab_file.exists():
            results = render_with_fallback(
                cab_file, "mk2_cabinet", exports_dir, renders_dir,
                CABINET_VIEWS, args.workers
            )
            all_results.extend(results)
    
    success = sum(1 for _, s in all_results if s)
    total = len(all_results)
    print(f"\nDone: {success}/{total}")
    
    return 0 if success == total else 1


if __name__ == "__main__":
    sys.exit(main())
