// =====================================================================
// Mk3 Reference Loudspeaker - cabinet (parametric, simulation-stage)
// =====================================================================
//
// v9 layout: 320 x 370 x 1080 mm, 22 mm birch ply, rounded front vertical
// edges, side-mounted push-push GRS 12SW-4HE woofers opposed at the same
// height. MIDRANGE (ScanSpeak 18W/4424G00) sits at the TOP of the front
// baffle with the sealed mid chamber behind it; the WAVEGUIDE sits BELOW
// the midrange, and the full-width tilted divider plate runs between them
// (mid chamber above, bass volume below — the waveguide body hangs in the
// bass volume; its bore is sealed by the tweeter and flange gasket).
//
// All driver dimensions come from official datasheets:
//   - GRS 12SW-4HE:        assets/datasheets/GRS-12SW-4HE.md
//   - ScanSpeak 18W/4424G00: cad/midrange.scad exports (18W-4424G00.pdf)
//   - SB26STAC + waveguide:  cad/waveguide.scad exports
// Anything that is an estimate rather than a datasheet value is marked
// ESTIMATE and must be caliper-verified before any panel is cut.
//
// The model computes its own volumes and mechanical clearances: open the
// console (or run openscad on the file) and read the ECHO block — bass and
// mid chamber volume in litres, predicted sealed Qtc/Fc, magnet gap,
// divider clearances, screw lands. Change any parameter and the numbers
// update automatically. WARNINGs are printed when something collides or
// misses its target.
//
// This is a DESIGN-CANDIDATE model for visualisation and dimension
// checking, NOT a cut list. See docs/07_cabinet_development.md and
// docs/09_volume_calculations.md.
//
// Axes: X = width, Y = depth (front baffle at +Y), Z = height (0 at floor).
// Units: millimetres.   Render: `openscad -o cabinet.stl cabinet.scad`
// ---------------------------------------------------------------------

// Pull in the waveguide and midrange models + their exported dimension
// functions (only modules/functions are imported; nothing renders unless
// the show_* flags are set).
use <waveguide.scad>
use <midrange.scad>
use <GRS-12SW-4HE.scad>
use <SB26STAC-C000-4.scad>

// ---- External shell -------------------------------------------------
W       = 320;   // external width  [mm] (276 internal — two opposed 136 mm
                 //   deep 12SW-4HE do not fit the older 300 mm spec)
D       = 400;   // external depth  [mm]
H       = 1180;  // external height [mm]
wall    = 22;    // panel thickness [mm] (22 mm birch plywood)
round_r = 19;    // front vertical roundover radius [mm] (R50 leaves no
                 //   flat for the 242 mm waveguide flange — checked below)

// ---- GRS 12SW-4HE woofer (assets/datasheets/GRS-12SW-4HE.md) ---------
woofer_frame_d  = 332;   // overall frame diameter        [datasheet]
woofer_cut_d    = 284;   // baffle cutout diameter        [datasheet]
woofer_bcd      = 319;   // mounting BCD, 8 holes         [datasheet]
woofer_hole_d   = 5.5;   // mounting hole diameter        [datasheet]
woofer_n_holes  = 8;     //                               [datasheet]
woofer_depth    = 136;   // total depth below mounting flange [datasheet]
woofer_displ_L  = 4.5;   // ESTIMATE: basket+magnet volume inside the box [L]
                         //   (GRS-12SW-4HE.md budgets 8-10 L per pair)
woofer_Fs       = 22;    // free-air resonance [Hz]       [datasheet]
woofer_Qts      = 0.43;  // total Q                       [datasheet]
woofer_Vas_L    = 80.4;  // equivalent volume [L]         [datasheet]

woofer_z        = 520;   // woofer centre height [mm] (docs ch.7: ~520 nominal)

