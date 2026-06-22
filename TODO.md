# Mk2 Reference Loudspeaker - TODO

Inspired by Genelec 8361, Dutch & Dutch 8C and Revel Salon2.

---

# Current Main Design (v6b)

- [x] Select GRS 8SW-4HE-8 woofers
- [x] Select ScanSpeak 15W/4434G00 midrange
- [x] Select ScanSpeak H2606/920000 tweeter
- [x] Select sealed push-push bass configuration
- [x] Select 300 mm wide cabinet
- [x] Select R50 front edge roundovers
- [x] Target 69 L net bass volume
- [x] Target 5.7 L mid chamber
- [x] Target 150 Hz LR4 bass-mid crossover
- [x] Target 1250 Hz LR4 mid-tweeter crossover
- [x] Target 140 mm mid/tweeter c-c spacing

---

# Documentation

## Design Bible

- [ ] Create Design Bible master file
- [ ] Chapter 1 - Project goals and philosophy
- [ ] Chapter 2 - Loudspeaker theory
- [ ] Chapter 3 - Woofer investigations
- [ ] Chapter 4 - Midrange investigations
- [ ] Chapter 5 - Tweeter investigations
- [ ] Chapter 6 - Waveguide development
- [ ] Chapter 7 - Cabinet development
- [ ] Chapter 8 - Push-push bass
- [ ] Chapter 9 - Volume calculations
- [ ] Chapter 10 - Bracing
- [ ] Chapter 11 - Crossovers
- [ ] Chapter 12 - Directivity
- [ ] Chapter 13 - Spinorama
- [ ] Chapter 14 - DSP
- [ ] Chapter 15 - Measurements
- [ ] Chapter 16 - Build guide
- [ ] Chapter 17 - Future versions

---

# Simulations

## Bass

- [x] Compare 65 L
- [x] Compare 68 L
- [x] Compare 70 L
- [x] Compare Qtc
- [x] Compare group delay

## Midrange

- [x] Verify diffraction (polar_response.py - piston model)
- [x] Verify off-axis response (polar_response.py - horizontal polar)
- [x] Compare crossover frequencies (vertical_polar_map.py - 1250/1350/1450/1600 Hz)

## Tweeter

- [x] Compare 1250 Hz
- [x] Compare 1300 Hz (vertical_polar_map.py)
- [x] Compare 1400 Hz (vertical_polar_map.py)

## Complete system

- [x] Simulate spinorama (polar_response.py - on-axis, LW, ER, SP, DI, PIR)
- [x] Simulate listening window (polar_response.py)
- [x] Simulate early reflections (polar_response.py)
- [x] Simulate sound power (polar_response.py)
- [x] Simulate predicted in-room response (polar_response.py)
- [x] Simulate DI (estimate)

---

# Waveguide

## WG212

- [x] Define throat diameter (placeholder 28 mm - verify on H2606)
- [x] Define profile
- [x] Define mouth radius
- [x] Define depth
- [x] Define flange shape

## CAD

- [x] Generate OpenSCAD model
- [ ] Export STL
- [ ] Export STEP
- [ ] Generate drawing

## Print

- [ ] Print prototype
- [ ] Test fit H2606
- [ ] Verify c-c spacing

---

# Cabinet

## Geometry

- [x] Finalize external dimensions
- [ ] Verify internal dimensions
- [x] Verify driver spacing (cabinet.scad, c-c 150 mm)

## Bracing

- [x] Design window braces (representational in cabinet.scad)
- [x] Design shelf braces (representational in cabinet.scad)
- [ ] Add vertical braces

## Mid chamber

- [ ] Finalize volume
- [ ] Finalize damping

## Push-push woofers

- [ ] Verify positions
- [ ] Verify mechanical coupling

---

## CAD

## Cabinet

- [x] OpenSCAD model
- [x] STL export (CI: cad-render workflow, GitHub Releases)
- [ ] STEP model
- [ ] 2D drawings

## Driver cutouts

- [x] Woofer cutout
- [x] Midrange cutout
- [x] Waveguide cutout

---

# DSP

## Initial filters

- [ ] HP 20 Hz LR4
- [ ] LP 150 Hz LR4
- [ ] HP 150 Hz LR4
- [ ] LP 1250 Hz LR4
- [ ] HP 1250 Hz LR4

## Delay

- [ ] Estimate acoustic centers
- [ ] Initial delay values

## EQ

- [ ] Bass shelf
- [ ] Baffle step correction
- [ ] Waveguide correction

## House curves

- [ ] Flat
- [ ] Harman target
- [ ] Mild bass lift

---

# Measurements

## Drivers

- [ ] Measure woofer nearfield
- [ ] Measure midrange
- [ ] Measure tweeter

## Horizontal

- [ ] 0°
- [ ] 10°
- [ ] 20°
- [ ] 30°
- [ ] 40°
- [ ] 50°
- [ ] 60°

## Vertical

- [ ] ±10°
- [ ] ±15°
- [ ] ±20°
- [ ] ±30°

## Merge

- [ ] Import to VituixCAD
- [ ] Optimize crossover

---

# Build

## Prototype

- [ ] Cut panels
- [ ] Assemble cabinet
- [ ] Install damping
- [ ] Install drivers

## Electronics

- [ ] Amplifiers
- [ ] DSP
- [ ] Wiring

## Tuning

- [ ] Measurements
- [ ] EQ
- [ ] Delay
- [ ] Final voicing

---

# Future Versions

## v7

- [ ] Cardioid bass

## v8

- [ ] Purifi midrange

## v9

- [ ] Bliesma tweeter

## v10

- [ ] FIR filters

## v11

- [ ] Fully integrated active electronics

---

# Nice To Have

- [ ] Klippel NFS measurements
- [ ] Complete spinorama
- [x] Python simulation scripts (9 scripts in simulations/, CI auto-runs + commits)
- [ ] REW presets
- [ ] VituixCAD files
- [ ] OpenSCAD files
- [ ] STEP files
- [ ] Renderings
- [ ] Build pictures
- [ ] Public website
- [ ] GitHub Pages documentation