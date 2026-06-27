// =====================================================================
// Mk2 Reference Loudspeaker - cabinet (parametric, simulation-stage)
// =====================================================================
//
// v6b enclosure: 300 x 370 x 1080 mm, 22 mm birch ply, R50 front vertical
// roundovers, side-mounted push-push woofers opposed at the same height, sealed
// midrange chamber, WG212 + 15W on the front baffle at ~150 mm c-c.
//
// This is a DESIGN-CANDIDATE model for visualisation and dimension checking,
// NOT a cut list. Driver cut-outs and the mid-chamber volume are estimates and
// must be confirmed against the real driver flanges and a volume calculation
// before any panel is cut. See docs/07_cabinet_development.md and
// docs/09_volume_calculations.md.
//
// Axes: X = width, Y = depth (front baffle at +Y), Z = height (0 at floor).
// Units: millimetres.   Render: `openscad -o cabinet.stl cabinet.scad`
// ---------------------------------------------------------------------

// Pull in the waveguide model for the optional assembly view (only its
// modules are imported; nothing renders unless show_waveguide = true).
use <mk2_waveguide_os.scad>

// ---- External shell -------------------------------------------------
W      = 300;    // width  [mm]
D      = 370;    // depth  [mm]
H      = 1080;   // height [mm]
wall   = 22;     // panel thickness [mm]
round_r = 50;    // R50 front vertical roundovers [mm]

// ---- Driver placement (estimates) -----------------------------------
woofer_z      = 520;   // opposed push-push woofer centre height [mm]
woofer_cut_d  = 185;   // GRS 8SW-4HE cut-out diameter [mm]

tw_z          = 900;   // WG212/tweeter acoustic centre height [mm]
cc            = 150;   // mid/tweeter centre-to-centre [mm] (DD-011 realistic)
mid_z         = tw_z - cc;
// WG212 opening matches cad/mk2_waveguide_os.scad (asymmetric OS waveguide)
// WG212 mouth and flange dimensions — derived from mk2_waveguide_os.scad via
// exported functions so they stay in sync automatically when the waveguide
// profile changes (throat_d, angles, etc.).  Do NOT hardcode these here.
wg_mouth_w    = 2 * wg_mouth_rx();    // WG212 mouth width  (horizontal) [mm]
wg_mouth_h    = 2 * wg_mouth_ry();    // WG212 mouth height (vertical)   [mm]
wg_flange_w   = wg_flange_w_fn();     // WG212 flange recess width  [mm]
wg_flange_h   = wg_flange_h_fn();     // WG212 flange recess height [mm]
wg_flange_r   = wg_flange_r_fn();     // flange corner radius [mm]
wg_flange_t   = wg_flange_t_fn();     // flange thickness / recess depth [mm]
mid_cut_d     = 124;   // 15W/4434G00 cut-out diameter [mm]

// ---- Internals ------------------------------------------------------
midchamber_h  = 235;   // internal height of the sealed mid chamber [mm]
midchamber_d  = 210;   // internal depth of the mid chamber [mm] (<= inner depth)
show_internals = true; // true: cutaway with mid chamber + braces
show_waveguide = false;// true: seat the WG212 model into the baffle (assembly view)

// WG212 assembly placement. All positioning derives from mk2_waveguide_os.scad
// exports so the cabinet tracks the waveguide automatically - no hard-coded
// number to drift out of sync if you change Lr, flange_thick, or protrusion.
//
// wg_front_z()  = physical front face of the waveguide (z = D_tot_ext - flange_thick
//                 in the current design: 85 mm).  The flange front face sits at this
//                 z and is what we want flush with the baffle back face.
// wg_back_z()   = rear of the back plate (z = -tw_ring_thick = -8 mm).  Useful for
//                 keeping the assembly clear of the cabinet back wall.
// wg_protrusion_fn() = protrusion past the flange front (0 by default - the tube
//                 ends at the flange front, baffle hole is the aperture).
//
// The waveguide's throat (z=0) is positioned so the flange front face aligns
// with the baffle back face:  Y(z=0) = (D/2 - wall) - wg_front_z().
// With current numbers:  Y(z=0) = (185-22) - 85 = 78 ;  Y(z=85) = 163 (baffle back).
//
// wg_recess = small overlap so the flange and baffle material are not coplanar
//             (OpenSCAD renders coplanar joins as non-manifold smears).  0.3 mm
//             is safe and well below any acoustic concern.
wg_front       = wg_front_z();
wg_back        = wg_back_z();
wg_protrusion  = wg_protrusion_fn();
wg_recess      = 0.3;   // small overlap into the baffle material [mm] for clean CSG

eps = 0.1;             // generic cut overshoot for clean booleans [mm]
fn = 140;
// ---------------------------------------------------------------------

// 2D horizontal cross-section: rounded front (+Y) corners, square rear corners
module profile2d(w, d, r) {
    hull() {
        translate([-(w/2 - r),  (d/2 - r)]) circle(r, $fn = fn);   // front-left
        translate([ (w/2 - r),  (d/2 - r)]) circle(r, $fn = fn);   // front-right
        translate([-(w/2 - 0.5), -(d/2 - 0.5)]) square(1, center = true); // rear-left
        translate([ (w/2 - 0.5), -(d/2 - 0.5)]) square(1, center = true); // rear-right
    }
}

