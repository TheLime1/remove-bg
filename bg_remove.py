import os
from PIL import Image
import requests
import time
import json

# Set your API key here
api_key = 'UefwKbdgLakSUj52rVhkZj4w'

# Set the maximum supported resolution (in megapixels)
max_resolution = 50

# Set the rate limit (in megapixels per minute)
rate_limit = 500

# Create the subfolder if it doesn't exist
if not os.path.exists('bg_removed'):
    os.makedirs('bg_removed')

# Get a list of all image files in the current folder that do not end with "_bgr"
image_files = [f for f in os.listdir() if f.endswith(('.jpg', '.jpeg', '.png')) and not f.endswith('_bgr.jpg') and not f.endswith('_bgr.jpeg') and not f.endswith('_bgr.png')]

# Initialize the rate limit counter
rate_limit_counter = 0

# Initialize the VIP queue
vip_queue = []

# Process each image file
while image_files or vip_queue:
    # Check if there are any VIP images in the queue
    if vip_queue:
        # Get the next VIP image from the queue
        image_file = vip_queue.pop(0)
    else:
        # Get the next image file from the list
        image_file = image_files.pop(0)

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

    # Check if we have exceeded the rate limit
    if rate_limit_counter + current_resolution > rate_limit:
        # Wait for 61 seconds before continuing
        time.sleep(61)

        # Reset the rate limit counter
        rate_limit_counter = 0

    # Send the temporary file to the remove.bg API
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open('temp.jpg', 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key},
    )
    if response.status_code == requests.codes.ok:
        # Save the processed image to the subfolder with '_bgr' added to its name
        filename, file_extension = os.path.splitext(image_file)
        with open(os.path.join('bg_removed', filename + '_bgr' + file_extension), 'wb') as out:
            out.write(response.content)

        # Rename the original image by adding '_bgr' to its name
        os.rename(image_file, filename + '_bgr' + file_extension)
        
        print(f"Successfully processed {image_file}.")
    else:
        error_data = json.loads(response.text)
        error_code = error_data['errors'][0]['code']
        
        if error_code == 'rate_limit_exceeded':
            print(f"Rate limit exceeded for {image_file}. Sleeping for 61 seconds and adding it back to queue as a VIP image.")
            
            # Remove '_bgr' from original image name if it exists
            filename, file_extension = os.path.splitext(image_file)
            if filename.endswith('_bgr'):
                new_filename = filename[:-4]
                os.rename(image_file, new_filename + file_extension)
                image_file = new_filename + file_extension
            
            # Sleep for 61 seconds before continuing
            time.sleep(61)

            # Add it back to queue as a VIP image at first position 
            vip_queue.insert(0, image_file)
            
            # Reset rate limit counter 
            rate_limit_counter = 0
            
        else:
            print(f"Error processing {image_file}: {response.status_code} {response.text}")

    # Increment the rate limit counter by the current resolution
    rate_limit_counter += current_resolution

# Delete the temporary file
os.remove('temp.jpg')