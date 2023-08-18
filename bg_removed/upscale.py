import os
from PIL import Image

# Create a subdirectory named "originals" if it does not already exist
os.makedirs("originals", exist_ok=True)

# Get a list of all image files in the current working directory that do not have the suffix "_upscaled" in their filenames
image_files = [f for f in os.listdir() if f.endswith((".jpg", ".jpeg", ".png")) and not f.endswith("_upscaled.png")]

# Iterate over the image files, upscale them, and move the originals to the "originals" subdirectory
for image_file in image_files:
    # Open the image file
    img = Image.open(image_file)
    
    # Get the size of the image
    width, height = img.size
    
    # Calculate the new size of the image
    new_width = width * 2
    new_height = height * 2
    
    # Upscale the image while preserving its transparency
    upscaled_img = img.resize((new_width, new_height), resample=Image.LANCZOS)
    
    # Save the upscaled image with the suffix "_upscaled" added to its filename and with the ".png" extension
    upscaled_img.save(f"{os.path.splitext(image_file)[0]}_upscaled.png")
    
    # Move the original image file to the "originals" subdirectory
    os.rename(image_file, os.path.join("originals", image_file))
