from arduino_interface import arduinoInterface
import os
import numpy as np
import cv2 as cv

# import the correct libraries depending on the OS
if os.name == 'nt':
    # all of the right libraries are already imported
    pass
else : # assume it's the raspberry pi
    from picamera2 import Picamera2, Preview 

class imageGetter():
    def __init__(self, arduino_interface: arduinoInterface):
        """
        Initializes the image getter

        Args:
            arduino_interface (arduinoInterface): The interface to the arduino
        """

        # Save the arduino interface
        self.arduino_interface = arduino_interface

        # Set up the camera based on the OS
        if os.name == 'nt':
            self.cam = cv.VideoCapture(0)
        else: # assume it's the raspberry pi
            self.cam = Picamera2()
            
            camera_config = self.cam.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
            self.cam.configure(camera_config)
            
            self.cam.start()

        """
        Initializes the image getter
        """

    def get_image(self) -> np.ndarray[np.uint8, np.dtype[np.uint8]]:
        """
        Gets an image from the camera based on the OS

        Returns:
            np.ndarray: The image from the camera
        """

        self.arduino_interface.send("b") # wait for button press
        if os.name == 'nt':
            return np.asarray(self.cam.read()[1], dtype=np.uint8)
        else: # assume it's the raspberry pi
            return np.asarray(self.cam.capture_image(), dtype=np.uint8)

    def get_images(self) -> tuple[np.ndarray[np.uint8, np.dtype[np.uint8]], np.ndarray[np.uint8, np.dtype[np.uint8]], bool]:
        """
        Gets two images from the camera (one of the background and one of the subject) based on the OS

        Returns:
            np.ndarray: The first image from the camera (intended to be the background)
            np.ndarray: The second image from the camera (intended to be the picture)
        """

        # set up the return values
        background = self.get_image()
        picture = self.get_image()

        # TODO: Make the images the right color when you do the arduino stuff
        # TODO: Countdown

        cv.imshow('background', background)
        cv.imshow('picture', picture)
        return background, picture, False
