from .state_factory import StateFactory
from ..constants import StateEnum, MAX_TIME
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .states.State import State
    from ..robot import Robot


class RobotFSM:
    def __init__(self, robot: 'Robot'):
        self.robot = robot
        self.state_factory = StateFactory(self)

        self.current_state: 'State' = self.state_factory.get_state(StateEnum.IDLE)
        self.current_state.enter()

        self.start_match: bool = False
        self.start_time: float = 0.0

    def set_state(self, new_state: StateEnum) -> None:
        self.current_state.exit()
        self.current_state = self.state_factory.get_state(new_state)
        self.current_state.enter()

    def update(self) -> None:
        """Call this periodically to update the FSM"""
        if self.start_match and (time.time() - self.start_time >= MAX_TIME):
            self.set_state(StateEnum.STOP)

        self.current_state.execute()