// ---- ScanSpeak 18W/4424G00 midrange (all from cad/midrange.scad) -----
// Do NOT hardcode midrange numbers here — they track cad/midrange.scad,
// which carries the official drawing dimensions (18W-4424G00.pdf).
mid_face_d      = mid_flange_od_fn();   // Ø179.2 faceplate
mid_flange_t    = mid_flange_t_fn();    // 5.2 mm flange (rebate depth)
mid_depth       = mid_depth_fn();       // 72.2 mm total depth
mid_bcd         = mid_bcd_fn();         // Ø167 pitch circle
mid_hole_d      = mid_hole_d_fn();      // Ø5.3, x6 at 60 deg
mid_n_holes     = mid_n_holes_fn();
mid_bolt_offset = mid_bolt_offset_fn(); // 30 deg pattern offset
mid_cutout_clear = 0.5;                 // radial cutout clearance [mm]
mid_cut_d       = mid_cut_d_fn() + 2*mid_cutout_clear;  // Ø144.3 -> cut Ø145.3
mid_displ_L     = mid_displ_L_fn();     // 0.28 L displacement [datasheet]
mid_Fs          = mid_Fs_fn();          // 49 Hz
mid_Qts         = mid_Qts_fn();         // 0.38
mid_Vas_L       = mid_Vas_fn();         // 24.1 L
mid_flush       = true;   // rebate the faceplate flush into the front baffle
mid_fit_clear   = 0.7;    // rebate diametral clearance (faceplate tol +-0.3)

// ---- Driver placement (v9: midrange on TOP, waveguide below) ---------
mid_z  = 1065;          // midrange centre height [mm] — near the top; the
                       //   Ø145.3 cutout upper edge must stay clear of the
                       //   inner top face (checked below)
cc     = 164;          // mid/tweeter centre-to-centre [mm]. Physical minimum
                       //   with the Ø179.2 mid faceplate + 143 mm waveguide
                       //   flange both flush-recessed is ~164 mm (echoed
                       //   below as cc_min). DD-011's 140 mm is not reachable
                       //   with these parts.
tw_z   = mid_z - cc;   // waveguide/tweeter centre height [mm]

// ---- Waveguide (all values imported from cad/waveguide.scad) ---------
wg_flange_w = wg_flange_w_fn();   // flange width  242 [mm]
wg_flange_h = wg_flange_h_fn();   // flange height 143 [mm]
wg_flange_r = wg_flange_r_fn();   // flange corner radius [mm]
wg_flange_t = wg_flange_t_fn();   // flange thickness / recess depth [mm]
wg_front    = wg_front_z();       // z of flange FRONT face in the wg frame
wg_back     = wg_back_z();        // z of back-plate rear face in the wg frame
wg_fit_clear  = 0.5;   // flange recess w/h clearance [mm]
wg_body_clear = 1.5;   // radial clearance around the wg body in the baffle [mm]
// The waveguide is FRONT-mounted: the flange sits in a recess milled into
// the FRONT face of the baffle (flange front flush with the baffle front),
// and the body passes through a TAPERED clearance hole in the remaining
// thickness (following the body profile — this keeps the hole as small as
// possible at the inner face, which is what limits how close the divider
// plate above can come). Gasket the flange: the clearance gap opens into
// the bass volume behind it.
wg_clear_rx_o = wg_outer_rx(wg_front - wg_flange_t) + wg_body_clear; // at recess
wg_clear_ry_o = wg_outer_ry(wg_front - wg_flange_t) + wg_body_clear;
wg_clear_rx_i = wg_outer_rx(wg_front - wall) + wg_body_clear;        // at inner face
wg_clear_ry_i = wg_outer_ry(wg_front - wall) + wg_body_clear;
tw_body_displ_L = 0.25; // ESTIMATE: SB26STAC body behind the back plate [L]

// ---- Divider plate (mid chamber above / bass volume below) -----------
// Full-width tilted plate between the midrange and the waveguide: LOW at
// the front (squeezing under the mid basket), rising toward the rear. The
// tilt breaks the parallel ceiling/divider pair of the mid chamber and
// shrinks the chamber toward the datasheet's 13 L closed-box target.
// The plate height is DERIVED from the midrange basket envelope
// (mid_basket_r_at() from cad/midrange.scad): the basket cone falls away
// faster (~30 deg) than the divider rises (12 deg), so the binding point
// is at the inner baffle face.
divider_tilt      = 19;  // [deg] front edge low, rear edge high
divider_mid_clear = 18;   // clearance divider top -> mid basket underside [mm]
divider_front_z   = mid_z - mid_basket_r_at(wall) - divider_mid_clear;

// ---- Bracing ---------------------------------------------------------
shelf_zs  = [160, 330, 730]; // ring-shelf brace heights in the bass volume [mm]
shelf_rim = 45;         // ring-shelf rim width [mm] (open centre = airflow)
coupling_r = 55;        // coupling block radius [mm] — block length is
                        //   derived from the actual magnet gap (echoed)

