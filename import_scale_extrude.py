import bpy

# Path to the SVG file
svg_path = "/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 1/svg_output_filtered/floor_1_filtered.svg"

# Clear all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import SVG
bpy.ops.import_curve.svg(filepath=svg_path)

# Get the imported collection (assuming the collection is named after the SVG file)
collection_name = "floor_1_filtered.svg"
collection = bpy.context.scene.collection.children.get(collection_name)

if collection:
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select all path objects in the collection
    for obj in collection.objects:
        if obj.type == 'CURVE':  # Ensure we only select the curve objects (paths)
            obj.select_set(True)
    
    # Set the first selected object as active
    bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.active = collection.objects[0]
    
    # Join all selected objects (paths) into one object
    bpy.ops.object.join()

    # Convert the selected object (which is now a curve) to a mesh
    bpy.ops.object.convert(target='MESH')

    # Scale the mesh object by a factor (adjust the scale_factor as needed)
    scale_factor = 100
    bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

# Save the result
output_path = "/Users/marius/Documents/GitHub/Junction_Hackathon/Blender Output/output_file.blend"
bpy.ops.wm.save_as_mainfile(filepath=output_path)