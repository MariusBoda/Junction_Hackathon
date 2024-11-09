import cv2
import numpy as np
from pdf2image import convert_from_path

# Step 1: Convert PDF to image (you can choose the first page or all pages)
pdf_path = '/Users/marius/Documents/GitHub/Junction_Hackathon/Material to share/Site 1/floor_1.pdf'
images = convert_from_path(pdf_path)

# Choose the first page (or you can loop over all pages)
image = np.array(images[0])

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Step 2: Threshold the image to highlight the outlines (binary image)
_, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

# Step 3: Apply Gaussian Blur to smooth the image and reduce noise
blurred_image = cv2.GaussianBlur(binary_image, (5, 5), 0)

# Step 4: Use Canny Edge Detection for finer edge details
edges = cv2.Canny(blurred_image, 50, 150)

# Step 5: Apply dilation to thicken edges
kernel = np.ones((5, 5), np.uint8)
dilated_image = cv2.dilate(edges, kernel, iterations=2)

# Step 6: Find contours
contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 7: Filter the contours based on area (ignore small artifacts)
min_area = 500  # Adjust this based on the size of the building outline
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

# Step 8: Find the convex hull to get the outermost boundary (optional, depending on floor plan structure)
hulls = [cv2.convexHull(cnt) for cnt in filtered_contours]

# Step 9: Draw the contours on the image
contour_image = np.ones_like(image) * 255  # Blank white image for contours
cv2.drawContours(contour_image, hulls, -1, (0, 0, 0), 2)  # Draw black contours on white background

# Step 10: Save and display the result
cv2.imwrite("building_outline.png", contour_image)
cv2.imshow("Building Outline", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()