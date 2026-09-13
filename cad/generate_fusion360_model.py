import adsk.core, adsk.fusion, math

def add_hex_model(sk, cx, cz, r):
    lines = sk.sketchCurves.sketchLines
    pts = []
    for k in range(6):
        ang = math.pi / 2.0 + k * math.pi / 3.0
        x = cx + r * math.cos(ang)
        z = cz + r * math.sin(ang)
        p_m = adsk.core.Point3D.create(x, 0, z)
        p_sk = sk.modelToSketchSpace(p_m)
        pts.append(p_sk)
    for k in range(6):
        lines.addByTwoPoints(pts[k], pts[(k + 1) % 6])

def add_hex_nut_pocket_xz(sk, cx, cz, flat_to_flat):
    r = (flat_to_flat / math.sqrt(3))
    lines = sk.sketchCurves.sketchLines
    pts = []
    for k in range(6):
        ang = k * math.pi / 3.0
        x = cx + r * math.cos(ang)
        z = cz + r * math.sin(ang)
        p_m = adsk.core.Point3D.create(x, 0, z)
        p_sk = sk.modelToSketchSpace(p_m)
        pts.append(p_sk)
    for k in range(6):
        lines.addByTwoPoints(pts[k], pts[(k + 1) % 6])

def add_rect_yz(sk, x_plane, y1, z1, y2, z2):
    lines = sk.sketchCurves.sketchLines
    p1 = sk.modelToSketchSpace(adsk.core.Point3D.create(x_plane, y1, z1))
    p2 = sk.modelToSketchSpace(adsk.core.Point3D.create(x_plane, y2, z1))
    p3 = sk.modelToSketchSpace(adsk.core.Point3D.create(x_plane, y2, z2))
    p4 = sk.modelToSketchSpace(adsk.core.Point3D.create(x_plane, y1, z2))
    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p4)
    lines.addByTwoPoints(p4, p1)

