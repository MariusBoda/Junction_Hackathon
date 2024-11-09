import bpy
import os
import re
import argparse

# Argument parsing function
def parse_args():
    parser = argparse.ArgumentParser(description="Convert 2D SVGs to 3D in Blender")
    parser.add_argument('--folder_path', type=str, required=True, help='Path to the folder containing SVG files')
    parser.add_argument('--output_path', type=str, required=True, help='Path to save the output .blend file')
    return parser.parse_args()

# Parse the arguments from the command line
args = parse_args()
folder_path = args.folder_path
output_path = args.output_path

# List and sort SVG files
svg_files = [f for f in os.listdir(folder_path) if f.endswith(".svg")]

def extract_priority(filename):
    if filename == "kellari_filtered_paths.svg":
        return -1  # Assign high priority to 'kellari' file
    match = re.search(r'\d+', filename)
    return int(match.group(0)) if match else float('inf')

svg_files.sort(key=extract_priority)

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
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select all path objects in the collection
        print("Selecting all curve objects in the collection...")
        for obj in collection.objects:
            if obj.type == 'CURVE':
                obj.select_set(True)
        
        # Set the first selected object as active
        bpy.context.view_layer.objects.active = collection.objects[0]
        
        # Join all selected objects into one
        bpy.ops.object.join()

        # Convert to mesh
        bpy.ops.object.convert(target='MESH')

        # Scale the mesh
        scale_factor = 100
        bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

        # Move the object vertically
        bpy.ops.transform.translate(value=(0, 0, vertical_offset))

        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude and move upwards
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 3.5)})

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Update vertical offset
        vertical_offset += 3.5

    else:
        print(f"Collection '{collection_name}' not found.")

# Save the result
print(f"Saving the Blender file to {output_path}...")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("Script finished.")