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
    MOVE = 1
    ROTATE = 2
    OPEN_CLAW = 3
    CLOSE_CLAW = 4
    AVOID_OBSTACLE = 5
    STOP = 6


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
    OBSTACLE_CLEARED = 2
    NO_EVENT = 3


MAX_TIME: float = 100.0
"""Maximum time for the match in seconds."""
