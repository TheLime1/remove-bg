import os
from PIL import Image
import requests

# Set your API key here
api_key = 'UefwKbdgLakSUj52rVhkZj4w'

# Set the maximum supported resolution (in megapixels)
max_resolution = 50

# Create the subfolder if it doesn't exist
if not os.path.exists('bg_removed'):
    os.makedirs('bg_removed')

# Get a list of all image files in the current folder
image_files = [f for f in os.listdir() if f.endswith(('.jpg', '.jpeg', '.png'))]

# Process each image file
for image_file in image_files:
    # Open the image using Pillow
    with Image.open(image_file) as img:
        # Calculate the current resolution (in megapixels)
        current_resolution = (img.width * img.height) / 1_000_000

        # Check if the current resolution is larger than the maximum supported resolution
        if current_resolution > max_resolution:
            # Calculate the scale factor to resize the image
            scale_factor = (max_resolution / current_resolution) ** 0.5

            # Calculate the new size of the image
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))

            # Resize the image
            img = img.resize(new_size)

        # Save the resized image to a temporary file
        with open('temp.jpg', 'wb') as temp:
            img.save(temp, format='JPEG')

    # Send the temporary file to the remove.bg API
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open('temp.jpg', 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key},
    )
    if response.status_code == requests.codes.ok:
        # Save the processed image to the subfolder
        with open(os.path.join('bg_removed', image_file), 'wb') as out:
            out.write(response.content)
    else:
        print(f"Error processing {image_file}: {response.status_code} {response.text}")

# Delete the temporary file
os.remove('temp.jpg')
