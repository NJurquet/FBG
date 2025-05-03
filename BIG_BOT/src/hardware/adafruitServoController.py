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

        self._coef = 100

        self.lastAngles = [0] * len(names)

    def setAngles(self, angles: list):
        """
        Sets the goal angles of the servo motors.

        Parameters:
            angles (list): A list of goal angles in degrees.
        """
        for i in range(len(angles)):
            self.kit.servo[i].angle = angles[i]
            self.lastAngles[i] = angles[i]
            
    def setOuterAngles(self, angles: list):
        """
        Sets the goal angles of the outer servo motors.

        Parameters:
            angles (list): A list of goal angles in degrees.
        """

        self.kit.servo[2].angle = angles[0]
        self.kit.servo[3].angle = angles[1]

        self.lastAngles[2] = angles[0]
        self.lastAngles[3] = angles[1]
    
    def setPlankPusherAngles(self, angles: list):
        """
        Sets the goal angles of the plank pusher servo motors.

        Parameters:
            angles (list): A list of goal angles in degrees.
        """
        self.kit.servo[4].angle = angles[0]
        self.kit.servo[5].angle = angles[1]
        
        self.lastAngles[4] = angles[0]
        self.lastAngles[5] = angles[1]
        
    def setBannerDeployerAngle(self, angle: int):
        self.kit.servo[7].angle = angle
        
        self.lastAngles[7] = angle

    def stopServo(self, channel: int):
        """
        Stops a specific servo motor.

        Parameters:
            channel (int): The channel number of the servo motor.
        """
        self.kit.servo[channel].angle = None

    def setAngle(self, name: str, angle: int):
        """
        Sets the goal angle of a specific servo motor.

        Parameters:
            name (int): The channel number of the servo motor.
            angle (int): The goal angle in degrees.
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

    def stopOuterServos(self):
        """
        Stops all outer servo motors.
        """
        for i in range(2, 4):
            self.kit.servo[i].angle = None

    def computeTimeNeeded(self, angles: list[int], servos: str) -> float:
        """ Computes the time needed for all servos to reach the specified angles."""
        diff_angles = []

        if servos == "all":
            # For all servos, compare with all last angles
            diff_angles = [abs(angles[i] - self.lastAngles[i]) for i in range(len(angles))]

        elif servos == "outer":
            # For outer servos (indexes 2,3), compare the passed angles[0] and angles[1] with lastAngles[2] and lastAngles[3]
            diff_angles = [abs(angles[0] - self.lastAngles[2]), abs(angles[1] - self.lastAngles[3])]

        elif servos == "plankPushers":
            # For plank pushers (indexes 4,5), compare the passed angles[0] and angles[1] with lastAngles[4] and lastAngles[5]
            diff_angles = [abs(angles[0] - self.lastAngles[4]), abs(angles[1] - self.lastAngles[5])]

        elif servos == "hinge":
            # For hinge (index 6), compare passed angle with lastAngles[6]
            diff_angles = [abs(angles[0] - self.lastAngles[6])]

        elif servos == "bannerDeployer":
            # For banner deployer (index 7), compare passed angle with lastAngles[7]
            diff_angles = [abs(angles[0] - self.lastAngles[7])]

        # Avoid div by zero in case _coef is 0 
        if not diff_angles or self._coef == 0:
            return 0.1  # Minimum execution time

        max_angle = max(diff_angles)
        time_needed = max_angle / self._coef

        # Add a minimum time to ensure execution completes
        return max(time_needed, 0.1)