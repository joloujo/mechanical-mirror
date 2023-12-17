from arduino_interface import arduinoInterface
from image_converter import imageConverter
from get_image import imageGetter
import numpy as np
import cv2 as cv

WIDTH = 13
HEIGHT = 15

arduino_interface = arduinoInterface('sim', WIDTH, HEIGHT)
'''
states = np.asarray([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
], dtype=np.bool_)

arduino_interface.display(states)

arduino_interface.close()
'''

image_getter = imageGetter(arduino_interface)

background, picture = image_getter.get_images()

image_converter = imageConverter(WIDTH, HEIGHT)

print(image_converter.convert(background, picture))

