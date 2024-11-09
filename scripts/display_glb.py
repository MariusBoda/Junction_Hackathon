import streamlit as st
import tempfile
import base64

st.title("3D Model Viewer using Model Viewer")

# Upload the GLB file
uploaded_file = st.file_uploader("Upload a GLB file", type="glb")

# If a file is uploaded, use it; otherwise, use a default model URL
if uploaded_file:
    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".glb") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_filepath = tmp_file.name

    # Convert the file to a base64 data URL for use in model-viewer
    with open(tmp_filepath, "rb") as f:
        glb_data = f.read()
    glb_base64 = base64.b64encode(glb_data).decode("utf-8")
    model_url = f"data:model/gltf-binary;base64,{glb_base64}"
else:
    # Default model URL if no file is uploaded
    model_url = ""

# HTML template using <model-viewer> with model URL
html_code = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
    </head>
    <body>
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
            <model-viewer src="{model_url}" alt="3D model" camera-controls auto-rotate style="width: 1000px; height: 700px;"></model-viewer>
        </div>
    </body>
</html>
"""

# Render the HTML in Streamlit
st.components.v1.html(html_code, height=800)