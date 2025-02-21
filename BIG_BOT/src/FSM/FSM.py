from .State import State
from .detectionStates import DetectTargetsState, CheckObstaclesState
from .collectStates import CollectState, MoveToCollectState
from .dropStates import MoveToDrop, DropState
from .movementStates import MoveState, StopState, RotateState, SlowMoveState, SlowRotateState, AvoidObstacleState, DetectTargetsState, CheckObstaclesState


class RobotFSM:
    def __init__(self, lMotorControl, rMotorControl):
        self.lMotorControl = lMotorControl
        self.righMotorControl = rMotorControl
        # Save all states as attributes of the FSM
        self.detect_targets_state = DetectTargetsState(self, {}, [lMotorControl, rMotorControl])
        self.check_obstacles_state = CheckObstaclesState(self)
        self.collect_state = CollectState(self)
        self.move_to_collect_state = MoveToCollectState(self)
        self.move_to_drop_state = MoveToDrop(self)
        self.drop_state = DropState(self)
        self.move_state = MoveState(self, {}, [lMotorControl, rMotorControl])
        self.stop_state = StopState(self, {}, [lMotorControl, rMotorControl])
        self.rotate_state = RotateState(self, {})
        self.slow_move_state = SlowMoveState(self, {})
        self.slow_rotate_state = SlowRotateState(self, {})
        self.avoid_obstacle_state = AvoidObstacleState(self, {})

        self.current_state: State = self.detect_targets_state
        self.current_state.enter()

    def on_event(self, event):
        self.current_state = self.current_state.on_event(event)  # type: ignore
        self.current_state.enter()

    def set_state(self, new_state: State):
        self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()

    def update(self):
        """Call this periodically to update the FSM"""
        self.current_state.execute()


# Example usage
if __name__ == "__main__":
    fsm = RobotFSM()
