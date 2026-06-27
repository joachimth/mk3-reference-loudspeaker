// =====================================================================
//  Mk2 Waveguide  -  H2606/920000 constant-directivity OS waveguide
//  Units: mm
//
//  Design goal:
//   - Oblate-spheroid (OS) bore  => smooth throat (no diffraction edge)
//     and near-conical, CONSTANT-DIRECTIVITY main section.
//   - Asymmetric coverage: ~100 deg horizontal, ~64 deg vertical.
//   - Tangent rolled mouth at the acoustic end (z = D_tot).  A cylindrical
//     PROTRUSION (z = D_tot .. D_tot + protrusion) extends past the flange
//     so the waveguide tube ends FLUSH with the OUTSIDE of the cabinet
//     baffle - no visible step, no protrusion past the cabinet face.
//     Default `protrusion = 22` matches `cabinet.scad`'s `wall = 22;`
//     (panel thickness).  Keep these two values in sync.
//   - Horizontal pattern control down to ~1620 Hz.
//     Current crossover target: 1250 Hz LR4 (well below the control limit).
//     1250 Hz is UNCONFIRMED — pending H2606/920000 distortion measurement
//     in the finished waveguide. Fallback options: 1350 / 1450 / 1600 Hz.
//
//  After editing, render with F6 and export STL.
//  $fn high = slow but smooth; drop to 64 while iterating.
// =====================================================================

$fn = 128;

// ----------------------- MAIN ACOUSTIC PARAMETERS --------------------
throat_d   = 33;     // horn exit diameter of the H2606/920000 built-in horn.
                     // Confirmed from official ScanSpeak STEP file (H2606-920000.STEP,
                     // assets/datasheets/): ø33.0 mm at the front face of the faceplate
                     // (Y=44.09 mm in STEP model, the unique small circle d=33.0 mm).
                     // The H2606 dome is ø26 mm; the built-in horn expands to ø33 mm
                     // at the exit. Our WG212 is an extension waveguide starting there.
                     // Verify with calipers on the physical unit before final print.
theta_h    = 50;     // horizontal half-angle (deg)  -> ~100 deg coverage
theta_v    = 32;     // vertical   half-angle (deg)  -> ~64  deg coverage
D_os       = 65;     // depth of the OS (constant-directivity) section
Lr         = 25;     // forward depth of the mouth roundover
wall       = 8;      // wall thickness
protrusion = 0;     // cylindrical extension past the flange front face.
                     // Default 0: the waveguide tube ends FLUSH with the
                     // cabinet baffle BACK face (z = 85) and the baffle has
                     // a through-cutout exposing the waveguide mouth from
                     // the outside.  The tube does NOT physically extend
                     // through the baffle - the baffle hole is the aperture.
                     // Set higher (e.g. 22 to match cabinet.scad's wall = 22)
                     // only if you want the tube to physically protrude past
                     // the baffle OUTSIDE face; in that case keep the two
                     // values in sync so the waveguide tube ends flush with
                     // the cabinet's outside surface.
steps      = 96;     // loft resolution along depth

// Derived mouth (echoed on render): ~293.5 x 174.4 mm, total depth 90 mm
// (D_tot = D_os + Lr = 65 + 25).  Tube extends from z=-5 (overlap with back plate)
// to z=D_tot_ext-flange_thick=85 (flush with cabinet baffle back face).

// ----------------------- FLANGE / MOUNTING ---------------------------
flange_w     = 252;  // outer flange width  (baffle face)
flange_h     = 168;  // outer flange height
flange_thick = 5;    // flange thickness — 5 mm is plenty for wood-screw mounting
                     // into the cabinet baffle (back plate still 8 mm thick,
                     // separate from this flange).
corner_r     = 4;   // flange corner radius

// Tweeter (rear) mounting — all dimensions from official ScanSpeak datasheet
// (H2606-920000.pdf + .STEP, assets/datasheets/). Do NOT edit without re-checking
// the physical unit; tolerances are tight on the faceplate pocket and BCD.
tw_face_d    = 104.0;  // faceplate OD: ø104 ±0.2 mm  (drawing + STEP r=52.0)
tw_bcd       = 95.0;   // mounting pitch circle: ø95 ±0.1 mm  (drawing + STEP r=47.5)
tw_hole_d    = 4.0;    // mounting screw hole: ø4 ±0.10 mm x4 at 90°  (drawing)
//
// Cabinet direct-mount cutout (not used in waveguide mount but noted for reference):
//   tw_cutout_d = 72  (ø72 mm baffle cutout if H2606 mounted directly to baffle)

