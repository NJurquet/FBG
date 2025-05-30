from gpiozero import Motor
import os
import platform
if os.getenv("GITHUB_ACTIONS") == "true" or platform.system() == "Windows":
    factory = None
else:
    try:
        from gpiozero.pins.pigpio import PiGPIOFactory
        factory = PiGPIOFactory()
    except OSError:
        factory = None

class BigMotor:
    """ 
    Class for the big motor used to move the robot
    Parameters:
        forwardPin (int): The pin number the motor forward pin is connected to.
        backwardPin (int): The pin number the motor backward pin is connected to.
        
    **Methods**:
        **forward(speed)**: Move the motor forward at the specified speed. Speed should be between 0 and 1.
           
        **backward(speed)**: Move the motor backward at the specified speed. Speed should be between 0 and 1.
            
        **stop()**: Stop the motor.
        
        """
    
    def __init__(self, forwardPin, backwardPin, enablePin):
        self.motor = Motor(forwardPin, backwardPin, enable=enablePin, pin_factory=factory)
        self.speed = 0

    def forward(self, speed):
        """ Move the motor forward at the specified speed """
        self.speed = speed
        self.motor.forward(self.speed)
    
    def backward(self, speed):
        """ Move the motor backward at the specified speed """
        self.speed = speed
        self.motor.backward(self.speed)
    
    def stop(self):
        """ Stop the motor """
        self.motor.stop()

    def cleanup(self):
        """ Release GPIO resources """
        self.motor.close()

    
    

