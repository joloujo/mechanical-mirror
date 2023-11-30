import time
import os
import RPi.GPIO as GPIO

def shutdown_on_push():
    # Pin definitions
    off_pin = 3

    # Use "GPIO" pin numbering
    GPIO.setmode(GPIO.BCM)

    # Set shutdown pin as input with pull-up resistor
    GPIO.setup(off_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Check if button is pressed forever
    try:
        while True:
            if not GPIO.input(off_pin):
                os.system("sudo shutdown -h now")
            time.sleep(0.01)

    # When you press ctrl+c, nicely release GPIO resources
    finally:
        GPIO.cleanup()
