import os
import re
from lxml import etree

# Load the SVG file and filter paths based on stroke widths
def filter_paths_by_stroke_width(filename, target_stroke_widths, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open and read the SVG file
    with open(filename, "rb") as file:
        content = file.read().decode("ISO-8859-1")

    # Remove the encoding declaration if it exists
    content = content.replace('<?xml version="1.0" encoding="ISO-8859-1"?>', '')

    # Parse from the string content without encoding declaration
    tree = etree.fromstring(content.encode("utf-8"))

    # Define namespaces for proper XML parsing (SVG and Inkscape)
    namespace = {
        "svg": "http://www.w3.org/2000/svg",
        "inkscape": "http://www.inkscape.org/namespaces/inkscape"
    }

    # Regular expression to extract stroke-width from the style attribute
    stroke_width_pattern = re.compile(r"stroke-width\s*:\s*([^;]+)")

    # Create the new SVG root element with the same namespace
    new_tree = etree.Element("svg", nsmap={"svg": "http://www.w3.org/2000/svg"})

    # Copy the original <svg> root attributes (e.g., width, height, viewBox)
    for attrib, value in tree.attrib.items():
        if attrib not in ["xmlns", "xmlns:svg", "xmlns:inkscape"]:  # Exclude xmlns attributes
            new_tree.set(attrib, value)

    # Copy the original <defs> section if it exists
    defs = tree.find(".//svg:defs", namespaces=namespace)
    if defs is not None:
        new_defs = etree.SubElement(new_tree, "defs", nsmap={"svg": "http://www.w3.org/2000/svg"})
        for elem in defs:
            new_defs.append(elem)

    # Initialize counters for debugging
    total_paths = 0
    matched_paths = 0

    # Iterate through all groups (<g>) in the original SVG to preserve layers
    for group in tree.xpath("//svg:g", namespaces=namespace):
        # Create a corresponding group in the new SVG tree
        new_group = etree.SubElement(new_tree, "g", nsmap={"svg": "http://www.w3.org/2000/svg"})
        
        # Copy attributes of the group (like `id`, `style`, etc.)
        for attrib, value in group.attrib.items():
            new_group.set(attrib, value)

        # Find all paths inside the group (<g>)
        for path in group.xpath(".//svg:path", namespaces=namespace):
            total_paths += 1  # Count total paths
            style = path.get("style")
            if style:
                # Search for the stroke-width in the style attribute
                match = stroke_width_pattern.search(style)
                if match:
                    stroke_width = match.group(1)
                    # If the stroke-width matches, keep the path
                    if stroke_width in target_stroke_widths:
                        new_group.append(path)
                        matched_paths += 1  # Count matched paths

    # Debug output: Print how many paths were found and matched
    print(f"Total paths found: {total_paths}")
    print(f"Paths matching stroke widths {target_stroke_widths}: {matched_paths}")

    # Generate the new SVG content with filtered paths
    new_svg_content = etree.tostring(new_tree, pretty_print=True, xml_declaration=True, encoding="utf-8")

    # Save the new SVG with the filtered paths to the specified output folder
    output_filename = os.path.join(output_folder, os.path.basename(filename).replace(".svg", "_filtered_paths.svg"))
    with open(output_filename, "wb") as f:
        f.write(new_svg_content)

    print(f"Filtered paths with stroke widths {target_stroke_widths} have been saved to '{output_filename}'.")

# Process all SVG files in the "Site 1" folder and save them to "fully filtered svgs" folder
def process_all_svgs_in_folder(folder_path, target_stroke_widths, output_folder):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".svg"):  # Only process SVG files
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            filter_paths_by_stroke_width(file_path, target_stroke_widths, output_folder)

# Example Usage: process all SVG files in the "Site X" folder and save to "fully filtered svgs" folder
#folder_path = 'Material to share/Site 2/svg_output'  # Replace with your folder path
#output_folder = 'Material to share/Site 2/fully filtered svgs'  # New output folder path
#target_stroke_widths = ['0.18', '0.13']  # Example stroke widths to filter by
#process_all_svgs_in_folder(folder_path, target_stroke_widths, output_folder)