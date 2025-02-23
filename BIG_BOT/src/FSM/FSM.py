# from .detectionStates import DetectTargetsState, CheckObstaclesState
# from .collectStates import CollectState, MoveToCollectState
# from .dropStates import MoveToDrop, DropState
# from .movementStates import MoveState, StopState, RotateState, SlowMoveState, SlowRotateState, AvoidObstacleState, DetectTargetsState, CheckObstaclesState
from .state_factory import StateFactory
from ..constants import StateEnum, MAX_TIME
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .State import State
    from ..robot import Robot


class RobotFSM:
    def __init__(self, robot: 'Robot'):
        self.robot = robot
        self.state_factory = StateFactory(self)

        # Save all states as attributes of the FSM
        # self.detect_targets_state = DetectTargetsState(self)
        # self.check_obstacles_state = CheckObstaclesState(self)
        # self.collect_state = CollectState(self)
        # self.move_to_collect_state = MoveToCollectState(self)
        # self.move_to_drop_state = MoveToDrop(self)
        # self.drop_state = DropState(self)
        # self.move_state = MoveState(self, {})
        # self.stop_state = StopState(self, {})
        # self.rotate_state = RotateState(self, {})
        # self.slow_move_state = SlowMoveState(self, {})
        # self.slow_rotate_state = SlowRotateState(self, {})
        # self.avoid_obstacle_state = AvoidObstacleState(self, {})

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
