from .bigMotor import BigMotor
from threading import Timer
import time

class MotorsControl:
    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, enableLeftPin: int, forwardRightPin: int, backwardRightPin: int, enableRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin, enableLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin, enableRightPin)
        self.speed = 0
        self.leftOffset = - 0.025
        self.rightOffset = 0
        self.movement_timer = None
        self.distance_per_second = 12.08 # cm/s
        self.degrees_per_second = None # degrees/s
        self._is_moving = False

    def forward(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed + self.leftOffset)
        self.rightMotor.forward(self.speed + self.rightOffset)

    def backward(self, speed):
        self.speed = speed
        self.leftMotor.backward(self.speed + self.leftOffset)
        self.rightMotor.backward(self.speed + self.rightOffset)

    def rotateLeft(self, speed):
        self.speed = speed
        self.leftMotor.backward(self.speed + self.leftOffset)
        self.rightMotor.forward(self.speed + self.rightOffset)

    def rotateRight(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed + self.leftOffset)
        self.rightMotor.backward(self.speed + self.rightOffset)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    # Additional methods for control in distance and not speed

    def moveForward(self, distance_cm, speed = 0.5):
        if distance_cm <= 0:
            return 0
    
        self.speed = speed
        coeff = self.speed / self.distance_per_second

        # Calculate the time needed to cover the distance in cm
        time_needed = distance_cm / (self.speed * coeff)

        self.leftMotor.forward(self.speed + self.leftOffset)
        self.rightMotor.forward(self.speed + self.rightOffset)

        if self.movement_timer:
            self.movement_timer.cancel()

        self.movement_timer = Timer(time_needed, self.stop())
        self.movement_timer.start()

        return time_needed

    def moveBackward(self, distance_cm, speed = 0.5):
        if distance_cm <= 0:
            return 0
    
        self.speed = speed
        coeff = self.speed / self.distance_per_second

        # Calculate the time needed to cover the distance in cm
        time_needed = distance_cm / (self.speed * coeff)

        self.leftMotor.backward(self.speed + self.leftOffset)
        self.rightMotor.backward(self.speed + self.rightOffset)

        if self.movement_timer:
            self.movement_timer.cancel()

        self.movement_timer = Timer(time_needed, self.stop())
        self.movement_timer.start()

        return time_needed

    # Additional methods for control in degrees and not speed

    def rotateLeftDegrees(self, degrees):
        pass

    def rotateRightDegrees(self, degrees):
        pass