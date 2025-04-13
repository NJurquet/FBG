from .command import ICommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class InitCommand(ICommand):
    """
    Command to initialize the robot.
    """
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        self._is_finished = False
        
    def execute(self):
        self.time_needed = 0.2
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.time_needed = 0.2

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self._is_finished = True
    