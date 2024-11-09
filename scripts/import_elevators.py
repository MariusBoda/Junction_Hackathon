import bpy
import os
import sys

# Argument parsing function to pass file path for the elevator model
def parse_args():
    args = sys.argv[sys.argv.index("--") + 1:]  # Arguments after '--'
    
    elevator_file = None  # Path to the elevator 3D model
    
    for i in range(len(args)):
        if args[i] == "--elevator_3d_file":
            elevator_file = args[i + 1]
    
    if not elevator_file:
        raise ValueError("The --elevator_3d_file argument is required.")
    
    return elevator_file

# Parse the arguments from the command line
elevator_file = parse_args()

# Function to load and place the elevator model
def load_elevator(elevator_file):
    # Check if the elevator file exists
    if os.path.exists(elevator_file):
        print(f"Loading elevator model from {elevator_file}...")
        
        # Import the elevator model (assuming it's in .gltf format)
        bpy.ops.import_scene.gltf(filepath=elevator_file)
        
        # After import, position the elevator at (0, 0, 0)
        if bpy.context.selected_objects:
            elevator_object = bpy.context.selected_objects[-1]  # Get the last selected object (assumed to be the elevator)
            print(f"Elevator imported: {elevator_object.name}")
            elevator_object.location = (0, 0, 0)  # Position at (0, 0, 0)
            
            # Optionally convert the imported model to a curve
            bpy.ops.object.convert(target='CURVE')
        else:
            print(f"Failed to import elevator from {elevator_file}")
    else:
        print(f"Elevator model not found at {elevator_file}.")

# Call the function to load the elevator
load_elevator(elevator_file)

print("Elevator import script finished.")