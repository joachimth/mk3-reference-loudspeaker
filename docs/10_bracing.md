# Chapter 10 - Bracing

---

## Purpose

Cabinet bracing serves two purposes:

1. **Increase panel stiffness** - raise the resonant frequencies of the cabinet panels above the bass operating range
2. **Reduce panel vibration amplitude** - reduce the sound radiated by vibrating cabinet panels ("cabinet talk")

Unbraced panels in a bass cabinet can produce significant resonances in the 100-400 Hz range. This adds coloration to the bass and midrange response and degrades the measured performance.

---

## General approach

The primary bracing strategy for this design is a combination of:

- **Shelf braces** - horizontal panels that span the full cabinet width/depth, dividing the cabinet into sections
- **Window braces** - shelf braces with a central opening ("window") that allows air to pass between sections, maintaining the full shared bass volume while still bracing the side panels
- **Vertical braces** - vertical members running along the inside of the baffle or side panels to stiffen the tallest unsupported spans

---

## Shelf braces

Shelf braces are full-width panels of plywood installed horizontally inside the cabinet. They are primarily used to:

- Stiffen the side panels by reducing their free span
- Create the top boundary of the mid chamber
- Add mass and rigidity to the cabinet structure

For the push-push woofer placement (both woofers opposed at the same height, ~520 mm nominal), a shelf brace near the woofer line may be considered for bracing the woofer cutout areas in the side panels.

---

## Window braces

A window brace is a horizontal shelf with a large central opening. The opening allows bass frequencies to couple the upper and lower regions of the bass chamber freely, so the full cabinet volume is acoustically shared.

Window braces are preferred over solid shelf braces inside the main bass chamber to avoid reducing the effective bass volume.

The window opening should be at least 50% of the panel area to minimize acoustic restriction.

---

## Vertical braces

Vertical braces are applied behind the front baffle and/or inside the side panels. They are particularly useful for:

- Stiffening the front baffle between driver cutouts
- Reducing the free span of the side panels in the bass frequency range
- Connecting opposite panels (e.g. front to rear brace, or side-to-side brace)

A front-to-rear diagonal or straight brace can be especially effective at stiffening both the baffle and the rear panel simultaneously.

---

## Mid chamber bracing

The mid chamber walls inherently brace the upper cabinet. The chamber walls connect multiple panels and add rigidity in the area of the midrange driver.

---

## Material

Bracing should use the same 22 mm birch plywood as the main cabinet walls, or 18 mm if weight savings are important. Solid hardwood is an alternative for smaller vertical braces.

---

## Damping material

In addition to structural bracing, internal damping material is applied to the bass chamber panels:

- **Bitumen or constrained-layer damping pads** - adhered to the inside faces of the panels, increasing the effective damping of panel resonances
- **Acoustic fill** - open-cell foam, mineral wool, or long-fiber polyester in the bass chamber to moderate the Q of the bass alignment and reduce standing waves

The level of bass chamber fill affects the acoustic volume: heavily stuffed chambers can appear acoustically larger than their physical dimensions. For a sealed design targeting Qtc ~0.62, moderate fill is recommended. The precise fill level is best optimized by measurement after the prototype is built.

---

## Brace layout (to be finalized in CAD)

| Location | Type | Purpose |
|---|---|---|
| Woofer line (~520 mm, both sides) | Window brace | Stiffen side panels around the opposed woofer cutouts |
| Mid chamber top | Shelf brace | Top wall of mid chamber, separates bass/mid |
| Opposed magnet gap (~520 mm) | Coupling block | Tie the two woofer motors together (see Chapter 8) |
| Baffle interior | Vertical brace | Stiffen baffle between driver cutouts |
| Side panels (behind baffle) | Vertical braces | Reduce free span of longest panel sections |

---

## Open items

- Finalize brace positions in CAD model
- Calculate panel resonant frequencies with and without bracing (FEM or estimate)
- Select damping pad material and adhesive
- Determine internal fill type and quantity
- Confirm that brace positions do not interfere with woofer mounting depths
