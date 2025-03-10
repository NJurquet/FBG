from .config import LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN
from .config import CENTER_RIGHT_CLAW_NAME
from .config import CENTER_RIGHT_CLAW_PIN
from .fsm.FSM import RobotFSM
from .hardware.motorsControl import MotorsControl as Motors
from .hardware.servoControl import ServoControl

class Robot:
    """
    Class representing the robot, including its Finite State Machine (FSM), hardware components and characteristics.
    """

    def __init__(self):
        self.fsm = RobotFSM(self)
        self.motor = Motors(LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN)
        self.servoControl = ServoControl([CENTER_RIGHT_CLAW_NAME], [CENTER_RIGHT_CLAW_PIN])
        self.camera = None

        self.__position: tuple[int, int] = (0, 0)

    @property
    def position(self):
        """
        Getter for the position of the robot.

        Returns
        -------
        tuple[int, int]
            The x and y coordinates of the robot.
        """
        return self.__position

    @position.setter
    def position(self, value: tuple[int, int]):
        """
        Setter for the position of the robot.

        Parameters
        ----------
        value : tuple[int, int]
            The new x and y coordinates of the robot.

        Raises
        ------
        ValueError
            If the position is not a tuple of two integers.
        """
        if isinstance(value, tuple) and len(value) == 2:
            self.__position = value
        else:
            raise ValueError("Position must be a tuple of the x and y coordinates (x, y).")
