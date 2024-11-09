# DEMO

This project provides tools for converting 2D SVG floor maps into a 3D model and viewing it in a browser-based interface. The following scripts are included:

## Scripts

- **filter.py**  
  A helper script that preprocesses the 2D SVG floor maps by filtering files based on user selections in the interface.

- **get_stroke_widths.py**  
  Assists in filtering and preprocessing by extracting the widths of the strokes used in the 2D floor maps.

- **multi_2d_to_3d.py**  
  Combines multiple 2D floor maps (e.g., maps for floors 1–7) to generate a 3D model.

- **web_app.py**  
  Launches a Streamlit application for running the demo. This interface allows you to upload a directory containing 2D SVG floor maps. Once processing is complete, Blender will open with the generated 3D model, saved as `output.blend`, which can be exported as a GLB file for viewing in `display_3d_model.py`.

- **display_3d_model.py**  
  A Streamlit application for viewing the 3D model in a browser. This requires uploading the GLB file generated from `web_app.py`.

## Demo Videos

[Voice over Video](https://drive.google.com/file/d/1t6s4Di1beESPZgIF-SyoPk5uiOd2E-hh/view?usp=sharing)

[Watch Demo Videos](https://drive.google.com/file/d/18aUhQWOFmRV8kD4NR1utztUxzUA4NuKR/view?usp=share_link)

## Requirements

- Blender
- Various Python libraries
- Terminal access

## How to Run the Demo

### web_app.py

1. **Configure Blender Path**  
   Open `web_app.py`. Import dependencies and confirm Blender is installed. Update the `run_blender_script` function with your Blender path:
   ```python
   "/Applications/Blender.app/Contents/MacOS/Blender"  # Update this to your Blender executable location
