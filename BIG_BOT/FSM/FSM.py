from State import State
from detectionStates import DetectTargetsState, CheckObstaclesState
from collectStates import CollectState, MoveToCollectState
from dropStates import MoveToDrop, DropState


class RobotFSM:
    def __init__(self):
        self.state = DetectTargetsState()
        self.state.enter()

    def on_event(self, event):
        self.state = self.state.on_event(event)
        self.state.enter()

# Example usage
if __name__ == "__main__":
    fsm = RobotFSM()
    fsm.on_event("targets_detected")