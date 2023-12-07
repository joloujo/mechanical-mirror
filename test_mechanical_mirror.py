from arduino_interface import arduinoInterface
import time
import os

WIDTH = 5
HEIGHT = 5
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
    command = input("Command to send: ")

    if command == "":
        break

    # Display the states on the mechanical mirror
    arduino_interface.send(command)

# Close the serial port
arduino_interface.close()
