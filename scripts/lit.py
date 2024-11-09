import os
import subprocess
import json
import tempfile
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

# Streamlit app UI
st.title("SVG to Blender Converter with 3D Viewer")
st.write("Choose the directory with SVG files, select stroke widths, and run the conversion to Blender.")

# Directory selection for SVG files
input_dir = st.text_input("Enter directory path for SVG files", "/path/to/your/svg/folder")

# File upload for Elevator and Shaft 3D models
elevator_gltf = st.file_uploader("Upload Elevator 3D model (GLTF)", type=["glb", "gltf"])
shaft_gltf = st.file_uploader("Upload Shaft 3D model (GLTF)", type=["glb", "gltf"])

# Button to trigger stroke width extraction
if st.button("Apply"):
    if not input_dir or not os.path.isdir(input_dir):
        st.error("Please provide a valid directory path for SVG files.")
    elif elevator_gltf is None or shaft_gltf is None:
        st.error("Please upload both elevator and shaft 3D model files.")
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
            os.makedirs(input_dir + "/blender_output", exist_ok=True)
            output_file = input_dir + "/blender_output" + "/output.blend"

            # Save the uploaded files to temporary locations
            with tempfile.NamedTemporaryFile(delete=False) as temp_elevator_gltf:
                temp_elevator_gltf.write(elevator_gltf.getvalue())
                elevator_temp_gltf_path = temp_elevator_gltf.name

            with tempfile.NamedTemporaryFile(delete=False) as temp_shaft_gltf:
                temp_shaft_gltf.write(shaft_gltf.getvalue())
                shaft_temp_gltf_path = temp_shaft_gltf.name

            # Generate the Three.js HTML code to display the 3D model
            three_js_code = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>3D Model Viewer</title>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/three@0.128/examples/js/loaders/GLTFLoader.js"></script>
            </head>
            <body>
                <script>
                    const scene = new THREE.Scene();
                    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                    const renderer = new THREE.WebGLRenderer();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    document.body.appendChild(renderer.domElement);

                    const loader = new THREE.GLTFLoader();
                    loader.load("{elevator_temp_gltf_path}", (gltf) => {{
                        scene.add(gltf.scene);
                    }}, undefined, (error) => {{
                        console.error('Error loading elevator model:', error);
                    }});

                    loader.load("{shaft_temp_gltf_path}", (gltf) => {{
                        scene.add(gltf.scene);
                    }}, undefined, (error) => {{
                        console.error('Error loading shaft model:', error);
                    }});

                    const ambientLight = new THREE.AmbientLight(0x404040, 2);
                    scene.add(ambientLight);

                    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
                    directionalLight.position.set(1, 1, 1).normalize();
                    scene.add(directionalLight);

                    camera.position.z = 5;

                    function animate() {{
                        requestAnimationFrame(animate);
                        renderer.render(scene, camera);
                    }}
                    animate();
                </script>
            </body>
            </html>
            """

            # Embed the Three.js HTML/JS code in the Streamlit app using the HTML component
            st.components.v1.html(three_js_code, height=600)

# Reset button to clear selections
if st.button("Reset Selections"):
    st.session_state.clear()  # Clears all session state variables (including selected widths)
    st.experimental_rerun()  # Reload the app to reset state