import numpy as np
from enum import Enum

class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    PLANK = 2
    DROP_ZONE = 4
    END_ZONE = 5
    ROBOT = 6

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=int)