from gpiozero import Motor

class BigMotor:
    def __init__(self, forwardPin, backwardPin):
        self.motor = Motor(forwardPin, backwardPin)
        self.speed = 0

    def forward(self, speed):
        self.speed = speed
        self.motor.forward(self.speed)
    
    def backward(self, speed):
        self.speed = speed
        self.motor.backward(self.speed)
    
    def stop(self):
        self.motor.stop()

    
    

