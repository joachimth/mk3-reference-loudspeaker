// =====================================================================
// Mk2 Reference Loudspeaker - cabinet (parametric, simulation-stage)
// =====================================================================
//
// v6b enclosure: 320 x 370 x 1080 mm, 22 mm birch ply, R50 front vertical
// roundovers, side-mounted push-push GRS 12SW-4HE woofers opposed at the same
// height, sealed midrange chamber above a full-width divider plate (bass volume
// below), WG212 + 15W on the front baffle at ~150 mm c-c.
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
use <waveguide.scad>

// ---- External shell -------------------------------------------------
W      = 320;    // width  [mm]
D      = 370;    // depth  [mm]
H      = 1080;   // height [mm]
wall   = 22;     // panel thickness [mm]
round_r = 40;    // R50 front vertical roundovers [mm]

// ---- Driver placement (estimates) -----------------------------------
woofer_z      = 520;   // opposed push-push woofer centre height [mm]
                      //   284 mm cutout on the 370 mm deep side panel leaves
                      //   ~43 mm margin each side; 520 mm keeps the woofer clear
                      //   of the mid-chamber divider plate above.
woofer_cut_d  = 284;   // GRS 12SW-4HE cut-out diameter [mm] (datasheet Ø284)

tw_z          = 900;   // WG212/tweeter acoustic centre height [mm]
cc            = 150;   // mid/tweeter centre-to-centre [mm] (DD-011 realistic)
mid_z         = tw_z - cc;
// WG212 opening matches cad/mk2_waveguide_os.scad (asymmetric OS waveguide)
// WG212 mouth and flange dimensions — derived from mk2_waveguide_os.scad via
// exported functions so they stay in sync automatically when the waveguide
// profile changes (throat_d, angles, etc.).  Do NOT hardcode these here.
wg_mouth_w    = wg_flange_w_fn();    // WG212 mouth width  (horizontal) [mm]
wg_mouth_h    = wg_flange_h_fn();    // WG212 mouth height (vertical)   [mm]
wg_flange_w   = wg_flange_w_fn();     // WG212 flange recess width  [mm]
wg_flange_h   = wg_flange_h_fn();     // WG212 flange recess height [mm]
wg_flange_r   = wg_flange_r_fn();     // flange corner radius [mm]
wg_flange_t   = wg_flange_t_fn();     // flange thickness / recess depth [mm]
mid_cut_d     = 72;    // 15W/4434G00 cut-out diameter [mm] - from datasheet drawing (chassis/basket Ø72 mm)

// ---- Internals ------------------------------------------------------
midchamber_h  = 175;   // internal height of the sealed mid chamber [mm]
midchamber_d  = 282;   // internal depth of the mid chamber [mm] (<= inner depth)
show_internals = false;  // true: cutaway with mid chamber + braces (CI overrides per view)
show_waveguide = false; // true: seat the WG212 model into the baffle (CI overrides per view)
show_drivers = false;   // true: show placeholder driver disks for scale reference

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
wg_recess      = wall+0.01;   // small overlap into the baffle material [mm] for clean CSG //Editied since it needs to blend into the front baffel and not the back of the baffel.

eps = 0.1;             // generic cut overshoot for clean booleans [mm]
fn = 64;
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
    // Sealed mid chamber above a full-width divider plate. The divider runs the
    // full internal width and depth at z0 (bottom of the mid chamber), so ALL
    // volume below the plate is bass volume (for the GRS 12SW-4HE push-push
    // woofers) and the volume above the plate — bounded by the cabinet walls,
    // the divider, and the top panel, around the midrange driver — is the sealed
    // mid chamber. The divider is rendered by shelf_brace() so the two volumes
    // are structurally and acoustically isolated.
    z0 = mid_z - midchamber_h/2;
    shelf_brace(z0);
}

module brace_window(z) {
    // window brace ring tying the side panels around the woofer line
    color("Khaki", 0.8)
    translate([0, 0, z - 18]) linear_extrude(36)
        difference() { offset(-wall - 4) profile2d(W, D, round_r);
                       offset(-wall - 70) profile2d(W, D, round_r); }
}

module shelf_brace(z) {
    // Full-width divider plate separating the bass volume (below) from the
    // sealed mid chamber (above). Runs the full internal width and depth so the
    // two volumes are structurally and acoustically isolated.
    color("Tan", 0.85)
    translate([0,0,z]) linear_extrude(wall) offset(-wall) profile2d(W, D, round_r);
}

module coupling_block() {
    // rigid block bonded across the gap between the opposed 12SW magnet back
    // plates. With ~136 mm mounting depth each and 276 mm internal width
    // (W - 2*wall) the magnets nearly meet (~4 mm gap); the block overlaps both
    // back plates to tie the push-push pair together rigidly.
    color("IndianRed", 0.9)
    translate([0, 0, woofer_z]) rotate([0,90,0])
        cylinder(h = 20, r = 55, center = true, $fn = 48);
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

  // ---- Placeholder driver disks for scale visualization ----------------
  // Simple colored disks representing the physical driver sizes for render scale.
  // These are NOT accurate driver models - just visual references for cabinet renders.
  module driver_woofer_placeholder(sign) {
      // GRS 12SW-4HE: ~332mm overall frame, Ø284mm cutout, ~136mm total depth.
      // Frame disk sits in the side-panel plane; basket/magnet extends inward.
      color("DarkSlateGray", 0.85)
      translate([sign*(W/2), 0, woofer_z]) rotate([0, -sign*90, 0]) {
          // frame/faceplate disk at the side-panel plane
          cylinder(h = 8, r = 166, $fn = 64);
          // basket + magnet depth extending inward toward cabinet centre
          translate([0, 0, 8])
              cylinder(h = 128, r = 70, $fn = 48);
      }
  }
  module driver_mid_placeholder() {
      // 15W/4434G00: ~104mm faceplate
      color("DimGray", 0.85)
      translate([0, D/2 + 10, mid_z]) rotate([-90, 0, 0])
          cylinder(h = 20, r = 52, $fn = 48);
  }
  module driver_tweeter_placeholder() {
      // H2606/920000: ~25mm dome + small faceplate
      color("Silver", 0.9)
      translate([0, D/2 - wall - wg_front + wg_recess + 5, tw_z]) rotate([-90, 0, 0])
          cylinder(h = 15, r = 35, $fn = 32);
  }

if (show_internals) {
      difference() {
          union() {
              enclosure();
              mid_chamber();
              brace_window(woofer_z);
              coupling_block();
              if (show_waveguide) wg_in_baffle();
              if (show_drivers) {
                  driver_woofer_placeholder(+1);
                  driver_woofer_placeholder(-1);
                  driver_mid_placeholder();
                  if (show_waveguide) driver_tweeter_placeholder();
              }
          }
          // cutaway: remove the +X half for an internal view
          translate([0, -D, -10]) cube([W, 2*D, H + 20]);
      }
  } else {
      enclosure();
      if (show_waveguide) wg_in_baffle();
      if (show_drivers) {
          driver_woofer_placeholder(+1);
          driver_woofer_placeholder(-1);
          driver_mid_placeholder();
          if (show_waveguide) driver_tweeter_placeholder();
      }
  }
