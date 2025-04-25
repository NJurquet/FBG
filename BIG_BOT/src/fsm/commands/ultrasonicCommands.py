from .command import ICommand
from ...constants import USPosition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class  DisableUltrasonicSensorsCommand(ICommand):
    """Command to disable specific ultrasonic sensors."""
    def __init__(self, fsm: 'RobotFSM', positions: list[USPosition]):
        self._is_finished = False
        self.fsm = fsm
        self.positions = positions

    def execute(self):
        for position in self.positions:
            self.fsm.robot.ultrasonicController.disable_sensor(position)
        self.fsm.robot.logger.info(f"Sensors : {self.positions} have been disabled")
        self.finished()

    def pause(self):
        pass  # No action needed for pause

    def resume(self):
        pass

    def stop(self):
        pass  # No action needed for stop

    def finished(self):
        self._is_finished = True

class EnableUltrasonicSensorsCommand(ICommand):
    """Command to enable specific ultrasonic sensors."""
    def __init__(self, fsm: 'RobotFSM', positions: list[USPosition]):
        self._is_finished = False
        self.fsm = fsm
        self.positions = positions

    def execute(self):
        for position in self.positions:
            self.fsm.robot.ultrasonicController.enable_sensor(position)
        self.fsm.robot.logger.info(f"Sensors : {self.positions} have been enabled")
        self.finished()

    def pause(self):
        pass  # No action needed for pause

    def resume(self):
        pass

    def stop(self):
        pass  # No action needed for stop

    def finished(self):
        self._is_finished = True

