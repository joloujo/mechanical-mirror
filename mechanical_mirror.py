from get_image import imageGetter
from image_converter import imageConverter
from arduino_interface import arduinoInterface
import time
import os

WIDTH = 13
HEIGHT = 15
SIM_ARDUINO = False # Set to true to use the simulator

def mechancial_mirror():
    # Pick the port based on the OS
    port = ''
    if SIM_ARDUINO:
        port = 'sim'
    elif os.name == 'nt':
        port = 'COM4'
    else: # assume it's the raspberry pi
        port = '/dev/ttyACM0'

    if not os.name == 'nt': # assume it's the raspberry pi
        os.chdir("/home/mechmirror/GitHub/mechanical-mirror")

    print("creating arduino interface")
    arduino_interface = arduinoInterface(port, WIDTH, HEIGHT)

    print("creating image getter")
    image_getter = imageGetter(arduino_interface)

    print("creating image converter")
    image_converter = imageConverter(WIDTH, HEIGHT)

    # We need to wait for a bit before continuing or the readline will return nothing
    print("waiting for serial port")
    time.sleep(2)

    arduino_interface.send("b") # wait for button press
    arduino_interface.home()

    try:
        while True:
            # Get the images from the camera
            background, picture = image_getter.get_images()

            # Find what state each pixel should be in
            states = image_converter.convert(background, picture)

            # Display the states on the mechanical mirror
            arduino_interface.display(states)
    except:
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
