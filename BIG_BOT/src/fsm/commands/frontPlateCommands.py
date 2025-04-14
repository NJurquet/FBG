from .command import ICommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class InitFrontPlateCommand(ICommand):
    def __init__(self, fsm:'RobotFSM'):
        self._is_finished = False
        self.fsm = fsm

    def execute(self):
        self.fsm.robot.stepper.home_bottom()
        self.time_needed = 1.0

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True


class RaiseFrontPlateCommand(ICommand):
    def __init__(self, fsm:'RobotFSM'):
        self._is_finished = False
        self.fsm = fsm

    def execute(self):
        self.fsm.robot.stepper.move_to_top()
        self.time_needed = 1.0

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True


class LowerFrontPlateCommand(ICommand):
    def __init__(self, fsm:'RobotFSM'):
        self._is_finished = False
        self.fsm = fsm

    def execute(self):
        self.fsm.robot.stepper.move_to_bottom()
        self.time_needed = 1.0

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True


class MoveFrontPlateCommand(ICommand):
    def __init__(self, fsm:'RobotFSM', position: int):
        self._is_finished = False
        self.fsm = fsm
        self.current_position = self.fsm.robot.stepper.current_position
        self.target_position = position

    def execute(self):
        if self.current_position != self.target_position:
            self.fsm.robot.stepper.move_to_position(self.target_position)
        self.time_needed = 1.0

    def pause(self):
        pass

    def resume(self):
        self.current_position = self.fsm.robot.stepper.current_position
        if self.current_position != self.target_position:
            self.fsm.robot.stepper.move_to_position(self.target_position)
        self.time_needed = 1.0

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True