// ---- Targets ----------------------------------------------------------
bass_target_L = 75;    // net bass volume target (docs/09) [L]
mid_target_L  = 13;    // 18W/4424G00 datasheet closed-box recommendation [L]

// ---- View flags (CI overrides these per render) ----------------------
show_internals      = false; // cutaway with divider + braces
show_waveguide      = false; // seat the waveguide model into the baffle
show_drivers        = false; // show real driver models for scale
show_pilot_holes    = true;  // Ø3 pilot holes on the datasheet BCDs
show_coupling_block = true;  // block between the opposed woofer magnets

eps = 0.1;             // generic cut overshoot for clean booleans [mm]
fn  = 64;
pilot_d = 3;           // pilot hole diameter [mm]

// =====================================================================
// Derived dimensions, volumes and mechanical checks (all automatic)
// =====================================================================
w_in = W - 2*wall;                 // internal width
d_in = D - 2*wall;                 // internal depth
h_in = H - 2*wall;                 // internal height

// horizontal cavity cross-section area at inset k from the outer profile
function sect_A(k) = (W - 2*k) * (D - 2*k)
                     - 2 * (1 - PI/4) * pow(max(round_r - k, 0), 2);
function sumv(v, i = 0) = i >= len(v) ? 0 : v[i] + sumv(v, i + 1);
function r1(x) = round(x * 10) / 10;
function r2(x) = round(x * 100) / 100;

A_in = sect_A(wall);               // internal cross-section [mm^2]

// woofers intrude (depth - wall) past the inner face when surface-mounted
magnet_gap = w_in - 2 * (woofer_depth - wall);

// divider plane: top surface passes (y = +d_in/2, z = divider_front_z),
// rising toward the rear at divider_tilt
div_top_avg = divider_front_z + (d_in/2) * tan(divider_tilt); // mean top z
div_rear_z  = divider_front_z + d_in * tan(divider_tilt);     // rear edge z
div_t_vert  = wall / cos(divider_tilt);   // vertical plate thickness

// ---- volumes [mm^3] ---------------------------------------------------
V_bass_gross = A_in * (div_top_avg - div_t_vert - wall);
V_mid_gross  = A_in * ((H - wall) - div_top_avg);

// brace displacement (notches for the woofer baskets ignored -> slightly
// conservative, i.e. net volumes err low)
V_window   = (sect_A(wall + 4) - sect_A(wall + 70)) * 36;
V_shelves  = len(shelf_zs) * (sect_A(wall) - sect_A(wall + shelf_rim)) * wall;
V_coupling = show_coupling_block ? PI * coupling_r * coupling_r * max(magnet_gap, 0) : 0;

// waveguide body behind the inner baffle face (numeric integration of the
// exported outer profile) + its tweeter back plate — sits in the BASS volume
V_wg = let(z1 = wg_front - wall, n = 48, dz = z1 / n)
       sumv([for (i = [0:n-1]) let(zm = (i + 0.5) * dz)
             PI * wg_outer_rx(zm) * wg_outer_ry(zm) * dz])
       + PI * pow(wg_backplate_d_fn()/2, 2) * wg_backplate_t_fn();

V_bass_net = V_bass_gross - 2*woofer_displ_L*1e6 - V_window - V_shelves
             - V_coupling - V_wg - tw_body_displ_L*1e6;
V_mid_net  = V_mid_gross - mid_displ_L*1e6;

// ---- predicted sealed alignments (simplified, no damping/stuffing) ----
Vb_per_woofer = (V_bass_net / 1e6) / 2;      // shared volume, split per driver
bass_ratio = sqrt(1 + woofer_Vas_L / Vb_per_woofer);
bass_Qtc   = woofer_Qts * bass_ratio;
bass_Fc    = woofer_Fs  * bass_ratio;
mid_ratio  = sqrt(1 + mid_Vas_L / (V_mid_net / 1e6));
mid_Qtc    = mid_Qts * mid_ratio;
mid_Fc     = mid_Fs  * mid_ratio;

// ---- mechanical clearance checks --------------------------------------
// woofer cutout vs divider underside (measured in the side-panel plane)
woofer_div_clear = (div_top_avg - div_t_vert - woofer_z) * cos(divider_tilt)
                   - woofer_cut_d/2;
