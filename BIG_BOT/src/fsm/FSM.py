from .state_factory import StateFactory
from ..constants import StateEnum, USEvent, MAX_TIME
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .states.State import State
    from ..robot import Robot


class RobotFSM:
    """
    Finite State Machine (FSM) of the robot.

    Parameters
    ----------
    `robot` : Robot
        The robot instance that uses the FSM.
    """

    def __init__(self, robot: 'Robot'):
        self.robot = robot
        self.state_factory = StateFactory(self)

        self.current_state: 'State' = self.state_factory.get_state(StateEnum.IDLE)
        self.current_state.enter()
        self.paused_state: StateEnum | None = None

        self.start_match: bool = True  # TODO: Set to False
        self.start_time: float = time.time()  # TODO: Change to 0.0

    def set_state(self, new_state: StateEnum) -> None:
        """
        Set the current state of the FSM to the new specified state.

        Parameters
        ----------
        new_state : StateEnum
            The new state to switch to.
        """
        self.current_state.exit()
        self.current_state = self.state_factory.get_state(new_state)
        self.current_state.enter()

    def update(self) -> None:
        """
        Execute the current state of the FSM.
        """
        us_event = self.robot.ultrasonicController.checkObstacle()
        if us_event == USEvent.OBSTACLE_DETECTED:
            self.paused_state = self.current_state.enum
            self.set_state(StateEnum.AVOID_OBSTACLE)
        elif us_event == USEvent.OBSTACLE_CLEARED:
            if self.paused_state is not None:
                self.set_state(self.paused_state)  # Return to pre-obstacle state
                self.paused_state = None

        if self.start_match and (time.time() - self.start_time >= MAX_TIME):
            self.set_state(StateEnum.STOP)

        elif self.start_match and (time.time() - self.start_time >= 22.0):
            self.set_state(StateEnum.OPEN_CLAW)

        elif self.start_match and (time.time() - self.start_time >= 14.0):
            self.set_state(StateEnum.CLOSE_CLAW)

        elif self.start_match and (time.time() - self.start_time >= 12.0):
            self.set_state(StateEnum.OPEN_CLAW)

        elif self.start_match and (time.time() - self.start_time >= 11.0):
            self.set_state(StateEnum.STOP)

        elif self.start_match and (time.time() - self.start_time >= 10.0):
            self.set_state(StateEnum.MOVE)

        elif self.start_match and (time.time() - self.start_time >= 6.0):
            self.set_state(StateEnum.ROTATE)

        elif self.start_match and (time.time() - self.start_time >= 5.0):
            self.set_state(StateEnum.STOP)

        self.current_state.execute()
