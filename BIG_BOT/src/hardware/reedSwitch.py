from gpiozero import Button

#Class for the magnetic switch used to start the robot
class reedSwitch:
    """
        Class to control a reed switch

        Parameters:
            pin (int): The pin number the reed switch is connected to.

        **Methods**:
            read(): Reads the state of the reed switch.
    """

    def __init__(self, pin: int):
        self.pin = pin
        self.reedSwitch = Button(pin, pull_up=True)
    
    def read(self):
        """Reads the state of the reed switch.
            True if the reed switch is pressed, False otherwise."""
        return self.reedSwitch.is_pressed