def run(_context: str):
    app = adsk.core.Application.get()
    
    # Create new document
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType, True)
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    root = design.rootComponent

    # --- PARAMETERS (cm) ---
    # Hard Drive: 78.0 mm wide x 14.0 mm deep/thick x 125.0 mm tall
    drive_w = 7.80   # 78.0 mm
    drive_t = 1.40   # 14.0 mm
    drive_h = 12.50  # 125.0 mm
    
    # +10 mm Ventilation Expansion:
    # Slot width increased from 14.8 mm to 24.8 mm (2.48 cm)
    # Clearance between 4 guide pins remains exactly 14.8 mm (snug fit for 14.0 mm drive)
    # Air gap between drive and each honeycomb wall is 5.0 mm (0.50 cm)!
    slot_l = 7.90    # 79.0 mm internal slot length (0.5mm clearance each end)
    slot_t = 2.48    # 24.8 mm internal slot width (+10mm for massive airflow)
    wall_t = 0.40    # 4.0 mm side walls
    base_t = 0.35    # 3.5 mm floor
    caddy_h = 7.00   # 70.0 mm height
    front_lip = 0.50 # 5.0 mm front pillar
    rear_lip = 0.50  # 5.0 mm rear pillar
    lip_t = 0.20     # 2.0 mm window retaining lip
    
    mod_w = slot_t + 2 * wall_t # 2.48 + 0.80 = 3.28 cm (32.8 mm outer width)
    mod_l = slot_l + front_lip + rear_lip # 7.9 + 1.0 = 8.90 cm (89.0 mm outer length)
    
    ext_feats = root.features.extrudeFeatures
    sketches = root.sketches
    planes = root.constructionPlanes
    
    # 1. Main outer solid block: X = -front_lip to slot_l + rear_lip, Y = 0 to mod_w, Z = 0 to caddy_h
    sk_main = sketches.add(root.xYConstructionPlane)
    lines = sk_main.sketchCurves.sketchLines
    p0 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(-front_lip, 0, 0))
    p1 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(slot_l + rear_lip, 0, 0))
    p2 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(slot_l + rear_lip, mod_w, 0))
    p3 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(-front_lip, mod_w, 0))
    lines.addByTwoPoints(p0, p1)
    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p0)
    
    ext_in = ext_feats.createInput(sk_main.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_in.setDistanceExtent(False, adsk.core.ValueInput.createByReal(caddy_h))
    mod_body = ext_feats.add(ext_in).bodies.item(0)
    mod_body.name = "Modular_Bay_70mm_Vent10mm"
    
    # 2. Drive Slot (from Z = base_t to caddy_h)
    plane_floor_in = planes.createInput()
    plane_floor_in.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(base_t))
    plane_floor = planes.add(plane_floor_in)
    
    sk_slot = sketches.add(plane_floor)
    ssl = sk_slot.sketchCurves.sketchLines
    pa = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(0, wall_t, base_t))
    pb = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(slot_l + 0.05, wall_t, base_t))
    pc = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(slot_l + 0.05, wall_t + slot_t, base_t))
    pd = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(0, wall_t + slot_t, base_t))
    ssl.addByTwoPoints(pa, pb)
    ssl.addByTwoPoints(pb, pc)
    ssl.addByTwoPoints(pc, pd)
    ssl.addByTwoPoints(pd, pa)
    
    ext_slot = ext_feats.createInput(sk_slot.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_slot.setDistanceExtent(False, adsk.core.ValueInput.createByReal(caddy_h))
    ext_feats.add(ext_slot)
    
    # 3. Bottom Chimney Vent (through floor Z = 0 to base_t)
    sk_vent = sketches.add(root.xYConstructionPlane)
    svl = sk_vent.sketchCurves.sketchLines
    va = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(0.8, wall_t + lip_t, 0))
    vb = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(slot_l - 0.8, wall_t + lip_t, 0))
    vc = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(slot_l - 0.8, wall_t + slot_t - lip_t, 0))
    vd = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(0.8, wall_t + slot_t - lip_t, 0))
    svl.addByTwoPoints(va, vb)
    svl.addByTwoPoints(vb, vc)
    svl.addByTwoPoints(vc, vd)
    svl.addByTwoPoints(vd, va)
    
    ext_vent = ext_feats.createInput(sk_vent.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_vent.setDistanceExtent(False, adsk.core.ValueInput.createByReal(base_t + 0.1))
    ext_feats.add(ext_vent)
    
    # 4. Honeycomb Grid on Large Side Wall (7 rows reaching to top)
    sk_hex = sketches.add(root.xZConstructionPlane)
    r_hex = 0.46
    dx_hex = 0.88
    dz_hex = 0.72
    
    for row in range(7):
        z_c = 1.35 + row * dz_hex
        x_shift = (dx_hex / 2.0) if (row % 2 == 1) else 0.0
        for col in range(9):
            x_c = 0.75 + col * dx_hex + x_shift
            if 0.55 <= x_c <= (slot_l - 0.55) and z_c + r_hex <= caddy_h - 0.45:
                add_hex_model(sk_hex, x_c, z_c, r_hex)
                
    hex_profs = adsk.core.ObjectCollection.create()
    for p in sk_hex.profiles:
        hex_profs.add(p)
    ext_hex = ext_feats.createInput(hex_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_hex.participantBodies = [mod_body]
    ext_hex.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mod_w + 0.1))
    ext_feats.add(ext_hex)

    # 5. Front & Rear Vertical Windows
    y_in_left = wall_t + lip_t   # 0.60 cm (6.0 mm)
    y_in_right = wall_t + slot_t - lip_t # 2.68 cm (26.8 mm)
    z_bot = base_t + 0.4
    z_top = caddy_h - 0.5
    
    sk_front = sketches.add(root.yZConstructionPlane)
    add_rect_yz(sk_front, 0, y_in_left, z_bot, y_in_right, z_top)
    
    ext_front = ext_feats.createInput(sk_front.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_front.participantBodies = [mod_body]
    ext_front.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-front_lip - 0.1))
    ext_feats.add(ext_front)
    
    ext_rear = ext_feats.createInput(sk_front.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_rear.participantBodies = [mod_body]
    ext_rear.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(rear_lip + 0.2)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    start_def = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(slot_l - 0.05))
    ext_rear.startExtent = start_def
    ext_feats.add(ext_rear)

    # 6. M3 HORIZONTAL JOINING SYSTEM IN SOLID PILLARS
    z_screws = [2.0, 5.5]
    
    # A. M3 Through-Holes (3.4 mm dia) from Y = 0 to Y = mod_w across entire part
    sk_m3_holes = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        c1 = sk_m3_holes.modelToSketchSpace(adsk.core.Point3D.create(-front_lip / 2.0, 0, zs))
        c2 = sk_m3_holes.modelToSketchSpace(adsk.core.Point3D.create(slot_l + rear_lip / 2.0, 0, zs))
        sk_m3_holes.sketchCurves.sketchCircles.addByCenterRadius(c1, 0.17)
        sk_m3_holes.sketchCurves.sketchCircles.addByCenterRadius(c2, 0.17)
    
    m3_hole_profs = adsk.core.ObjectCollection.create()
    for p in sk_m3_holes.profiles:
        m3_hole_profs.add(p)
    ext_m3 = ext_feats.createInput(m3_hole_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_m3.participantBodies = [mod_body]
    ext_m3.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mod_w + 0.1))
    ext_feats.add(ext_m3)
    
    # B. Screw Head + Washer Counterbore on INSIDE face of LEFT pillar (y_in_left = 0.60 cm):
    # Dia 7.5 mm, depth 2.5 mm in -Y direction.
    sk_cb_in = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        cb1 = sk_cb_in.modelToSketchSpace(adsk.core.Point3D.create(-front_lip / 2.0, 0, zs))
        cb2 = sk_cb_in.modelToSketchSpace(adsk.core.Point3D.create(slot_l + rear_lip / 2.0, 0, zs))
        sk_cb_in.sketchCurves.sketchCircles.addByCenterRadius(cb1, 0.375)
        sk_cb_in.sketchCurves.sketchCircles.addByCenterRadius(cb2, 0.375)
        
    cb_in_profs = adsk.core.ObjectCollection.create()
    for p in sk_cb_in.profiles:
        cb_in_profs.add(p)
        
    ext_cb_left = ext_feats.createInput(cb_in_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_cb_left.participantBodies = [mod_body]
    ext_cb_left.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.25)), adsk.fusion.ExtentDirections.NegativeExtentDirection)
    ext_cb_left.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(y_in_left))
    ext_feats.add(ext_cb_left)

    # C. Captive Hex Nut Pocket on INSIDE face of RIGHT pillar (y_in_right = 2.68 cm):
    # Flat-to-flat 5.6 mm, depth 2.6 mm in +Y direction.
    sk_nut = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        add_hex_nut_pocket_xz(sk_nut, -front_lip / 2.0, zs, 0.56)
        add_hex_nut_pocket_xz(sk_nut, slot_l + rear_lip / 2.0, zs, 0.56)
        
    nut_profs = adsk.core.ObjectCollection.create()
    for p in sk_nut.profiles:
        nut_profs.add(p)
    ext_nut = ext_feats.createInput(nut_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_nut.participantBodies = [mod_body]
    ext_nut.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.26)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ext_nut.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(y_in_right))
    ext_feats.add(ext_nut)

    # Washer recess on nut side (7.5 mm dia, 0.8 mm depth)
    sk_nut_w = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        nw1 = sk_nut_w.modelToSketchSpace(adsk.core.Point3D.create(-front_lip / 2.0, 0, zs))
        nw2 = sk_nut_w.modelToSketchSpace(adsk.core.Point3D.create(slot_l + rear_lip / 2.0, 0, zs))
        sk_nut_w.sketchCurves.sketchCircles.addByCenterRadius(nw1, 0.375)
        sk_nut_w.sketchCurves.sketchCircles.addByCenterRadius(nw2, 0.375)
    nw_profs = adsk.core.ObjectCollection.create()
    for p in sk_nut_w.profiles:
        nw_profs.add(p)
    ext_nw = ext_feats.createInput(nw_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_nw.participantBodies = [mod_body]
    ext_nw.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.08)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ext_nw.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(y_in_right))
    ext_feats.add(ext_nw)

    # 7. ADD 4 SPLIT CYLINDER GUIDE PINS INSIDE THE HOLDER (7mm Bottom + 7mm Top)
    # User requirement:
    # "4 цилиндрических направляющих пина don't need to go from top to bottom.
    # to save the time and plastic, you can make it like 7mm at the bottom and 7mm at the top and it should be enough."
    # 4 cylindrical pins in the 4 corners of the drive slot:
    # Radius = 0.30 cm (6.0 mm dia).
    # Left pins center: Y = 0.60 cm -> inner tangent at Y = 0.90 cm
    # Right pins center: Y = 2.68 cm -> inner tangent at Y = 2.38 cm
    # Distance between pin inner tangents = 2.38 - 0.90 = 1.48 cm (14.8 mm - exact snug fit for 14.0 mm drive!)
    # Air gap between drive and each side honeycomb wall = 5.0 mm!
    # Front pins at X = 0.80 cm, Rear pins at X = slot_l - 0.80 = 7.10 cm
    
    pin_r = 0.30 # 3.0 mm radius = 6.0 mm dia cylinder
    pin_h = 0.70 # 7.0 mm height
    x_pins = [0.80, slot_l - 0.80]
    y_pins = [0.60, 2.68]
    
    # A. Bottom 4 Pins: from floor Z = base_t (0.35 cm) extending up by 7.0 mm (0.70 cm) to Z = 1.05 cm
    sk_pins_bot = sketches.add(plane_floor)
    for xp in x_pins:
        for yp in y_pins:
            pt = sk_pins_bot.modelToSketchSpace(adsk.core.Point3D.create(xp, yp, base_t))
            sk_pins_bot.sketchCurves.sketchCircles.addByCenterRadius(pt, pin_r)
            
    pin_bot_profs = adsk.core.ObjectCollection.create()
    for p in sk_pins_bot.profiles:
        pin_bot_profs.add(p)
        
    ext_pins_bot = ext_feats.createInput(pin_bot_profs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    ext_pins_bot.participantBodies = [mod_body]
    ext_pins_bot.setDistanceExtent(False, adsk.core.ValueInput.createByReal(pin_h))
    ext_feats.add(ext_pins_bot)

    # B. Top 4 Pins: from Z = caddy_h - pin_h (6.30 cm) extending up by 7.0 mm (0.70 cm) to Z = 7.00 cm
    plane_top_pins_in = planes.createInput()
    plane_top_pins_in.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(caddy_h - pin_h))
    plane_top_pins = planes.add(plane_top_pins_in)

    sk_pins_top = sketches.add(plane_top_pins)
    for xp in x_pins:
        for yp in y_pins:
            pt = sk_pins_top.modelToSketchSpace(adsk.core.Point3D.create(xp, yp, caddy_h - pin_h))
            sk_pins_top.sketchCurves.sketchCircles.addByCenterRadius(pt, pin_r)

    pin_top_profs = adsk.core.ObjectCollection.create()
    for p in sk_pins_top.profiles:
        pin_top_profs.add(p)

    ext_pins_top = ext_feats.createInput(pin_top_profs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    ext_pins_top.participantBodies = [mod_body]
    ext_pins_top.setDistanceExtent(False, adsk.core.ValueInput.createByReal(pin_h))
    ext_feats.add(ext_pins_top)

    # 8. Add 1 Hard Drive (78.0 mm wide x 14.0 mm thick x 125 mm tall) for verification
    y_drive_center = 0.90 + 0.04 # centered between pins with 0.4mm clearance on each side
    x_drive_center = (slot_l - drive_w) / 2.0 # centered along X with 0.5mm clearance on each end
    sk_drv = sketches.add(plane_floor)
    sdl = sk_drv.sketchCurves.sketchLines
    da = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(x_drive_center, y_drive_center, base_t))
    db = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(x_drive_center + drive_w, y_drive_center, base_t))
    dc = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(x_drive_center + drive_w, y_drive_center + drive_t, base_t))
    dd = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(x_drive_center, y_drive_center + drive_t, base_t))
    sdl.addByTwoPoints(da, db)
    sdl.addByTwoPoints(db, dc)
    sdl.addByTwoPoints(dc, dd)
    sdl.addByTwoPoints(dd, da)
    
    ext_drv = ext_feats.createInput(sk_drv.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_drv.setDistanceExtent(False, adsk.core.ValueInput.createByReal(drive_h))
    b_drv = ext_feats.add(ext_drv).bodies.item(0)
    b_drv.name = "HardDrive_78x14mm"

    # Export STL
    export_mgr = design.exportManager
    stl_path = r"C:/dev/3d-printing-models/Modular_SingleBay_70mm_Tight.stl"
    stl_opts = export_mgr.createSTLExportOptions(mod_body, stl_path)
    stl_opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    export_mgr.execute(stl_opts)
    print("Exported updated STL with split pins (7mm top/bottom) to:", stl_path)

    # Save document in Default Project
    dp = None
    for p in app.data.dataProjects:
        if p.name == "Default Project":
            dp = p
            break
    if dp:
        try:
            doc.saveAs("14_Modular_SingleBay_Vent10mm_SplitPins", dp.rootFolder, "+10mm ventilation with split 7mm bottom and 7mm top guide pins", "")
            print("Saved document as 14_Modular_SingleBay_Vent10mm_SplitPins")
        except Exception as e:
            print("Save notice:", e)
