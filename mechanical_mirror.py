'''
Command list:
g (number of any length): go to step
h : set home
s (number of any length): step 
m (number, length = HEIGHT): set servo motors
'''

# Example command 1: m09 g5000 m00 g10000 m99 g5000 m00 g0
# Example command 2: g2000 m00 g0 m09 g5000 m00 g10000 m99 g5000 m00 g0

import serial
import time

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2 as cv

HEIGHT = 2

# set up the serial port
PORT = 'COM4'
BAUDRATE = 115200
serialPort = serial.Serial(PORT, BAUDRATE, timeout=60)
serialPort.flush()


def send(data: str):
    print("sending:", data)

    serialPort.write(bytes(data + "\n", 'utf-8'))
    response = serialPort.readline().decode().rstrip()

    if response != "":
        raise ValueError(response)


# We need to wait for a bit before continuing or the readline will return nothing
time.sleep(2)
while True:
    commands = input("Enter a commands separated by spaces: ")
    if commands == "":
        break

    for command in commands.split(" "):
        try:
            send(command)
        except ValueError as e:
            print("Error:", e)

serialPort.close()