from .command import ICommand
from ...constants import StateEnum
from ..myTimer import MyTimer
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class ReedSwitchCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM',):
        self._is_finished = False
        self.fsm = fsm


    def execute(self) -> None:
        #Stays stucked in a loop if hte reedswitch value doesn't change
        value = self.fsm.robot.reedSwitch.read()
        new_value = value
        while value == new_value:
            time.sleep(0.01)
            new_value = self.fsm.robot.reedSwitch.read()
        print("ReedSwitch value changed")

    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
    
    def finished(self):
        self.stop()
        self._is_finished = True

