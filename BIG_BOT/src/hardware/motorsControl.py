from .bigMotor import BigMotor


class MotorsControl:
    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, enableLeftPin: int, forwardRightPin: int, backwardRightPin: int, enableRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin, enableLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin, enableRightPin)
        self.speed = 0

    def forward(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed)
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
