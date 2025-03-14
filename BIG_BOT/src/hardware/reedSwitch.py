from gpiozero import Button

#Class for the magnetic switch used to start the robot
class reedSwitch:
    def __init__(self, pin: int):
        self.pin = pin
        self.reedSwitch = Button(pin, pull_up=True)
    
    def read(self):
        return self.reedSwitch.is_pressed