module outer()  linear_extrude(H) profile2d(W, D, round_r);
module cavity() translate([0,0,wall])
                    linear_extrude(H - 2*wall) offset(-wall) profile2d(W, D, round_r);

// driver cut-out: pierce the full baffle thickness with eps overshoot both faces
module baffle_cut(z, dia) {
    translate([0, D/2 - wall - eps, z]) rotate([-90,0,0])
        cylinder(h = wall + 2*eps, r = dia/2, $fn = fn);
}
module rrect2d(w, h, r)
    hull() for (sx=[-1,1]) for (sy=[-1,1])
        translate([sx*(w/2 - r), sy*(h/2 - r)]) circle(r, $fn = fn);

// WG212 opening: elliptical mouth through the baffle + flange recess on the
// INSIDE of the baffle (matches the asymmetric OS waveguide in
// mk2_waveguide_os.scad, which mounts behind the baffle via the flange).
module baffle_wg(z) {
    // elliptical mouth pierces the baffle (eps overshoot both faces)
    translate([0, D/2 - wall - eps, z]) rotate([-90,0,0])
        linear_extrude(wall + 2*eps) scale([wg_mouth_w/2, wg_mouth_h/2]) circle(1, $fn = fn);
    // flange recess: pocket of depth wg_flange_t on the INNER baffle face so
    // the waveguide flange (5 mm thick, sits at z = wg_front - wg_flange_t ..
    // wg_front in the waveguide frame) lands flush against the baffle back face.
    // Open toward the cabinet interior (Y = D/2 - wall - wg_flange_t .. D/2 - wall).
    translate([0, D/2 - wall - wg_flange_t, z]) rotate([-90,0,0])
        linear_extrude(wg_flange_t + eps) rrect2d(wg_flange_w, wg_flange_h, wg_flange_r);
}
// woofer cut-out through a side panel (+/-X)
module side_cut(sign, z, dia) {
    translate([sign*(W/2 - wall - eps), 0, z]) rotate([0, sign*90, 0])
        cylinder(h = wall + 2*eps, r = dia/2, $fn = fn);
}

module enclosure() {
    difference() {
        outer();
        cavity();
        // front baffle: waveguide + midrange
        baffle_wg(tw_z);
        baffle_cut(mid_z, mid_cut_d);
        // sides: opposed push-push woofers at the same height
        side_cut(+1, woofer_z, woofer_cut_d);
        side_cut(-1, woofer_z, woofer_cut_d);
    }
}

// ---- Internal structure (representative) ----------------------------
module mid_chamber() {
    // sealed box behind the midrange, sitting just under the top
    z0 = mid_z - midchamber_h/2;
    color("LightSteelBlue", 0.65)
    translate([0, D/2 - wall - midchamber_d, z0])
        difference() {
            translate([-(mid_cut_d/2 + 18), 0, 0])
                cube([mid_cut_d + 36, midchamber_d, midchamber_h]);
            // open the front toward the baffle (where the mid mounts)
            translate([-mid_cut_d/2, -2, midchamber_h/2 - mid_cut_d/2])
                cube([mid_cut_d, wall + 4, mid_cut_d]);
        }
}

module brace_window(z) {
    // window brace ring tying the side panels around the woofer line
    color("Khaki", 0.8)
    translate([0, 0, z - 18]) linear_extrude(36)
        difference() { offset(-wall - 4) profile2d(W, D, round_r);
                       offset(-wall - 70) profile2d(W, D, round_r); }
}

module shelf_brace(z) {
    // bass/mid divider shelf
    color("Tan", 0.85)
    translate([0,0,z]) linear_extrude(wall) offset(-wall) profile2d(W, D, round_r);
}

module coupling_block() {
    // rigid block bonded across the ~22 mm gap between the opposed magnets
    color("IndianRed", 0.9)
    translate([0, 0, woofer_z]) rotate([0,90,0])
        cylinder(h = 26, r = 28, center = true, $fn = 48);
}

// ---- WG212 seated in the baffle (optional assembly) -----------------
module wg_in_baffle() {
    // Waveguide frame: throat at z=0, flange front face at z=wg_front, opening
    // toward +z.  rotate([-90,0,0]) maps the waveguide axis (+z) to the cabinet
    // baffle normal (+Y).
    //
    // Position so the FLANGE FRONT FACE aligns with the BAFFLE BACK FACE,
    // pushed in by wg_recess for a clean coplanar join (no coincident faces).
    // Y(z=0) = baffle_back_y - wg_front + wg_recess
    //       = (D/2 - wall) - wg_front + wg_recess
    // Y(z=wg_front) = baffle_back_y + wg_recess
    //
    // For protrusion > 0 the tube extends past the flange through the baffle
    // cutout; for protrusion = 0 (current default) the tube ends at the flange
    // and the baffle hole is the radiating aperture.
    color("Gainsboro")
    translate([0, D/2 - wall - wg_front + wg_recess, tw_z]) rotate([-90,0,0])
        waveguide();
}

if (show_internals) {
    difference() {
        union() {
            enclosure();
            mid_chamber();
            brace_window(woofer_z);
            shelf_brace(mid_z - midchamber_h/2 - 30);
            coupling_block();
            if (show_waveguide) wg_in_baffle();
        }
        // cutaway: remove the +X half for an internal view
        translate([0, -D, -10]) cube([W, 2*D, H + 20]);
    }
} else {
    enclosure();
    if (show_waveguide) wg_in_baffle();
}
