# Modular Single-Bay HDD / SSD Caddy (70mm Tall, +10mm Ventilation, Split Guide Pins)

A modular, linkable 3D-printable dock tailored specifically for **$78\text{ mm} \times 14\text{ mm}$ external hard drive / SSD enclosures**, featuring an expanded **$+10\text{ mm}$ ventilation clearance** with **4 internal split cylinder guide pins (7 mm bottom + 7 mm top)** that rigidly constrain the drive while maximizing airflow and reducing print time and plastic consumption.

| Hard Drive Enclosure in Dock (+5mm Air Gap) | 4 Cylinder Pins Inside Bay | 100% Flat Mating Exterior |
| :---: | :---: | :---: |
| ![Caddy with Drive](images/caddy_with_drive.png) | ![4 Cylinder Pins Inside](images/caddy_inside_recesses.png) | ![Outside Flat Face](images/caddy_outside_flat.png) |

---

## Key Features

1. **+10 mm Ventilation Expansion with Split Guide Pins (7 mm Bottom + 7 mm Top):**
   - **Total Slot Width:** Expanded from $14.8\text{ mm}$ to **$24.8\text{ mm}$** (+10 mm) for unrestricted airflow.
   - **Split Cylinder Guide Pins ($\varnothing 6.0\text{ mm}$):**
     - **Bottom Pins:** $7.0\text{ mm}$ tall rising from the floor ($Z = 3.5\text{ mm}$ to $10.5\text{ mm}$) to locate and seat the base of the drive.
     - **Top Pins:** $7.0\text{ mm}$ tall at the top rim ($Z = 63.0\text{ mm}$ to $70.0\text{ mm}$) to guide drive entry and prevent top wobble.
     - **Open Midsection:** The entire middle $52.5\text{ mm}$ is completely open air, cutting print time down to **1h 18m** and filament down to **36.5 g**.
   - **Zero-Wobble Drive Constraint:** The inner tangent distance between the left and right pins is precisely **$14.8\text{ mm}$** ($0.4\text{ mm}$ clearance on each side of the $14.0\text{ mm}$ drive).
   - **Generous 5.0 mm Air Gap on Both Sides:** Rather than resting flush against the honeycomb walls, the drive is held centered with a continuous **$5.0\text{ mm}$ air gap on each side**, allowing massive cross-ventilation across both large aluminium/plastic drive surfaces.

2. **Internal Fastening System (Inside Washer & Nut Recesses):**
   - **Screw Head & Washer Seat (Left Pillar):** $\varnothing 7.5\text{ mm}$ circular counterbore ($2.5\text{ mm}$ deep) on the **inside** face of the pillar ($Y = 6.0\text{ mm}$). Fits standard DIN 125 M3 washers ($\varnothing 7.0\text{ mm}$) and socket/button head screws completely flush inside the vertical window opening.
   - **Captive Hex Nut Pocket (Right Pillar):** $5.6\text{ mm}$ across flats ($2.6\text{ mm}$ deep) with washer recess ($0.8\text{ mm}$ deep) on the **inside** face ($Y = 26.8\text{ mm}$).
   - **100% Flat Exterior Mating Faces:** Both outside walls ($Y = 0$ and $Y = 32.8\text{ mm}$) have **zero counterbores** — only clean $\varnothing 3.4\text{ mm}$ through-holes. When modules are joined side-by-side, their exterior walls mate completely flush with zero gap.
   - **Internal Assembly:** All screws, washers, and nuts are inserted and tightened from **inside** each bay.

3. **Optimized Cross-Ventilation:**
   - Full-height isometric honeycomb lattice (7 rows, 38 mm cell diagonal) on both large side walls for passive cross-ventilation.
   - Bottom chimney through-floor vent ($63.0 \times 20.8\text{ mm}$) for natural convective vertical airflow.

---

## Dimensions Summary

| Parameter | Drive Size | Internal Slot / Pins | External Footprint | Clearance / Tolerance |
| :--- | :---: | :---: | :---: | :--- |
| **Length (X axis)** | **$78.0\text{ mm}$** | **$79.0\text{ mm}$** | **$89.0\text{ mm}$** | $+0.5\text{ mm}$ per end ($1.0\text{ mm}$ total) for smooth insertion |
| **Width / Depth (Y axis)** | **$14.0\text{ mm}$** | **$24.8\text{ mm}$ slot**<br>($14.8\text{ mm}$ between pins) | **$32.8\text{ mm}$** | $+0.4\text{ mm}$ per side between pins; **$5.0\text{ mm}$ air gap** to each wall |
| **Height (Z axis)** | ~125 mm | Open top | **$70.0\text{ mm}$** | High lateral stability |
| **Side Wall Thickness** | — | — | **$4.0\text{ mm}$** | Solid perimeters (4 wall loops) |
| **Floor Thickness** | — | — | **$3.5\text{ mm}$** | Rigid base with chimney vent |
| **Guide Pins** | — | **$4 \times \varnothing 6.0\text{ mm}$ (Split)** | — | **$7.0\text{ mm}$ bottom** + **$7.0\text{ mm}$ top** |
| **Mounting Levels** | — | — | **$Z = 20\text{ mm}$, $Z = 55\text{ mm}$** | Dual screw rigidity |

