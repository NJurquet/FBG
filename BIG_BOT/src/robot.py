from .config import LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, LEFT_MOTOR_EN_PIN, RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_EN_PIN
# from .config import US_FRONT_RIGHT_TRIG_PIN, US_FRONT_RIGHT_ECHO_PIN, US_FRONT_LEFT_TRIG_PIN, US_FRONT_LEFT_ECHO_PIN, US_BACK_RIGHT_TRIG_PIN, US_BACK_RIGHT_ECHO_PIN, US_BACK_LEFT_TRIG_PIN, US_BACK_LEFT_ECHO_PIN
# from .config import SERVO_CHANNELS
# from .config import REED_SWITCH_PIN
# from .config import CENTER_RIGHT_CLAW_NAME, CENTER_LEFT_CLAW_NAME, OUTER_RIGHT_CLAW_NAME, OUTER_LEFT_CLAW_NAME, CENTER_RIGHT_CLAW_ADAFRUIT_PIN, CENTER_LEFT_CLAW_ADAFRUIT_PIN, OUTER_RIGHT_CLAW_ADAFRUIT_PIN, OUTER_LEFT_CLAW_ADAFRUIT_PIN
# from .config import PLANK_PUSHER_RIGHT_NAME, PLANK_PUSHER_LEFT_NAME, PLANK_PUSHER_RIGHT_ADAFRUIT_PIN, PLANK_PUSHER_LEFT_ADAFRUIT_PIN, HINGE_NAME, HINGE_ADAFRUIT_PIN, BANNER_DEPLOYER_NAME, BANNER_DEPLOYER_ADAFRUIT_PIN
# from .config import REED_SWITCH_PIN
from .config import DEFAULT_SCORE
# from .constants import USPosition
from .hardware.motorsControl import MotorsControl as Motors
# from .hardware.servoControl import ServoControl
# from .hardware.lcd import LCD
# from .hardware.adafruitServoController import AdafruitServoControl
# from .hardware.ultrasonicController import UltrasonicController
# from .hardware.reedSwitch import reedSwitch
from time import time
from .fsm.newcommands.newFSM import RobotFSM

from .fsm.newcommands.commands import ForwardCommand, BackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand, WaitCommand, CommandInvoker


class Robot:
    """
    Class representing the robot, including its Finite State Machine (FSM), hardware components and characteristics.

    """

    def __init__(self, color: str, score: int = DEFAULT_SCORE):
        self.command_invoker = CommandInvoker()

        self.fsm = RobotFSM(self)
        self.motor = Motors(LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, LEFT_MOTOR_EN_PIN,
                            RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_EN_PIN)
        # self.servoControl = AdafruitServoControl(channels=SERVO_CHANNELS,
        #                                          names=[CENTER_RIGHT_CLAW_NAME],
        #                                          pins=[CENTER_RIGHT_CLAW_ADAFRUIT_PIN])
        #                                          names=[CENTER_RIGHT_CLAW_NAME, CENTER_LEFT_CLAW_NAME, OUTER_RIGHT_CLAW_NAME, OUTER_LEFT_CLAW_NAME,
        #                                                 PLANK_PUSHER_RIGHT_NAME, PLANK_PUSHER_LEFT_NAME, HINGE_NAME, BANNER_DEPLOYER_NAME
        #                                           ],
        #                                          pins=[CENTER_RIGHT_CLAW_ADAFRUIT_PIN, CENTER_LEFT_CLAW_ADAFRUIT_PIN, OUTER_RIGHT_CLAW_ADAFRUIT_PIN, OUTER_LEFT_CLAW_ADAFRUIT_PIN,
        #                                                PLANK_PUSHER_RIGHT_ADAFRUIT_PIN, PLANK_PUSHER_LEFT_ADAFRUIT_PIN, HINGE_ADAFRUIT_PIN, BANNER_DEPLOYER_ADAFRUIT_PIN
        #                                           ])

        # self.lcd = LCD()
        self.camera = None
        # self.ultrasonicController = UltrasonicController()
        # self.ultrasonicController.add_sensor(USPosition.FRONT_RIGHT, US_FRONT_RIGHT_ECHO_PIN, US_FRONT_RIGHT_TRIG_PIN)
        # self.ultrasonicController.add_sensor(USPosition.FRONT_LEFT, US_FRONT_LEFT_ECHO_PIN, US_FRONT_LEFT_TRIG_PIN)
        # self.ultrasonicController.add_sensor(USPosition.BACK_RIGHT, US_BACK_RIGHT_ECHO_PIN, US_BACK_RIGHT_TRIG_PIN)
        # self.ultrasonicController.add_sensor(USPosition.BACK_LEFT, US_BACK_LEFT_ECHO_PIN, US_BACK_LEFT_TRIG_PIN)
        # self.reedSwitch = reedSwitch(REED_SWITCH_PIN)

        self.color = color
        self.score = score
        # self.lcd.write_score(self.score)
        self.__position: tuple[int, int] = (0, 0)
    

    # Create some helper methods to make command creation easier
    def move_forward(self, distance_cm: float, speed: float = 0.5) -> ForwardCommand:
        """Create a forward movement command"""
        return ForwardCommand(self, distance_cm, speed)
    
    def move_backward(self, distance_cm: float, speed: float = 0.5) -> BackwardCommand:
        """Create a backward movement command"""
        return BackwardCommand(self, distance_cm, speed)
    
    def rotate_left(self, degrees: float, speed: float = 0.5) -> RotateLeftCommand:
        """Create a rotate left command"""
        return RotateLeftCommand(self, degrees, speed)
    
    def rotate_right(self, degrees: float, speed: float = 0.5) -> RotateRightCommand:
        """Create a rotate right command"""
        return RotateRightCommand(self, degrees, speed)
    
    def stop(self) -> StopCommand:
        """Create a stop command"""
        return StopCommand(self)
    
    def wait(self, duration: float) -> WaitCommand:
        """Create a wait command"""
        return WaitCommand(duration)
    
    def run(self) -> None:
        """
        Main robot control loop.
        """
        self.fsm.start()  # Start the robot operations
        
        try:
            while not self.fsm.end_of_match:
                self.fsm.update()  # Update the FSM to execute commands
                time.sleep(0.01)  # Small delay to avoid CPU hogging
        except KeyboardInterrupt:
            print("Robot operation interrupted")
            self.motor.stop()  # Ensure motors are stopped
    

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
