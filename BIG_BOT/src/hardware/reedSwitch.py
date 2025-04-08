from gpiozero import Button


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
        self.reedSwitch: Button = Button(pin, pull_up=False)

    def read(self):
        """Reads the state of the reed switch.
            True if the reed switch is pressed, False otherwise."""
        return self.reedSwitch.is_pressed

    def long_read(self):
        measures = [self.read() for _ in range(10)]
        return 1 if sum(measures) > 5 else 0
