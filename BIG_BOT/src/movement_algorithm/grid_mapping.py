from .grid import Grid, CellType, Direction, TeamColor, StartingZone
from ..config import GRID_WIDTH, GRID_HEIGHT
from ..config import STARTING_ZONE_WIDTH, STARTING_ZONE_HEIGHT, V_DROP_ZONE_WIDTH, V_DROP_ZONE_HEIGHT, H_DROP_ZONE_WIDTH, H_DROP_ZONE_HEIGHT
from ..config import V_PLANK_WIDTH, V_PLANK_HEIGHT, H_PLANK_WIDTH, H_PLANK_HEIGHT
from ..config import PAMI_STARTING_ZONE_WIDTH, PAMI_STARTING_ZONE_HEIGHT

class GridMapping:
    """
    GridMapping class to manage the robot's grid and its position.
    Will be usefull if we manage to implement a pathfinding algorithm & camera.

    Parameters:
        beginning_colour (Enum): The color of the robot team. Can be "yellow" or "blue".
        beginning_zone (Enum): The position of the starting zone. Can be "up", "center" or "down".
    
    Attributes:
        grid (Grid): The grid object representing the environment.
        robot_position (tuple): The current position of the robot in the grid.
        robot_direction (Direction): The current direction of the robot.
    """
    
    def __init__(self, beginning_colour=TeamColor.YELLOW, beginning_zone=StartingZone.UP):
        """"Initialize the GridMapping with the specified team color and starting zone."""

        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT, (0, 0))
        
        # Place the end, starting and drop zones on the grid
        if beginning_colour == TeamColor.YELLOW:
            self.grid.set_cells(PAMI_STARTING_ZONE_WIDTH, STARTING_ZONE_WIDTH, 0, STARTING_ZONE_HEIGHT, CellType.END_ZONE)
            self.grid.set_cells(GRID_WIDTH - STARTING_ZONE_WIDTH, STARTING_ZONE_WIDTH, PAMI_STARTING_ZONE_HEIGHT + V_DROP_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.START_ZONE)
            self.grid.set_cells(2*H_DROP_ZONE_WIDTH + 100, STARTING_ZONE_WIDTH, GRID_HEIGHT - STARTING_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.START_ZONE)

            self.grid.set_cells(H_DROP_ZONE_WIDTH + 100, H_DROP_ZONE_WIDTH, GRID_HEIGHT - H_DROP_ZONE_HEIGHT, H_DROP_ZONE_HEIGHT, CellType.DROP_ZONE)
            self.grid.set_cells(GRID_WIDTH - H_DROP_ZONE_WIDTH, H_DROP_ZONE_WIDTH, GRID_HEIGHT - H_DROP_ZONE_HEIGHT, H_DROP_ZONE_HEIGHT, CellType.DROP_ZONE)        
        
            # Place the robot (not very accurate)
            if beginning_zone == StartingZone.UP:
                self.grid.set_cells(PAMI_STARTING_ZONE_WIDTH, STARTING_ZONE_WIDTH, 0, STARTING_ZONE_HEIGHT, CellType.ROBOT)
                self.grid.robot_direction = Direction.SOUTH
            elif beginning_zone == StartingZone.CENTER:
                self.grid.set_cells(GRID_WIDTH - STARTING_ZONE_WIDTH, STARTING_ZONE_WIDTH, PAMI_STARTING_ZONE_HEIGHT + V_DROP_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.ROBOT)
                self.grid.robot_direction = Direction.WEST
            elif beginning_zone == StartingZone.DOWN:
                self.grid.set_cells(2*H_DROP_ZONE_WIDTH + 100, STARTING_ZONE_WIDTH, GRID_HEIGHT - STARTING_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.ROBOT)
                self.grid.robot_direction = Direction.NORTH

        elif beginning_colour == TeamColor.BLUE:
            self.grid.set_cells(GRID_WIDTH - STARTING_ZONE_WIDTH - PAMI_STARTING_ZONE_WIDTH, STARTING_ZONE_WIDTH, 0, STARTING_ZONE_HEIGHT, CellType.END_ZONE)
            self.grid.set_cells(0, STARTING_ZONE_WIDTH, PAMI_STARTING_ZONE_HEIGHT + V_DROP_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.START_ZONE)
            self.grid.set_cells(GRID_WIDTH - 2*H_DROP_ZONE_WIDTH - 100, STARTING_ZONE_WIDTH, GRID_HEIGHT - STARTING_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.START_ZONE)

            self.grid.set_cells(0, H_DROP_ZONE_WIDTH, GRID_HEIGHT - H_DROP_ZONE_HEIGHT, H_DROP_ZONE_HEIGHT, CellType.DROP_ZONE)
            self.grid.set_cells(GRID_WIDTH - 2*H_DROP_ZONE_WIDTH - 100, H_DROP_ZONE_WIDTH, GRID_HEIGHT - H_DROP_ZONE_HEIGHT, H_DROP_ZONE_HEIGHT, CellType.DROP_ZONE)        

            # Place the robot (not very accurate)
            if beginning_zone == StartingZone.UP:
                self.grid.set_cells(GRID_WIDTH - STARTING_ZONE_WIDTH - PAMI_STARTING_ZONE_WIDTH, STARTING_ZONE_WIDTH, 0, STARTING_ZONE_HEIGHT, CellType, CellType.ROBOT)
                self.grid.robot_direction = Direction.SOUTH
            elif beginning_zone == StartingZone.CENTER:
                self.grid.set_cells(0, STARTING_ZONE_WIDTH, PAMI_STARTING_ZONE_HEIGHT + V_DROP_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.ROBOT)
                self.grid.robot_direction = Direction.EAST
            elif beginning_zone == StartingZone.DOWN:
                self.grid.set_cells(GRID_WIDTH - 2*H_DROP_ZONE_WIDTH - 100, STARTING_ZONE_WIDTH, GRID_HEIGHT - STARTING_ZONE_HEIGHT, STARTING_ZONE_HEIGHT, CellType.ROBOT)
                self.grid.robot_direction = Direction.NORTH

        # Place the planks on the grid
        self.grid.set_cells(PAMI_STARTING_ZONE_WIDTH + STARTING_ZONE_WIDTH, H_DROP_ZONE_WIDTH, STARTING_ZONE_HEIGHT - H_DROP_ZONE_HEIGHT, H_DROP_ZONE_HEIGHT, CellType.PLANK)
        self.grid.set_cells(GRID_WIDTH - PAMI_STARTING_ZONE_WIDTH - STARTING_ZONE_WIDTH - H_DROP_ZONE_WIDTH, H_PLANK_WIDTH, STARTING_ZONE_HEIGHT - H_DROP_ZONE_HEIGHT, H_PLANK_HEIGHT, CellType.PLANK)

        self.grid.set_cells(0, V_PLANK_WIDTH, PAMI_STARTING_ZONE_HEIGHT, V_PLANK_HEIGHT, CellType.PLANK)
        self.grid.set_cells(GRID_WIDTH - V_PLANK_WIDTH, V_PLANK_WIDTH, PAMI_STARTING_ZONE_HEIGHT, V_PLANK_HEIGHT, CellType.PLANK)

        self.grid.set_cells(0, V_PLANK_WIDTH, PAMI_STARTING_ZONE_HEIGHT + V_PLANK_HEIGHT + STARTING_ZONE_HEIGHT, V_PLANK_HEIGHT, CellType.PLANK)
        self.grid.set_cells(GRID_WIDTH - V_PLANK_WIDTH, V_PLANK_WIDTH, PAMI_STARTING_ZONE_HEIGHT + V_PLANK_HEIGHT + STARTING_ZONE_HEIGHT, V_PLANK_HEIGHT, CellType.PLANK)

        self.grid.set_cells(H_DROP_ZONE_WIDTH + 100, H_PLANK_WIDTH, GRID_HEIGHT - H_DROP_ZONE_HEIGHT - H_PLANK_HEIGHT, H_PLANK_HEIGHT, CellType.PLANK)
        self.grid.set_cells(GRID_WIDTH - H_DROP_ZONE_WIDTH - 100 - H_PLANK_WIDTH, H_PLANK_WIDTH, GRID_HEIGHT - H_DROP_ZONE_HEIGHT - H_PLANK_HEIGHT, H_PLANK_HEIGHT, CellType.PLANK)

        # There are 2 more in the middle but i don't know their precise location yet

    def get_robot_position(self):
        """Get the current position of the robot."""
        return self.grid.robot_position
    


