// ==============================================================================
// Modular Single-Bay HDD / SSD Caddy (70mm Tall, Snug 74mm Depth)
// Parametric OpenSCAD Model for Git Version Control and Change Tracking
// ==============================================================================

$fn = 60;

// --- PARAMETERS (All dimensions in mm) ---

// Enclosure / Drive Slot Dimensions
drive_d         = 74.0;  // Internal slot length (X axis) - snug fit for enclosure
drive_t         = 16.0;  // Nominal drive thickness
slot_t          = 16.5;  // Internal slot width (Y axis) - 0.5mm total clearance
caddy_h         = 70.0;  // Total height (Z axis)
wall_t          = 4.0;   // Side wall thickness (Y axis)
base_t          = 3.5;   // Bottom floor thickness (Z axis)
front_lip       = 5.0;   // Solid front pillar length (X axis)
rear_lip        = 5.0;   // Solid rear pillar length (X axis)

// Retaining Lips & Windows
lip_t           = 2.0;   // Front/rear retaining lip width on each side
window_z_bot    = 7.5;   // Window bottom Z coordinate
window_z_top    = 65.0;  // Window top Z coordinate

// Derived Module Dimensions
mod_w           = slot_t + 2 * wall_t;            // 24.5 mm total width
mod_l           = drive_d + front_lip + rear_lip; // 84.0 mm total length
window_w        = slot_t - 2 * lip_t;             // 12.5 mm window opening width

// M3 Joining Hardware Parameters
z_screws        = [20.0, 55.0]; // Mounting hole heights
x_screw_front   = front_lip / 2.0;                // 2.5 mm
x_screw_rear    = front_lip + drive_d + rear_lip / 2.0; // 81.5 mm
m3_hole_dia     = 3.4;   // Clearance through-hole diameter
m3_washer_dia   = 7.5;   // Inside counterbore diameter (for DIN 125 washer + screw head)
m3_washer_depth = 2.5;   // Inside counterbore depth
m3_nut_f2f      = 5.6;   // Captive hex nut pocket width across flats
m3_nut_depth    = 2.6;   // Captive hex nut pocket depth
nut_washer_depth= 0.8;   // Optional washer recess on nut side

// Honeycomb Lattice Parameters
hex_r           = 4.6;   // Hexagon circumradius
hex_dx          = 8.8;   // Horizontal column spacing
hex_dz          = 7.2;   // Vertical row spacing

// --- MODULES ---

module hexagon(r, h) {
    cylinder(r = r, h = h, center = true, $fn = 6);
}

module hex_nut_pocket(f2f, depth) {
    r = f2f / sqrt(3);
    cylinder(r = r, h = depth, $fn = 6);
}

module caddy_body() {
    difference() {
        // 1. Solid Outer Block
        cube([mod_l, mod_w, caddy_h]);

        // 2. Drive Slot Pocket
        translate([front_lip, wall_t, base_t])
            cube([drive_d + 0.1, slot_t, caddy_h]);

        // 3. Bottom Chimney Vent (through floor)
        translate([front_lip + 8.0, wall_t + lip_t, -1])
            cube([drive_d - 16.0, slot_t - 2 * lip_t, base_t + 2]);

        // 4. Front Vertical Window
        translate([-1, wall_t + lip_t, window_z_bot])
            cube([front_lip + 2, window_w, window_z_top - window_z_bot]);

        // 5. Rear Vertical Window
        translate([front_lip + drive_d - 1, wall_t + lip_t, window_z_bot])
            cube([rear_lip + 2, window_w, window_z_top - window_z_bot]);

        // 6. Honeycomb Lattice on Side Walls
        for (row = [0:6]) {
            z_c = 13.5 + row * hex_dz;
            x_shift = (row % 2 == 1) ? (hex_dx / 2.0) : 0.0;
            for (col = [0:7]) {
                x_c = front_lip + 8.5 + col * hex_dx + x_shift;
                if (x_c >= (front_lip + 5.5) && 
                    x_c <= (front_lip + drive_d - 5.5) && 
                    (z_c + hex_r) <= (caddy_h - 4.5)) {
                    translate([x_c, -1, z_c])
                        rotate([-90, 0, 0])
                        hexagon(hex_r, mod_w + 2);
                }
            }
        }

        // 7. M3 Joining System in Solid Pillars
        for (zs = z_screws) {
            for (xs = [x_screw_front, x_screw_rear]) {
                // A. M3 Through-Hole (3.4 mm) across entire width
                translate([xs, -1, zs])
                    rotate([-90, 0, 0])
                    cylinder(d = m3_hole_dia, h = mod_w + 2);

                // B. Inside Washer / Screw Head Counterbore (Left Pillar)
                // Inside face of left pillar is at Y = wall_t + lip_t (6.0 mm)
                // Cuts outward (towards -Y) by 2.5 mm (down to Y = 3.5 mm).
                // Outer face at Y = 0 remains 100% FLAT with 3.5 mm solid wall!
                translate([xs, wall_t + lip_t - m3_washer_depth, zs])
                    rotate([-90, 0, 0])
                    cylinder(d = m3_washer_dia, h = m3_washer_depth + 0.1);

                // C. Inside Hex Nut Pocket (Right Pillar)
                // Inside face of right pillar is at Y = wall_t + slot_t - lip_t (18.5 mm)
                // Cuts outward (towards +Y) by 2.6 mm (up to Y = 21.1 mm).
                // Outer face at Y = 24.5 mm remains 100% FLAT with 3.4 mm solid wall!
                translate([xs, wall_t + slot_t - lip_t - 0.05, zs])
                    rotate([-90, 0, 0])
                    hex_nut_pocket(m3_nut_f2f, m3_nut_depth + 0.1);

                // D. Optional Inside Washer Recess on Nut Side
                translate([xs, wall_t + slot_t - lip_t - 0.05, zs])
                    rotate([-90, 0, 0])
                    cylinder(d = m3_washer_dia, h = nut_washer_depth + 0.1);
            }
        }
    }
}

// Render the single bay
caddy_body();
