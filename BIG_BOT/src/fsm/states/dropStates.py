from .State import State
from .detectionStates import DetectTargetsState
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class DropState(State):
    """
    State in which the robot opens his grippers to drop the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    
    **Methods**:
        drop(): Opens the grippers to drop the cans.
    """

    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'targets_detected':
            return DetectTargetsState(self.fsm)
        return self

    @override
    def enter(self):
        pass

    @override
    def execute(self):
        pass

    @override
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

    **Methods**:
    
    """

    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'drop':
            return DropState(self.fsm)
        return self

    @override
    def enter(self):
        pass

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass
