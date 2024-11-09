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

Step 1: To run the demo please open the web_app.py file. Import all dependencies and requirements. Please have Blender downloaded on your computer. In the web_app.py file please enter the path location to your Blender download on your computer in the <run_blender_script> function! Replace this line: "/Applications/Blender.app/Contents/MacOS/Blender",  # Blender executable with your Blender file location inside the quotations. 

Step 2: Open the terminal. Run the following command: streamlit run <FILE LOCATION OF web_app.py file>. This should open up the streamlit application in your browser. 

Step 3: Follow the directions in the streamlit application in the browser. The first entry should be for the directory path for the 2D svg files, for example: </Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 1/svg_output> 

Step 4: Add the elevator files. These can be found in the Material to share folder under the respective site folders!

Step 5: Press Apply. Then options for chosing stroke width will appear. You can play around with the different options to see what works best, but for demo purposes if you are testing Site 1 please choose 0.3 and 1. For Site 2 please choose 0.25. 

Step 6: Press Process SVGs. This will start running in the background and may take up to a minute. After it is finished it will open Blender automatically on your computer and show the generated 3D model along with the elevator and shaft. 

-- display_3d_model.py -- 

Step 1: Install and import all dependencies. 

Step 2: Run the web_app.py DEMO to generate a output.blend file. This file contains the generated 3D model from the 2D floor plans. Once the web_app.py application opens the Blender window with the generated 3D model, please export the file as GLB format. If you would like to run the display_3d_model.py demo without generating the model yourself, please use the site_1.glb file in the DEMO folder.

Step 3: Open the Terminal. Run the following command: streamlit run <FILE LOCATION to display_3d_model.py>. For example run streamlit run DEMO/display_3d_model.py

Step 4: This should open the browser application. Once in the app please upload the .GLB file from step 2. It should then open the 3D model visualization in the web based browser! This allows for simple and browser based 3D modeling.

