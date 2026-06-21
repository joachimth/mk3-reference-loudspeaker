// =====================================================================
//  Mk2 Waveguide  -  H2606/920000 constant-directivity OS waveguide
//  Units: mm
//
//  Design goal:
//   - Oblate-spheroid (OS) bore  => smooth throat (no diffraction edge)
//     and near-conical, CONSTANT-DIRECTIVITY main section.
//   - Asymmetric coverage: ~100 deg horizontal, ~64 deg vertical.
//   - Tangent rolled mouth that ends flush with the baffle plane
//     (kills mouth diffraction ripple).
//   - Horizontal pattern control down to ~1620 Hz  => clean LR4
//     crossover to the 15W/4434G00 at ~1600 Hz.
//
//  After editing, render with F6 and export STL.
//  $fn high = slow but smooth; drop to 64 while iterating.
// =====================================================================

$fn = 120;

// ----------------------- MAIN ACOUSTIC PARAMETERS --------------------
throat_d   = 28;     // throat diameter. VERIFY against the real H2606
                     // dome/faceplate exit (26-30 typical). Critical.
theta_h    = 50;     // horizontal half-angle (deg)  -> ~100 deg coverage
theta_v    = 32;     // vertical   half-angle (deg)  -> ~64  deg coverage
D_os       = 65;     // depth of the OS (constant-directivity) section
Lr         = 10;     // forward depth of the mouth roundover
wall       = 8;      // wall thickness
steps      = 96;     // loft resolution along depth

// Derived mouth (computed below): ~211.7 x 121.0 mm, total depth 75 mm

// ----------------------- FLANGE / MOUNTING ---------------------------
flange_w     = 252;  // outer flange width  (baffle face)
flange_h     = 168;  // outer flange height
flange_thick = 9;
corner_r     = 22;   // flange corner radius

// Tweeter (rear) mounting reference - adapt to measured H2606
tw_face_d    = 104.3;
tw_bcd       = 92;
tw_hole_d    = 4.4;

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

// radius at depth z for a given half-angle th (OS, then tangent arc)
function prof_r(z, th) =
    (z <= D_os)
      ? sqrt(r_t*r_t + pow(z*tan(th),2))
      : r_e(th) + Rroll(th) * ( cos(a0(th))
            - cos( asin( sin(a0(th)) + (z - D_os)/Rroll(th) ) ) );

D_tot = D_os + Lr;

// Depth of the finished part's FRONT (baffle) face, measured from the throat
// plane. With the flush termination the front face IS the mouth plane (D_tot) -
// the flange sits behind it. Exposed so cabinet.scad can seat the waveguide
// without a hard-coded number. (If a build needs ~D_tot + flange_thick to sit
// flush, the flange is still FORWARD of the mouth = the old, sharp-edged
// geometry: pull the current file.)
function wg_front_z() = D_tot;

// ----------------------- HELPERS -------------------------------------
module ellipse_2d(rx, ry){ scale([rx, ry]) circle(r=1); }

module rounded_rect_2d(w,h,r){
    hull(){
        for(sx=[-1,1]) for(sy=[-1,1])
            translate([sx*(w/2-r), sy*(h/2-r)]) circle(r=r);
    }
}

// loft an elliptical bore between (rx,ry) cross-sections along z
module loft_bore(off=0){
    for(i=[0:steps-1]){
        z1 = (i/steps)     * D_tot;
        z2 = ((i+1)/steps) * D_tot;
        rx1 = prof_r(z1,theta_h)+off; ry1 = prof_r(z1,theta_v)+off;
        rx2 = prof_r(z2,theta_h)+off; ry2 = prof_r(z2,theta_v)+off;
        hull(){
            translate([0,0,z1]) linear_extrude(0.12) ellipse_2d(rx1,ry1);
            translate([0,0,z2]) linear_extrude(0.12) ellipse_2d(rx2,ry2);
        }
    }
}

module countersunk(x,y,d,csd,csdepth,total){
    translate([x,y,-1]) cylinder(d=d, h=total+3);
    translate([x,y,total-csdepth]) cylinder(d1=d, d2=csd, h=csdepth+1);
}

// ----------------------- MODEL ---------------------------------------
mouth_rx = prof_r(D_tot, theta_h);
mouth_ry = prof_r(D_tot, theta_v);

module waveguide(){
    difference(){
        union(){
            loft_bore(wall);                         // outer shell = bore + wall
            // Flange sits BEHIND the flush mouth plane (z = D_tot) so the bore
            // meets the baffle with no forward lip / sharp edge -> less mouth
            // diffraction. (Earlier the flange was forward of D_tot with a
            // straight mouth cut, leaving a sharp 90 deg edge at the baffle.)
            // See simulations/waveguide_profile.py. For an even gentler baffle
            // blend, increase Lr (bigger roundover) at the cost of depth.
            translate([0,0,D_tot-flange_thick])
                linear_extrude(flange_thick)
                    rounded_rect_2d(flange_w, flange_h, corner_r);
        }
        loft_bore(0);                                // hollow out acoustic bore

        // clear the mouth opening through the rearward flange, up to the flush
        // plane at z = D_tot (the baffle face) - no forward straight lip
        translate([0,0,D_tot-flange_thick-0.5])
            linear_extrude(flange_thick+0.6)
                ellipse_2d(mouth_rx, mouth_ry);

        // rear faceplate clearance for the tweeter
        translate([0,0,-2]) cylinder(d=tw_face_d+1.0, h=4);

        // tweeter screw holes (reference)
        for(a=[45,135,225,315])
            translate([(tw_bcd/2)*cos(a),(tw_bcd/2)*sin(a),-2])
                cylinder(d=tw_hole_d, h=16);

        // baffle mounting, countersunk from the front (flush) face at z = D_tot
        for(x=[-baf_bcd_x/2, baf_bcd_x/2])
        for(y=[-baf_bcd_y/2, baf_bcd_y/2])
            countersunk(x,y,baf_screw_d,baf_cs_d,baf_cs_depth, D_tot);
    }
}

waveguide();

echo(str("MOUTH  ", 2*mouth_rx, " x ", 2*mouth_ry, " mm   depth ", D_tot, " mm"));
