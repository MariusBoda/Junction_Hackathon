import os
import subprocess
from get_stroke_widths import get_stroke_widths
from filter import process_all_svgs_in_folder
import json

# Example paths (you can modify these paths based on your input/output location)
main_dir = "/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 2"
output_file = "/Users/marius/Documents/GitHub/Junction_Hackathon/Blender Output/output_file.blend"


input_dir = main_dir + "/svg_output"
# Get stroke widths
widths = get_stroke_widths(input_dir)

#get floor height
def get_floor_height(folder_path):
    # Find the first JSON file in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    
    if len(json_files) != 1:
        raise ValueError(f"Expected one JSON file, but found {len(json_files)}.")
    
    # Load the JSON file
    json_path = os.path.join(folder_path, json_files[0])
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Extract the "Floor_to_floor_height_mm" value
    floor_height = data["Elevators"][0]["Floor_to_floor_height_mm"]

    if floor_height is None:
        raise ValueError(f"'Floor_to_floor_height_mm' not found in {json_files[0]}")
    
    return floor_height / 1000  # Convert from mm to meters for Blender

height = get_floor_height(main_dir)

# Process SVGs
output_dir = os.path.join(input_dir, "processed_svgs")
os.makedirs(output_dir, exist_ok=True)
process_all_svgs_in_folder(input_dir, output_folder=output_dir, target_stroke_widths=['0.25', '0.35'])

def run_blender_script(input_dir, output_file):
    # Construct the Blender command with the necessary arguments
    blender_command = [
        "/Applications/Blender.app/Contents/MacOS/Blender",  # Blender executable
        "--background",  # Run Blender in the background
        "--python", "/Users/marius/Documents/GitHub/Junction_Hackathon/scripts/multi_2d_to_3d.py",  # Path to the Blender script
        "--",  # Separator for passing arguments to the script
        "--folder_path", output_dir,  # Path to the SVG folder
        "--output_path", output_file,  # Path to save the .blend output file
        "--height", str(height)
    ]

    try:
        print(f"Running Blender command: {' '.join(blender_command)}")
        subprocess.run(blender_command, check=True)
        print("Blender script ran successfully.")

         # Now launch Blender with the output file in the foreground
        blender_open_command = [
            "/Applications/Blender.app/Contents/MacOS/Blender",  # Blender executable
            output_file  # Path to the .blend file
        ]
        
        print(f"Opening Blender with: {' '.join(blender_open_command)}")
        subprocess.run(blender_open_command, check=True)  # Launch Blender with the .blend file
        print("Blender opened successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error running Blender script: {e}")

# Run the Blender script with the specified folder and output file paths
run_blender_script(input_dir, output_file)