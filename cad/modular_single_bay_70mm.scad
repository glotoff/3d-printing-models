// ==============================================================================
// Modular Single-Bay HDD / SSD Caddy (70mm Tall, Exact 78x14mm Drive Fit)
// Parametric OpenSCAD Model for Git Version Control and Change Tracking
// ==============================================================================

$fn = 60;

// --- PARAMETERS (All dimensions in mm) ---

// Hard Drive Dimensions
drive_w         = 78.0;  // Drive width (X axis)
drive_t         = 14.0;  // Drive depth / thickness (Y axis)
drive_h         = 125.0; // Drive upright height (Z axis)

// Internal Slot Dimensions
slot_l          = 79.0;  // Internal slot length (X axis) - 0.5mm clearance each end
slot_t          = 14.8;  // Internal slot width (Y axis) - 0.4mm clearance each side (snug upright fit)
caddy_h         = 70.0;  // Total height (Z axis)
wall_t          = 4.0;   // Solid side wall thickness (Y axis)
base_t          = 3.5;   // Bottom floor thickness (Z axis)
front_lip       = 5.0;   // Solid front pillar length (X axis)
rear_lip        = 5.0;   // Solid rear pillar length (X axis)

// Retaining Lips & Windows
lip_t           = 2.0;   // Front/rear retaining lip width on each side
window_z_bot    = 7.5;   // Window bottom Z coordinate
window_z_top    = 65.0;  // Window top Z coordinate

// Derived Module Dimensions
mod_w           = slot_t + 2 * wall_t;           // 22.8 mm total width
mod_l           = slot_l + front_lip + rear_lip; // 89.0 mm total length
window_w        = slot_t - 2 * lip_t;            // 10.8 mm window opening width

// M3 Joining Hardware Parameters
z_screws        = [20.0, 55.0]; // Dual mounting hole heights
x_screw_front   = front_lip / 2.0;               // 2.5 mm
x_screw_rear    = front_lip + slot_l + rear_lip / 2.0; // 86.5 mm
m3_hole_dia     = 3.4;   // Clearance through-hole diameter
m3_washer_dia   = 7.5;   // Inside counterbore diameter (for DIN 125 washer + screw head)
m3_washer_depth = 2.5;   // Inside counterbore depth
m3_nut_f2f      = 5.6;   // Captive hex nut pocket width across flats
m3_nut_depth    = 2.6;   // Captive hex nut pocket depth
nut_washer_depth= 0.8;   // Inside washer recess on nut side

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
            cube([slot_l + 0.1, slot_t, caddy_h]);

        // 3. Bottom Chimney Vent (through floor)
        translate([front_lip + 8.0, wall_t + lip_t, -1])
            cube([slot_l - 16.0, slot_t - 2 * lip_t, base_t + 2]);

        // 4. Front Vertical Window
        translate([-1, wall_t + lip_t, window_z_bot])
            cube([front_lip + 2, window_w, window_z_top - window_z_bot]);

        // 5. Rear Vertical Window
        translate([front_lip + slot_l - 1, wall_t + lip_t, window_z_bot])
            cube([rear_lip + 2, window_w, window_z_top - window_z_bot]);

        // 6. Honeycomb Lattice on Side Walls (7 rows)
        for (row = [0:6]) {
            z_c = 13.5 + row * hex_dz;
            x_shift = (row % 2 == 1) ? (hex_dx / 2.0) : 0.0;
            for (col = [0:8]) {
                x_c = front_lip + 7.5 + col * hex_dx + x_shift;
                if (x_c >= (front_lip + 5.5) && 
                    x_c <= (front_lip + slot_l - 5.5) && 
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
                // Inside face of right pillar is at Y = wall_t + slot_t - lip_t (16.8 mm)
                // Cuts outward (towards +Y) by 2.6 mm (up to Y = 19.4 mm).
                // Outer face at Y = 22.8 mm remains 100% FLAT with 3.4 mm solid wall!
                translate([xs, wall_t + slot_t - lip_t - 0.05, zs])
                    rotate([-90, 0, 0])
                    hex_nut_pocket(m3_nut_f2f, m3_nut_depth + 0.1);

                // D. Inside Washer Recess on Nut Side
                translate([xs, wall_t + slot_t - lip_t - 0.05, zs])
                    rotate([-90, 0, 0])
                    cylinder(d = m3_washer_dia, h = nut_washer_depth + 0.1);
            }
        }
    }
}

// Render the single bay
caddy_body();
