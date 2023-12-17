from arduino_interface import arduinoInterface
import time
import os
import numpy as np

WIDTH = 13
HEIGHT = 15
SIM_ARDUINO = False # Set to true to use the simulator

IMAGE = [
    ".............",
    ".............",
    ".............",
    "...##...##...",
    "...##...##...",
    ".............",
    ".............",
    "..#########..",
    "..#########..",
    "..#########..",
    "...#######...",
    ".....###.....",
    ".............",
    ".............",
    "............."
]

# IMAGE = [
#     ".............",
#     ".............",
#     "...##...##...",
#     "..####.####..",
#     ".###########.",
#     ".###########.",
#     ".###########.",
#     ".###########.",
#     "..#########..",
#     "...#######...",
#     "....#####....",
#     ".....###.....",
#     "......#......",
#     ".............",
#     "............."
# ]

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

# We need to wait for a bit before continuing or the readline will return nothing
print("waiting for serial port")
time.sleep(2)

# Convert the image to a boolean array
image_array = np.zeros((HEIGHT, WIDTH), np.bool_)
for i, line in enumerate(IMAGE):
    image_array[i] = np.array([np.True_ if c == "#" else np.False_ for c in line])

# Wait for the button press, then display the image
arduino_interface.send("b")
arduino_interface.display(image_array)

# Close the serial port
arduino_interface.close()

# theoretically 225 step increments
# col 1, 9: step 0
# col 3, 13: step 225
# col 6, 11: 
# col 2, 10: 
# col 4, 14: 
# col 7, 12:
#
# col 5, 15:
# col 8: 