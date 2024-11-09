import bpy
import os

# Path to the folder containing the SVG files
folder_path = "fully_filtered_svgs"
svg_files = [f for f in os.listdir(folder_path) if f.endswith(".svg")]

print("Starting script...")

# Clear all existing objects
print("Clearing existing objects...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set initial vertical offset
vertical_offset = 0

# Loop through all SVG files in the folder
for svg_file in svg_files:
    svg_path = os.path.join(folder_path, svg_file)
    print(f"Importing SVG file from {svg_path}...")
    
    # Import the SVG
    bpy.ops.import_curve.svg(filepath=svg_path)
    
    # Get the collection associated with the imported SVG
    collection_name = svg_file
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

        # Move the object vertically by the vertical_offset
        print(f"Moving the object vertically by {vertical_offset} units...")
        bpy.ops.transform.translate(value=(0, 0, vertical_offset))

        # Switch to Edit Mode
        print("Switching to Edit Mode...")
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all vertices in Edit Mode
        print("Selecting all vertices in Edit Mode...")
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude and move upwards by 24.5 units
        print("Extruding and moving upwards by 24.5 units...")
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 24.5)})

        # Switch back to Object Mode
        print("Switching back to Object Mode...")
        bpy.ops.object.mode_set(mode='OBJECT')

        # Update the vertical offset for the next SVG
        vertical_offset += 3.5

    else:
        print(f"Collection '{collection_name}' not found.")

# Save the result
output_path = "/Blender Output/output_file.blend"
print(f"Saving the Blender file to {output_path}...")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("Script finished.")