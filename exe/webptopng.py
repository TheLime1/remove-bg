import os
from PIL import Image

# Create the 'webp_to_png' directory if it doesn't exist
if not os.path.exists('webp_to_png'):
    os.makedirs('webp_to_png')

# Iterate over all files in the current directory
for filename in os.listdir('.'):
    # Check if the file is a .webp image
    if filename.endswith('.webp'):
        # Open the image using PIL
        image = Image.open(filename)
        # Convert the image to RGBA mode (to support transparency)
        image = image.convert('RGBA')
        # Save the image as a .png file in the 'webp_to_png' directory
        new_filename = os.path.join('webp_to_png', os.path.splitext(filename)[0] + '.png')
        image.save(new_filename)
