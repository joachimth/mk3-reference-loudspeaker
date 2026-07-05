// ============================================================
//  Scan-Speak 18W/4424G00 - 18 cm bas/mellemtone-enhed
//  Parametrisk OpenSCAD-model genereret ud fra maaltegning
//  Alle maal i millimeter (mm)
// ------------------------------------------------------------
//  KOTEDE MAAL (fra tegning) = praecise
//  ESTIMEREDE MAAL (kegle/magnet) = tilnaermede, justerbare
//
//  Kotede maal verificeret mod det officielle ScanSpeak-datablad
//  assets/datasheets/18W-4424G00.pdf (Discovery, 18 cm midwoofer):
//  flange Ø179,20 ±0,30, udskaering Ø144,3 +2/-0, dybde 72,2,
//  hulcirkel Ø167, 6 x Ø5,3 ±0,15 ved 60 grader.
//
//  Bruges af cad/cabinet.scad via `use <midrange.scad>` — kabinettet
//  henter alle maal gennem eksportfunktionerne nederst i filen, saa
//  intet skal vedligeholdes to steder.
// ============================================================

/* [Visning] */
// Hvad skal vises?
vis = "driver"; // [driver:Komplet enhed, cutout:Baffel-udskaering (2D), skabelon:Boreskabelon (3D), snit:Enhed i halvsnit]

/* [Kotede maal - fra tegning] */
flange_od       = 179.20;  // Udvendig flangediameter
flange_tyk      = 5.20;    // Flangens/frontpladens tykkelse
udskaering_dia  = 144.30;  // Kurv-/udskaeringsdiameter (baffelhul)
total_dybde     = 72.20;   // Samlet dybde
bolt_cirkel     = 167.0;   // Hulcirkel (pitch diameter)
bolt_hul_dia    = 5.30;    // Monteringshuller
antal_huller    = 6;       // Antal huller (60 grader indbyrdes)
bolt_offset     = 30;      // Vinkelforskydning af hulmoenster [grader]

/* [Thiele-Small - fra datablad 18W-4424G00.pdf] */
ts_fs      = 49;    // Resonansfrekvens [Hz]
ts_qts     = 0.38;  // Total Q
ts_vas     = 24.1;  // Aekvivalentvolumen [L]
ts_sd      = 137;   // Effektivt membranareal [cm2]
ts_displ   = 0.28;  // Cabinet Displacement Volume [L]
ts_sens    = 91;    // Foelsomhed [dB / 2,83 V / 1 m]
// Datablad anbefaler lukket kasse: Vbox 13 L, f(-3dB) 85 Hz

/* [Baffel-parametre] */
baffel_tyk       = 21;     // Bafflens tykkelse (til skabelon)
cutout_clearance = 0.5;    // Ekstra spillerum paa udskaeringen (radius pr. side)

/* [Estimerede maal - IKKE kotet, juster efter behov] */
kegle_top_dia = 120;   // Keglens diameter oppe (ved surround)
surround_od   = 150;   // Surround/pakning yderdiameter (limet paa flange)
kegle_bund_dia= 45;    // Keglens diameter nede (svingspole)
stoevhat_dia  = 50;    // Stoevhaettens diameter
magnet_dia    = 90;    // Magnetsystemets diameter
magnet_start_z= -52;   // Hvor magneten begynder (bagud fra front)

/* [Render] */
$fn = 128;
eps = 0.05;

// ------------------------------------------------------------
//  EKSPORT — bruges af cabinet.scad (importeres med `use`)
// ------------------------------------------------------------
function mid_flange_od_fn()  = flange_od;
function mid_flange_t_fn()   = flange_tyk;
function mid_cut_d_fn()      = udskaering_dia;
function mid_depth_fn()      = total_dybde;
function mid_bcd_fn()        = bolt_cirkel;
function mid_hole_d_fn()     = bolt_hul_dia;
function mid_n_holes_fn()    = antal_huller;
function mid_bolt_offset_fn()= bolt_offset;
function mid_magnet_d_fn()   = magnet_dia;
function mid_Fs_fn()         = ts_fs;
function mid_Qts_fn()        = ts_qts;
function mid_Vas_fn()        = ts_vas;
function mid_displ_L_fn()    = ts_displ;
// Kurvens/magnetens radius i dybden d bag flangens FRONT (kegleformet
// kurv fra udskaeringen til magneten, derefter magnetdiameteren) —
// bruges til at aflede skillevaeggens hoejde i cabinet.scad.
function mid_basket_r_at(d) =
    d <= flange_tyk      ? udskaering_dia/2 :
    d >= -magnet_start_z ? magnet_dia/2 :
    udskaering_dia/2 + (magnet_dia/2 - udskaering_dia/2)
        * (d - flange_tyk) / (-magnet_start_z - flange_tyk);
// Alias med entydigt navn til brug i samlinger (undgaar det generiske
// modulnavn `driver` udenfor denne fil).
module midrange_driver() driver();

// ------------------------------------------------------------
//  HJAELPERE
// ------------------------------------------------------------

