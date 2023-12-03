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
    def __init__(self):
        """
        Initializes the image getter
        """

        # Save the OS
        self.os = os.name

        # Set up the camera based on the OS
        if self.os == 'nt':
            self.cam = cv.VideoCapture(0)
        else: # assume it's the raspberry pi
            self.cam = Picamera2()
            
            camera_config = self.cam.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
            self.cam.configure(camera_config)
            
            self.cam.start()

        """
        Initializes the image getter
        """

    def get_images(self) -> tuple[np.ndarray[np.uint8, np.dtype[np.uint8]], np.ndarray[np.uint8, np.dtype[np.uint8]], bool]:
        """
        Gets two images from the camera (one of the background and one of the subject) based on the OS

        Returns:
            np.ndarray: The first image from the camera (intended to be the background)
            np.ndarray: The second image from the camera (intended to be the picture)
        """

        # set up the return values
        background: np.ndarray[np.uint8, np.dtype[np.uint8]] = np.array([])
        picture: np.ndarray[np.uint8, np.dtype[np.uint8]] = np.array([])

        # Get the images from the camera based on the OS
        if self.os == 'nt':

            # If the OS is windows, use the keyboard for user input and OpenCV for the camera

            # get background image
            user_input = input("Press enter to take a picture of the background:")
            if user_input != "":
                return background, picture, True
            background = np.asarray(self.cam.read()[1], dtype=np.uint8)

            # get picture image
            user_input = input("Press enter to take a picture of the subject:")
            if user_input != "":
                return background, picture, True
            picture = np.asarray(self.cam.read()[1], dtype=np.uint8)

        else: # assume it's the raspberry pi
            
            # Use the keyboard for user input and PyCam2 for the camera

            # get background image
            user_input = input("Press enter to take a picture of the background:")
            if user_input != "":
                return background, picture, True
            background = np.asarray(self.cam.capture_image(), dtype=np.uint8)

            # get picture image
            user_input = input("Press enter to take a picture of the subject:")
            if user_input != "":
                return background, picture, True
            picture = np.asarray(self.cam.capture_image(), dtype=np.uint8)

        # TODO: Make the images the right color when you do the arduino stuff

        cv.imshow('background', background)
        cv.imshow('picture', picture)
        return background, picture, False
