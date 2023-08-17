import os
from removebg import RemoveBg

# Your Remove.bg API key
rmbg = RemoveBg("UefwKbdgLakSUj52rVhkZj4w", "error.log")

# Path of the folder containing the script
folder_path = os.path.dirname(os.path.abspath(__file__))

def process_images():
    # Get a list of files in the specified folder
    files = os.listdir(folder_path)

    for file_name in files:
        # Check if the file is an image by checking its extension
        if file_name.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_name}")

            # Remove the background from the image
            rmbg.remove_background_from_img_file(file_path)

            # Save the processed image to the same folder as the script
            upload_file_path = os.path.join(folder_path, f"processed_{file_name}")
            os.rename(f"{file_path}_no_bg.png", upload_file_path)


# Process all images in the specified folder
process_images()
