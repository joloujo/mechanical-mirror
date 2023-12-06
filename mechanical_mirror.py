from get_image import imageGetter
from image_converter import imageConverter
from arduino_interface import arduinoInterface
import time
import os

WIDTH = 5
HEIGHT = 5
SIM_ARDUINO = False # Set to true to use the simulator

def mechancial_mirror():
    # Pick the port based on the OS
    port = ''
    if SIM_ARDUINO:
        port = 'sim'
    elif os.name == 'nt':
        port = 'COM5'
    else: # assume it's the raspberry pi
        port = '/dev/ttyACM0'

    print("creating arduino interface")
    arduino_interface = arduinoInterface(port, WIDTH, HEIGHT)

    print("creating image getter")
    image_getter = imageGetter(arduino_interface)

    print("creating image converter")
    image_converter = imageConverter(WIDTH, HEIGHT)

    # We need to wait for a bit before continuing or the readline will return nothing
    print("waiting for serial port")
    time.sleep(2)
    while True:
        # Get the images from the camera
        background, picture, break_loop = image_getter.get_images()

        # If the user typed anything when asked to take a picture, break the loop
        if break_loop:
            break

        # Find what state each pixel should be in
        states = image_converter.convert(background, picture)

        # Display the states on the mechanical mirror
        arduino_interface.display(states)

    # Close the serial port
    arduino_interface.close()

if __name__ == "__main__":
    mechancial_mirror()

'''
Code structure:
    Setup:
        - Set up serial port
        - Set up camera
        - Home the VSA on the mirror
    Loop:
        - Wait for button press
        - Get image from camera based on os
        - Image processing
        - Send commands to arduino
'''