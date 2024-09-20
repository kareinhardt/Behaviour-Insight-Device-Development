# dHX Design Team internal testing tools; not for production use.

import os
import logging
import socket
import subprocess
from waveshare_epd import epd4in26  # Ensure this is the correct driver for your 4.26 inch display
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

def get_ip_address():
    try:
        # Get the IP address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        logging.info(f"Error getting IP address: {e}")
        return "Unknown"

def get_network_name():
    try:
        # Get the network name (SSID) by using the 'iwgetid' command
        network_name = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return network_name if network_name else "Unknown"
    except Exception as e:
        logging.info(f"Error getting network name: {e}")
        return "Unknown"

try:
    # Initialize the display
    epd = epd4in26.EPD()
    epd.init()

    # Clear the display
    epd.Clear()

    # Get the current time (boot time)
    boot_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get the device hostname
    hostname = os.uname()[1]

    # Get the network name (SSID) and IP address
    network_name = get_network_name()
    ip_address = get_ip_address()

    # Prepare the welcome message, splitting the second line
    message = f"This device was booted on {boot_time}\n" \
              f"It is connected to the network {network_name}\n" \
              f"with IP address {ip_address}\n" \
              f"Device Hostname: {hostname}\n" \
              "National Innovation Centre for Ageing | dHX Team"

    # Create a new blank image in '1' mode for 1-bit color
    image = Image.new('1', (epd.width, epd.height), 255)  # White background

    # Initialize drawing object
    draw = ImageDraw.Draw(image)

    # Define font (use a font file available on your system)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)

    # Split the message into lines
    lines = message.split('\n')

    # Calculate the total height of the text block, including added line spacing
    line_spacing = 10  # Increase line spacing
    text_height = sum([draw.textsize(line, font=font)[1] for line in lines]) + (line_spacing * (len(lines) - 1))
    start_y = (epd.height - text_height) // 2  # Start y position for vertically centering the text

    # Draw each line of text in the center of the screen
    for line in lines:
        text_width, text_height = draw.textsize(line, font=font)
        start_x = (epd.width - text_width) // 2  # Center the text horizontally
        draw.text((start_x, start_y), line, font=font, fill=0)
        start_y += text_height + line_spacing  # Move down for the next line of text, including the extra spacing

    # Rotate the image 180 degrees
    image = image.rotate(180)

    # Display the image with the welcome message
    epd.display(epd.getbuffer(image))

    # Put the display to sleep after showing the message
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("Ctrl+C detected. Exiting...")
    epd4in26.epdconfig.module_exit()
    exit()
