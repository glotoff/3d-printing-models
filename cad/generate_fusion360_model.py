import adsk.core, adsk.fusion, math

def get_app_safe(collection, name):
    for i in range(collection.count):
        item = collection.item(i)
        if item.name == name:
            return item
    return None

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
    
    # Close any currently open document or create a fresh one
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType, True)
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    root = design.rootComponent

    # 1. Dimensions (cm)
    # Requirement 2: Reduce depth by 4mm (slot from 78mm to 74mm, outer from 88mm to 84mm)
    drive_d = 7.4    # 74.0 mm internal slot length along X
    drive_t = 1.60   # 16.0 mm hard drive enclosure thickness along Y
    drive_h = 12.5   # 125.0 mm drive height along Z
    plug_l = 4.0
    plug_w = 1.6
    plug_t = 0.8
    
    # Slot thickness: 16.5 mm (1.65 cm) for snug fit with 16.0 mm enclosure
    slot_t = 1.65    
    wall_t = 0.40    # 4.0 mm side walls maintained!
    base_t = 0.35    # 3.5 mm floor
    caddy_h = 7.0    # 70.0 mm height (Requirement 1: 70mm tall)
    front_lip = 0.5  # 5.0 mm solid front pillar
    rear_lip = 0.5   # 5.0 mm solid rear pillar
    
    mod_w = slot_t + 2 * wall_t # 1.65 + 0.80 = 2.45 cm (24.5 mm)
    mod_l = drive_d + front_lip + rear_lip # 7.4 + 1.0 = 8.4 cm (84.0 mm)
    
    ext_feats = root.features.extrudeFeatures
    sketches = root.sketches
    planes = root.constructionPlanes
    
    # 1. Main outer solid box: X = -front_lip to drive_d + rear_lip, Y = 0 to mod_w, Z = 0 to caddy_h
    sk_main = sketches.add(root.xYConstructionPlane)
    lines = sk_main.sketchCurves.sketchLines
    p0 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(-front_lip, 0, 0))
    p1 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(drive_d + rear_lip, 0, 0))
    p2 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(drive_d + rear_lip, mod_w, 0))
    p3 = sk_main.modelToSketchSpace(adsk.core.Point3D.create(-front_lip, mod_w, 0))
    lines.addByTwoPoints(p0, p1)
    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p0)
    
    ext_in = ext_feats.createInput(sk_main.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_in.setDistanceExtent(False, adsk.core.ValueInput.createByReal(caddy_h))
    mod_body = ext_feats.add(ext_in).bodies.item(0)
    mod_body.name = "Modular_Bay_70mm_Tight"
    
    # 2. Drive Slot (from Z = base_t to caddy_h)
    plane_floor_in = planes.createInput()
    plane_floor_in.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(base_t))
    plane_floor = planes.add(plane_floor_in)
    
    sk_slot = sketches.add(plane_floor)
    ssl = sk_slot.sketchCurves.sketchLines
    pa = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(0, wall_t, base_t))
    pb = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(drive_d + 0.05, wall_t, base_t))
    pc = sk_slot.modelToSketchSpace(adsk.core.Point3D.create(drive_d + 0.05, wall_t + slot_t, base_t))
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
    va = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(0.8, wall_t + 0.20, 0))
    vb = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(drive_d - 0.8, wall_t + 0.20, 0))
    vc = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(drive_d - 0.8, wall_t + slot_t - 0.20, 0))
    vd = sk_vent.modelToSketchSpace(adsk.core.Point3D.create(0.8, wall_t + slot_t - 0.20, 0))
    svl.addByTwoPoints(va, vb)
    svl.addByTwoPoints(vb, vc)
    svl.addByTwoPoints(vc, vd)
    svl.addByTwoPoints(vd, va)
    
    ext_vent = ext_feats.createInput(sk_vent.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_vent.setDistanceExtent(False, adsk.core.ValueInput.createByReal(base_t + 0.1))
    ext_feats.add(ext_vent)
    
    # 4. Honeycomb Grid on Large Side Wall (sketched on XZ plane, going all way up to 70mm!)
    sk_hex = sketches.add(root.xZConstructionPlane)
    r_hex = 0.46
    dx_hex = 0.88
    dz_hex = 0.72
    
    # 7 rows of hexagons reaching up to ~61 mm
    for row in range(7):
        z_c = 1.35 + row * dz_hex
        x_shift = (dx_hex / 2.0) if (row % 2 == 1) else 0.0
        for col in range(8):
            x_c = 0.85 + col * dx_hex + x_shift
            if 0.55 <= x_c <= (drive_d - 0.55) and z_c + r_hex <= caddy_h - 0.45:
                add_hex_model(sk_hex, x_c, z_c, r_hex)
                
    hex_profs = adsk.core.ObjectCollection.create()
    for p in sk_hex.profiles:
        hex_profs.add(p)
    ext_hex = ext_feats.createInput(hex_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_hex.participantBodies = [mod_body]
    ext_hex.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mod_w + 0.1))
    ext_feats.add(ext_hex)

    # 5. Front & Rear Vertical Windows
    # Window opening in Y is from y_in_left to y_in_right
    y_in_left = wall_t + 0.20   # 0.60 cm (6.0 mm)
    y_in_right = wall_t + 0.20 + (slot_t - 0.40) # 1.85 cm (18.5 mm)
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
    start_def = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(drive_d - 0.05))
    ext_rear.startExtent = start_def
    ext_feats.add(ext_rear)

    # 6. M3 HORIZONTAL JOINING SYSTEM IN SOLID PILLARS
    # Centers of mounting holes in pillars:
    # Front pillar: X = -front_lip / 2.0 (-0.25 cm = -2.5 mm)
    # Rear pillar: X = drive_d + rear_lip / 2.0 (7.65 cm = 76.5 mm)
    # Heights: Z = 2.0 cm and Z = 5.5 cm
    z_screws = [2.0, 5.5]
    
    # A. M3 Through-Holes (3.4 mm dia) from Y = 0 to Y = mod_w across the entire part
    sk_m3_holes = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        c1 = sk_m3_holes.modelToSketchSpace(adsk.core.Point3D.create(-front_lip / 2.0, 0, zs))
        c2 = sk_m3_holes.modelToSketchSpace(adsk.core.Point3D.create(drive_d + rear_lip / 2.0, 0, zs))
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
    # Requirement: "головка для шайбы должна быть внутри, а не снаружи детали"
    # Washer OD is 7.0 mm (DIN 125 M3 washer). We use dia 7.5 mm (radius 0.375 cm) so washer fits cleanly.
    # Depth: 2.5 mm (0.25 cm) into the pillar from the inside face (Y = 0.60 cm cutting towards -Y to Y = 0.35 cm).
    # Solid outer wall remaining: 3.5 mm (from Y = 0.35 to Y = 0.0). Outer face Y = 0 is 100% FLAT.
    sk_cb_in = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        cb1 = sk_cb_in.modelToSketchSpace(adsk.core.Point3D.create(-front_lip / 2.0, 0, zs))
        cb2 = sk_cb_in.modelToSketchSpace(adsk.core.Point3D.create(drive_d + rear_lip / 2.0, 0, zs))
        sk_cb_in.sketchCurves.sketchCircles.addByCenterRadius(cb1, 0.375) # 7.5 mm dia washer counterbore
        sk_cb_in.sketchCurves.sketchCircles.addByCenterRadius(cb2, 0.375)
        
    cb_in_profs = adsk.core.ObjectCollection.create()
    for p in sk_cb_in.profiles:
        cb_in_profs.add(p)
        
    ext_cb_left = ext_feats.createInput(cb_in_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_cb_left.participantBodies = [mod_body]
    # Cut in -Y direction from Y = y_in_left (0.60 cm) by 0.25 cm
    ext_cb_left.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.25)), adsk.fusion.ExtentDirections.NegativeExtentDirection)
    ext_cb_left.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(y_in_left))
    ext_feats.add(ext_cb_left)

    # C. Captive Hex Nut Pocket on INSIDE face of RIGHT pillar (y_in_right = 1.85 cm):
    # Requirement: "i will insert the screws and гайки from inside, hence i need the spaces on the inside side of the wall"
    # Nut pocket cuts into right pillar in +Y direction from Y = 1.85 cm by 0.26 cm (to Y = 2.11 cm).
    # Solid outer wall remaining: 3.4 mm (from Y = 2.11 to Y = 2.45). Outer face Y = 2.45 is 100% FLAT.
    sk_nut = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        add_hex_nut_pocket_xz(sk_nut, -front_lip / 2.0, zs, 0.56)
        add_hex_nut_pocket_xz(sk_nut, drive_d + rear_lip / 2.0, zs, 0.56)
        
    nut_profs = adsk.core.ObjectCollection.create()
    for p in sk_nut.profiles:
        nut_profs.add(p)
    ext_nut = ext_feats.createInput(nut_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_nut.participantBodies = [mod_body]
    ext_nut.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.26)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ext_nut.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(y_in_right))
    ext_feats.add(ext_nut)

    # Optional washer pocket on nut side (dia 7.5 mm, depth 0.8 mm) so if a washer is used with the nut, it sits flush!
    sk_nut_washer = sketches.add(root.xZConstructionPlane)
    for zs in z_screws:
        nw1 = sk_nut_washer.modelToSketchSpace(adsk.core.Point3D.create(-front_lip / 2.0, 0, zs))
        nw2 = sk_nut_washer.modelToSketchSpace(adsk.core.Point3D.create(drive_d + rear_lip / 2.0, 0, zs))
        sk_nut_washer.sketchCurves.sketchCircles.addByCenterRadius(nw1, 0.375)
        sk_nut_washer.sketchCurves.sketchCircles.addByCenterRadius(nw2, 0.375)
    nw_profs = adsk.core.ObjectCollection.create()
    for p in sk_nut_washer.profiles:
        nw_profs.add(p)
    ext_nw = ext_feats.createInput(nw_profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_nw.participantBodies = [mod_body]
    ext_nw.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.08)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ext_nw.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(y_in_right))
    ext_feats.add(ext_nw)

    # 7. Add 1 SSD Drive (16.0 mm thick) + Top USB Plug for visual verification
    y_drive_center = wall_t + (slot_t - drive_t) / 2.0
    sk_drv = sketches.add(plane_floor)
    sdl = sk_drv.sketchCurves.sketchLines
    da = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(0.01, y_drive_center, base_t))
    db = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(0.01 + drive_d - 0.02, y_drive_center, base_t))
    dc = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(0.01 + drive_d - 0.02, y_drive_center + drive_t, base_t))
    dd = sk_drv.modelToSketchSpace(adsk.core.Point3D.create(0.01, y_drive_center + drive_t, base_t))
    sdl.addByTwoPoints(da, db)
    sdl.addByTwoPoints(db, dc)
    sdl.addByTwoPoints(dc, dd)
    sdl.addByTwoPoints(dd, da)
    
    ext_drv = ext_feats.createInput(sk_drv.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_drv.setDistanceExtent(False, adsk.core.ValueInput.createByReal(drive_h))
    b_drv = ext_feats.add(ext_drv).bodies.item(0)
    b_drv.name = "SSD_Drive_16mm"
    
    # 40mm Plug
    plane_top_in = planes.createInput()
    plane_top_in.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(base_t + drive_h))
    plane_top = planes.add(plane_top_in)
    
    sk_plug = sketches.add(plane_top)
    spl = sk_plug.sketchCurves.sketchLines
    px0 = (drive_d - plug_l) / 2.0
    py0 = wall_t + (slot_t - plug_w) / 2.0
    pa = sk_plug.modelToSketchSpace(adsk.core.Point3D.create(px0, py0, base_t + drive_h))
    pb = sk_plug.modelToSketchSpace(adsk.core.Point3D.create(px0 + plug_l, py0, base_t + drive_h))
    pc = sk_plug.modelToSketchSpace(adsk.core.Point3D.create(px0 + plug_l, py0 + plug_w, base_t + drive_h))
    pd = sk_plug.modelToSketchSpace(adsk.core.Point3D.create(px0, py0 + plug_w, base_t + drive_h))
    spl.addByTwoPoints(pa, pb)
    spl.addByTwoPoints(pb, pc)
    spl.addByTwoPoints(pc, pd)
    spl.addByTwoPoints(pd, pa)
    
    ext_plug = ext_feats.createInput(sk_plug.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_plug.setDistanceExtent(False, adsk.core.ValueInput.createByReal(plug_t))
    b_plug = ext_feats.add(ext_plug).bodies.item(0)
    b_plug.name = "USB_Plug_Top"
    
    # Apply appearances
    mat_lib = app.materialLibraries.itemByName("Fusion 360 Appearance Library")
    app_yellow = None
    app_black = None
    app_alu = None
    if mat_lib:
        try:
            app_yellow = mat_lib.appearances.itemByName("Paint - Enamel Glossy (Yellow)")
        except: pass
        try:
            app_black = mat_lib.appearances.itemByName("Paint - Matte (Black)")
        except: pass
        try:
            app_alu = mat_lib.appearances.itemByName("Aluminum - Anodized Rough (Grey)")
        except: pass
        
    if app_yellow:
        try:
            y_app = design.appearances.addByCopy(app_yellow)
            mod_body.appearance = y_app
        except: pass
    if app_black:
        try:
            b_app = design.appearances.addByCopy(app_black)
            b_drv.appearance = b_app
        except: pass
    if app_alu:
        try:
            a_app = design.appearances.addByCopy(app_alu)
            b_plug.appearance = a_app
        except: pass

    # Export STL
    export_mgr = design.exportManager
    stl_path = r"C:/dev/3d-printing-models/Modular_SingleBay_70mm_Tight.stl"
    stl_opts = export_mgr.createSTLExportOptions(mod_body, stl_path)
    stl_opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    export_mgr.execute(stl_opts)
    print("Exported STL to:", stl_path)

    # Save document
    doc.saveAs("11_Modular_SingleBay_70mm_InsideScrews", app.data.defaultProject.rootFolder, "Inside washer counterbores & nut pockets", "")
    print("Saved document as 11_Modular_SingleBay_70mm_InsideScrews")
