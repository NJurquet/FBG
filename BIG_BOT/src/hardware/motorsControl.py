from .bigMotor import BigMotor

class MotorsControl:
    """ 
    Class to move the robot using two motors
    Parameters:
        forwardLeftPin (int): The pin number the left motor forward pin is connected to.
        backwardLeftPin (int): The pin number the left motor backward pin is connected to.
        forwardRightPin (int): The pin number the right motor forward pin is connected to.
        backwardRightPin (int): The pin number the right motor backward pin is connected to.
    """

    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, enableLeftPin: int, forwardRightPin: int, backwardRightPin: int, enableRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin, enableLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin, enableRightPin)
        self.speed = 0
        self.leftStraightOffset = -0.025
        self.rightStraightOffset = 0
        self.leftRotateOffset = -0.025
        self.rightRotateOffset = 0.0
        self.movement_timer: MyTimer | None = None
        self.distance_per_second = 10.4 # cm/s
        self.degrees_per_second_left = 52.8 # degrees/s
        self.degrees_per_second_right = 45.2 # degrees/s
        self._is_moving = False

    def forward(self, speed):
        """ 
        Move the robot forward at the specified speed 

        Parameters:
            speed (float): The speed at which to move the robot (value between 0 & 1).         
        """

        self.speed = speed
        self.leftMotor.forward(self.speed + self.leftStraightOffset)
        self.rightMotor.forward(self.speed + self.rightStraightOffset)

    def backward(self, speed):
        """ 
        Move the robot backward at the specified speed
        
        Parameters:
            speed (float): The speed at which to move the robot (value between 0 & 1).
        """

        self.speed = speed
        self.leftMotor.backward(self.speed + self.leftStraightOffset)
        self.rightMotor.backward(self.speed + self.rightStraightOffset)

    def rotateLeft(self, speed):
        """ Rotate the robot to the left at the specified speed (left motor backward, right motor forward)

        Parameters:
            speed (float): The speed at which to rotate the robot (value between 0 & 1).
        """

        self.speed = speed
        self.leftMotor.backward(self.speed + self.leftRotateOffset)
        self.rightMotor.forward(self.speed + self.rightRotateOffset)

    def rotateRight(self, speed):
        """ 
        Rotate the robot to the right at the specified speed (left motor forward, right motor backward)
            
        Parameters:
            speed (float): The speed at which to rotate the robot (value between 0 & 1).
        """

        self.speed = speed
        self.leftMotor.forward(self.speed + self.leftStraightOffset)
        self.rightMotor.backward(self.speed + self.rightStraightOffset)

    def stop(self):
        """ Stop the robot """
        
        self.leftMotor.stop()
        self.rightMotor.stop()

    # Additional methods for getting the time needed to achieve a certain movement

    def computeMoveForward(self, distance_cm, speed = 0.5):
        """
        Compute the time needed to move forward a certain distance at a given speed.
        
        Parameters:
            distance_cm (float): The distance to move in centimeters.
            speed (float): The speed at which to move the robot (value between 0 & 1), base value = 0.5.
        """
        if distance_cm <= 0:
            return 0
    
        self.speed = speed
        coeff = self.distance_per_second/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = distance_cm / (self.speed * coeff)

        return time_needed

    def computeMoveBackward(self, distance_cm, speed = 0.5):
        """
        Compute the time needed to move backward a certain distance at a given speed.
        
        Parameters:
            distance_cm (float): The distance to move in centimeters.
            speed (float): The speed at which to move the robot (value between 0 & 1), base value = 0.5.
        """
        if distance_cm <= 0:
            return 0
    
        self.speed = speed
        coeff = self.distance_per_second/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = distance_cm / (self.speed * coeff)

        return time_needed

    def computeRotateLeftDegrees(self, degrees, speed = 0.5):
        """
        Compute the time needed to rotate left a certain angle at a given speed.
        
        Parameters:
            degrees (float): The angle to rotate in degrees.
            speed (float): The speed at which to rotate the robot (value between 0 & 1), base value = 0.5.
        """
        if degrees <= 0:
            return 0
    
        self.speed = speed
        coeff = self.degrees_per_second_left/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = degrees / (self.speed * coeff)

        return time_needed

    def computeRotateRightDegrees(self, degrees, speed = 0.5):
        """
        Compute the time needed to rotate right a certain angle at a given speed.
        
        Parameters:
            degrees (int): The angle to rotate in degrees.
            speed (float): The speed at which to rotate the robot (value between 0 & 1), base value = 0.5.
        """
        if degrees <= 0:
            return 0
    
        self.speed = speed
        coeff = self.degrees_per_second_left/self.speed 

        # Calculate the time needed to cover the distance in cm
        time_needed = degrees / (self.speed * coeff)

        return time_needed

    def cleanup(self):
        """Clean up all motor resources"""
        if self.leftMotor:
            self.leftMotor.stop()
            self.leftMotor.cleanup()
        if self.rightMotor:
            self.leftMotor.stop()
            self.rightMotor.cleanup()
        if self.movement_timer:
            self.movement_timer.cancel()
            self.movement_timer = None