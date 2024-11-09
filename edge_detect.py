import cv2
import numpy as np
from svgpathtools import svg2paths, Path, Line
from svgpathtools import wsvg

# Step 1: Load and parse the SVG file to extract the paths
paths, attributes = svg2paths('/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 1/svg_output_filtered/floor_2_filtered.svg')

# Set image dimensions (change these values based on your SVG size)
image_width, image_height = 1000, 1000

# Create a blank white image (binary, 255 = white, 0 = black)
image = np.ones((image_height, image_width), dtype=np.uint8) * 255  # white background

# Step 2: Convert SVG paths to a binary image (black lines on white background)
for path in paths:
    for segment in path:
        if isinstance(segment, Line):  # Process only line segments
            start = (int(segment.start.real), int(segment.start.imag))
            end = (int(segment.end.real), int(segment.end.imag))
            cv2.line(image, start, end, (0), 1)  # Draw black line (0) on white (255)

# Optional: Save the binary image for reference
cv2.imwrite("floor_plan_binary.png", image)

# Step 3: Apply edge detection (Canny edge detection)
edges = cv2.Canny(image, threshold1=50, threshold2=150)

# Optional: Save the edge-detected image
cv2.imwrite("edges_floor_plan.png", edges)

# Optional: Display the edges
cv2.imshow("Detected Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 4: Post-process the edges (e.g., dilation to make edges thicker)
kernel = np.ones((3, 3), np.uint8)  # Define a kernel for dilation
edges_dilated = cv2.dilate(edges, kernel, iterations=1)  # Dilate edges

# Optional: Save the dilated edges
cv2.imwrite("dilated_edges_floor_plan.png", edges_dilated)

# Optional: Display the dilated edges
cv2.imshow("Dilated Edges", edges_dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 5: Extract contours from the dilated edges
contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 6: Rebuild the SVG with simplified edges from the contours
simplified_paths = []
for contour in contours:
    path = Path()
    for i in range(len(contour) - 1):
        # Convert contour points to Path segments (lines between consecutive points)
        start_point = complex(contour[i][0][0], contour[i][0][1])
        end_point = complex(contour[i + 1][0][0], contour[i + 1][0][1])
        path.append(Line(start_point, end_point))  # Add a line segment to the path
    simplified_paths.append(path)

# Step 7: Save the simplified floor plan as a new SVG file
wsvg(simplified_paths, filename="simplified_floor_plan.svg")

print("Edge detection and simplification complete. The result is saved as 'simplified_floor_plan.svg'.")