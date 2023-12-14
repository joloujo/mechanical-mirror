from arduino_interface import arduinoInterface
import time
import os

WIDTH = 13
HEIGHT = 15
SIM_ARDUINO = False # Set to true to use the simulator

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
while True:
    commands = input("Command to send: ")

    if commands == "":
        break

    for command in commands.split():
        if command[0] == "m":
            if len(command) == 2:
                command = "m" + command[1] * HEIGHT

        # Display the states on the mechanical mirror
        arduino_interface.send(command)

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