---

## Multi-Bay Stacking Guide

Modules are daisy-chained side-by-side:

```
       [Bay 1]                  [Bay 2]
+--------------------+   +--------------------+
|  (Inside Bay 1)    |   |  (Inside Bay 2)    |
|                    |   |                    |
|  [Screw + Washer]  |   |    [M3 Hex Nut]    |
|         |          |   |          ^         |
|         +==========>===>==========+         |
|         4mm wall   |   |   4mm wall         |
+--------------------+   +--------------------+
     Flat Mating Joint: 8mm total solid plastic
```

1. Align the flat right exterior wall of Bay 1 with the flat left exterior wall of Bay 2.
2. From **inside Bay 1**, pass an M3 screw with an M3 washer through the inside counterbore.
3. In **inside Bay 2**, thread the screw into the captive M3 hex nut.
4. Tighten with a hex key from inside Bay 1. Both screw head and nut are recessed flush inside the respective window frames, leaving the drive pocket completely clear!

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
- **Wall Loops:** **4** (ensures 100% solid perimeters through the 4.0 mm walls, guide pins, and around screw holes)
- **Top / Bottom Shells:** 4 layers
- **Infill:** $15\text{--}20\%$ Gyroid
- **Supports:** **None required** (honeycombs, vertical pins, and bridges are 100% self-supporting)
- **Print Time:** ~1h 36m
- **Filament Consumption:** ~43.2 g

---

## Change Tracking in Git (Code-CAD)

Binary 3D models (`.stl`, `.3mf`, `.f3d`) cannot be diffed cleanly in Git. This repository provides text-based parametric models that allow full **Git change tracking**:

1. **OpenSCAD (`cad/modular_single_bay_70mm.scad`):**
   - Pure text-based CSG script.
   - All dimensions (`drive_w`, `drive_t`, `slot_l`, `slot_t`, `caddy_h`, `pin_r`, etc.) are declared as parametric variables at the top of the file.
   - Any modification will produce clear, line-by-line `git diff` outputs.
2. **Fusion 360 Python Generator (`cad/generate_fusion360_model.py`):**
   - Standalone Python script for the Fusion 360 API.
   - Fully parametric generation, appearance assignment, and automated export to STL.
3. **Fusion MCP Client (`cad/fusion_client.py`):**
   - Lightweight JSON-RPC client to execute scripts and export models directly via Fusion 360 MCP.

---

---

## Print Monitoring & Web Dashboard

This repository includes real-time telemetry tools to monitor Flashforge Adventurer 5M series printers via TCP socket (port 8899) and live MJPEG chamber camera stream (port 8080).

### 1. CLI Monitor (`print_status.py`)
Quick command-line tool for checking temperatures, layer count, file, and progress:
```bash
python print_status.py          # One-time status snapshot
python print_status.py --watch  # Auto-refreshing terminal HUD (every 5s)
```

### 2. Real-Time Web Dashboard (`app/`)
A responsive dark-themed dashboard containerized with Docker and deployed to `kopilka:4000`:
- **Live Chamber Camera Feed:** Embedded low-latency MJPEG stream with real-time XYZ toolhead coordinate overlay.
- **WebSocket Telemetry:** Zero-latency updates for Nozzle & Bed temperatures (actual vs. target), layer progress (`Layer X / Y`), elapsed time, and extruded filament length (A).
- **Printer Controls:** Remote chamber LED light toggle (`~M651` / `~M652`) and Pause / Resume controls (`~M25` / `~M24`).
- **Stream Recording & Archive:** Direct server-side recording of the camera feed into compressed H.264 MP4 clips via FFmpeg, with a built-in gallery for downloads and management.
- **Access:** Available on local network at `http://kopilka:4000/`.

To run locally or deploy:
```bash
cd app
docker compose up -d --build
```

---

---

## Fresh Laptop Setup Guide (Zero to Ready)

If you clone this repository onto a brand-new computer, here is exactly what to install and how to work with the project files:

### 1. Requirements Checklist

