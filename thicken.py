import chardet
import xml.etree.ElementTree as ET

def clean_svg_file(svg_file):
    """Clean the SVG file to remove problematic characters."""
    # Read the SVG file in binary mode to avoid encoding issues
    with open(svg_file, 'rb') as file:
        raw_content = file.read()

    # Use chardet to detect the file encoding
    detected_encoding = chardet.detect(raw_content)['encoding']
    print(f"Detected encoding: {detected_encoding}")

    # Decode the raw bytes to a string using the detected encoding
    content = raw_content.decode(detected_encoding)

    # Replace problematic characters or any non-XML-safe content
    content = content.replace('ä', 'a').replace('ö', 'o').replace('å', 'a')  # Example replacements

    # Optionally, use regex to remove anything that might break XML parsing
    # content = re.sub(r'[^a-zA-Z0-9\s<>\-"/]', '', content)  # Remove non-XML-safe characters

    # Write the cleaned content back to a temporary file
    cleaned_file = svg_file.replace('.svg', '_cleaned.svg')
    with open(cleaned_file, 'w', encoding='utf-8') as file:
        file.write(content)

    return cleaned_file

def remove_text_and_thicken_paths(svg_file, multiplier):
    # Clean the SVG file first
    cleaned_svg_file = clean_svg_file(svg_file)

    # Parse the cleaned SVG file
    tree = ET.parse(cleaned_svg_file)
    root = tree.getroot()

    # Remove all text nodes
    for elem in root.iter():
        if elem.tag == '{http://www.w3.org/2000/svg}text' or elem.tag == '{http://www.w3.org/2000/svg}tspan':
            root.remove(elem)

    # Find all <path> elements
    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        # Get current stroke width (if exists) and convert to float
        stroke_width = path.attrib.get('stroke-width', None)
        if stroke_width:
            try:
                stroke_width = float(stroke_width)
                # Multiply the stroke width by the multiplier
                path.attrib['stroke-width'] = str(stroke_width * multiplier)
            except ValueError:
                pass  # Ignore if stroke-width is not a valid number

    # Save the modified SVG back to a file
    tree.write('thickened_floor_plan_no_text.svg')

# Example usage
remove_text_and_thicken_paths('Material to share/Site 1/svg_output/floor_1.svg', 1.5)