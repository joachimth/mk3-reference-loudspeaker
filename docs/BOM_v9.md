# mk3 v9 — Bill of Materials (per speaker, qty 2 total)

Approximate prices in EUR (incl. VAT). Updated July 7, 2026.

## Drivers

| Driver | Qty | Unit Price | Total | Source |
|--------|:---:|:----------:|:-----:|--------|
| GRS 12SW-4HE 12" high-excursion woofer | 2 | ~€30 | €60 | [Parts Express 292-824](https://www.parts-express.com/GRS-12SW-4HE-12-Paper-Cone-Rubber-Surround-High-Excursion-Subwoofer-4-Ohm-292-824) |
| ScanSpeak 18W/4424G00 7" midwoofer | 1 | ~€68 | €68 | [SoundImports](https://www.soundimports.eu/en/scan-speak-18w-4424g00.html) / [Willys-Hifi £58.41](https://willys-hifi.com/products/scanspeak-18w-4424g00-bass-midrange) |
| SB Acoustics SB26STAC-C000-4 1" tweeter | 1 | ~€48 | €48 | [hifisound.de €47.45](https://www.hifisound.de/Do-it-yourself-Products/SB-Acoustics-SB26STAC-C000-4-Tweeter.html) / [Madisound ~$52](https://www.madisoundspeakerstore.com/soft-dome-tweeters-sb-acoustics/sb-acoustics-sb26stac-c000-4-tweeter-4-ohm/) |
| **Drivers total** | **4** | | **€176** | |

## Cabinet Materials

| Item | Qty | Unit Price | Total | Notes |
|------|:---:|:----------:|:-----:|-------|
| 25mm MDF (1.22×2.44m sheet) | 1 | ~€35 | €35 | HDF or BB ply preferred if available |
| 18mm MDF (bracing) | 0.5 sheet | ~€20 | €10 | Internal braces and driver mounting rings |
| T-nuts M6 (driver mounting) | 20 | ~€0.20 | €4 | 8 per woofer + 4 per mid + 4 per tweeter |
| Bolts M6×25mm (driver mounting) | 20 | ~€0.15 | €3 | |
| Wood screws (various) | 1 box | ~€5 | €5 | For bracing and assembly |
| Wood glue (e.g. Titebond II) | 1L | ~€12 | €12 | |
| **Cabinet total** | | | **€69** | |

## Damping & Acoustics

| Item | Qty | Unit Price | Total | Notes |
|------|:---:|:----------:|:-----:|-------|
| Acoustic foam / polyester damping | 1 roll | ~€15 | €15 | Internal cabinet lining, ~30mm thick |
| Acoustic damping putty | 2 sheets | ~€5 | €10 | For panel constrained-layer damping |
| Self-adhesive bitumen pads | 1 pack | ~€10 | €10 | Panel damping on large surfaces |
| Port tube (if ported) | 2 | ~€3 | €6 | 2x flared ports for each woofer chamber |
| **Damping total** | | | **€41** | |

## Crossover / DSP (active, MiniDSP-based)

| Item | Qty | Unit Price | Total | Notes |
|------|:---:|:----------:|:-----:|-------|
| MiniDSP 4×10 HD (already in system) | 0 | €0 | €0 | Existing, no incremental cost |
| Speaker wire, 2.5mm² (internal wiring) | 5m | ~€3/m | €15 | Per speaker |
| Binding posts (gold-plated, 4 pairs) | 4 pairs | ~€5 | €20 | Woofer pair, mid, tweeter, sub |
| Speakon connectors (if active) | 0 | €0 | €0 | Only if using pro audio connectors |
| **Active crossover total** | | | **€35** | |

Passive crossover (if building passive version as backup):

| Item | Qty | Unit Price | Total | Notes |
|------|:---:|:----------:|:-----:|-------|
| Air-core inductor (woofer path, 3-5 mH) | 1 | ~€15 | €15 | |
| Air-core inductor (mid path, 1-2 mH) | 1 | ~€10 | €10 | |
| Air-core inductor (tweeter path, 0.5 mH) | 1 | ~€8 | €8 | |
| MKP poly caps (woofer path, 150-220 µF) | 1 | ~€12 | €12 | |
| MKP poly caps (mid path, 47-68 µF) | 2 | ~€10 | €20 | |
| MKP poly caps (tweeter path, 10-15 µF) | 1 | ~€8 | €8 | |
| Wirewound resistors (L-pad) | 4 | ~€3 | €12 | |
| PCB / perfboard + solder + binding | 1 | ~€10 | €10 | |
| **Passive crossover total (optional)** | | | **€95** | |

## Waveguide (3D printed)

| Item | Qty | Unit Price | Total | Notes |
|------|:---:|:----------:|:-----:|-------|
| PLA/PETG filament (1kg spool) | 1 | ~€25 | €25 | Enough for both waveguides + test prints |
| Fine sandpaper + finishing | 1 set | ~€10 | €10 | Post-print surface smoothing |
| **Waveguide total** | | | **€35** | |

## Finishing

| Item | Qty | Unit Price | Total | Notes |
|------|:---:|:----------:|:-----:|-------|
| Primer + paint / veneer | 1 kit | ~€40 | €40 | Per speaker |
| **Finishing total** | | | **€40** | |

---

## Summary

| Category | Cost (EUR, per speaker) | Cost (EUR, for pair) |
|----------|:-----------------------:|:--------------------:|
| Drivers | €176 | €352 |
| Cabinet materials | €69 | €138 |
| Damping & acoustics | €41 | €82 |
| Active wiring + connectors | €35 | €70 |
| Waveguide (3D printed) | €35 | €70 |
| Finishing | €40 | €80 |
| **Active subtotal** | **€396** | **€792** |
| Optional passive crossover | €95 | €190 |
| **Total with passive backup** | **€491** | **€982** |

## Notes

- **Active system recommended.** All v9 simulation work assumes MiniDSP 4×10 HD with DSP crossovers, PEQ, gain, and delay. Passive crossovers add complexity, cost, and insertion loss for no benefit when the MiniDSP is already in the signal chain.
- **GRS 12SW-4HE** is the budget champion — $28-32 per driver, dual push-push gives +6 dB sensitivity over single, yielding ~93 dB/2.83V effective. Two per cabinet (four per pair).
- **18W/4424G00 replacement of 15W/4434G00** was cost-neutral: the 18W is ~€68 vs the 15W at ~€55, but the 18W offers 91 dB sensitivity vs 89 dB for the 15W — a significant system-level improvement that needed less tweeter padding.
- **SB26STAC-C000-4** replaced H2606 at a fraction of the cost: €48 vs ~€120+ for the H2606, with comparable or better performance above 1100 Hz.
- **Total driver savings vs Mk2:** ~€150+ per pair by switching from H2606 to SB26STAC.
- Prices are approximate and vary by distributor, region, and current exchange rates. Danish prices (incl. 25% VAT) will be higher than the EU-ex-VAT or US prices shown here — add ~20-25% for Danish purchase.