// Positioner monteringshullerne paa hulcirklen
module bolt_hoved() {
    for (i = [0:antal_huller-1]) {
        a = bolt_offset + i * 360/antal_huller;
        rotate([0,0,a])
            translate([bolt_cirkel/2, 0, 0])
                children();
    }
}

// Gennemgaaende monteringshuller
module bolt_huller(h, z0) {
    bolt_hoved()
        translate([0,0,z0])
            cylinder(d=bolt_hul_dia, h=h);
}

// ------------------------------------------------------------
//  DRIVER-DELE
//  Koordinatsystem: front af flange = z=0, enheden gaar i -z
// ------------------------------------------------------------

// Flange / frontplade (ring med bolt-huller) - KOTET
module flange() {
    color("dimgray")
    difference() {
        translate([0,0,-flange_tyk])
            cylinder(d=flange_od, h=flange_tyk);
        // aabning i midten hvor surround/kegle sidder
        translate([0,0,-flange_tyk-eps])
            cylinder(d=surround_od, h=flange_tyk+2*eps);
        bolt_huller(flange_tyk+2*eps, -flange_tyk-eps);
    }
}

// Kurv/basket som tynd konisk skal - ESTIMAT
module kurv() {
    vaeg = 3;
    color("gray")
    difference() {
        hull() {
            translate([0,0,-flange_tyk])       cylinder(d=udskaering_dia, h=eps);
            translate([0,0,magnet_start_z])     cylinder(d=magnet_dia, h=eps);
        }
        hull() {
            translate([0,0,-flange_tyk-eps])    cylinder(d=udskaering_dia-2*vaeg, h=eps);
            translate([0,0,magnet_start_z+vaeg])cylinder(d=magnet_dia-2*vaeg, h=eps);
        }
        // aaben front saa kegle er synlig
        translate([0,0,-flange_tyk-eps])
            cylinder(d=udskaering_dia-2*vaeg, h=eps+vaeg);
    }
}

// Surround (halvrund rulle) - ESTIMAT
module surround() {
    rulle_r = (surround_od - kegle_top_dia)/4;
    center_r = kegle_top_dia/2 + rulle_r;
    color("black")
    translate([0,0,-flange_tyk])
        rotate_extrude()
            translate([center_r, 0]) circle(r=rulle_r);
}

// Membran/kegle som tynd skal - ESTIMAT
module kegle() {
    vaeg = 1.2;
    kh = 36;                       // keglens hoejde
    top_z = -flange_tyk - 2;       // toppen lidt bag flangens front
    color("peru")
    translate([0,0,top_z-kh])
    difference() {
        cylinder(d1=kegle_bund_dia, d2=kegle_top_dia, h=kh);
        translate([0,0,vaeg])
            cylinder(d1=kegle_bund_dia-2*vaeg, d2=kegle_top_dia-2*vaeg, h=kh);
    }
}

// Stoevhaette (flad kuppel) - ESTIMAT
module stoevhat() {
    color("saddlebrown")
    translate([0,0,-total_dybde-magnet_start_z-10])
        scale([1,1,0.45]) sphere(d=stoevhat_dia);
}

// Magnetsystem - ESTIMAT
module magnet() {
    color("dimgray")
    union() {
        // magnetslug
        translate([0,0,-total_dybde])
            cylinder(d=magnet_dia, h=total_dybde+magnet_start_z);
        // polplade-overgang op mod kegle
        translate([0,0,magnet_start_z-eps])
            cylinder(d1=magnet_dia, d2=kegle_bund_dia+6, h=8);
    }
}

// Samlet enhed
module driver() {
    flange();
    kurv();
    surround();
    kegle();
    stoevhat();
    magnet();
}

// ------------------------------------------------------------
//  BAFFEL-VAERKTOEJ
// ------------------------------------------------------------

// 2D udskaering til baffel (hul + bolthuller) - til DXF/laser/CNC
module baffel_cutout_2d() {
    circle(d = udskaering_dia + 2*cutout_clearance);
    bolt_hoved() circle(d = bolt_hul_dia);
}

// 3D boreskabelon der laegges paa bafflen
module boreskabelon() {
    skab_od = flange_od + 6;
    skab_tyk = 4;
    difference() {
        cylinder(d=skab_od, h=skab_tyk);
        // center-hul markerer udskaeringens kant
        translate([0,0,-eps]) cylinder(d=udskaering_dia, h=skab_tyk+2*eps);
        // gennemgaaende borehuller
        bolt_huller(skab_tyk+2*eps, -eps);
    }
    // lille markeringsring for flange-yderkant
    difference() {
        cylinder(d=flange_od, h=0.6);
        translate([0,0,-eps]) cylinder(d=flange_od-1.5, h=0.6+2*eps);
    }
}

// ------------------------------------------------------------
//  RENDER-DISPATCH
// ------------------------------------------------------------
if (vis == "driver") {
    driver();
} else if (vis == "cutout") {
    baffel_cutout_2d();
} else if (vis == "skabelon") {
    boreskabelon();
} else if (vis == "snit") {
    difference() {
        driver();
        translate([0,-200,-200]) cube([200,400,400]); // fjern y<0
    }
}
