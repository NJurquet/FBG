from gpiozero import Button

#Class for the magnetic switch used to start the robot
class reedSwitch:
    """
    Class representing a reed switch, use to start our robot.

    Parameters
    ----------
    `pin` : int
        The GPIO pin number to which the reed switch is connected.

    
    Methods
    -------
    `read()` : int
        Returns the state of the reed switch (0 for not pressed, 1 for pressed).
    
    `long_read()` : int
        Waits for the reed switch to be pressed for a certain duration (10 checks) and returns 1 if pressed, 0 otherwise.

    """
    def __init__(self, pin: int):
        self.pin = pin
        self.reedSwitch = Button(pin, pull_up=False)
    
    def read(self):
        return self.reedSwitch.is_pressed

    def long_read(self):
        counter = 0
        while counter < 10:
            if self.read() == 0:
                counter += 1
            else:
                counter = 0
        return 1 if counter == 10 else 0

