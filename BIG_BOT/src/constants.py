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
    STOP = 2


MAX_TIME: float = 100.0
"""Maximum time for the match in seconds."""
