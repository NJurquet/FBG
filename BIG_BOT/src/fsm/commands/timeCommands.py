from .command import ITimeBasedCommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class WaitCommand(ITimeBasedCommand):
    """Command to wait for a certain amount of time."""
    def __init__(self, fsm: 'RobotFSM', time_needed: float = 0.0):
        self._is_finished = False
        self.fsm = fsm
        self.time_needed = time_needed

    def execute(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True


class WaitForTargetTimeCommand(ITimeBasedCommand):
    """Command to wait for a certain moment to arrive."""
    def __init__(self, fsm: 'RobotFSM', time_target: float = 0.0):
        self._is_finished = False
        self.fsm = fsm
        self.time_target = time_target

        time_needed = self.time_target - self.fsm.match_time
        if time_needed < 0:
            self.time_needed = 0
        else:
            self.time_needed = time_needed
            
    def execute(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True