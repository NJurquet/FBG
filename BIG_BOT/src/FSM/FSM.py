from State import State
from detectionStates import DetectTargetsState, CheckObstaclesState
from collectStates import CollectState, MoveToCollectState
from dropStates import MoveToDrop, DropState


class RobotFSM:
    def __init__(self):
        self.current_state = DetectTargetsState()
        self.current_state.enter()

    def on_event(self, event):
        self.current_state = self.current_state.on_event(event)
        self.current_state.enter()


# Example usage
if __name__ == "__main__":
    fsm = RobotFSM()
    fsm.on_event("targets_detected")
