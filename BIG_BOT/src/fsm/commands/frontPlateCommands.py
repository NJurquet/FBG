from .command import ITimeBasedCommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class InitFrontPlateCommand(ITimeBasedCommand):
    def __init__(self, fsm:'RobotFSM'):
        self._is_finished = False
        self.fsm = fsm
        self.time_needed = 1.0

    def execute(self):
        self.fsm.robot.stepper.home_bottom()

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        self.fsm.robot.stepper.stop()

    def finished(self):
        self._is_finished = True


class RaiseFrontPlateCommand(ITimeBasedCommand):
    def __init__(self, fsm:'RobotFSM'):
        self._is_finished = False
        self.fsm = fsm
        self.time_needed = 1.0

    def execute(self):
        self.fsm.robot.stepper.move_to_top()

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        self.fsm.robot.stepper.stop()

    def finished(self):
        self._is_finished = True


class LowerFrontPlateCommand(ITimeBasedCommand):
    def __init__(self, fsm:'RobotFSM'):
        self._is_finished = False
        self.fsm = fsm
        self.time_needed = 1.0

    def execute(self):
        self.fsm.robot.stepper.move_to_bottom()

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        self.fsm.robot.stepper.stop()

    def finished(self):
        self._is_finished = True


class MoveFrontPlateCommand(ITimeBasedCommand):
    def __init__(self, fsm:'RobotFSM', position: int):
        self._is_finished = False
        self.fsm = fsm
        self.current_position = self.fsm.robot.stepper.current_position
        self.target_position = position
        self.time_needed = 1.0

    def execute(self):
        if self.current_position != self.target_position:
            self.fsm.robot.stepper.move_to_position(self.target_position)

    def pause(self):
        pass

    def resume(self):
        self.current_position = self.fsm.robot.stepper.current_position
        if self.current_position != self.target_position:
            self.fsm.robot.stepper.move_to_position(self.target_position)

    def stop(self):
        pass

    def finished(self):
        self._is_finished = True