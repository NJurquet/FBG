from .State import State
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class CollectState(State):
    """
    State in which the robot closes his grippers to collect the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)

    def on_event(self, event) -> None:
        if event == 'collected':
            pass

    @override
    def enter(self) -> None:
        pass

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        pass

    def collect(self):
        print("Collecting")


class MoveToCollectState(State):
    """
    State in which the robot moves to the position of available cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)

    def on_event(self, event) -> None:
        if event == 'on_position':
            pass

    @override
    def enter(self) -> None:
        pass

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        pass
