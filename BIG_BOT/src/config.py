"""
config.py

This module contains all configuration constants used throughout the project.
It serves as a centralized location for managing settings and values that are used in multiple parts of the project.
Change these config constants to customize the behavior of the robot.
"""

# =============================================================================
# Hardware Pins Configuration
# =============================================================================

# Motor Pins
LEFT_MOTOR_FORWARD_PIN = 17
LEFT_MOTOR_BACKWARD_PIN = 27
LEFT_MOTOR_EN_PIN = 2

RIGHT_MOTOR_FORWARD_PIN = 13
RIGHT_MOTOR_BACKWARD_PIN = 19
RIGHT_MOTOR_EN_PIN = 6

# Servo Names
CENTER_RIGHT_CLAW_NAME = "centerRightClaw"

# Servo Claws Pins
#CENTER_RIGHT_CLAW_PIN = 12

# Adafruit Servo Controller Channels
SERVO_CHANNELS = 16

# Servo Claws Adafruit Pins
CENTER_RIGHT_CLAW_ADAFRUIT_PIN = 0

# Ultrasonic Sensors Pins
US_FRONT_RIGHT_TRIG_PIN = 0
US_FRONT_RIGHT_ECHO_PIN = 0

US_FRONT_LEFT_TRIG_PIN = 0
US_FRONT_LEFT_ECHO_PIN = 0

US_BACK_RIGHT_TRIG_PIN = 0
US_BACK_RIGHT_ECHO_PIN = 0

US_BACK_LEFT_TRIG_PIN = 0
US_BACK_LEFT_ECHO_PIN = 0
