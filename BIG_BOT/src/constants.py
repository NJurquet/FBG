"""
constants.py

This module contains all constants used throughout the project.

THIS FILE SHOULD NOT BE MODIFIED EXCEPT FOR ADDING NEW CONSTANTS. ALL CONFIGURATION SHOULD BE DONE IN config.py.
"""

from enum import Enum

class USPosition(Enum):
    """
    Enumeration of all possible positions of the ultrasonic sensors.
    """
    FRONT_RIGHT = 0
    FRONT_MIDDLE = 1
    FRONT_LEFT = 2
    BACK_RIGHT = 3
    BACK_LEFT = 4
    CENTER_RIGHT = 5
    CENTER_LEFT = 6


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
