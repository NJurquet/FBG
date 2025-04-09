from .command import ICommand
from ...constants import StateEnum
from ..myTimer import MyTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class InitCommand(ICommand):
    """
    Command to initialize the robot.
    """
    def __init__(self, fsm: 'RobotFSM', color):
        self.fsm = fsm
        self._is_finished = False

        self.color = color
        
    def execute(self) -> float:
        self.fsm.start_match = True
        return 0.2
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        pass

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self._is_finished = True
    