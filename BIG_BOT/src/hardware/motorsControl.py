from .bigMotor import BigMotor
from threading import Timer
import time

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

    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, enableLeftPin: int, forwardRightPin: int, backwardRightPin: int, enableRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin, enableLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin, enableRightPin)
        self.speed = 0
        self.leftStraightOffset = - 0.025
        self.rightStraightOffset = 0
        self.leftRotateOffset = 0.0
        self.rightRotateOffset = 0.0
        self.movement_timer = None
        self.distance_per_second = 11.8 # cm/s
        self.degrees_per_second_left = 48.45 # degrees/s
        self.degrees_per_second_right = 47.4 # degrees/s
        self._is_moving = False

    def forward(self, speed):

        """ Move the robot forward at the specified speed """

        self.speed = speed
        self.leftMotor.forward(self.speed + self.leftStraightOffset)
        self.rightMotor.forward(self.speed + self.rightStraightOffset)

    def backward(self, speed):

        """ Move the robot backward at the specified speed """

        self.speed = speed
        self.leftMotor.backward(self.speed + self.leftStraightOffset)
        self.rightMotor.backward(self.speed + self.rightStraightOffset)

    def rotateLeft(self, speed):
            
        """ Rotate the robot to the left at the specified speed (left motor backward, right motor forward) """

        self.speed = speed
        self.leftMotor.backward(self.speed + self.leftRotateOffset)
        self.rightMotor.forward(self.speed + self.rightRotateOffset)

    def rotateRight(self, speed):

        """ Rotate the robot to the right at the specified speed (left motor forward, right motor backward) """

        self.speed = speed
        self.leftMotor.forward(self.speed + self.leftStraightOffset)
        self.rightMotor.backward(self.speed + self.rightStraightOffset)

    def stop(self):

        """ Stop the robot """
        
        self.leftMotor.stop()
        self.rightMotor.stop()

    # Additional methods for control in distance and not speed

    def moveForward(self, distance_cm, speed = 0.5):
        if distance_cm <= 0:
            return 0
    
        self.speed = speed
        coeff = self.distance_per_second/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = distance_cm / (self.speed * coeff)

        self.leftMotor.forward(self.speed + self.leftStraightOffset)
        self.rightMotor.forward(self.speed + self.rightStraightOffset)

        if self.movement_timer:
            self.movement_timer.cancel()

        self.movement_timer = Timer(time_needed, lambda : self.stop())
        self.movement_timer.start()

        return time_needed

    def moveBackward(self, distance_cm, speed = 0.5):
        if distance_cm <= 0:
            return 0
    
        self.speed = speed
        coeff = self.distance_per_second/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = distance_cm / (self.speed * coeff)

        self.leftMotor.backward(self.speed + self.leftStraightOffset)
        self.rightMotor.backward(self.speed + self.rightStraightOffset)

        if self.movement_timer:
            self.movement_timer.cancel()

        self.movement_timer = Timer(time_needed, lambda : self.stop())
        self.movement_timer.start()

        return time_needed

    # Additional methods for control in degrees and not speed

    def rotateLeftDegrees(self, degrees, speed = 0.5):
        if degrees <= 0:
            return 0
    
        self.speed = speed
        coeff = self.degrees_per_second_left/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = degrees / (self.speed * coeff)

        self.leftMotor.backward(self.speed + self.leftRotateOffset)
        self.rightMotor.forward(self.speed + self.rightRotateOffset)

        if self.movement_timer:
            self.movement_timer.cancel()

        self.movement_timer = Timer(time_needed, lambda : self.stop())
        self.movement_timer.start()

        return time_needed

    def rotateRightDegrees(self, degrees, speed = 0.5):
        if degrees <= 0:
            return 0
    
        self.speed = speed
        coeff = self.degrees_per_second_left/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = degrees / (self.speed * coeff)

        self.leftMotor.forward(self.speed + self.leftStraightOffset)
        self.rightMotor.backward(self.speed + self.rightStraightOffset)

        if self.movement_timer:
            self.movement_timer.cancel()

        self.movement_timer = Timer(time_needed, lambda : self.stop())
        self.movement_timer.start()

        return time_needed

    def cleanup(self):
        """Clean up all motor resources"""
        if self.leftMotor:
            self.leftMotor.cleanup()
        if self.rightMotor:
            self.rightMotor.cleanup()
        if self.movement_timer:
            self.movement_timer.cancel()
            self.movement_timer = None