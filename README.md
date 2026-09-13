# Modular Single-Bay HDD / SSD Caddy (70mm Tall, Snug 78x14mm Fit)

A modular, linkable 3D-printable stand/dock tailored specifically for **$78\text{ mm} \times 14\text{ mm}$ external hard drive / SSD enclosures**. Each bay is printed individually and can be ganged together side-by-side using standard M3 hardware into a rigid array of 2, 3, 5, or more bays.

| Hard Drive Enclosure In Dock | Inside Washer & Nut Recesses | 100% Flat Mating Exterior |
| :---: | :---: | :---: |
| ![Caddy with Drive](images/caddy_with_drive.png) | ![Inside Washer & Nut Recesses](images/caddy_inside_recesses.png) | ![Outside Flat Face](images/caddy_outside_flat.png) |

---

## Key Features

1. **Precision Fit for $78\text{ mm} \times 14\text{ mm}$ Drives:**
   - **Internal Slot Length:** $79.0\text{ mm}$ ($+1.0\text{ mm}$ total clearance / $0.5\text{ mm}$ each end) — the $78\text{ mm}$ wide drive slides in smoothly without binding or catching.
   - **Internal Slot Width / Thickness:** $14.8\text{ mm}$ ($+0.8\text{ mm}$ total clearance / $0.4\text{ mm}$ each side) — holds the $14\text{ mm}$ thick drive upright with zero wobble or rattling.
   - **Support Height:** $70.0\text{ mm}$ tall caddy structure provides high lateral support, preventing tall drives (~125 mm) from tipping.

2. **Internal Fastening System (Inside Washer & Nut Recesses):**
   - **Screw Head & Washer Seat (Left Pillar):** $\varnothing 7.5\text{ mm}$ circular counterbore ($2.5\text{ mm}$ deep) on the **inside** face of the pillar ($Y = 6.0\text{ mm}$). Accommodates a standard DIN 125 M3 washer ($\varnothing 7.0\text{ mm}$) and socket/button head screw completely flush inside the vertical window opening.
   - **Captive Hex Nut Pocket (Right Pillar):** $5.6\text{ mm}$ across flats ($2.6\text{ mm}$ deep) with washer recess ($0.8\text{ mm}$ deep) on the **inside** face ($Y = 16.8\text{ mm}$).
   - **100% Flat Exterior Mating Faces:** On both outside walls ($Y = 0$ and $Y = 22.8\text{ mm}$), there are **zero counterbores** — only clean $\varnothing 3.4\text{ mm}$ through-holes. When modules are joined side-by-side, their exterior walls mate completely flush with zero gap.
   - **Internal Assembly:** All screws, washers, and nuts are inserted and tightened from **inside** each bay.

3. **Optimized Cross-Ventilation:**
   - Full-height isometric honeycomb lattice (7 rows, 38 mm cell diagonal) on both large side walls for passive cross-ventilation.
   - Bottom chimney through-floor vent ($58.0 \times 10.8\text{ mm}$) for natural convective airflow.

---

## Dimensions Summary

| Parameter | Drive Size | Internal Slot | External Footprint | Clearance / Tolerance |
| :--- | :---: | :---: | :---: | :--- |
| **Length (X axis)** | **$78.0\text{ mm}$** | **$79.0\text{ mm}$** | **$89.0\text{ mm}$** | $+0.5\text{ mm}$ per end ($1.0\text{ mm}$ total) for smooth insertion |
| **Width / Depth (Y axis)** | **$14.0\text{ mm}$** | **$14.8\text{ mm}$** | **$22.8\text{ mm}$** | $+0.4\text{ mm}$ per side ($0.8\text{ mm}$ total) for snug upright fit |
| **Height (Z axis)** | ~125 mm | Open top | **$70.0\text{ mm}$** | High lateral stability |
| **Side Wall Thickness** | — | — | **$4.0\text{ mm}$** | Solid perimeters (4 wall loops) |
| **Floor Thickness** | — | — | **$3.5\text{ mm}$** | Rigid base with chimney vent |
| **Front / Rear Pillars** | — | — | **$5.0\text{ mm}$ each** | Housing dual-level M3 joining holes |
| **Mounting Levels** | — | — | **$Z = 20\text{ mm}$, $Z = 55\text{ mm}$** | Dual screw rigidity |

> **Density Note:** At $22.8\text{ mm}$ pitch per bay, a 5-drive array occupies only **$114\text{ mm}$** of desktop width!

---

## Bill of Materials (BOM) per Joint

To connect two adjacent bays:
- **$2 \times$ M3 Screws:** M3 $\times 12\text{ mm}$ or M3 $\times 14\text{ mm}$ (Socket head DIN 912 or Button head ISO 7380)
- **$2 \times$ M3 Washers:** DIN 125A ($\varnothing 7.0\text{ mm}$ OD, $0.5\text{ mm}$ thickness)
- **$2 \times$ M3 Hex Nuts:** DIN 934 ($5.5\text{ mm}$ across flats)

---

## Slicer & Print Guidelines

![OrcaSlicer Bed Layout](images/orcaslicer_plate.png)

- **Printer:** Flashforge Adventurer 5M Pro / Bambu Lab / Prusa (or any FDM printer)
- **Nozzle:** $0.4\text{ mm}$
- **Layer Height:** $0.20\text{ mm}$
- **Wall Loops:** **4** (ensures 100% solid perimeters through the 4.0 mm walls and around screw holes)
- **Top / Bottom Shells:** 4 layers
- **Infill:** $15\text{--}20\%$ Gyroid (walls are solid with 4 perimeters)
- **Supports:** **None required** (honeycombs and bridges are self-supporting)
- **Print Time:** ~1h 09m
- **Filament Consumption:** ~33.2 g

---

## Change Tracking in Git (Code-CAD)

Binary 3D models (`.stl`, `.3mf`, `.f3d`) cannot be diffed cleanly in Git. This repository provides text-based parametric models that allow full **Git change tracking**:

1. **OpenSCAD (`cad/modular_single_bay_70mm.scad`):**
   - Pure text-based CSG script.
   - All dimensions (`drive_w`, `drive_t`, `slot_l`, `slot_t`, `caddy_h`, `m3_washer_dia`, etc.) are declared as parametric variables at the top of the file.
   - Any modification will produce clear, line-by-line `git diff` outputs.
2. **Fusion 360 Python Generator (`cad/generate_fusion360_model.py`):**
   - Standalone Python script for the Fusion 360 API.
   - Fully parametric generation, appearance assignment, and automated export to STL and STEP.
3. **Fusion MCP Client (`cad/fusion_client.py`):**
   - Lightweight JSON-RPC client to execute scripts and export models directly via Fusion 360 MCP.

---

## Repository Structure

```
.
├── cad/
│   ├── modular_single_bay_70mm.scad      # Parametric OpenSCAD source (Git diff friendly)
│   ├── generate_fusion360_model.py       # Parametric Fusion 360 API generator
│   └── fusion_client.py                  # Direct JSON-RPC client for Fusion MCP
├── models/
│   └── Modular_SingleBay_70mm_Tight.stl  # Production STL model (89.0 x 22.8 x 70.0 mm)
├── gcode/
│   └── Modular_SingleBay_70mm_Tight.gcode # Print-ready G-code (Adventurer 5M Pro)
├── images/                               # 3D viewport renders and slicer plate preview
├── legacy/                               # Previous prototype iterations and test models
├── .gitignore
└── README.md
```
