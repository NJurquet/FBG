from servoMotor import ServoMotor

class ServoControl:
    """
        Class to control multiple servo motors
        
        Parameters:
            names (list): A list of names for the servo motors.
            pins (list): A list of pins the servo motors are connected to.
            
        Methods:
            setAngles(angles): Sets the angles of the servo motors.
            stop(name): Stops a specific servo motor.
            setAngle(name, angle): Sets the angle of a specific servo motor.
    """
    def __init__(self, names: list, pins):
        self.servos = []
        for i in range(len(names)):
            self.servos.append(ServoMotor(names[i], pins[i]))

    def setAngles(self, angles: list):
        """
        Sets the goal angles of the servo motors.

        Parameters:
            angles (list): A list of goal angles in degrees.
        """
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])

    def stop(self, name: str):
        """
        Stops a specific servo motor.

        Parameters:
            name (str): The name of the servo motor.
        """
        for servo in self.servos:
            if servo.name == name:
                servo.stop()

    def setAngle(self, name, angle):
        """
        Sets the goal angle of a specific servo motor.

        Parameters:
            name (str): The name of the servo motor.
            angle (float): The goal angle in degrees.
        """
        for servo in self.servos:
            if isinstance(servo, ServoMotor) and servo.name == name:
                servo.setAngle(angle)
        
    
