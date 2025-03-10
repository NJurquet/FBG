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
    STOP = 5


MAX_TIME: float = 100.0
"""Maximum time for the match in seconds."""
