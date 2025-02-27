from .State import State
from .detectionStates import DetectTargetsState


class DropState(State):
    """
    State in which the robot opens his grippers to drop the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'targets_detected':
            return DetectTargetsState(self.fsm)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass

    def drop(self):
        print("Dropping")


class MoveToDrop(State):
    """
    State in which the robot moves to a targeted construction zone to drop the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'drop':
            return DropState(self.fsm)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass
