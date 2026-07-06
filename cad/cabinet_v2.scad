// =====================================================================
// Mk3 Reference Loudspeaker - cabinet v2 (baffel_insert variant)
// =====================================================================
//
// ALTERNATIVE cabinet design. Same enclosure, bracing, and woofer
// placement as cabinet.scad, but the front baffle uses a 3D-printed
// baffel_insert (cad/baffel_insert_1.scad) instead of cutouts in the
// plywood baffle. The insert provides:
//   - Flush rebate (planfræset) for the 18W/4424G00 midrange
//   - Flush pocket + elliptical body hole for the WG212 waveguide
//   - Precise screw patterns for both drivers
//   - Edge screws for cabinet mounting
//   - Backside ribbing for stiffness
//
// The plywood front baffle in v2 has a single large opening (the insert
// pocket) rather than individual driver cutouts. The insert is glued or
// screwed into this pocket and carries all the precision geometry.
//
// This is NOT a replacement for cabinet.scad — it is an alternative for
// builders who want 3D-printed baffle precision without CNC routing
// complex cutout patterns in plywood.
//
// Axes: X = width, Y = depth (front baffle at +Y), Z = height (0 at floor).
// Units: millimetres.  Render: `openscad -o cabinet_v2.stl cabinet_v2.scad`
// ---------------------------------------------------------------------

use <waveguide.scad>
use <midrange.scad>
use <GRS-12SW-4HE.scad>
use <SB26STAC-C000-4.scad>
use <baffel_insert_1.scad>

// ---- External shell (same as cabinet.scad) --------------------------
W       = 320;   // external width  [mm]
D       = 380;   // external depth  [mm]
H       = 1180;  // external height [mm]
wall    = 22;    // panel thickness [mm]
round_r = 19;    // front vertical roundover radius [mm]

// ---- Baffel insert opening -------------------------------------------
// The insert sits in a pocket cut through the front baffle.
// Insert dimensions come from baffel_insert_1.scad.
insert_w   = baffel_b;     // 285 mm — insert width
insert_h   = baffel_h;     // 380 mm — insert height
insert_t   = baffel_tyk;   // 15 mm  — insert thickness
insert_r   = hjoerne_r;    // 14 mm  — corner radius
// Pocket clearance so the insert drops in cleanly
pocket_clear = 1.0;        // per side [mm]

// Pocket opening in the plywood baffle (slightly larger than insert)
pocket_w = insert_w + 2*pocket_clear;
pocket_h = insert_h + 2*pocket_clear;

// Where the insert sits vertically — same driver positions as cabinet.scad
// The insert's internal layout (enhed_cc, gruppe_offset) places the
// midrange at top and waveguide below, matching v9 layout.
insert_z = H/2;  // centered vertically (adjust if needed)

// ---- Woofer (same as cabinet.scad) ----------------------------------
woofer_frame_d  = 332;
woofer_cut_d    = 284;
woofer_bcd      = 319;
woofer_hole_d   = 5.5;
woofer_n_holes  = 8;
woofer_depth    = 136;
woofer_displ_L  = 4.5;
woofer_z        = 520;

woofer_Fs       = 22;
woofer_Qts      = 0.43;
woofer_Vas_L    = 80.4;

// ---- Midrange & waveguide placement (from baffel_insert) -------------
// These come from baffel_insert_1.scad's layout
enhed_cc_v2     = enhed_cc;       // 164 mm c-c
gruppe_offset_v2 = gruppe_offset;  // 9 mm lift

// Midrange is at the top of the insert, waveguide below
mid_z_v2  = insert_z + enhed_cc_v2/2 + gruppe_offset_v2;
tw_z_v2   = insert_z - enhed_cc_v2/2 + gruppe_offset_v2;

// ---- Divider plate ---------------------------------------------------
divider_tilt     = 12;
divider_front_z  = (mid_z_v2 + tw_z_v2) / 2;

// ---- Bracing (same as cabinet.scad) ----------------------------------
shelf_rim   = 60;
shelf_zs    = [260, 780];
coupling_r  = 55;

// ---- Internal dimensions ---------------------------------------------
w_in = W - 2*wall;
d_in = D - 2*wall;
h_in = H - 2*wall;

// ---- View flags ------------------------------------------------------
show_internals      = false;
show_drivers        = false;
show_waveguide      = false;
show_insert         = true;   // show the baffel_insert in the baffle
show_pilot_holes    = true;
show_coupling_block = true;

$fn = 120;
eps = 0.05;

// ---- Volume calculations (same as cabinet.scad) ----------------------
V_bass_gross = w_in * d_in * (H - divider_front_z - wall);
V_mid_gross  = w_in * d_in * (divider_front_z - wall);
V_window = 0;
V_shelves = 0;
V_coupling = 0;
V_bass_net = V_bass_gross - 2*woofer_displ_L*1e6 - V_window - V_shelves
             - V_coupling;
Vb_per_woofer = (V_bass_net / 1e6) / 2;
bass_ratio = sqrt(1 + woofer_Vas_L / Vb_per_woofer);
bass_Qtc   = woofer_Qts * bass_ratio;
bass_Fc    = woofer_Fs  * bass_ratio;

echo(str("=== Cabinet v2 (baffel_insert variant) ==="));
echo(str("Bass: ", r1(V_bass_net/1e6), " L net, ",
         r1(Vb_per_woofer), " L per woofer"));
echo(str("Bass alignment: Fc ", r1(bass_Fc), " Hz, Qtc ", r2(bass_Qtc)));
echo(str("Baffel insert: ", insert_w, " x ", insert_h, " x ", insert_t, " mm"));
echo(str("Pocket opening: ", pocket_w, " x ", pocket_h, " mm"));

function r1(x) = round(x*10)/10;
function r2(x) = round(x*100)/100;

// ---- Profile ---------------------------------------------------------
module profile2d(w, d, r) {
    offset(r = r) offset(delta = -r) square([w, d], center = true);
}
module outer()  linear_extrude(H) profile2d(W, D, round_r);
module cavity() translate([0,0,wall]) linear_extrude(h_in)
    offset(-wall) profile2d(W, D, round_r);
module rrect2d(w, h, r)
    offset(r = r) offset(delta = -r) square([w, h], center = true);

// ---- Baffle pocket (the insert opening) ------------------------------
module baffle_pocket() {
    translate([0, D/2, insert_z - pocket_h/2])
        rotate([90, 0, 0])
            linear_extrude(wall + 2*eps, center = true)
                rrect2d(pocket_w, pocket_h, insert_r + pocket_clear);
}

// ---- Side woofer cutouts (same as cabinet.scad) ----------------------
module side_cut(sign, z, dia) {
    translate([sign*(W/2), 0, z]) rotate([0, -sign*90, 0])
        cylinder(h = wall + 2*eps, d = dia, $fn = 64, center = true);
}
module side_pilots(sign, z) {
    for (i = [0 : woofer_n_holes-1])
        let (a = i * 360 / woofer_n_holes)
            translate([sign*(W/2), 0, z])
                rotate([0, -sign*90, 0])
                    rotate([0, 0, a])
                        translate([woofer_bcd/2, 0, 0])
                            cylinder(h = wall + 2*eps, d = woofer_hole_d,
                                     $fn = 24, center = true);
}

// ---- Enclosure (v2: baffle has a pocket, not individual cutouts) -----
module enclosure() {
    difference() {
        outer();
        cavity();
        // front baffle: single pocket for the baffel_insert
        baffle_pocket();
        // sides: opposed push-push woofers
        side_cut(+1, woofer_z, woofer_cut_d);
        side_cut(-1, woofer_z, woofer_cut_d);
        if (show_pilot_holes) { side_pilots(+1, woofer_z); side_pilots(-1, woofer_z); }
    }
}

