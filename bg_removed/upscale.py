import os
from PIL import Image

def crop_image(image_path, output_path):
    with Image.open(image_path) as im:
        width, height = im.size
        left = width * 0.1
        top = height * 0.1
        right = width * 0.9
        bottom = height * 0.9
        im = im.crop((left, top, right, bottom))
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        im.save(output_path)

# Create a subdirectory named "originals" if it does not already exist
os.makedirs("originals", exist_ok=True)

# Get a list of all image files in the current working directory that do not have the suffix "_upscaled_cropped" in their filenames
image_files = [f for f in os.listdir() if f.endswith((".jpg", ".jpeg", ".png")) and not f.endswith("_upscaled_cropped.png")]

# Iterate over the image files, upscale them, crop them, and move the originals to the "originals" subdirectory
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
    upscaled_image_path = f"{os.path.splitext(image_file)[0]}_upscaled.png"
    upscaled_img.save(upscaled_image_path)
    
    # Crop the upscaled image using the crop_image function and save it with an additional suffix "_cropped" added to its filename
    cropped_image_path = f"{os.path.splitext(image_file)[0]}_upscaled_cropped.png"
    crop_image(upscaled_image_path, cropped_image_path)
    
    # Move the original image file to the "originals" subdirectory
    os.rename(image_file, os.path.join("originals", image_file))
