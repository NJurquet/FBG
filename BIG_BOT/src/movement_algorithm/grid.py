import numpy as np
from enum import Enum

class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    PLANK = 2
    START_ZONE = 4
    DROP_ZONE = 5
    END_ZONE = 6
    ROBOT = 7
    ADVERSARY = 8

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class TeamColor(Enum):
    YELLOW = 0
    BLUE = 1

class StartingZone(Enum):
    UP = 0
    CENTER = 1
    DOWN = 2

class Grid:
    def __init__(self, width = 3000, height= 2000, robot_position=(0, 0)):
        self.width = width
        self.height = height
        # Position is centered in (0, 0) which is in the upper left corner of the grid
        self.grid = np.zeros((height, width), dtype=int)  # Note: height is rows (y), width is columns (x)
        self.robot_position = robot_position

    def set_cell(self, x, y, cell_type):
        """Set the cell at (x, y) to the specified cell type."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = cell_type.value
        else:
            raise ValueError("Coordinates out of bounds")
        
    def set_cells(self, x1, x2, y1, y2, cell_type):
        """Set a rectangular region of cells to the specified cell type."""
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(self.width, x2)
        y2 = min(self.height, y2)
        
        if x1 < x2 and y1 < y2:
            self.grid[y1:y2, x1:x2] = cell_type.value
        else:
            raise ValueError("Invalid rectangle dimensions")
        
    def move_robot(self, x, y, direction):
        """Move to the specified coordinates & direction."""
        self.robot_position = (x, y)
        self.robot_direction = direction
        self.set_cell(x, y, CellType.ROBOT)

    def get_cell(self, x, y):
        """Get the cell type at (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return CellType(self.grid[y, x])
        else:
            raise ValueError("Coordinates out of bounds")
        
    def get_robot_position(self):
        """Get the robot's current position."""
        return self.robot_position
    
    def print_grid(self, region=None):
        """
        Print a portion of the grid for debugging
        region: tuple (x1, y1, x2, y2) defining the region to print
        """
        if region:
            x1, y1, x2, y2 = region
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(self.width, x2)
            y2 = min(self.height, y2)
        else:
            # If grid is too large, print a portion around the robot
            rx, ry = self.robot_position
            x1 = max(0, rx - 10)
            y1 = max(0, ry - 10)
            x2 = min(self.width, rx + 11)
            y2 = min(self.height, ry + 11)
        
        symbols = {
            CellType.EMPTY.value: '.',
            CellType.OBSTACLE.value: 'X',
            CellType.PLANK.value: 'P',
            CellType.START_ZONE.value: 'S',
            CellType.DROP_ZONE.value: 'D',
            CellType.END_ZONE.value: 'E',
            CellType.ROBOT.value: 'R',
            CellType.ADVERSARY.value: 'A'
        }
        
        print(f"Grid section from ({x1},{y1}) to ({x2-1},{y2-1}):")
        for y in range(y1, y2):
            row = ''
            for x in range(x1, x2):
                row += symbols[self.grid[y, x]] + ' '
            print(row)
        

