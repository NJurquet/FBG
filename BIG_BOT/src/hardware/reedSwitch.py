from gpiozero import Button

#Class for the magnetic switch used to start the robot
class reedSwitch:
    def __init__(self, pin: int):
        self.pin = pin
        self.reedSwitch = Button(pin, pull_up=True)
    
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

