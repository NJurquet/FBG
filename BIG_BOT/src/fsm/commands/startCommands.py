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
        self.timer = None
        self.fsm = fsm
        self._is_finished = False

        self.color = color
        
    def execute(self) -> MyTimer:
        # Initialize the robot
        self.fsm.start_match = True
        return MyTimer(0.5, self.finished)
    
    def pause(self):
        if self.timer:
            self.timer.pause()
        self.fsm.robot.motor.stop()

    def resume(self):
        if self.timer:
            self.timer.resume(self.finished)

    def stop(self):
        self.fsm.robot.motor.stop()
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def finished(self):
        self._is_finished = True
    