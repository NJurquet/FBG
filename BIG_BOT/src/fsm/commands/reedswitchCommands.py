from .command import ICommand
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class ReedSwitchCommand(ICommand):
    """Command to detect a change in the reed switch value, it keeps the robot in a loop until the value change."""
    def __init__(self, fsm: 'RobotFSM',):
        self._is_finished = False
        self.fsm = fsm

    def execute(self):
        #Stays stucked in a loop if the reedswitch value doesn't change
        value = self.fsm.robot.reedSwitch.read()
        new_value = value
        while value == new_value:
            time.sleep(0.01)
            new_value = self.fsm.robot.reedSwitch.read()
        print(f"ReedSwitch value changed from {value} to {new_value}")
        self.finished()
    
    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
    
    def finished(self):
        self.stop()
        self.fsm.start_time = time.time()
        self.fsm.start_match = True
        self._is_finished = True

        print("ReedSwitchCommand finished")

