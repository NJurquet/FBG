from .State import State
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class CollectState(State):
    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)
        # super().__init__("Collect", None)

    def on_event(self, event) -> None:
        if event == 'collected':
            pass

    def enter(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def collect(self):
        print("Collecting")


class MoveToCollectState(State):
    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)
        # super().__init__("Move to Collect", None)

    def on_event(self, event) -> None:
        if event == 'on_position':
            pass

    def enter(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def exit(self) -> None:
        pass