// Tweeter rear mounting plate
// Provides a proper seating surface + screw holes for the H2606 at the throat end.
// Without this plate the tube wall at z=0 is only ø44 mm — far too narrow for
// the 104.3 mm faceplate and 92 mm BCD holes.
tw_ring_od    = 130;   // outer diameter of rear plate (> tw_bcd + 2×material)
tw_ring_thick =   8;   // total plate thickness (z = -tw_ring_thick … 0)
tw_fp_recess  =   4;   // depth of faceplate seating pocket (on rear face)

// Baffle mounting (countersunk, front)
baf_bcd_x    = 222;
baf_bcd_y    = 142;
baf_screw_d  = 4.5;
baf_cs_d     = 9;
baf_cs_depth = 3;

// ----------------------- PROFILE MATH (OS + rolled mouth) ------------
r_t = throat_d/2;

function r_e(th)  = sqrt(r_t*r_t + pow(D_os*tan(th),2));            // OS radius at D_os
function a0(th)   = atan( D_os*pow(tan(th),2) / r_e(th) );          // wall angle at OS end (deg)
function Rroll(th)= Lr / (1 - sin(a0(th)) );                        // roundover radius

// radius at depth z for a given half-angle th (OS, then tangent arc, then
// cylindrical protrusion past the acoustic mouth)
//   z <= D_os           : OS (constant-directivity) bore profile
//   D_os < z <= D_tot   : tangent roundover to the mouth
//   z >  D_tot          : constant mouth radius (cylindrical continuation
//                         through the cabinet baffle cutout; the acoustic
//                         profile is already settled, this is geometry only)
//
// The asin argument is exactly 1.0 at z=D_tot by design (Rroll ensures it),
// but floating-point accumulation through atan→sin→division can yield 1+ε on
// some platforms, causing asin() to return undef.  The min() clamp is harmless
// algebraically and prevents degenerate geometry in the mouth-end loft segment.
function prof_r(z, th) =
    (z <= D_os)
      ? sqrt(r_t*r_t + pow(z*tan(th),2))
      : (z <= D_tot)
        ? r_e(th) + Rroll(th) * ( cos(a0(th))
              - cos( asin( min(1.0, sin(a0(th)) + (z - D_os)/Rroll(th)) ) ) )
        : prof_r(D_tot, th);

D_tot       = D_os + Lr;                  // acoustic mouth position (mm)
D_tot_ext   = D_tot + protrusion;          // front face of the protrusion (mm)

// Physical front face of the finished part, measured from the throat plane.
// Returns z = D_tot_ext - flange_thick: the loft_bore tube terminates
// flange_thick short of D_tot_ext (the tube is shifted back by flange_thick
// so it overlaps the back plate by 5 mm and ends flush with the flange front
// face, not with the acoustic mouth).  Cabinet.scad uses this to seat the
// waveguide so the flange front face aligns with the baffle back face.
// (D_tot_ext itself is only useful for the protrusion-style extrusion past
// the flange, which this design no longer uses by default.)
function wg_front_z() = D_tot_ext - flange_thick;

// Back face of the finished part (rear of the back plate).
// Useful for cabinet.scad to keep the back plate clear of the cabinet back wall.
function wg_back_z() = -tw_ring_thick;

// ----------------------- HELPERS -------------------------------------
module ellipse_2d(rx, ry){ scale([rx, ry]) circle(r=1); }

module rounded_rect_2d(w,h,r){
    hull(){
        for(sx=[-1,1]) for(sy=[-1,1])
            translate([sx*(w/2-r), sy*(h/2-r)]) circle(r=r);
    }
}

// loft an elliptical bore between (rx,ry) cross-sections along z
// Total length = D_tot + protrusion (the protrusion section is a cylindrical
// continuation of the mouth since prof_r is constant there).
module loft_bore(off=0){
    for(i=[0:steps-1]){
        z1 = (i/steps)     * D_tot_ext-flange_thick;
        z2 = ((i+1)/steps) * D_tot_ext-flange_thick;
        rx1 = prof_r(z1,theta_h)+off; ry1 = prof_r(z1,theta_v)+off;
        rx2 = prof_r(z2,theta_h)+off; ry2 = prof_r(z2,theta_v)+off;
        hull(){
            translate([0,0,z1]) linear_extrude(0.12) ellipse_2d(rx1,ry1);
            translate([0,0,z2]) linear_extrude(0.12) ellipse_2d(rx2,ry2);
        }
    }
}

module countersunk(x,y,d,csd,csdepth,total){
    translate([x,y,-1]) cylinder(d=d, h=total);
    translate([x,y,total-csdepth]) cylinder(d1=d, d2=csd, h=csdepth+1);
}

// ----------------------- MODEL ---------------------------------------
mouth_rx = prof_r(D_tot, theta_h);
mouth_ry = prof_r(D_tot, theta_v);