mid_screw_land = (mid_bcd - mid_hole_d - mid_cut_d) / 2;  // wood inside BCD
mid_top_margin = (H - wall) - (mid_z + mid_cut_d/2);      // cutout vs inner top
flat_front_w   = W - 2*round_r;               // flat width of the front face
side_cut_margin = (D - woofer_cut_d) / 2;     // side panel margin at cutout
// vertical gap on the front face between the mid rebate (above) and the
// waveguide flange recess (below)
baffle_gap = (mid_z - (mid_face_d + mid_fit_clear)/2)
             - (tw_z + (wg_flange_h + wg_fit_clear)/2);
// divider window at the inner baffle face: below the mid basket, above the
// waveguide clearance hole
div_window = (divider_front_z - div_t_vert) - (tw_z + wg_clear_ry_i + 5);
cc_min = max((wg_flange_h + wg_fit_clear + mid_face_d + mid_fit_clear)/2 + 2,
             cc - div_window + 3);

echo("=================================================================");
echo(str("Mk3 cabinet v9 ", W, " x ", D, " x ", H, " mm, wall ", wall,
         " mm  |  internal ", w_in, " x ", d_in, " x ", h_in, " mm"));
echo(str("Layout: mid 18W/4424G00 @ ", mid_z, " mm (top), waveguide @ ", tw_z,
         " mm, divider between, woofers @ ", woofer_z, " mm"));
echo(str("BASS chamber: gross ", r1(V_bass_gross/1e6), " L, net ~",
         r1(V_bass_net/1e6), " L (target ", bass_target_L, " L)  |  ",
         r1(Vb_per_woofer), " L per woofer"));
echo(str("  -> sealed estimate: Qtc ~", r2(bass_Qtc), ", Fc ~", r1(bass_Fc),
         " Hz   (Fs ", woofer_Fs, " Hz, Qts ", woofer_Qts, ", Vas ",
         woofer_Vas_L, " L)"));
echo(str("MID chamber: gross ", r1(V_mid_gross/1e6), " L, net ~",
         r1(V_mid_net/1e6), " L (datasheet closed-box rec. ", mid_target_L, " L)"));
echo(str("  -> sealed estimate: Qtc ~", r2(mid_Qtc), ", Fc ~", r1(mid_Fc),
         " Hz   (Fs ", mid_Fs, " Hz, Qts ", mid_Qts, ", Vas ", mid_Vas_L, " L)"));
echo(str("Divider plate: front edge ", r1(divider_front_z), " mm, rear edge ",
         r1(div_rear_z), " mm, tilt ", divider_tilt, " deg (front low)"));
echo(str("Displacements: woofers ", 2*woofer_displ_L, " L, braces ",
         r1((V_window + V_shelves + V_coupling)/1e6), " L, waveguide+tweeter ",
         r1((V_wg + tw_body_displ_L*1e6)/1e6), " L (in bass), mid driver ",
         mid_displ_L, " L (in mid)"));
echo(str("Woofer magnet gap (push-push): ", r1(magnet_gap),
         " mm  -> coupling block length"));
echo(str("Woofer cutout -> divider clearance: ", r1(woofer_div_clear), " mm"));
echo(str("Mid cutout Ø", r1(mid_cut_d), ": screw land ", r1(mid_screw_land),
         " mm inside BCD Ø", mid_bcd, ", top panel margin ", r1(mid_top_margin),
         " mm"));
echo(str("Front baffle flat width ", flat_front_w, " mm vs waveguide flange ",
         wg_flange_w + wg_fit_clear, " mm  |  mid-wg face gap ", r1(baffle_gap),
         " mm  |  divider window ", r1(div_window), " mm  |  min c-c ",
         r1(cc_min), " mm"));
echo("=================================================================");

if (V_bass_net/1e6 < bass_target_L)
    echo(str("WARNING: bass net volume ", r1(V_bass_net/1e6), " L is below the ",
             bass_target_L, " L target — raise the divider, grow the cabinet, ",
             "or revise the target/alignment."));
if (abs(V_mid_net/1e6 - mid_target_L) > 4)
    echo(str("WARNING: mid chamber ", r1(V_mid_net/1e6), " L is far from the ",
             mid_target_L, " L datasheet recommendation — adjust divider_tilt ",
             "or divider_mid_clear."));
if (magnet_gap < 2)
    echo("WARNING: opposed woofer magnets collide — cabinet too narrow (W).");
if (woofer_div_clear < 5)
    echo("WARNING: divider plate hits the woofer cutout — lower woofer_z or raise the divider.");
