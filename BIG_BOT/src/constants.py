"""
constants.py

This module contains all constants used throughout the project.

THIS FILE SHOULD NOT BE MODIFIED EXCEPT FOR ADDING NEW CONSTANTS. ALL CONFIGURATION SHOULD BE DONE IN config.py.
"""

from enum import Enum


class StateEnum(Enum):
    """
    Enumeration of all possible states of the robot.
    """
    IDLE = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2
    ROTATE_LEFT = 3
    ROTATE_RIGHT = 4
    OPEN_CLAW = 5
    CLOSE_CLAW = 6
    AVOID_OBSTACLE = 7
    STOP = 8
    SLOW_MOVE = 9
    FAST_MOVE = 10


class USPosition(Enum):
    """
    Enumeration of all possible positions of the ultrasonic sensors.
    """
    FRONT_RIGHT = 0
    FRONT_LEFT = 1
    BACK_RIGHT = 2
    BACK_LEFT = 3


class USEvent(Enum):
    """
    Enumeration of all possible events that can occur with the ultrasonic sensors.
    """
    OBSTACLE_DETECTED = 1
    OBSTACLE_PRESENT = 2
    OBSTACLE_CLEARED = 3
    NO_EVENT = 4


MAX_TIME: float = 100.0
"""Maximum time for the match in seconds."""
