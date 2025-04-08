# from gpiozero import Motor

# class BigMotor:
#     def __init__(self, forwardPin, backwardPin, enablePin):
#         self.motor = Motor(forwardPin, backwardPin, enable=enablePin)
#         self.speed = 0

#     def forward(self, speed):
#         self.speed = speed
#         self.motor.forward(self.speed)
    
#     def backward(self, speed):
#         self.speed = speed
#         self.motor.backward(self.speed)
    
#     def stop(self):
#         self.motor.stop()

from gpiozero import OutputDevice, PWMOutputDevice

class BigMotor:
    """ 
    Class for the big motor used to move the robot
    """
    
    def __init__(self, forwardPin, backwardPin, enablePin):
        self.forward_device = OutputDevice(forwardPin, active_high=True, initial_value=False)
        self.backward_device = OutputDevice(backwardPin, active_high=True, initial_value=False)
        self.enable_device = PWMOutputDevice(enablePin, frequency=100, initial_value=0)
        self.speed = 0

    def forward(self, speed):
        """ Move the motor forward at the specified speed """
        self.speed = max(0, min(1, speed))  # Clamp between 0 and 1
        self.forward_device.on()
        self.backward_device.off()
        self.enable_device.value = self.speed
    
    def backward(self, speed):
        """ Move the motor backward at the specified speed """
        self.speed = max(0, min(1, speed))  # Clamp between 0 and 1
        self.forward_device.off()
        self.backward_device.on()
        self.enable_device.value = self.speed
    
    def stop(self):
        """ Stop the motor """
        self.enable_device.value = 0
        self.forward_device.off()
        self.backward_device.off()
    
    