// ---- Internal structure (same as cabinet.scad) -----------------------
module woofer_body_clear() {
    for (s = [-1, 1])
        translate([s*(w_in/2 + eps), 0, woofer_z]) rotate([0, -s*90, 0])
            cylinder(h = woofer_depth, r1 = woofer_cut_d/2 + 8, r2 = 85, $fn = 48);
}

module divider_plate() {
    color("Yellow", 0.85)
    intersection() {
        translate([0, 0, wall]) linear_extrude(H - 2*wall)
            offset(-wall + 1) profile2d(W, D, round_r);
        translate([0, d_in/2, divider_front_z]) rotate([-divider_tilt, 0, 0])
            translate([0, 0, -wall]) linear_extrude(wall)
                square([W, 3*D], center = true);
    }
}

module brace_window(z) {
    color("Blue", 0.8)
    difference() {
        translate([0, 0, z - 18]) linear_extrude(36)
            difference() { offset(-wall - 4)  profile2d(W, D, round_r);
                           offset(-wall - 70) profile2d(W, D, round_r); }
        woofer_body_clear();
    }
}

module shelf_ring(z) {
    color("Red", 0.7)
    difference() {
        translate([0, 0, z]) linear_extrude(wall)
            difference() { offset(-wall + 1)         profile2d(W, D, round_r);
                           offset(-wall - shelf_rim) profile2d(W, D, round_r); }
        woofer_body_clear();
    }
}

magnet_gap = w_in - 2 * (woofer_depth - wall);
module coupling_block() {
    color("Orange", 0.9)
    translate([0, 0, woofer_z]) rotate([0, 90, 0])
        cylinder(h = max(magnet_gap, 1), r = coupling_r, center = true, $fn = 48);
}

module internals() {
    divider_plate();
    brace_window(woofer_z);
    for (z = shelf_zs) shelf_ring(z);
    if (show_coupling_block) coupling_block();
}

// ---- Baffel insert placed in the baffle pocket -----------------------
module baffel_insert_in_place() {
    // The insert's front is at +Z (its local frame), baffle front at +Y.
    // Rotate so the insert's Z axis aligns with the cabinet Y axis,
    // and position it in the pocket.
    translate([0, D/2 - wall/2, insert_z])
        rotate([90, 0, 0])
            translate([0, 0, -insert_t/2])
                baffel();
}

// ---- Waveguide seated in baffle (for assembly view) ------------------
wg_front = wg_front_z();
wg_back  = wg_back_z();
module wg_in_baffle() {
    color("SteelBlue", 0.9)
    translate([0, D/2 - wg_front, tw_z_v2]) rotate([-90, 0, 0])
        waveguide();
}

// ---- Driver models (real parametric models, same as cabinet.scad) ----
module driver_woofer(sign) {
    translate([sign*(W/2), 0, woofer_z]) rotate([0, sign*90, 0]) {
        driver();
    }
}
module driver_mid() {
    // Midrange sits in the insert's flush rebate
    translate([0, D/2, mid_z_v2])
        rotate([-90, 0, 0]) midrange_driver();
}
module driver_tweeter() {
    translate([0, D/2 - wg_front + wg_back, tw_z_v2]) rotate([-90, 0, 0]) {
        diskant();
    }
}

// ---- Top-level -------------------------------------------------------
if (show_internals) {
    difference() {
        union() {
            enclosure();
            internals();
            if (show_waveguide) wg_in_baffle();
            if (show_insert) baffel_insert_in_place();
            if (show_drivers) {
                driver_woofer(+1);
                driver_woofer(-1);
                driver_mid();
                if (show_waveguide) driver_tweeter();
            }
        }
        // cutaway: remove the +X half for an internal view
        translate([0, -D, -10]) cube([W, 2*D, H + 20]);
    }
} else {
    enclosure();
    if (show_waveguide) wg_in_baffle();
    if (show_insert) baffel_insert_in_place();
    if (show_drivers) {
        driver_woofer(+1);
        driver_woofer(-1);
        driver_mid();
        if (show_waveguide) driver_tweeter();
    }
}
