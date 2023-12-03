import os
import numpy as np

# import the correct libraries depending on the OS
if os.name == 'nt':
    import cv2 as cv
        
else : # assume it's the raspberry pi
    # need to set up the camera for the raspberry pi
    pass

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
            pass
            # Set up the camera for the raspberry pi

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
            pass
            # Get the image from the camera

        return background, picture, False