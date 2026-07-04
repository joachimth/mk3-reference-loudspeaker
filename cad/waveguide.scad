// =====================================================================
//  Mk2 Waveguide ALT - SB26STAC-C000-4 OS waveguide (alternative)
//  Units: mm
//
//  Alternative waveguide for the SB Acoustics SB26STAC-C000-4 tweeter.
//  This is a conventional 26mm soft dome tweeter (no built-in horn),
//  so the OS bore starts directly at the dome — unlike the H2606
//  version where the bore starts at the Ø33mm horn exit.
//
//  Key differences from mk2_waveguide_os.scad (H2606 version):
//    - throat_d:  28 mm (26mm dome + surround) vs 33 mm (H2606 horn exit)
//    - tw_face_d: 100.0 mm vs 104.0 mm
//    - tw_bcd:    88.5 mm vs 95.0 mm
//    - tw_hole_d: 4.0 mm (same) but with Ø8.0 counterbores
//    - tw_ring_od: 115 mm vs 130 mm (smaller BCD needs less material)
//    - tw_fp_recess: 4.0 mm (same)
//    - tweeter depth: 39.7 mm vs ~44 mm (shallower)
//    - Crossover target: 1000-1100 Hz LR4 (Fs=750 gives 250-350 Hz margin)
//      vs 1250 Hz (Fs=1030, only 220 Hz margin)
//
//  The OS coverage angles (theta_h=50, theta_v=32) are kept identical
//  to the H2606 version so the directivity match with the 15W midrange
//  is comparable. The smaller throat (28 vs 33) produces a marginally
//  smaller mouth (~289×172 vs 293×174) — negligible difference.
//
//  After editing, render with F6 and export STL.
// =====================================================================

$fn = 128;

// ----------------------- MAIN ACOUSTIC PARAMETERS --------------------
throat_d   = 28;     // SB26STAC dome + surround diameter.
                     // The SB26STAC has a 26mm dome with no built-in horn.
                     // The OS bore starts directly at the dome edge.
                     // Ø28mm accounts for the dome + ~1mm surround per side.
                     // The faceplate has a Ø53mm recess around the dome —
                     // the bore fills this recess and transitions to OS.
                     // Verify with calipers on the physical unit.
theta_h    = 50;     // horizontal half-angle (deg)  -> ~100 deg coverage
theta_v    = 32;     // vertical   half-angle (deg)  -> ~64  deg coverage
D_os       = 65;     // depth of the OS (constant-directivity) section
Lr         = 25;     // forward depth of the mouth roundover
wall       = 6;      // wall thickness
protrusion = 0;      // flush with baffle back face (same as H2606 version)
steps      = 96;     // loft resolution along depth
show_cutaway = false;

// Derived mouth: ~289 x 172 mm (vs 293 x 174 for H2606 version)
// Total depth 90 mm (D_os + Lr = 65 + 25, same as H2606).

// ----------------------- FLANGE / MOUNTING ---------------------------
flange_w     = 242;  // outer flange width  (baffle face) — same as H2606
flange_h     = 143;  // outer flange height — same as H2606
flange_thick = 5;    // flange thickness — same
corner_r     = 4;   // flange corner radius — same

// SB26STAC-C000-4 tweeter mounting — all dimensions from official SB
// Acoustics datasheet (SB26STAC-C000-4.pdf, assets/datasheets/).
// Cross-checked against dimension drawing (Ø100.0±0.35 faceplate,
// 88.50±0.10 BCD, 4-Ø4.0 + 4-Ø8.0 holes, 39.7mm depth, Ø53.0 recess).
tw_face_d    = 100.0;  // faceplate OD: ø100.0 ±0.35 mm
tw_bcd       = 88.5;   // mounting pitch circle: ø88.5 ±0.10 mm
tw_hole_d    = 4.0;    // mounting screw hole: ø4.0 mm x4 at 90°
tw_cb_d      = 8.0;    // counterbore diameter: ø8.0 mm x4 at 90°
tw_cb_depth  = 2.0;    // counterbore depth (estimated — verify with caliper)
tw_recess_d  = 53.0;   // faceplate front recess: ø53.0 mm (around dome)

// Tweeter rear mounting plate
tw_ring_od    = 115;   // outer diameter (tw_bcd/2=44.25 + 13mm material = 57.25 -> ø115)
tw_ring_thick =   8;   // total plate thickness (z = -tw_ring_thick … 0)
tw_fp_recess  =   4;   // depth of faceplate seating pocket (on rear face)

// Baffle mounting (countersunk, front) — same as H2606 version
baf_bcd_x    = 212;
baf_bcd_y    = 128;
baf_screw_d  = 4.5;
baf_cs_d     = 9;
baf_cs_depth = 3;

// ----------------------- PROFILE MATH (OS + rolled mouth) ------------
r_t = throat_d/2;

