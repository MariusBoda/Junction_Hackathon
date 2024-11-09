import bpy
import os
import re
import argparse
import sys

# Argument parsing function
def parse_args():
    # sys.argv[0] is the Blender executable path, so skip it and get the real arguments
    args = sys.argv[sys.argv.index("--") + 1:]  # Arguments after '--'
    
    folder_path = None
    output_path = None
    height = 0
    elevator_file = None  # New argument for the elevator 3D model
    shaft_file = None  # New argument for the shaft 3D model
    
    # Loop over arguments and extract the folder_path, output_path, elevator_file, shaft_file, and height
    for i in range(len(args)):
        if args[i] == "--folder_path":
            folder_path = args[i + 1]
        elif args[i] == "--height":
            height = float(args[i+1])
        elif args[i] == "--output_path":
            output_path = args[i + 1]
        elif args[i] == "--elevator_3d_file":  # New argument for elevator file
            elevator_file = args[i + 1]
        elif args[i] == "--shaft_3d_file":  # New argument for shaft file
            shaft_file = args[i + 1]
    
    if not folder_path or not output_path:
        raise ValueError("Both --folder_path and --output_path are required arguments.")
    
    return folder_path, output_path, height, elevator_file, shaft_file

# Parse the arguments from the command line
folder_path, output_path, height, elevator_file, shaft_file = parse_args()

# Path to the folder containing the SVG files
svg_files = [f for f in os.listdir(folder_path) if f.endswith(".svg")]

# Sort files with special handling for "kellari_filtered_paths.svg" and other cases
def extract_priority(filename):
    if filename == "kellari_filtered_paths.svg":
        return -1  # Assign a high priority to kellari file to make it first in order
    match = re.search(r'\d+', filename)
    return int(match.group(0)) if match else float('inf')  # Sort numbered files next, then unnumbered

# Sort the files, prioritizing kellari, then numbered files, then others
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
        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select all path objects in the collection
        print("Selecting all curve objects in the collection...")
        for obj in collection.objects:
            if obj.type == 'CURVE':  # Ensure we only select the curve objects (paths)
                obj.select_set(True)
        
        # Set the first selected object as active
        print("Setting the first selected object as active...")
        bpy.context.view_layer.objects.active = collection.objects[0]
        
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

        # Extrude and move upwards by height units
        print("Extruding and moving upwards by height units...")
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, height)})

        # Switch back to Object Mode
        print("Switching back to Object Mode...")
        bpy.ops.object.mode_set(mode='OBJECT')

        # Update the vertical offset for the next SVG
        vertical_offset += height

    else:
        print(f"Collection '{collection_name}' not found.")

# Load the elevator and shaft models into Blender
def load_elevator_and_shaft(elevator_file, shaft_file, height):
    # Load the elevator model
    if elevator_file and os.path.exists(elevator_file):
        print(f"Loading elevator model from {elevator_file}...")
        bpy.ops.import_scene.gltf(filepath=elevator_file)
        
        # Select and position the elevator model
        elevator_obj = bpy.context.selected_objects[-1]
        elevator_obj.location = (0, 0, height)  # Adjust Z position to match height
        elevator_obj.name = "Elevator_Model"
        print("Elevator model loaded and positioned.")
        
        # Convert elevator model to .glb
        glb_elevator_path = os.path.splitext(elevator_file)[0] + ".glb"
        bpy.ops.export_scene.gltf(filepath=glb_elevator_path, export_format='GLB')
        print(f"Elevator model exported to .glb at {glb_elevator_path}")
    else:
        print(f"Elevator model not found at {elevator_file}.")

    # Load the shaft model
    if shaft_file and os.path.exists(shaft_file):
        print(f"Loading shaft model from {shaft_file}...")
        bpy.ops.import_scene.gltf(filepath=shaft_file)
        
        # Select and position the shaft model
        shaft_obj = bpy.context.selected_objects[-1]
        shaft_obj.location = (0, 0, 0)  # Adjust Z position as necessary
        shaft_obj.name = "Shaft_Model"
        print("Shaft model loaded and positioned.")
        
        # Convert shaft model to .glb
        glb_shaft_path = os.path.splitext(shaft_file)[0] + ".glb"
        bpy.ops.export_scene.gltf(filepath=glb_shaft_path, export_format='GLB')
        print(f"Shaft model exported to .glb at {glb_shaft_path}")
    else:
        print(f"Shaft model not found at {shaft_file}.")

# In the main part of the script, after processing SVG files:
print("Loading elevator and shaft models...")
load_elevator_and_shaft(elevator_file, shaft_file, height)

# Save the result
print(f"Saving the Blender file to {output_path}...")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("Script finished.")