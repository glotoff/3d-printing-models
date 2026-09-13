# Modular Single-Bay HDD / SSD Caddy (70mm Tall, Snug 74mm Fit)

A modular, linkable 3D-printable stand/dock designed for 16 mm external hard drive enclosures (or SSDs). Each bay is printed individually and can be ganged together side-by-side using standard M3 hardware to form an array of 2, 3, 5, or more bays.

![Inside Washer & Nut Recesses](images/caddy_inside_recesses.png)

---

## Key Features

1. **Modular Daisy-Chaining:**
   - 100% flat exterior side mating walls ($Y = 0$ and $Y = 24.5\text{ mm}$) allow multiple modules to mate flush against each other with zero gap.
   - Dual M3 horizontal fastening holes at $Z = 20\text{ mm}$ and $Z = 55\text{ mm}$ for rigid assembly.
2. **Internal Hardware Recesses (Inside Fastening):**
   - **Screw Head & Washer Seat (Left Pillar):** $\varnothing 7.5\text{ mm}$ circular counterbore ($2.5\text{ mm}$ deep) on the **inside** face of the pillar. Fits standard DIN 125 M3 washers ($\varnothing 7.0\text{ mm}$) and socket/button head screws completely flush inside the window opening.
   - **Captive Hex Nut Pocket (Right Pillar):** $5.6\text{ mm}$ flat-to-flat ($2.6\text{ mm}$ deep) with optional washer recess ($0.8\text{ mm}$ deep) on the **inside** face.
   - **No Exterior Protrusions:** All heads, washers, and nuts are installed and tightened from **inside** each bay.
3. **Optimized Ventilation:**
   - Full-height isometric honeycomb lattice (7 rows, 38 mm cell diagonal) covering both large side walls for passive cross-ventilation.
   - Bottom chimney through-floor vent ($58.0 \times 12.5\text{ mm}$) for vertical convection.
4. **Snug & Stable Drive Pocket:**
   - Designed for enclosures up to $16.0\text{ mm}$ thick $\times 74.0\text{ mm}$ long $\times 125.0\text{ mm}$ tall.
   - $70.0\text{ mm}$ tall caddy structure provides high lateral stability and prevents tall drives from tipping.

---

## Dimensions

| Dimension | Value | Description |
| :--- | :--- | :--- |
| **Total Height (Z)** | $70.0\text{ mm}$ | Upright support height |
| **Total Length (X)** | $84.0\text{ mm}$ | Outer footprint front-to-back |
| **Total Width (Y)** | $24.5\text{ mm}$ | Single bay pitch ($16.5\text{ mm}$ slot + $2 \times 4.0\text{ mm}$ walls) |
| **Slot Length (X)** | $74.0\text{ mm}$ | Snug fit for 74 mm enclosure |
| **Slot Width (Y)** | $16.5\text{ mm}$ | $0.5\text{ mm}$ clearance for 16 mm enclosure |
| **Wall Thickness** | $4.0\text{ mm}$ | Solid perimeters (4 loops) |
| **Floor Thickness** | $3.5\text{ mm}$ | Solid base with chimney cutout |
| **Mounting Holes** | $4 \times \varnothing 3.4\text{ mm}$ | Dual level ($Z = 20\text{ mm}$ and $Z = 55\text{ mm}$) |

---

## Bill of Materials (BOM) per Joint

To connect two adjacent bays together:
- **$2 \times$ M3 Screws:** M3 $\times 12\text{ mm}$ or M3 $\times 14\text{ mm}$ (Socket head DIN 912 or Button head ISO 7380)
- **$2 \times$ M3 Washers:** DIN 125A ($\varnothing 7.0\text{ mm}$ OD, $0.5\text{ mm}$ thickness)
- **$2 \times$ M3 Hex Nuts:** DIN 934 ($5.5\text{ mm}$ across flats)

---

## Recommended Slicer Settings

- **Printer:** Flashforge Adventurer 5M Pro / Bambu Lab / Prusa (or any FDM printer)
- **Nozzle:** $0.4\text{ mm}$
- **Layer Height:** $0.20\text{ mm}$
- **Wall Loops:** **4** (produces 100% solid perimeters around all screw holes and pillars)
- **Top / Bottom Shells:** 4 layers
- **Infill:** $15\text{--}20\%$ Gyroid (walls are solid with 4 loops)
- **Supports:** None needed (honeycombs and bridges are self-supporting)
- **Material:** PLA / PETG / ABS
- **Print Time:** ~1h 06m (at standard speeds)
- **Filament:** ~33.8 g

---

## Change Tracking in Git (Code-CAD)

Binary CAD files (`.stl`, `.3mf`, `.f3d`) cannot be diffed cleanly in Git. This repository provides text-based parametric models that allow full **Git change tracking**:

1. **OpenSCAD (`cad/modular_single_bay_70mm.scad`):**
   - Pure text-based CSG script.
   - Every parameter (`drive_d`, `slot_t`, `caddy_h`, `m3_washer_dia`, etc.) is declared at the top of the file.
   - Any modification will produce clear, line-by-line `git diff` outputs.
2. **Fusion 360 Python Generator (`cad/generate_fusion360_model.py`):**
   - Standalone Python script for the Fusion 360 API.
   - Parametrically generates the model, applies appearances, and exports STL/STEP formats.

---

## Repository Structure

```
.
├── cad/
│   ├── modular_single_bay_70mm.scad      # Parametric OpenSCAD source (Git diff friendly)
│   └── generate_fusion360_model.py       # Parametric Fusion 360 Python API script
├── models/
│   ├── Modular_SingleBay_70mm_Tight.stl  # Current production-ready STL model
│   └── Modular_SingleBay_70mm_Tight.step # Standard STEP CAD exchange file
├── gcode/
│   └── Modular_SingleBay_70mm_Tight.gcode # Print-ready G-code (Adventurer 5M Pro)
├── images/                               # Renders and slicing preview images
├── legacy/                               # Previous prototypes and test models
├── .gitignore
└── README.md
```