| Software / Tool | Purpose | How to Get |
| :--- | :--- | :--- |
| **Git** | Cloning & updating the repository | [git-scm.com](https://git-scm.com/) |
| **Python 3.10+** | CLI telemetry scripts & running the local web app | [python.org](https://www.python.org/) or `winget install Python.Python.3.12` |
| **OrcaSlicer (v2.x+)** | Slicing models & sending prints to Flashforge / Klipper | [github.com/SoftFever/OrcaSlicer/releases](https://github.com/SoftFever/OrcaSlicer/releases) |
| **Autodesk Fusion 360** *(Optional for CAD editing)* | Inspecting or modifying the native parametric model | [autodesk.com/products/fusion-360](https://www.autodesk.com/products/fusion-360/personal) |
| **Docker Desktop** *(Optional for telemetry web dashboard)* | Containerized web dashboard deployment | [docker.com](https://www.docker.com/) |

---

### 2. Workflow: 3D Printing (Ready Out of the Box)

You do **not** need CAD software installed just to slice or print:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/glotoff/3d-printing-models.git
   cd 3d-printing-models
   ```
2. **Open in OrcaSlicer:**
   - Double-click [`Modular_SingleBay_16mm_M3.3mf`](Modular_SingleBay_16mm_M3.3mf).
   - This opens the exact project with all tuned print settings:
     - 4 wall loops (1.6 mm solid shell)
     - 15% infill
     - 0.20 mm layer height
     - Flashforge Adventurer 5M Pro profile
   - Click **Slice plate** and send directly to your printer over Wi-Fi.
3. **Alternatively, use the pre-sliced G-code directly:**
   - [`Modular_SingleBay_SplitPins_7mm_PLA_1h18m.gcode`](Modular_SingleBay_SplitPins_7mm_PLA_1h18m.gcode) can be loaded directly onto a USB stick or uploaded via Flashforge web UI.

---

### 3. Workflow: CAD Modeling & Editing in Autodesk Fusion 360

If you want to edit, customize, or export variations in Fusion 360:

#### Option A: Open the Standalone `.f3d` Archive (Easiest)
1. Open **Autodesk Fusion 360**.
2. Click **File** $\to$ **Open...** $\to$ **Open from my computer**.
3. Select [`cad/Modular_SingleBay_Vent10mm_SplitPins.f3d`](cad/Modular_SingleBay_Vent10mm_SplitPins.f3d).
4. All bodies (caddy body and hard drive reference mock-up) and geometry will load natively.

#### Option B: Import the Universal `.step` File
- In Fusion 360 (or FreeCAD / SolidWorks), go to **File** $\to$ **Open** $\to$ select [`cad/Modular_SingleBay_Vent10mm_SplitPins.step`](cad/Modular_SingleBay_Vent10mm_SplitPins.step).

#### Option C: Re-generate From Python Script (Parametric Automation)
1. In Fusion 360, press **Shift + S** to open the **Scripts and Add-Ins** window.
2. Under the **Scripts** tab, click the green **+** icon (Create / Add).
3. Select or paste the contents of [`cad/generate_fusion360_model.py`](cad/generate_fusion360_model.py).
4. Click **Run**. The script will automatically generate the 3D model, apply all cutouts and split guide pins, insert the hard drive verification body, and export the high-res STL mesh.

---

### 4. Workflow: Printer Monitoring & Telemetry

1. **Instant CLI Status:**
   ```bash
   pip install requests
   python print_status.py          # One-shot terminal status snapshot
   python print_status.py --watch  # Auto-refreshing HUD (every 5s)
   ```

2. **Web Monitoring App (Local or Docker):**
   - **Running locally with Python:**
     ```bash
     cd app
     pip install -r requirements.txt
     python -m uvicorn main:app --host 0.0.0.0 --port 4000
     ```
   - **Running with Docker:**
     ```bash
     cd app
     docker compose up -d --build
     ```
   - Open your browser to `http://localhost:4000/`.

---

## Repository Structure

```
.
├── app/                                            # Real-time web telemetry dashboard
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py                                     # FastAPI + WebSocket backend & camera proxy
│   ├── requirements.txt
│   └── templates/
│       └── index.html                              # Dark-mode dashboard with Tailwind CSS
├── cad/
│   ├── Modular_SingleBay_Vent10mm_SplitPins.f3d   # Standalone native Autodesk Fusion 360 archive
│   ├── Modular_SingleBay_Vent10mm_SplitPins.step  # Universal CAD solid exchange model
│   └── generate_fusion360_model.py                 # Parametric Fusion 360 API generator
├── models/
│   └── Modular_SingleBay_70mm_Tight.stl            # Production STL model (89.0 x 32.8 x 70.0 mm)
├── Modular_SingleBay_SplitPins_7mm_PLA_1h18m.gcode # Print-ready G-code (Adventurer 5M Pro)
├── Modular_SingleBay_16mm_M3.3mf                   # OrcaSlicer complete project file
├── print_status.py                                 # CLI printer telemetry script
├── images/                                         # 3D viewport renders and slicer plate previews
├── legacy/                                         # Previous prototype iterations and test models
├── .gitignore
└── README.md
```

