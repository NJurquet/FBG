from gpiozero import Servo

class ServoMotor:
    """
        Class to control a servo motor

        Parameters:
            name (str): The name of the servo motor.
            pin (int): The pin number the servo motor is connected to.

        Methods:
            setAngle(angle): Sets the angle of the servo motor.
            stop(): Stops the servo motor.
    """
    def __init__(self, name: str, pin: int):
        self.name = name
        self.servo = Servo(pin)
        self.angle = 0

    def setAngle(self, angle: int):
        """
        Sets the goal angle of the servo motor.

        Parameters:
            angle (int): The goal angle in degrees.
        """
        self.angle = angle
        self.servo.value = self.angle

    def stop(self):
        """
            Stops the servo motor.
        """
        self.servo.detach()