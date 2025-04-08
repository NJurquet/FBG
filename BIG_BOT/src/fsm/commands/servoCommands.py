from .command import ICommand
from ...constants import StateEnum
from ..myTimer import MyTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class OpenClawCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.OPEN_CLAW)
        return 2   # Minimal time for opening claw

class CloseClawCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.CLOSE_CLAW)
        return 2  # Minimal time for closing claw