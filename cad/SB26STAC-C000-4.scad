// ============================================================
//  SB Acoustics SB26STAC-C000-4  - 26 mm diskant
//  Parametrisk OpenSCAD-model, maalt fra officiel databladstegning
//  Front af frontplade = z=0, kuppel rager frem (+z), motor bag (-z)
//
//  KILDE: SB Acoustics officielle datablad (SB26STAC-C000-4.pdf)
//  BCD 88.5 mm ±0.10, frontplade ø100.0 ±0.35, recess ø53.0 mm.
//  STEP-fil i assets/cad/SB26STAC-C000-4.stp er en GrabCAD-brugermodel
//  af en LIGNENDE SB Acoustics-diskant — IKKE identisk med SB26STAC.
//  Brug ALDRIG STEP-dimensioner (ex. bolt_cirkel=90) som databladet
//  angiver 88.5.
// ============================================================

/* [Visning] */
vis = "diskant"; // [diskant:Komplet enhed, cutout:Frontplade-udskaering (2D), snit:Halvsnit]

/* [Datablad — SB26STAC-C000-4.pdf] */
frontplade_od  = 100.0; // Datablad: ø100.0 ±0.35 (STEP siger 100.2 — inden for tolerance)
frontplade_tyk = 4.0;   // Frontplade tykkelse (datablad)
magnet_od      = 84.4;  // Motor-/magnethus diameter (STEP)
total_dybde    = 30.5;  // Fra frontplade-bagside til motor bagest (datablad: total dybde 39.7 mm forfra — motorhus ca. 30.5 bag frontplade)
kuppel_frem    = 2.5;   // Hvor langt kuplen rager frem (STEP, estimeret)
bolt_cirkel    = 88.5;  // Datablad: BCD ø88.5 ±0.10 — IKKE 90 (GrabCAD STEP er forkert)
bolt_antal     = 4;
bolt_hul_dia   = 4.0;   // Datablad: 4-ø4.0 mm skruehuller (med ø8.0 mm forsænkning)
bolt_offset    = 0;     // Huller paa N/S/OE/V (0 = +X foerst)

/* [Datablad — frontfladens fordybning/kuppel] */
recess_dia   = 53.0; // Datablad: fordybning i frontpladen omkring kuplen — IKKE 44 (STEP)
recess_dyb   = 2.0;  // Fordybningens dybde (datablad)
kuppel_dia   = 26;   // Kuppeldiameter (26 mm, datablad)

/* [Baffel/waveguide-montering] */
cutout_clearance = 0.5;

/* [Render] */
$fn = 120;
eps = 0.05;

module bolt_hoved() {
    for (i=[0:bolt_antal-1]) rotate([0,0,bolt_offset+i*360/bolt_antal])
        translate([bolt_cirkel/2,0,0]) children();
}

module diskant() {
    // frontplade
    color("dimgray")
    difference() {
        translate([0,0,-frontplade_tyk]) cylinder(d=frontplade_od,h=frontplade_tyk);
        // fordybning omkring kuppel
        translate([0,0,-recess_dyb]) cylinder(d=recess_dia,h=recess_dyb+eps);
        // haloebning gennem pladen
        translate([0,0,-frontplade_tyk-eps]) cylinder(d=kuppel_dia+4,h=frontplade_tyk+2*eps);
        bolt_hoved() translate([0,0,-frontplade_tyk-eps]) cylinder(d=bolt_hul_dia,h=frontplade_tyk+2*eps);
    }
    // kuppel
    color("silver") translate([0,0,-recess_dyb]) scale([1,1,ecl()]) sphere(d=kuppel_dia);
    // motorhus
    color("dimgray") translate([0,0,-total_dybde])
        cylinder(d=magnet_od,h=total_dybde-frontplade_tyk+eps);
}
function ecl() = (kuppel_frem+recess_dyb)/(kuppel_dia/2);

module frontplade_cutout_2d() {
    circle(d=recess_dia+2*cutout_clearance);          // hul til kuppel/hals
    bolt_hoved() circle(d=bolt_hul_dia);
}

if (vis=="diskant") diskant();
else if (vis=="cutout") frontplade_cutout_2d();
else if (vis=="snit") difference(){ diskant(); translate([0,-80,-80]) cube([80,160,160]); }
