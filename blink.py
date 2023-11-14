import time
import RPi.GPIO as GPIO

def blink():
    # Pin definitions
    led_pin = 12

    # Use "GPIO" pin numbering
    GPIO.setmode(GPIO.BCM)

    # Set LED pin as output
    GPIO.setup(led_pin, GPIO.OUT)

    # Blink forever
    try:
        while True:
            GPIO.output(led_pin, GPIO.HIGH) # Turn LED on
            time.sleep(1)
            GPIO.output(led_pin, GPIO.LOW)  # Turn LED off
            time.sleep(1)

    # When you press ctrl+c, nicely release GPIO resources
    finally:
        GPIO.cleanup()
