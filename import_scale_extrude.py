import bpy

# Path to the SVG file
svg_path = "/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 1/svg_output_filtered/filtered_paths_with_layers (6).svg"

print("Starting script...")

# Clear all existing objects
print("Clearing existing objects...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import SVG
print(f"Importing SVG file from {svg_path}...")
bpy.ops.import_curve.svg(filepath=svg_path)

# Get the imported collection (assuming the collection is named after the SVG file)
collection_name = "filtered_paths_with_layers (6).svg"
print(f"Looking for collection: {collection_name}...")
collection = bpy.context.scene.collection.children.get(collection_name)

if collection:
    print(f"Collection '{collection_name}' found. Deselecting all objects...")
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select all path objects in the collection
    print("Selecting all curve objects in the collection...")
    for obj in collection.objects:
        if obj.type == 'CURVE':  # Ensure we only select the curve objects (paths)
            obj.select_set(True)
    
    # Set the first selected object as active
    print("Setting the first selected object as active...")
    bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.active = collection.objects[0]
    
    # Join all selected objects (paths) into one object
    print("Joining all selected path objects into one object...")
    bpy.ops.object.join()

    # Convert the selected object (which is now a curve) to a mesh
    print("Converting the curve object to a mesh...")
    bpy.ops.object.convert(target='MESH')

    # Scale the mesh object by a factor (adjust the scale_factor as needed)
    scale_factor = 100
    print(f"Scaling the mesh by a factor of {scale_factor}...")
    bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

    # Switch to Edit Mode
    print("Switching to Edit Mode...")
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices in Edit Mode
    print("Selecting all vertices in Edit Mode...")
    bpy.ops.mesh.select_all(action='SELECT')

    # Extrude and move upwards by 3.5 units
    print("Extruding and moving upwards by 24.5 units...")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 24.5)})

    # Switch back to Object Mode
    print("Switching back to Object Mode...")
    bpy.ops.object.mode_set(mode='OBJECT')

else:
    print(f"Collection '{collection_name}' not found.")

# Save the result
output_path = "/Users/marius/Documents/GitHub/Junction_Hackathon/Blender Output/output_file.blend"
print(f"Saving the Blender file to {output_path}...")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("Script finished.")