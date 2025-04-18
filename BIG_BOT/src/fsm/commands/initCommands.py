from .command import ICommand
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class InitLCDCommand(ICommand):
    """."""
    def __init__(self, fsm: 'RobotFSM',):
        self._is_finished = False
        self.fsm = fsm

    def execute(self):
        print("Resetting LCD...")
        self.fsm.robot.lcd.clear()
        self.fsm.robot.lcd.write_score(self.fsm.robot.score)

        self.finished()
    
    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
    
    def finished(self):
        self.stop()
        self._is_finished = True


