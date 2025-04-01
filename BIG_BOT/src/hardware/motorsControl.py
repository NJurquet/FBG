from .bigMotor import BigMotor
from threading import Thread
from time import time

class MotorsControl:
    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, enableLeftPin: int, forwardRightPin: int, backwardRightPin: int, enableRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin, enableLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin, enableRightPin)
        self.speed = 0

    def forward(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed - 0.025)
        self.rightMotor.forward(self.speed)

    def backward(self, speed):
        self.speed = speed
        self.leftMotor.backward(self.speed)
        self.rightMotor.backward(self.speed)

    def rotateLeft(self, speed):
        self.speed = speed
        self.leftMotor.backward(self.speed)
        self.rightMotor.forward(self.speed)

    def rotateRight(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed)
        self.rightMotor.backward(self.speed)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    # Additional methods for control in distance and not speed

    def moveForward(self, distance):
        self.speed = 0.5
        real_speed = 12.08 # cm/s
        coeff = self.speed / real_speed
        timeLeft = distance / (self.speed * coeff)


    def moveBackward(self, distance):
        pass

    # Additional methods for control in degrees and not speed

    def rotateLeftDegrees(self, degrees):
        pass

    def rotateRightDegrees(self, degrees):
        pass