from adafruit_servokit import ServoKit

class AdafruitServoControl:
    """
        Class to control multiple servo motors using PCA9685
        The I2C connection is automatically initialized by the Adafruit ServoKit library.

        Parameters:
            channels (int): Number of channels on the PCA9685 board.
            names (list): A list of names for the servo motors.
            pins (list): A list of pins the servo motors are connected to.
            
        Methods:
            setAngles(angles): Sets the angles of the servo motors.
            stopServo(channel): Stops a specific servo motor.
            setAngle(channel, angle): Sets the angle of a specific servo motor.
            stopServos(): Stops all servo motors.
    """
    def __init__(self, channels, names: list, pins: list):
        self.kit = ServoKit(channels=channels)
        self.names = names
        self.pins = pins

    def setAngles(self, angles: list):
        """
        Sets the goal angles of the servo motors.

        Parameters:
            angles (list): A list of goal angles in degrees.
        """
        for i in range(len(angles)):
            self.kit.servo[i].angle = angles[i]
            
    def setOuterAngles(self, angles: list):
        """
        Sets the goal angles of the outer servo motors.

        Parameters:
            angles (list): A list of goal angles in degrees.
        """
        for i in range(2, 4):
            self.kit.servo[i].angle = angles[i]

    def stopServo(self, channel: int):
        """
        Stops a specific servo motor.

        Parameters:
            channel (int): The channel number of the servo motor.
        """
        self.kit.servo[channel].angle = None

    def setAngle(self, name: str, angle: float):
        """
        Sets the goal angle of a specific servo motor.

        Parameters:
            name (int): The channel number of the servo motor.
            angle (float): The goal angle in degrees.
        """
        for i in range(len(self.names)):
            if self.names[i] == name:
                self.kit.servo[self.pins[i]].angle = angle

    def stopServos(self):
        """
        Stops all servo motors.
        """
        for i in range(16):
            self.kit.servo[i].angle = None