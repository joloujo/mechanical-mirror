"""
This module runs on the Raspberry Pi on startup.
"""

from blink import blink

def main():
    """ Main entry point of the app """
    blink()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
