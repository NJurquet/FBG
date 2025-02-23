from .fsm.FSM import RobotFSM
from .bigMotorControl import BigMotorControl as Motors


class Robot:
    def __init__(self):
        self.fsm = RobotFSM(self)
        self.motor = Motors()
        # self.camera = None

        self.__position: tuple[int, int] = (0, 0)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value: tuple[int, int]):
        if isinstance(value, tuple) and len(value) == 2:
            self.__position = value
        else:
            raise ValueError("Position must be a tuple of the x and y coordinates (x, y).")
