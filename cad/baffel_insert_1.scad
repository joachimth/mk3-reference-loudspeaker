// ============================================================
//  MODULAER BAFFEL-INSERT v2  (3D-print)
//  - 18W/4424G00 mellemtone, PLANFRAESET (flush rebate)
//  - WG212 waveguide (SB26STAC) i FLUSH RUM + elliptisk kropshul
//  - Diskanten sidder BAG waveguiden (paa dens bagplade)
//
//  KOBLER TIL waveguide.scad via 'use' - alle WG-maal hentes fra
//  dens egne funktioner (flange, krop, skruemoenster). Hold begge
//  filer i samme mappe.
//
//  Front = +Z, bagside = 0.  PRINT: bagside paa pladen, front opad.
// ============================================================

use <waveguide.scad>
use <midrange.scad>
use <SB26STAC-C000-4.scad>

/* [Visning] */
vis = "baffel"; // [baffel:Printklar insert, fit:Med rigtige enheder (GUI-preview), snit:Lodret halvsnit]

/* [Plade] */
baffel_b   = 285;   // Bredde (rummer WG-flangens 242 mm)
baffel_h   = 380;   // Hoejde
baffel_tyk = 15;    // Pladetykkelse
hjoerne_r  = 14;    // Hjoerneradius

/* [Placering] */
enhed_cc      = 164; // Center-center mellemtone <-> waveguide
gruppe_offset = 9;   // Loft gruppen for lige marginer

/* [Mellemtone 18W/4424G00 - KOTEDE maal] */
mid_udskaering   = 144.30;
mid_flange_dia   = 179.20;
mid_flange_tyk   = 5.20;
mid_bolt_cirkel  = 167.0;
mid_bolt_antal   = 6;
mid_bolt_offset  = 30;
mid_bolt_hul     = 5.50;
mid_udsk_clear   = 0.6;
mid_flange_clear = 0.6;
mid_rebate_ekstra= 0.2;

/* [Waveguide WG212 - hentet fra waveguide.scad, kun spillerum her] */
wg_flange_clear = 0.4;   // Sidespillerum paa fals (pr. side)
wg_pocket_ekstra= 0.3;   // Ekstra falsdybde
wg_body_clear   = 1.5;   // Spillerum paa kropshul (radius)
wg_baf_hul      = 5.6;   // Baflens skruehul til WG (M4 heat-set insert)

/* [Kabinet-montering - undersaenkede skruer i kanten] */
kant_inset   = 12;
kant_v_antal = 4;
kant_h_antal = 2;
ks_hul       = 4.50;
ks_hoved     = 9.0;
ks_dybde     = 2.5;

/* [Afstivning bagside] */
ribber       = true;
rib_tyk      = 4;
rib_hoejde   = 8;
rib_ramme_inset = 8;

/* [Render] */
$fn = 120;
eps = 0.05;

// --- afledte positioner ---
mid_cy = -enhed_cc/2 + gruppe_offset;
wg_cy  =  enhed_cc/2 + gruppe_offset;

// --- WG-maal hentet fra waveguide.scad ---
WG_FLW = wg_flange_w_fn();
WG_FLH = wg_flange_h_fn();
WG_FLR = wg_flange_r_fn();
WG_FLT = wg_flange_t_fn();
WG_FLOOR_Z = wg_front_z() - WG_FLT;
WG_BRX = wg_outer_rx(WG_FLOOR_Z);
WG_BRY = wg_outer_ry(WG_FLOOR_Z);
WG_SX  = wg_baf_bcd_x_fn()/2;
WG_SY  = wg_baf_bcd_y_fn()/2;

// ------------------------------------------------------------
module rrect(w,h,r) { offset(r=r) offset(delta=-r) square([w,h], center=true); }
module plade() { linear_extrude(baffel_tyk) rrect(baffel_b, baffel_h, hjoerne_r); }