if (mid_screw_land < 3)
    echo("WARNING: mid cutout leaves <3 mm screw land inside the mounting BCD.");
if (mid_top_margin < 10)
    echo("WARNING: mid cutout too close to the inner top face — lower mid_z.");
if (flat_front_w < wg_flange_w + wg_fit_clear + 2)
    echo("WARNING: front roundovers eat into the waveguide flange recess — reduce round_r.");
if (baffle_gap < 2)
    echo("WARNING: mid rebate and waveguide recess overlap on the baffle — increase cc.");
if (div_window < 3)
    echo("WARNING: no room for the divider between the mid basket and the waveguide hole — increase cc or thin the divider.");
if (side_cut_margin < 30)
    echo("WARNING: <30 mm side panel margin around the woofer cutout.");

// =====================================================================
// Geometry
// =====================================================================

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

module rrect2d(w, h, r)
    hull() for (sx=[-1,1]) for (sy=[-1,1])
        translate([sx*(w/2 - r), sy*(h/2 - r)]) circle(r, $fn = fn);

// driver cut-out: pierce the full baffle thickness with eps overshoot both faces
module baffle_cut(z, dia) {
    translate([0, D/2 - wall - eps, z]) rotate([-90,0,0])
        cylinder(h = wall + 2*eps, r = dia/2, $fn = fn);
}

// thin elliptical slab used as a hull section for the tapered wg hole
module wg_hole_section(y, rx, ry, z) {
    translate([0, y, z]) rotate([-90,0,0])
        linear_extrude(eps) scale([rx, ry]) circle(1, $fn = fn);
}

// Waveguide opening, FRONT-mounted:
//  1) flange recess milled into the FRONT face (depth = flange thickness,
//     so the flange front sits flush with the baffle front), and
//  2) a TAPERED elliptical clearance hole for the waveguide body through
//     the remaining thickness, lofted between the exported outer profile
//     at the inner face and at the recess bottom (the body profile is
//     convex, so the straight taper always clears it).
module baffle_wg(z) {
    translate([0, D/2 - wg_flange_t, z]) rotate([-90,0,0])
        linear_extrude(wg_flange_t + eps)
            rrect2d(wg_flange_w + wg_fit_clear, wg_flange_h + wg_fit_clear, wg_flange_r);
    hull() {
        wg_hole_section(D/2 - wall - eps,        wg_clear_rx_i, wg_clear_ry_i, z);
        wg_hole_section(D/2 - wg_flange_t + eps, wg_clear_rx_o, wg_clear_ry_o, z);
    }
    // pilot holes for the flange's countersunk baffle screws (blind, 12 mm)
    if (show_pilot_holes)
        for (sx=[-1,1]) for (sy=[-1,1])
            translate([sx*wg_baf_bcd_x_fn()/2, D/2 - wg_flange_t - 12,
                       z + sy*wg_baf_bcd_y_fn()/2])
                rotate([-90,0,0]) cylinder(h = 12 + eps, d = pilot_d, $fn = 24);
}

// Midrange opening: through cutout + flush-mount faceplate rebate + pilots
// (18W/4424G00: 6 x Ø5.3 on Ø167 BCD, pattern offset 30 deg)
module baffle_mid(z) {
    baffle_cut(z, mid_cut_d);
    if (mid_flush)
        translate([0, D/2 - mid_flange_t, z]) rotate([-90,0,0])
            cylinder(h = mid_flange_t + eps, d = mid_face_d + mid_fit_clear, $fn = fn);
    if (show_pilot_holes)
        for (i = [0:mid_n_holes-1]) {
            a = mid_bolt_offset + i * 360/mid_n_holes;
            translate([(mid_bcd/2)*cos(a), D/2 - wall - eps, z + (mid_bcd/2)*sin(a)])
                rotate([-90,0,0]) cylinder(h = wall + 2*eps, d = pilot_d, $fn = 24);
        }
}

// woofer cut-out through a side panel (+/-X)
module side_cut(sign, z, dia) {
    translate([sign*(W/2 - wall - eps), 0, z]) rotate([0, sign*90, 0])
        cylinder(h = wall + 2*eps, r = dia/2, $fn = fn);
}
// woofer mounting pilots (datasheet: 8 x Ø5.5 on Ø319 BCD)
module side_pilots(sign, z) {
    for (a = [0:360/woofer_n_holes:359])
        translate([sign*(W/2 - wall - eps), (woofer_bcd/2)*cos(a), z + (woofer_bcd/2)*sin(a)])
            rotate([0, sign*90, 0]) cylinder(h = wall + 2*eps, d = pilot_d, $fn = 24);
}

