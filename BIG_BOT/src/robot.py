from .config import LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, LEFT_MOTOR_EN_PIN, RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_EN_PIN
from .config import US_FRONT_RIGHT_TRIG_PIN, US_FRONT_RIGHT_ECHO_PIN, US_FRONT_LEFT_TRIG_PIN, US_FRONT_MIDDLE_ECHO_PIN, US_FRONT_MIDDLE_TRIG_PIN, US_FRONT_LEFT_ECHO_PIN, US_BACK_RIGHT_TRIG_PIN, US_BACK_RIGHT_ECHO_PIN, US_BACK_LEFT_TRIG_PIN, US_BACK_LEFT_ECHO_PIN, US_CENTER_RIGHT_TRIG_PIN, US_CENTER_RIGHT_ECHO_PIN, US_CENTER_LEFT_TRIG_PIN, US_CENTER_LEFT_ECHO_PIN
from .config import SERVO_CHANNELS
from .config import REED_SWITCH_PIN
from .config import CENTER_RIGHT_CLAW_NAME, CENTER_LEFT_CLAW_NAME, OUTER_RIGHT_CLAW_NAME, OUTER_LEFT_CLAW_NAME, CENTER_RIGHT_CLAW_ADAFRUIT_PIN, CENTER_LEFT_CLAW_ADAFRUIT_PIN, OUTER_RIGHT_CLAW_ADAFRUIT_PIN, OUTER_LEFT_CLAW_ADAFRUIT_PIN
from .config import PLANK_PUSHER_RIGHT_NAME, PLANK_PUSHER_LEFT_NAME, PLANK_PUSHER_RIGHT_ADAFRUIT_PIN, PLANK_PUSHER_LEFT_ADAFRUIT_PIN, BANNER_DEPLOYER_NAME, BANNER_DEPLOYER_ADAFRUIT_PIN
from .config import REED_SWITCH_PIN
from .config import STEPPER_DIR_PIN, STEPPER_STEP_PIN, STEPPER_MS1_PIN, STEPPER_MS2_PIN, STEPPER_MS3_PIN
# from .config import STEPPER_BOTTOM_LIMIT_PIN, STEPPER_TOP_LIMIT_PIN
from .config import DEFAULT_SCORE
from .constants import USPosition
from .fsm.FSM import RobotFSM
from .hardware.motorsControl import MotorsControl as Motors
from .hardware.servoControl import ServoControl
from .hardware.lcd import LCD
from .hardware.adafruitServoController import AdafruitServoControl
from .hardware.ultrasonicController import UltrasonicController
from .hardware.reedSwitch import reedSwitch
from .hardware.steppermotor import StepperMotor


class Robot:
    """
    Class representing the robot, including its Finite State Machine (FSM), hardware components and characteristics.

    """

    def __init__(self, logger, color: str, score: int = DEFAULT_SCORE):
        self.color = color

        self.motor = Motors(LEFT_MOTOR_FORWARD_PIN, LEFT_MOTOR_BACKWARD_PIN, LEFT_MOTOR_EN_PIN,
                            RIGHT_MOTOR_FORWARD_PIN, RIGHT_MOTOR_BACKWARD_PIN, RIGHT_MOTOR_EN_PIN)
        self.servoControl = AdafruitServoControl(channels=SERVO_CHANNELS,
                                                 names=[CENTER_RIGHT_CLAW_NAME, CENTER_LEFT_CLAW_NAME, OUTER_RIGHT_CLAW_NAME, OUTER_LEFT_CLAW_NAME,
                                                        PLANK_PUSHER_RIGHT_NAME, PLANK_PUSHER_LEFT_NAME, HINGE_NAME, BANNER_DEPLOYER_NAME
                                                  ],
                                                 pins=[CENTER_RIGHT_CLAW_ADAFRUIT_PIN, CENTER_LEFT_CLAW_ADAFRUIT_PIN, OUTER_RIGHT_CLAW_ADAFRUIT_PIN, OUTER_LEFT_CLAW_ADAFRUIT_PIN,
                                                       PLANK_PUSHER_RIGHT_ADAFRUIT_PIN, PLANK_PUSHER_LEFT_ADAFRUIT_PIN, HINGE_ADAFRUIT_PIN, BANNER_DEPLOYER_ADAFRUIT_PIN
                                                  ])
        
        # The stepper was disconnected because of a lack of pins (lacking a pin to connect the enable pin)

        # self.stepper = StepperMotor(step=STEPPER_STEP_PIN, dir=STEPPER_DIR_PIN,
        #                             ms1=STEPPER_MS1_PIN, ms2=STEPPER_MS2_PIN, ms3=STEPPER_MS3_PIN,
        #                             step_delay=0.003, microstep=2,
        #                             top_limit_pin=STEPPER_TOP_LIMIT_PIN, bottom_limit_pin=STEPPER_BOTTOM_LIMIT_PIN)
        self.lcd = LCD()
        self.camera = None
        self.ultrasonicController = UltrasonicController()
        self.ultrasonicController.add_sensor(USPosition.FRONT_RIGHT, US_FRONT_RIGHT_ECHO_PIN, US_FRONT_RIGHT_TRIG_PIN)
        self.ultrasonicController.add_sensor(USPosition.FRONT_MIDDLE, US_FRONT_MIDDLE_ECHO_PIN, US_FRONT_MIDDLE_TRIG_PIN)
        self.ultrasonicController.add_sensor(USPosition.FRONT_LEFT, US_FRONT_LEFT_ECHO_PIN, US_FRONT_LEFT_TRIG_PIN)
        self.ultrasonicController.add_sensor(USPosition.BACK_RIGHT, US_BACK_RIGHT_ECHO_PIN, US_BACK_RIGHT_TRIG_PIN)
        self.ultrasonicController.add_sensor(USPosition.BACK_LEFT, US_BACK_LEFT_ECHO_PIN, US_BACK_LEFT_TRIG_PIN)
        self.ultrasonicController.add_sensor(USPosition.CENTER_RIGHT, US_CENTER_RIGHT_ECHO_PIN, US_CENTER_RIGHT_TRIG_PIN)
        self.ultrasonicController.add_sensor(USPosition.CENTER_LEFT, US_CENTER_LEFT_ECHO_PIN, US_CENTER_LEFT_TRIG_PIN)
        
        self.reedSwitch = reedSwitch(REED_SWITCH_PIN)

        self.score = score
        self.lcd.write_score(self.score)

        self.logger = logger

        self.logger.info(f"Robot score: {self.score}")
        self.logger.info(f"Robot color: {self.color}")

        self.fsm = RobotFSM(self)

