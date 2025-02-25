from .bigMotor import BigMotor


class MotorsControl:
    def __init__(self, forwardLeftPin: int, backwardLeftPin: int, forwardRightPin: int, backwardRightPin: int):
        self.leftMotor = BigMotor(forwardLeftPin, backwardLeftPin)
        self.rightMotor = BigMotor(forwardRightPin, backwardRightPin)
        self.speed = 0

    def forward(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed)
        self.rightMotor.forward(self.speed)

    def backward(self, speed):
        self.speed = speed
        self.leftMotor.backward(self.speed)
        self.rightMotor.backward(self.speed)

    def turnLeft(self, speed):
        self.speed = speed
        self.leftMotor.backward(self.speed)
        self.rightMotor.forward(self.speed)

    def turnRight(self, speed):
        self.speed = speed
        self.leftMotor.forward(self.speed)
        self.rightMotor.backward(self.speed)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
