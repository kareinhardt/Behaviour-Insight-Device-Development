# dHX Design Team internal testing tools; not for production use.
import os
import sys
import logging
from waveshare_epd import epd4in26  # Ensure this is the correct driver for your 4.26 inch display
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    # Initialize the display
    epd = epd4in26.EPD()
    epd.init()

    # Clear the display
    epd.Clear()

    # Get the current directory (same as the script location)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the 'slideshow' folder
    slideshow_dir = os.path.join(current_dir, "slideshow")

    # Get a list of all png files in the folder, sorted by name
    png_files = sorted([f for f in os.listdir(slideshow_dir) if f.endswith(".png")], key=lambda x: int(x.split('.')[0]))

    if not png_files:
        print("No PNG files found in the 'slideshow' folder.")
        sys.exit(1)

    # Loop through each image file in the folder
    for image_filename in png_files:
        image_path = os.path.join(slideshow_dir, image_filename)

        # Load the image
        image = Image.open(image_path)

        # Resize the image to fit the display
        image = image.resize((epd.width, epd.height), Image.ANTIALIAS)
        
        # Rotate the image 180 degrees
        image = image.rotate(180)

        # Display the image
        epd.display(epd.getbuffer(image))

        # Wait for the user to press "Enter" before displaying the next image
        input(f"Displaying {image_filename}. Press Enter to continue to the next image...")

    # Put the display to sleep after showing all images
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("Ctrl+C detected. Exiting...")
    epd4in26.epdconfig.module_exit()
    exit()
