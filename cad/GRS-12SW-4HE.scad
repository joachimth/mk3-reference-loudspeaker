// ============================================================
//  GRS 12SW-4HE - 12" High Excursion Subwoofer (sidefyret bas)
//  Parametrisk OpenSCAD-model ud fra datablad-tegning
//  Alle maal i mm.  Front af flange = z=0, enheden gaar i -z.
// ============================================================

/* [Visning] */
vis = "driver"; // [driver:Komplet enhed, cutout:Baffel-udskaering (2D), skabelon:Boreskabelon (3D), snit:Halvsnit]

/* [Kotede maal - fra datablad] */
flange_od      = 308;    // Udvendig flangediameter (Ø308)
flange_tyk     = 8.5;    // Flange-/pakningstykkelse
udskaering_dia = 280;    // Kurv-/udskaeringsdiameter (Ø280)
total_dybde    = 160;    // Samlet dybde inkl. bump (max)
magnet_bagside = 148;    // Dybde til magnetens (flade) bagside
bolt_cirkel    = 295;    // Hulcirkel (Ø295)
bolt_hul_dia   = 5.5;    // Monteringshuller (Ø5,5)
antal_huller   = 8;      // Antal huller (45 grader indbyrdes)
bolt_offset    = 0;      // Vinkelforskydning [grader]

/* [Estimerede maal - IKKE kotet, juster efter behov] */
vc_dia        = 50.8;  // Svingspolediameter (fra datablad)
kegle_top_dia = 245;   // Keglens diameter oppe (ved surround)
surround_od   = 272;   // Surround yderdiameter
kegle_bund_dia= 58;    // Keglens diameter nede
kegle_hoejde  = 78;    // Keglens dybde
stoevhat_dia  = 95;    // Stoevhaettens diameter
stoevhat_z    = -18;   // Stoevhaettens centrum-dybde (0 = flangefront)
magnet_dia    = 140;   // Magnetdiameter (Ø140)
magnet_hoejde = 40;    // Magnethoejde

/* [Baffel] */
baffel_tyk       = 21;
cutout_clearance = 1.0;  // Ekstra paa udskaering (radius pr. side)

/* [Render] */
$fn = 140;
eps = 0.05;

magnet_start_z = -(magnet_bagside - magnet_hoejde); // magnetens front

// ------------------------------------------------------------
module bolt_hoved() {
    for (i=[0:antal_huller-1]) {
        a = bolt_offset + i*360/antal_huller;
        rotate([0,0,a]) translate([bolt_cirkel/2,0,0]) children();
    }
}
module bolt_huller(h,z0) { bolt_hoved() translate([0,0,z0]) cylinder(d=bolt_hul_dia,h=h); }

// Flange / frontplade - KOTET
module flange() {
    color("dimgray")
    difference() {
        translate([0,0,-flange_tyk]) cylinder(d=flange_od,h=flange_tyk);
        translate([0,0,-flange_tyk-eps]) cylinder(d=surround_od,h=flange_tyk+2*eps);
        bolt_huller(flange_tyk+2*eps,-flange_tyk-eps);
    }
}

// Kurv (tynd konisk skal) - ESTIMAT
module kurv() {
    v=4;
    color("gray")
    difference() {
        hull() {
            translate([0,0,-flange_tyk]) cylinder(d=udskaering_dia,h=eps);
            translate([0,0,magnet_start_z]) cylinder(d=magnet_dia,h=eps);
        }
        hull() {
            translate([0,0,-flange_tyk-eps]) cylinder(d=udskaering_dia-2*v,h=eps);
            translate([0,0,magnet_start_z+v]) cylinder(d=magnet_dia-2*v,h=eps);
        }
        translate([0,0,-flange_tyk-eps]) cylinder(d=udskaering_dia-2*v,h=eps+v);
    }
}

// Surround - ESTIMAT
module surround() {
    r=(surround_od-kegle_top_dia)/4; c=kegle_top_dia/2+r;
    color("black") translate([0,0,-flange_tyk])
        rotate_extrude() translate([c,0]) circle(r=r);
}

// Kegle - ESTIMAT
module kegle() {
    v=2; top=-flange_tyk-3;
    color("peru") translate([0,0,top-kegle_hoejde])
    difference() {
        cylinder(d1=kegle_bund_dia,d2=kegle_top_dia,h=kegle_hoejde);
        translate([0,0,v]) cylinder(d1=kegle_bund_dia-2*v,d2=kegle_top_dia-2*v,h=kegle_hoejde);
    }
}

// Stoevhat - ESTIMAT
module stoevhat() {
    color("saddlebrown") translate([0,0,stoevhat_z]) scale([1,1,0.4]) sphere(d=stoevhat_dia);
}

// Magnetsystem - ESTIMAT (Ø140 x 40, bumpet bagplade til dybde 160)
module magnet() {
    color("dimgray") union() {
        translate([0,0,-magnet_bagside]) cylinder(d=magnet_dia,h=magnet_hoejde);
        translate([0,0,magnet_start_z-eps]) cylinder(d1=magnet_dia,d2=vc_dia+18,h=14);
        // bumpet bagplade (fra 148 til 160)
        translate([0,0,-total_dybde]) cylinder(d=magnet_dia*0.5,h=total_dybde-magnet_bagside);
    }
}

module driver() { flange(); kurv(); surround(); kegle(); stoevhat(); magnet(); }

// ------------------------------------------------------------
module baffel_cutout_2d() {
    circle(d=udskaering_dia+2*cutout_clearance);
    bolt_hoved() circle(d=bolt_hul_dia);
}
module boreskabelon() {
    od=flange_od+8; t=4;
    difference() {
        cylinder(d=od,h=t);
        translate([0,0,-eps]) cylinder(d=udskaering_dia,h=t+2*eps);
        bolt_huller(t+2*eps,-eps);
    }
    difference() { cylinder(d=flange_od,h=0.6); translate([0,0,-eps]) cylinder(d=flange_od-1.5,h=0.6+2*eps); }
}

// ------------------------------------------------------------
if (vis=="driver") driver();
else if (vis=="cutout") baffel_cutout_2d();
else if (vis=="skabelon") boreskabelon();
else if (vis=="snit") difference(){ driver(); translate([0,-250,-250]) cube([250,500,500]); }
