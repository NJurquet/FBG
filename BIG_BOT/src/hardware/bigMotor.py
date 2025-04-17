from gpiozero import Motor

class BigMotor:
    """ 
    Class for the big motor used to move the robot
    Parameters:
        forwardPin (int): The pin number the motor forward pin is connected to.
        backwardPin (int): The pin number the motor backward pin is connected to.
        
    **Methods**:
        **forward(speed)**: Move the motor forward at the specified speed.
           
        **backward(speed)**: Move the motor backward at the specified speed.
            
        **stop()**: Stop the motor.
        
        """
    
    def __init__(self, forwardPin, backwardPin, enablePin):
        self.motor = Motor(forwardPin, backwardPin, enable=enablePin)
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

    
    