// ----------------------- EXPORTED FUNCTIONS (for cabinet.scad) -------
// These allow cabinet.scad (via `use`) to derive the correct mouth size
// and flange dimensions automatically instead of hardcoding them.
// Any change to throat_d, theta_h, theta_v, D_os, Lr, or flange_* here
// propagates to the cabinet without a separate manual update.
function wg_mouth_rx()    = prof_r(D_tot, theta_h);  // horizontal mouth radius [mm]
function wg_mouth_ry()    = prof_r(D_tot, theta_v);  // vertical   mouth radius [mm]
function wg_protrusion_fn() = protrusion;            // forward protrusion past flange [mm]
function wg_flange_w_fn() = flange_w;                // outer flange width  [mm]
function wg_flange_h_fn() = flange_h;                // outer flange height [mm]
function wg_flange_r_fn() = corner_r;                // flange corner radius [mm]
function wg_flange_t_fn() = flange_thick;            // flange thickness / recess depth [mm] 

module waveguide(){
    difference(){
        union(){
            loft_bore(wall+protrusion);                         // outer shell = bore + wall
            // Flange sits BEHIND the flush mouth plane (z = D_tot) so the bore
            // meets the baffle with no forward lip / sharp edge -> less mouth
            // diffraction. (Earlier the flange was forward of D_tot with a
            // straight mouth cut, leaving a sharp 90 deg edge at the baffle.)
            // See simulations/waveguide_profile.py. For an even gentler baffle
            // blend, increase Lr (bigger roundover) at the cost of depth.
            translate([0,0,D_tot-2*flange_thick])
                linear_extrude(flange_thick)
                    rounded_rect_2d(flange_w, flange_h, corner_r);

            // Rear tweeter mounting plate.  The loft_bore tube at z=0 is only
            // ø44 mm — too narrow to seat the ø104 mm H2606 faceplate or to
            // accommodate the 92 mm BCD screw holes.  This plate (z = -tw_ring_thick
            // … 0) provides a proper seating surface and screw-hole lands.
            translate([0, 0, -tw_ring_thick])
                linear_extrude(tw_ring_thick)
                    circle(d=tw_ring_od);
        }
        loft_bore(0);                                // hollow out acoustic bore

        // clear the mouth opening through the rearward flange, up to the flush
        // plane at z = D_tot (the baffle face) - no forward straight lip
        translate([0,0,D_tot-flange_thick+0.05])
            linear_extrude(flange_thick+0.6)
                ellipse_2d(mouth_rx, mouth_ry);

        // Faceplate seating pocket on the rear face of the back plate.
        // tw_fp_recess deep so the tweeter faceplate sits flush with the
        // back-plate rear surface; overrun by 0.5 mm for clean CSG.
        translate([0, 0, -tw_ring_thick - 0.5])
            cylinder(d=tw_face_d + 1.0, h=tw_fp_recess + 0.5);

        // Acoustic throat through-hole in the back plate.
        // loft_bore(0) only subtracts from z=0 upward; the plate (z<0) needs
        // its own opening for the tweeter dome to project into the bore.
        translate([0, 0, -tw_ring_thick - 1])
            cylinder(d=throat_d, h=tw_ring_thick + 2);

        // Tweeter mounting screw holes — through the full plate thickness.
        // Previously these sat at r=46 mm (BCD/2) but the shell at z=0 was
        // only r=22 mm, so the holes were entirely in mid-air.  They now
        // pass properly through the rear mounting plate.
        for(a=[45,135,225,315])
            translate([(tw_bcd/2)*cos(a),(tw_bcd/2)*sin(a),-tw_ring_thick-1])
                cylinder(d=tw_hole_d, h=tw_ring_thick+2);

        // baffle mounting, countersunk from the front face of the protrusion
        // (z = D_tot + protrusion) so the screw head sits flush with the
        // waveguide's exposed forward face.
        for(x=[-baf_bcd_x/2, baf_bcd_x/2])
        for(y=[-baf_bcd_y/2, baf_bcd_y/2])
            countersunk(x,y,baf_screw_d,baf_cs_d,baf_cs_depth, D_tot_ext);
    }
}

waveguide();

echo(str("MOUTH       ", 2*mouth_rx, " x ", 2*mouth_ry, " mm"));
echo(str("DEPTH       acoustic mouth at D_tot=", D_tot, " mm  |  front face (incl. protrusion) at D_tot+protrusion=", D_tot_ext, " mm  |  total incl. back plate ", D_tot_ext + tw_ring_thick, " mm"));
echo(str("PROTRUSION  ", protrusion, " mm past the flange front (cylindrical, mouth radius)"));
echo(str("BACK PLATE  ø", tw_ring_od, " mm  thick ", tw_ring_thick, " mm  faceplate pocket ø", tw_face_d+1.0, " x ", tw_fp_recess, " mm deep"));
