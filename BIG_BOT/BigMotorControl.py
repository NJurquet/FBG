from gpiozero import Motor



class BigMotorControl:
    def __init__(self, forward, backward):
        self.motor = Motor(forward, backward)
        self.speed = 0

    def forward(self, speed):
        self.speed = speed
        self.motor.forward(self.speed)
    
    def backward(self, speed):
        self.speed = speed
        self.motor.backward(self.speed)
    
    def stop(self):
        self.motor.stop()

    
    

