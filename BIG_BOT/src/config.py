"""
config.py

This module contains all configuration constants used throughout the project.
It serves as a centralized location for managing settings and values that are used in multiple parts of the project.
Change these config constants to customize the behavior of the robot.
"""

# ===================================================================
# Hardware Pins Configuration
# ===================================================================

## I2C Bus Pins ##
I2C_DATA_PIN = 2
I2C_CLOCK_PIN = 3

## Motor Pins ##

LEFT_MOTOR_FORWARD_PIN = 5
LEFT_MOTOR_BACKWARD_PIN = 6
LEFT_MOTOR_EN_PIN = 19  # PWM

RIGHT_MOTOR_FORWARD_PIN = 17
RIGHT_MOTOR_BACKWARD_PIN = 27
RIGHT_MOTOR_EN_PIN = 18  # PWM

# Motor driver to motor connection :
#   - OUT 1 -> Left motor red pin
#   - OUT 2 -> Left motor black pin
#   - OUT 3 -> Right motor red pin
#   - OUT 4 -> Right motor black pin


# Adafruit Servo Controller Channels
SERVO_CHANNELS = 16

## Servo Claws ##
CENTER_RIGHT_CLAW_NAME = "centerRightClaw"
CENTER_LEFT_CLAW_NAME = "centerLeftClaw"
OUTER_RIGHT_CLAW_NAME = "outerRightClaw"
OUTER_LEFT_CLAW_NAME = "outerLeftClaw"

CENTER_RIGHT_CLAW_ADAFRUIT_PIN = 0
CENTER_LEFT_CLAW_ADAFRUIT_PIN = 1
OUTER_RIGHT_CLAW_ADAFRUIT_PIN = 2
OUTER_LEFT_CLAW_ADAFRUIT_PIN = 3

## Servo PlankPushers ##
PLANK_PUSHER_RIGHT_NAME = "plankPusherRight"
PLANK_PUSHER_LEFT_NAME = "plankPusherLeft"

PLANK_PUSHER_RIGHT_ADAFRUIT_PIN = 4
PLANK_PUSHER_LEFT_ADAFRUIT_PIN = 5

## Servo Hinge ##
HINGE_NAME = "hinge"

HINGE_ADAFRUIT_PIN = 6

## Servo Banner Deployer ##
BANNER_DEPLOYER_NAME = "bannerDeployer"

BANNER_DEPLOYER_ADAFRUIT_PIN = 7

## Ultrasonic Sensors Pins ##
US_FRONT_RIGHT_TRIG_PIN = 7
US_FRONT_RIGHT_ECHO_PIN = 8

US_FRONT_LEFT_TRIG_PIN = 20
US_FRONT_LEFT_ECHO_PIN = 21

US_BACK_RIGHT_TRIG_PIN = 16
US_BACK_RIGHT_ECHO_PIN = 25

US_BACK_LEFT_TRIG_PIN = 23
US_BACK_LEFT_ECHO_PIN = 24

# Reed Switch Pin
REED_SWITCH_PIN = 26

# ===================================================================
# Robot Configuration
# ===================================================================

DEFAULT_SCORE = 73
"""Default score for the robot if nothing is passed as command line argument."""

MAX_OBSTACLE_DURATION = 5.0  # seconds
"""Maximum duration (in seconds) of obstacle detection, after which the robot should take action."""
