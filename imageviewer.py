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

    # Ask the user to input the image filename
    image_filename = input("Please enter the image filename (with extension, e.g., image.png): ")

    # Get the current directory (same as the script location)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full path for the image
    image_path = os.path.join(current_dir, image_filename)

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_filename}' does not exist in the current directory.")
        sys.exit(1)  # Exit if the file is not found

    # Load the image
    image = Image.open(image_path)

    # Resize the image to fit the display
    image = image.resize((epd.width, epd.height), Image.ANTIALIAS)
    
    # Rotate the image 180 degrees
    image = image.rotate(180)

    # Display the image
    epd.display(epd.getbuffer(image))

    # Put the display to sleep after showing the image
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("Ctrl+C detected. Exiting...")
    epd4in26.epdconfig.module_exit()
    exit()
