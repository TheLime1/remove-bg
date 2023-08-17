import os
from super_image import EdsrModel, ImageLoader
from PIL import Image

# Create an EdsrModel object
model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)

# Get a list of all image files in the current working directory
image_files = [f for f in os.listdir() if f.endswith((".jpg", ".jpeg", ".png"))]

# Iterate over the image files and upscale them
for image_file in image_files:
    # Load the image
    img = Image.open(image_file)
    
    # Prepare the inputs
    inputs = ImageLoader.load_image(img)
    
    # Upscale the image
    preds = model(inputs)
    
    # Save the upscaled image
    ImageLoader.save_image(preds, f"upscaled_{image_file}")
