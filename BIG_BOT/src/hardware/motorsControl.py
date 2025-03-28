from .bigMotor import BigMotor


class MotorsControl:
    """ 
    Class to move the robot using two motors
    Parameters:
        forwardLeftPin (int): The pin number the left motor forward pin is connected to.
        backwardLeftPin (int): The pin number the left motor backward pin is connected to.
        forwardRightPin (int): The pin number the right motor forward pin is connected to.
        backwardRightPin (int): The pin number the right motor backward pin is connected to.
        
    **Methods**:
        **forward(speed)**: Move the robot forward at the specified speed.
           
        **backward(speed)**: Move the robot backward at the specified speed.

        **rotateLeft(speed)**: Rotate the robot to the left at the specified speed (left motor backward, right motor forward).

        **rotateRight(speed)**: Rotate the robot to the right at the specified speed (left motor forward, right motor backward).
            
        **stop()**: Stop the robot.
        
    """

    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, forwardRightPin: int, backwardRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin)
        self.speed = 0

    def forward(self, speed):

        """ Move the robot forward at the specified speed """

        self.speed = speed
        self.leftMotor.forward(self.speed)
        self.rightMotor.forward(self.speed)

    def backward(self, speed):

        """ Move the robot backward at the specified speed """

        self.speed = speed
        self.leftMotor.backward(self.speed)
        self.rightMotor.backward(self.speed)

    def rotateLeft(self, speed):
            
        """ Rotate the robot to the left at the specified speed (left motor backward, right motor forward) """

        self.speed = speed
        self.leftMotor.backward(self.speed)
        self.rightMotor.forward(self.speed)

    def rotateRight(self, speed):

        """ Rotate the robot to the right at the specified speed (left motor forward, right motor backward) """

        self.speed = speed
        self.leftMotor.forward(self.speed)
        self.rightMotor.backward(self.speed)

    def stop(self):

        """ Stop the robot """
        
        self.leftMotor.stop()
        self.rightMotor.stop()
