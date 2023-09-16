# remove_bg

This repository contains Python scripts for image manipulation and background removal, designed to simplify the process of preparing images for various applications.

## bg_remove.py

The `bg_remove.py` script is focused on background removal from images. Key features include:

- Utilizes the remove.bg API for automatic background removal.
- Handles rate limits and VIP queue for processing large image volumes.
- Resizes images to optimal dimensions to improve processing speed.
- Converts images to a transparent background format.

## upscale.py

The `upscale.py` script deals with upscaling and cropping images. It offers the following functionalities:

- Upscales images by a factor of 2 while preserving transparency.
- Crops images to remove borders and empty spaces.
- Renames and organizes images into subdirectories.

## webptopng.py

The `webptopng.py` script is focused on converting WebP images to PNG format. It performs the following tasks:

- Converts WebP images to PNG format while retaining transparency.
- Organizes converted images into a dedicated subdirectory.

## Getting Started

To use these scripts:

1. Make sure you have Python installed.
2. Install the required dependencies mentioned in the scripts if necessary.
3. [Set API keys](https://www.remove.bg/dashboard#api-key) and customize script parameters as needed.
4. Run the desired script from the repository.



https://github.com/TheLime1/remove-bg/assets/47940043/b8c69509-729d-4c6d-9998-061982a77055


