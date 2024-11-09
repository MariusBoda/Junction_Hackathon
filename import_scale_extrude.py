import bpy
import os
import re

# Path to the folder containing the SVG files
svg_folder_path = "/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 1/svg_output_filtered"

# Parameters
scale_factor = 100  # Scale factor for the meshes
extrude_amount = 3.5  # Extrude amount for each floor

# Clear all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Initial Z offset to place the first floor at Z=0
z_offset = 0

# Get all SVG files in the folder
svg_files = [f for f in os.listdir(svg_folder_path) if f.endswith(".svg")]

# Sort the files numerically based on the number in the filename
svg_files.sort(key=lambda f: int(re.search(r'(\d+)', f).group()))

# Loop over each SVG file
for index, svg_file in enumerate(svg_files):
    print(f"Processing file {index + 1}/{len(svg_files)}: {svg_file}")
    
    svg_path = os.path.join(svg_folder_path, svg_file)
    
    # Clear all existing objects before each import
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Import SVG
    bpy.ops.import_curve.svg(filepath=svg_path)

    # Get the imported collection (assuming the collection is named after the SVG file)
    collection_name = os.path.splitext(svg_file)[0]
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

        # Scale the mesh object by the scale factor
        bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all vertices in Edit Mode
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude and move upwards by extrude_amount
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, extrude_amount)})

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Adjust the Z location of the object to stack it above the previous floor
        bpy.context.active_object.location.z = z_offset

        # Update the Z offset for the next floor
        z_offset += extrude_amount

    # Save the result incrementally after processing each floor
    output_path = f"/Users/marius/Documents/GitHub/Junction_Hackathon/Blender Output/output_batch_{index + 1}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    
    # Print progress
    print(f"Saved: {output_path}")

# Final save
final_output_path = "/Users/marius/Documents/GitHub/Junction_Hackathon/Blender Output/final_output_file.blend"
bpy.ops.wm.save_as_mainfile(filepath=final_output_path)
print(f"Final output saved as: {final_output_path}")

#/Applications/Blender.app/Contents/MacOS/Blender --background --python /Users/marius/Documents/GitHub/Junction_Hackathon/import_scale_extrude.py