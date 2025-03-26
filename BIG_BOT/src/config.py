"""
config.py

This module contains all configuration constants used throughout the project.
It serves as a centralized location for managing settings and values that are used in multiple parts of the project.
Change these config constants to customize the behavior of the robot.
"""

# =============================================================================
# Hardware Pins Configuration
# =============================================================================

# I2C Bus Pins
I2C_DATA_PIN = 2
I2C_CLOCK_PIN = 3

# Motor Pins
LEFT_MOTOR_FORWARD_PIN = 17
LEFT_MOTOR_BACKWARD_PIN = 27
LEFT_MOTOR_EN_PIN = 18  # PWM

RIGHT_MOTOR_FORWARD_PIN = 5
RIGHT_MOTOR_BACKWARD_PIN = 6
RIGHT_MOTOR_EN_PIN = 19  # PWM

# Servo Names
CENTER_RIGHT_CLAW_NAME = "centerRightClaw"

# Servo Claws Pins
#CENTER_RIGHT_CLAW_PIN = 12

# Adafruit Servo Controller Channels
SERVO_CHANNELS = 16

# Servo Claws Adafruit Pins
CENTER_RIGHT_CLAW_ADAFRUIT_PIN = 0

# Ultrasonic Sensors Pins
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