module ribber_bagside() {
    linear_extrude(rib_hoejde) {
        difference() {
            rrect(baffel_b-2*rib_ramme_inset, baffel_h-2*rib_ramme_inset, max(1,hjoerne_r-rib_ramme_inset));
            rrect(baffel_b-2*rib_ramme_inset-2*rib_tyk, baffel_h-2*rib_ramme_inset-2*rib_tyk, max(1,hjoerne_r-rib_ramme_inset));
        }
        translate([-rib_tyk/2, -baffel_h/2+rib_ramme_inset]) square([rib_tyk, baffel_h-2*rib_ramme_inset]);
        translate([-baffel_b/2+rib_ramme_inset, gruppe_offset-rib_tyk/2]) square([baffel_b-2*rib_ramme_inset, rib_tyk]);
    }
}

// ------------------------------------------------------------
module boltring(cirkel, antal, off_a) {
    for (i=[0:antal-1]) rotate([0,0,off_a+i*360/antal]) translate([cirkel/2,0,0]) children();
}

module mid_neg() {
    translate([0, mid_cy, 0]) {
        translate([0,0,-eps]) cylinder(d=mid_udskaering+2*mid_udsk_clear, h=baffel_tyk+2*eps);
        translate([0,0, baffel_tyk-(mid_flange_tyk+mid_rebate_ekstra)])
            cylinder(d=mid_flange_dia+2*mid_flange_clear, h=mid_flange_tyk+mid_rebate_ekstra+eps);
        boltring(mid_bolt_cirkel, mid_bolt_antal, mid_bolt_offset)
            translate([0,0,-eps]) cylinder(d=mid_bolt_hul, h=baffel_tyk+2*eps);
    }
}

module wg_neg() {
    translate([0, wg_cy, 0]) {
        translate([0,0, baffel_tyk-(WG_FLT+wg_pocket_ekstra)])
            linear_extrude(WG_FLT+wg_pocket_ekstra+eps)
                rrect(WG_FLW+2*wg_flange_clear, WG_FLH+2*wg_flange_clear, WG_FLR);
        translate([0,0,-eps])
            linear_extrude(baffel_tyk+2*eps)
                scale([WG_BRX+wg_body_clear, WG_BRY+wg_body_clear]) circle(r=1);
        for (sx=[-1,1], sy=[-1,1])
            translate([sx*WG_SX, sy*WG_SY, -eps]) cylinder(d=wg_baf_hul, h=baffel_tyk+2*eps);
    }
}

module kant_skrue(x,y) {
    translate([x,y,-eps]) cylinder(d=ks_hul, h=baffel_tyk+2*eps);
    translate([x,y,baffel_tyk-ks_dybde]) cylinder(d1=ks_hul, d2=ks_hoved, h=ks_dybde+eps);
}
module kant_neg() {
    xv=baffel_b/2-kant_inset; yh=baffel_h/2-kant_inset;
    for (s=[-1,1], i=[0:kant_v_antal-1]) kant_skrue(s*xv, -yh + i*(2*yh)/(kant_v_antal-1));
    for (s=[-1,1], i=[0:kant_h_antal-1]) {
        x = (kant_h_antal==1)?0:-(xv-25)+i*2*(xv-25)/(kant_h_antal-1);
        kant_skrue(x, s*yh);
    }
}

// ------------------------------------------------------------
module baffel() {
    difference() {
        union() { plade(); if (ribber) ribber_bagside(); }
        mid_neg();
        wg_neg();
        kant_neg();
    }
}

// ------------------------------------------------------------
mid_ref_front = 80.1;
module fit() {
    baffel();
    // 18W/4424G00 midrange — real parametric model, flange front flush with insert front
    color("dimgray")
        translate([0, mid_cy, baffel_tyk - mid_ref_front])
            rotate([90,0,0]) midrange_driver();
    // WG212 waveguide — already imported via use <waveguide.scad>
    color("gray")
        translate([0, wg_cy, baffel_tyk - wg_front_z()]) waveguide();
    // SB26STAC-C000-4 tweeter — real parametric model, seated behind waveguide
    color("silver")
        translate([0, wg_cy, baffel_tyk - wg_front_z() + wg_back_z() + 4])
            diskant();
}

// ------------------------------------------------------------
if (vis=="baffel") baffel();
else if (vis=="fit") fit();
else if (vis=="snit")
    difference(){ baffel(); translate([-baffel_b,0,-baffel_tyk]) cube([2*baffel_b, baffel_b, 3*baffel_tyk]); }