module enclosure() {
    difference() {
        outer();
        cavity();
        // front baffle: midrange on top, waveguide below
        baffle_mid(mid_z);
        baffle_wg(tw_z);
        // sides: opposed push-push woofers at the same height
        side_cut(+1, woofer_z, woofer_cut_d);
        side_cut(-1, woofer_z, woofer_cut_d);
        if (show_pilot_holes) { side_pilots(+1, woofer_z); side_pilots(-1, woofer_z); }
    }
}

// ---- Internal structure ----------------------------------------------

// conical clearance volume for the woofer baskets (frame -> magnet), used
// to notch every brace that crosses the woofer region
module woofer_body_clear() {
    for (s = [-1, 1])
        translate([s*(w_in/2 + eps), 0, woofer_z]) rotate([0, -s*90, 0])
            cylinder(h = woofer_depth, r1 = woofer_cut_d/2 + 8, r2 = 85, $fn = 48);
}

// Full-width tilted divider plate between the midrange (above) and the
// waveguide (below). Built as an intersection of a tilted slab with the
// cavity prism so it meets every wall exactly, at any tilt. Extends 1 mm
// into the walls so it welds cleanly in the assembly view.
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

// window brace ring tying all four panels around the woofer line,
// notched for the woofer baskets
module brace_window(z) {
    color("Blue", 0.8)
    difference() {
        translate([0, 0, z - 18]) linear_extrude(36)
            difference() { offset(-wall - 4)  profile2d(W, D, round_r);
                           offset(-wall - 70) profile2d(W, D, round_r); }
        woofer_body_clear();
    }
}

// ring shelf brace: ties all four panels, open centre so the bass volume
// stays one connected air space, notched for the woofer baskets
module shelf_ring(z) {
    color("Red", 0.7)
    difference() {
        translate([0, 0, z]) linear_extrude(wall)
            difference() { offset(-wall + 1)         profile2d(W, D, round_r);
                           offset(-wall - shelf_rim) profile2d(W, D, round_r); }
        woofer_body_clear();
    }
}

// rigid block bonded between the opposed 12SW magnet back plates; its
// length is DERIVED from the actual magnet gap so it always just fits
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

// ---- Waveguide seated in the baffle (optional assembly) ---------------
// Front-mounted: flange front face flush with the baffle FRONT face.
// The waveguide frame has its throat at z=0 opening toward +z, so
// Y(z=0) = D/2 - wg_front puts the flange front exactly at Y = D/2.
module wg_in_baffle() {
    color("Gainsboro")
    translate([0, D/2 - wg_front, tw_z]) rotate([-90,0,0])
        waveguide();
}

// ---- Driver models (real parametric models) --------------------------
module driver_woofer(sign) {
    // GRS 12SW-4HE: surface-mounted on the side panel, flange front at z=0
    // The driver() module has flange front at z=0, body toward -z
    // rotate([0, sign*90, 0]) maps -z (body) to -sign*x → into the cabinet
    translate([sign*(W/2), 0, woofer_z]) rotate([0, sign*90, 0]) {
        driver();
    }
}
module driver_mid() {
    // ScanSpeak 18W/4424G00 — the real parametric model from
    // cad/midrange.scad, flange front flush with the baffle front when
    // mid_flush (its local frame: flange front at z=0, body toward -z).
    translate([0, D/2 + (mid_flush ? 0 : mid_flange_t), mid_z])
        rotate([-90,0,0]) midrange_driver();
}
module driver_tweeter() {
    // SB26STAC-C000-4: faceplate seated in the waveguide back-plate
    // pocket, motor behind it. diskant() has frontplate front at z=0,
    // motor toward -z.
    translate([0, D/2 - wg_front + wg_back, tw_z]) rotate([-90,0,0]) {
        diskant();
    }
}

// ---- Top-level ---------------------------------------------------------
if (show_internals) {
    difference() {
        union() {
            enclosure();
            internals();
            if (show_waveguide) wg_in_baffle();
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
    if (show_drivers) {
        driver_woofer(+1);
        driver_woofer(-1);
        driver_mid();
        if (show_waveguide) driver_tweeter();
    }
}
