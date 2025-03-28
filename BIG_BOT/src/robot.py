from .config import LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN, US_FRONT_RIGHT_TRIG_PIN, US_FRONT_RIGHT_ECHO_PIN, US_FRONT_LEFT_TRIG_PIN, US_FRONT_LEFT_ECHO_PIN, US_BACK_RIGHT_TRIG_PIN, US_BACK_RIGHT_ECHO_PIN, US_BACK_LEFT_TRIG_PIN, US_BACK_LEFT_ECHO_PIN, REED_SWITCH_PIN
from .config import SERVO_CHANNELS
from .config import CENTER_RIGHT_CLAW_NAME
from .config import CENTER_RIGHT_CLAW_ADAFRUIT_PIN
from .constants import USPosition
from .fsm.FSM import RobotFSM
from .hardware.motorsControl import MotorsControl as Motors
from .hardware.servoControl import ServoControl
from .hardware.adafruitServoController import AdafruitServoControl
from .hardware.ultrasonicController import UltrasonicController
from .hardware.reedSwitch import reedSwitch


class Robot:
    """
    Class representing the robot, including its Finite State Machine (FSM), hardware components and characteristics.
    """

    def __init__(self):
        self.fsm = RobotFSM(self)
        self.motor = Motors(LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN)
        #self.servoControl = ServoControl([CENTER_RIGHT_CLAW_NAME], [CENTER_RIGHT_CLAW_PIN])
        self.servoControl = AdafruitServoControl(channels=SERVO_CHANNELS,
                                                 names=[CENTER_RIGHT_CLAW_NAME],
                                                 pins=[CENTER_RIGHT_CLAW_ADAFRUIT_PIN])
        self.camera = None
        self.ultrasonicController = UltrasonicController({
            # USPosition.FRONT_RIGHT: (US_FRONT_RIGHT_ECHO_PIN, US_FRONT_RIGHT_TRIG_PIN),
            # USPosition.FRONT_LEFT: (US_FRONT_LEFT_ECHO_PIN, US_FRONT_LEFT_TRIG_PIN),
            # USPosition.BACK_RIGHT: (US_BACK_RIGHT_ECHO_PIN, US_BACK_RIGHT_TRIG_PIN),
            # USPosition.BACK_LEFT: (US_BACK_LEFT_ECHO_PIN, US_BACK_LEFT_TRIG_PIN)
        })

        self.__position: tuple[int, int] = (0, 0)
        self.reedSwitch = reedSwitch(REED_SWITCH_PIN)

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
