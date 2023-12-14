from arduino_interface import arduinoInterface
import time
import os

WIDTH = 15
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
# while True:
for _ in range(1):
    for i in range(30):
        command = "m" + "1" * i + "0" * (30-i)
        arduino_interface.send(command)
        time.sleep(0.25)

    for i in range(30):
        command = "m" + "0" * i + "1" * (30-i)
        arduino_interface.send(command)
        time.sleep(0.25)

# Close the serial port
arduino_interface.close()