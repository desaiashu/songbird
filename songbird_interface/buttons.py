# Button A is 15 // IO38
# Button B is 32 // IO33
# Button C is 14 // IO9

import board
from digitalio import DigitalInOut, Direction, Pull

class Buttons:
    def __init__(
        self,
        callback1=None,
        callback2=None,
        callback3=None
    ):
        self.buttons = [DigitalInOut(board.D5), DigitalInOut(board.D21), DigitalInOut(board.D20)]
        self.state = [False, False, False]
        self.callbacks = [callback1, callback2, callback3]

        for i in range(3):
            self.buttons[i].direction = Direction.INPUT
            self.buttons[i].pull = Pull.UP

    def checkClicks(self):
        for i in range(3):
            if self.state[i] == False and not self.buttons[i].value:
                self.state[i] = True
                if self.callbacks[i]:
                    self.callbacks[i]()
            elif self.state[i] == True and self.buttons[i].value:
                self.state[i] = False
