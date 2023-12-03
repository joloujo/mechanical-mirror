import serial
import warnings
import numpy as np
import os.path

'''
Command list:
g (number of any length): go to step
h : set home
s (number of any length): step 
m (number, length = HEIGHT): set servo motors
l (number): home using limit switch, with a maximum of number of steps
'''

class arduinoInterface:
    def __init__(self, port, width, height):
        """
        Initializes the arduino interface

        Args:
            port (str): The port the arduino is connected to, or 'sim' to simulate
            width (int): The width of the mechanical mirror
            height (int): The height of the mechanical mirror
        """

        # Save the width and height
        self.WIDTH = width
        self.HEIGHT = height

        # load the current state
        self.current_state = np.zeros((self.HEIGHT, self.WIDTH), dtype=np.bool_)
        if os.path.isfile('current_state.npy'):
            saved_state = np.load('current_state.npy')
            if saved_state.shape == self.current_state.shape:
                self.current_state = saved_state       
            else:
                self.updateState(self.current_state)         
        else:
            self.updateState(self.current_state)

        # set up the serial port
        if port == 'sim':
            self.serialPort = None
        else:
            # set up the serial port
            BAUDRATE = 115200
            self.serialPort = serial.Serial(port, BAUDRATE, timeout=60)
            self.serialPort.flush()

    def close(self):
        """
        Closes the serial port
        """
        
        # if the serial port is simulated, it doesn't need to be closed
        if not self.serialPort is None: 
            self.serialPort.close()

    def updateState(self, states: np.ndarray[int, np.dtype[np.bool_]]):
        """
        Updates and saves the current state of the mechanical mirror

        Args:
            states (ndarray of bool): The new state of the mechanical mirror
        """

        self.current_state = states
        np.save('current_state.npy', self.current_state)

    def home(self):
        """
            Homes the VSA and goes to the first column
        """

        # set all servos to 0
        self.send("m00000")

        # home the VSA
        self.send("l10000")

        # go to the first column
        self.send("g0")
    
    def send(self, data: str):
        """
        Sends a command to the arduino

        Args:
            data (str): The command to send
        """

        # if the serial port is simulated, print the command instead of sending it
        if self.serialPort is None:
            print("sending:", data)
            return

        self.serialPort.write(bytes(data + "\n", 'utf-8'))
        response = self.serialPort.readline().decode().rstrip()

        if response != "":
            warnings.warn(response)

    def display(self, states: np.ndarray[int, np.dtype[np.bool_]]):
        """
        Displays the states on the mechanical mirror

        Args:
            states (ndarray of bool): The desired state of the mechanical mirror
        """

        # find the difference between the current state and the desired state
        flip = states != self.current_state

        # if the serial port is simulated, print the states instead of sending them
        if self.serialPort is None:
            for row in self.current_state:
                print(''.join([str(int(x)) for x in row]))
            print()
            for row in states:
                print(''.join(["#" if x else " " for x in row]))
            print()
            for row in flip:
                print(''.join(["#" if x else " " for x in row]))
            print()
            self.updateState(states)
            return
        
        # TODO: Update state while the mirror is moving

        # reset the servos and go to the first column
        self.send("m00000")
        self.send('g0')

        # send the states to the arduino
        for col in range(self.WIDTH):
            # go to the column
            self.send(f'g{col}')

            # turn the servos that need to be turned
            pixels = ''.join([str(row[col] * 9) for row in flip])
            self.send(f'm{pixels}')

            # keep going it's not the last column
            if col != self.WIDTH - 1:
                # go between the columns and reset the servos
                self.send(f'g{col+0.5}')
                self.send("m00000")
                
        # go between the columns and reset the servos
        self.send(f"g{self.WIDTH-1.5}")
        self.send("m00000")

        # go to the first column
        self.send("g0")
