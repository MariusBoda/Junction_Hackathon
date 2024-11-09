import os
import subprocess
import json
import scripts.lit as st
from get_stroke_widths import get_stroke_widths
from filter import process_all_svgs_in_folder

# Function to get floor height
def get_floor_height(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    
    if len(json_files) != 1:
        raise ValueError(f"Expected one JSON file, but found {len(json_files)}.")
    
    json_path = os.path.join(folder_path, json_files[0])
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    floor_height = data["Elevators"][0]["Floor_to_floor_height_mm"]
    if floor_height is None:
        raise ValueError(f"'Floor_to_floor_height_mm' not found in {json_files[0]}")
    
    return floor_height / 1000  # Convert mm to meters

# Function to process SVGs
def process_svgs(input_dir, output_dir, target_stroke_widths):
    os.makedirs(output_dir, exist_ok=True)
    process_all_svgs_in_folder(input_dir, output_folder=output_dir, target_stroke_widths=target_stroke_widths)

# Function to run Blender script
def run_blender_script(input_dir, output_file, output_dir, height, elevator_3d_dir):
    blender_command = [
        "/Applications/Blender.app/Contents/MacOS/Blender",  # Blender executable
        "--background",  # Run Blender in the background
        "--python", "/Users/marius/Documents/GitHub/Junction_Hackathon/scripts/multi_2d_to_3d.py",  # Path to Blender script
        "--",  # Separator for arguments to the script
        "--folder_path", output_dir,
        "--output_path", output_file,
        "--height", str(height),
        "--elevator_3d_dir", elevator_3d_dir  # New argument for the elevator and shaft directory
    ]
    try:
        subprocess.run(blender_command, check=True)
        blender_open_command = [
            "/Applications/Blender.app/Contents/MacOS/Blender", 
            output_file
        ]
        subprocess.run(blender_open_command, check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error running Blender script: {e}")
        return False
    return True

# Streamlit app UI
st.title("SVG to Blender Converter")
st.write("Choose the directory with SVG files, select stroke widths, and run the conversion to Blender.")

# Directory selection for SVG files
input_dir = st.text_input("Enter directory path for SVG files", "/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 2/svg_output")

# Directory selection for Elevator and Shaft 3D Models
elevator_3d_dir = st.text_input("Enter directory path for Elevator and Shaft 3D models (GLTF)", "/path/to/elevator_and_shaft")

# Button to trigger stroke width extraction
if st.button("Apply"):
    if not input_dir or not os.path.isdir(input_dir):
        st.error("Please provide a valid directory path for SVG files.")
    elif not elevator_3d_dir or not os.path.isdir(elevator_3d_dir):
        st.error("Please provide a valid directory path for Elevator and Shaft 3D models.")
    else:
        # Get the stroke widths for the selected SVG folder
        try:
            widths = get_stroke_widths(input_dir)
            # Store the widths in session state
            st.session_state.widths = widths
            st.success(f"Stroke widths found: {', '.join(widths)}")
        except Exception as e:
            st.error(f"Error extracting stroke widths: {e}")

# Show width selection only after "Apply" is clicked and stroke widths are extracted
if 'widths' in st.session_state:
    # Stroke width selection (simple multiple choice)
    stroke_widths = st.multiselect("Select stroke widths to include", st.session_state.widths, default=st.session_state.widths)

    # Process button
    if st.button("Process SVGs"):
        # Get floor height from the directory (assuming one JSON file exists in the directory)
        try:
            height = get_floor_height(os.path.dirname(input_dir))
        except Exception as e:
            st.error(f"Error getting floor height: {e}")
            height = None

        if height:
            output_dir = os.path.join(input_dir, "processed_svgs")
            process_svgs(input_dir, output_dir, stroke_widths)

            # Set output file path for Blender
            os.makedirs(input_dir + "/blender_output", exist_ok= True)
            output_file = input_dir + "/blender_output" + "/output.blend"

            # Run the Blender script with the elevator and shaft 3D models
            if run_blender_script(input_dir, output_file, output_dir, height, elevator_3d_dir):
                st.success("Blender file generated successfully! Opening Blender...")
            else:
                st.error("Blender file generation failed.")

# Reset button to clear selections
if st.button("Reset Selections"):
    st.session_state.clear()  # Clears all session state variables (including selected widths)
    st.experimental_rerun()  # Reload the app to reset state