"""
This module runs on the Raspberry Pi on startup.
"""

from blink import blink
from shutdown import shutdown_on_push
import threading

def main():
    """ Main entry point of the app """
    threading.Thread(target=blink).start()
    threading.Thread(target=shutdown_on_push).start()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
