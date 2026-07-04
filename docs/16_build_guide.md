# Chapter 16 - Build Guide

---

## Status

The physical build has not yet started. This chapter documents the planned build sequence. It will be updated with actual notes, problems, and fixes as the prototype is built.

See also: [BUILD_LOG.md](../BUILD_LOG.md) for the running construction log.

---

## Prerequisites

Before starting the build:

- [ ] Finalize cabinet CAD drawings
- [ ] Verify all driver dimensions (cutout, frame, mounting depth)
- [ ] Verify waveguide CAD and print prototype
- [ ] Confirm mid chamber dimensions
- [ ] Order all materials and drivers
- [ ] Confirm DSP/amplifier platform

---

## Materials list

### Cabinet

| Item | Specification | Quantity |
|---|---|---|
| Birch plywood | 22 mm, grade BB or better | ~3-4 sheets (1220×2440 mm) |
| Wood glue | PVA or similar | 1 bottle |
| Clamps | Various sizes | As needed |
| Sandpaper | 80/120/180/240 grit | Assorted |
| Primer and paint | Or veneer finish | TBD |

### Damping

| Item | Quantity |
|---|---|
| Bitumen damping pads | For inside panel faces |
| Acoustic foam or mineral wool (bass chamber) | ~2-3 L |
| Acoustic foam or long-fiber wool (mid chamber) | ~0.5-1 L |

### Hardware

| Item | Specification | Quantity |
|---|---|
| Threaded inserts | M4 or M5 for driver mounting | ~20 |
| Driver mounting screws | M4 or M5 | ~20 |
| Gasket tape | 3-5 mm foam, self-adhesive | ~2 m |
| Terminal plate or amplifier cutout plate | TBD | 1 per speaker |
| Internal speaker cable | TBD | ~2 m per speaker |

### Drivers (per speaker)

| Driver | Quantity |
|---|---|
| GRS 12SW-4HE | 2 |
| ScanSpeak 15W/4434G00 | 1 |
| SB Acoustics SB26STAC-C000-4 | 1 |
| Printed waveguide | 1 |

---

## Build sequence

### Phase 1: Panel cutting

1. Cut all cabinet panels to final dimensions from plywood sheet
2. Cut mid chamber panels
3. Cut shelf/window brace panels
4. Label all panels
5. Check fit (dry assembly without glue)

### Phase 2: Driver cutouts

1. Cut woofer cutouts on side panels (284 mm diameter per GRS 12SW-4HE datasheet — verify on physical driver first)
2. Cut midrange cutout on front baffle
3. Cut waveguide cutout on front baffle
4. Cut terminal/amplifier cutout on rear panel
5. Deburr and sand all cutouts smooth

### Phase 3: Mid chamber assembly

1. Assemble mid chamber sub-enclosure (panels + glue)
2. Seal all mid chamber joints with glue
3. Test fit into main cabinet
4. Line mid chamber interior with damping material
5. Install midrange threaded inserts in front baffle

### Phase 4: Main cabinet assembly

1. Glue bottom panel to front and rear panels
2. Add side panels
3. Install window brace(s) in bass chamber
4. Install shelf brace at mid chamber location
5. Glue top panel
6. Clamp and let cure fully (24 h minimum)
7. Check all joints for gaps, fill if needed

### Phase 5: Internal damping

1. Apply bitumen pads to inside faces of all bass chamber panels
2. Apply acoustic fill (moderate amount) to bass chamber
3. Do not fill near woofer ports or in woofer path
4. Seal any remaining gaps around brace edges

### Phase 6: Woofer installation

1. Install threaded inserts in side panels at woofer positions
2. Apply gasket tape around woofer cutouts (284 mm)
3. Install lower woofer (GRS 12SW-4HE)
4. Install upper woofer (GRS 12SW-4HE)
5. Check push-push wiring polarity (battery test) — both cones must move in the same direction
6. Verify the coupling block (h=20 mm, r=55 mm) bridges the ~4 mm magnet gap without obstructing air flow
7. Run wiring to terminal area

### Phase 7: Mid chamber installation

1. Install mid chamber into cabinet
2. Seal mid chamber to front baffle and side walls
3. Install midrange (ScanSpeak 15W) with gasket tape
4. Run midrange wiring to terminal area

### Phase 8: Waveguide and tweeter

1. Test fit printed waveguide in front baffle cutout
2. Confirm c-c spacing to midrange (target: 140 mm)
3. Mount SB26STAC tweeter into waveguide
4. Install waveguide + tweeter assembly in front baffle
5. Run tweeter wiring to terminal area

### Phase 9: Finishing

1. Sand cabinet exterior (start with 80, finish with 180 or 240)
2. Apply primer coat
3. Fill any surface defects
4. Apply final paint or veneer

### Phase 10: Electronics

1. Install terminal plate or amplifier module in rear cutout
2. Terminate and route all internal wiring
3. Connect DSP/amplifier per signal chain
4. Set initial crossover settings in DSP
5. Connect source

---

## Commissioning and first checks

1. Apply signal and verify all three driver systems produce sound
2. Run polarity test on woofers (battery test on each, verify push-push)
3. Run initial frequency sweep - check for gross problems
4. Run distortion measurement on tweeter at 1100 Hz
5. Proceed to full measurement campaign (Chapter 15)

---

## Known risks and watch points

| Risk | Mitigation |
|---|---|
| Mid chamber not fully sealed | Check all joints with smoke test or listen for leaks |
| Push-push wiring reversed | Battery polarity test before full assembly |
| SB26STAC distortion too high at 1100 Hz | Measure before committing to crossover frequency (expected comfortable — 350 Hz Fs margin) |
| Woofer mounting depth too deep for 22 mm wall | Verify GRS 12SW-4HE spec (~136 mm total depth); opposed magnet gap is only ~4 mm — check basket profile |
| R50 roundovers - router tear-out | Sharp bit, slow passes, backing board |
| Waveguide print warping | Use PETG, print flat, allow to cool slowly |

---

## Issue log

Document all problems found during the build here. This becomes part of the permanent record for future versions.

(No issues yet - build not started.)
