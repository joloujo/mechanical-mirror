"""
This module runs on the Raspberry Pi on startup.
"""

from blink import blink
from shutdown import shutdown_on_push
from mechanical_mirror import mechancial_mirror
import threading

def main():
    """ Main entry point of the app """
    threading.Thread(target=blink).start()
    threading.Thread(target=shutdown_on_push).start()
    try:
        threading.Thread(target=mechancial_mirror).start()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
