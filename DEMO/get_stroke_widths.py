import re
import os
from lxml import etree

def get_stroke_widths(directory):
    # Set to store unique stroke widths from all files in the directory
    stroke_widths = set()

    # Namespace handling for SVG and Inkscape
    namespace = {
        "svg": "http://www.w3.org/2000/svg",
        "inkscape": "http://www.inkscape.org/namespaces/inkscape"
    }

    # Regular expression to extract stroke-width from style
    stroke_width_pattern = re.compile(r"stroke-width\s*:\s*([^;]+)")

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".svg"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "rb") as file:
                content = file.read().decode("ISO-8859-1")
                
            # Remove the encoding declaration if it exists
            content = content.replace('<?xml version="1.0" encoding="ISO-8859-1"?>', '')

            # Parse from the string content without encoding declaration
            tree = etree.fromstring(content.encode("utf-8"))

            # Find all path elements
            paths = tree.xpath("//svg:path", namespaces=namespace)

            # Iterate over each path element and extract stroke-width from the style attribute
            for path in paths:
                style = path.get("style")
                if style:
                    # Search for the stroke-width in the style attribute
                    match = stroke_width_pattern.search(style)
                    if match:
                        stroke_width = match.group(1)
                        stroke_widths.add(stroke_width)

    # Output the unique stroke widths found in all SVG files
    print("Unique Stroke Widths:")
    for stroke_width in stroke_widths:
        print(stroke_width)

    return stroke_widths

# Usage example
# get_stroke_widths('path/to/your/directory')