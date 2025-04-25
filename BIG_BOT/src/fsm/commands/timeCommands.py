from .command import ITimeBasedCommand
from ...constants import USPosition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class WaitCommand(ITimeBasedCommand):
    """Command to wait for a certain amount of time."""
    def __init__(self, fsm: 'RobotFSM', time_needed: float = 0.0, enable_sensors: bool = False):
        self._is_finished = False
        self.fsm = fsm
        self.time_needed = time_needed
        self.enable_sensors = enable_sensors

        self.sensors_to_enable = self.fsm.robot.ultrasonicController.get_enabled_sensors()

        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_MIDDLE)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)

    def execute(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        for pos, en in self.sensors_to_enable.items():
            if en:
                self.fsm.robot.ultrasonicController.enable_sensor(pos)

        if self.enable_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)

    def finished(self):
        self.stop()
        self._is_finished = True


class WaitForTargetTimeCommand(ITimeBasedCommand):
    """Command to wait for a certain moment to arrive."""
    def __init__(self, fsm: 'RobotFSM', time_target: float = 0.0):
        self._is_finished = False
        self.fsm = fsm
        self.time_target = time_target
            
    def execute(self):
        time_needed = self.time_target - self.fsm.match_time

        if time_needed <= 0:
            self.time_needed = 0
        else:
            self.time_needed = time_needed
        print("Time needed before target:", self.time_needed)
        self.fsm.robot.logger.info(f"WaitForTargetTimeCommand : Time needed before target: {self.time_needed}")

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True