function r_e(th)  = sqrt(r_t*r_t + pow(D_os*tan(th),2));
function a0(th)   = atan( D_os*pow(tan(th),2) / r_e(th) );
function Rroll(th)= Lr / (1 - sin(a0(th)) );

function prof_r(z, th) =
    (z <= D_os)
      ? sqrt(r_t*r_t + pow(z*tan(th),2))
      : (z <= D_tot)
        ? r_e(th) + Rroll(th) * ( cos(a0(th))
              - cos( asin( min(1.0, sin(a0(th)) + (z - D_os)/Rroll(th)) ) ) )
        : prof_r(D_tot, th);

D_tot       = D_os + Lr;
D_tot_ext   = D_tot + protrusion;

function wg_front_z() = D_tot_ext - flange_thick;
function wg_back_z() = -tw_ring_thick;

// ----------------------- HELPERS -------------------------------------
module ellipse_2d(rx, ry){ scale([rx, ry]) circle(r=1); }

module rounded_rect_2d(w,h,r){
    hull(){
        for(sx=[-1,1]) for(sy=[-1,1])
            translate([sx*(w/2-r), sy*(h/2-r)]) circle(r=r);
    }
}

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

function wg_mouth_rx()    = prof_r(D_tot, theta_h);
function wg_mouth_ry()    = prof_r(D_tot, theta_v);
function wg_protrusion_fn() = protrusion;
function wg_flange_w_fn() = flange_w;
function wg_flange_h_fn() = flange_h;
function wg_flange_r_fn() = corner_r;
function wg_flange_t_fn() = flange_thick;

module waveguide(){
    difference(){
        union(){
            loft_bore(wall+protrusion);
            translate([0,0,D_tot-2*flange_thick])
                linear_extrude(flange_thick)
                    rounded_rect_2d(flange_w, flange_h, corner_r);

            // Rear tweeter mounting plate
            translate([0, 0, -tw_ring_thick])
                linear_extrude(tw_ring_thick)
                    circle(d=tw_ring_od);
        }
        loft_bore(0);                                // hollow out acoustic bore

        // clear the mouth opening through the flange
        translate([0,0,D_tot-flange_thick+0.05])
            linear_extrude(flange_thick+0.6)
                ellipse_2d(mouth_rx, mouth_ry);

        // Faceplate seating pocket on the rear face of the back plate.
        translate([0, 0, -tw_ring_thick - 0.5])
            cylinder(d=tw_face_d + 1.0, h=tw_fp_recess + 0.5);

        // Acoustic throat through-hole in the back plate.
        // For the SB26STAC, the throat is Ø28mm (dome + surround).
        // The faceplate has a Ø53mm recess — we fill this with the
        // waveguide bore, so the bore transitions from Ø28 (dome) to
        // the OS profile. The back plate opening matches the throat.
        translate([0, 0, -tw_ring_thick - 1])
            cylinder(d=throat_d, h=tw_ring_thick + 2);

        // Tweeter mounting screw holes — through the full plate thickness.
        // 4-Ø4.0 through holes at BCD=88.5mm
        for(a=[45,135,225,315])
            translate([(tw_bcd/2)*cos(a),(tw_bcd/2)*sin(a),-tw_ring_thick-1])
                cylinder(d=tw_hole_d, h=tw_ring_thick+2);

        // 4-Ø8.0 counterbores on the rear face (for screw heads)
        for(a=[45,135,225,315])
            translate([(tw_bcd/2)*cos(a),(tw_bcd/2)*sin(a),-tw_ring_thick-1])
                cylinder(d=tw_cb_d, h=tw_cb_depth+1);

        // baffle mounting, countersunk from the front
        for(x=[-baf_bcd_x/2, baf_bcd_x/2])
        for(y=[-baf_bcd_y/2, baf_bcd_y/2])
            countersunk(x,y,baf_screw_d,baf_cs_d,baf_cs_depth, D_tot_ext);
    }
}

if (show_cutaway) {
    difference() {
        waveguide();
        translate([0, -200, -50]) cube([200, 400, 250]);
    }
} else {
    waveguide();
}

echo(str("MOUTH       ", 2*mouth_rx, " x ", 2*mouth_ry, " mm"));
echo(str("DEPTH       acoustic mouth at D_tot=", D_tot, " mm  |  total incl. back plate ", D_tot_ext + tw_ring_thick, " mm"));
echo(str("BACK PLATE  ø", tw_ring_od, " mm  thick ", tw_ring_thick, " mm  faceplate pocket ø", tw_face_d+1.0, " x ", tw_fp_recess, " mm deep"));
echo(str("THROAT      ø", throat_d, " mm (SB26STAC dome + surround)"));
echo(str("TWEETER     SB26STAC-C000-4  faceplate ø", tw_face_d, "  BCD ø", tw_bcd, "  depth 39.7 mm"));
