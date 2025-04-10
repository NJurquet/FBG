from .command import ICommand
from ...constants import USPosition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class UltrasonicSensorCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', pos: USPosition, enable: bool):
        self.fsm = fsm
        self.pos = pos
        self.enable = enable

    def execute(self) -> float:
        if self.enable:
            self.fsm.robot.ultrasonicController.enable_sensor(self.pos)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(self.pos)
        return 0.2  #Small delay just to be sure

    def pause(self):
        pass  # No action needed for pause

    def resume(self):
        pass  # No action needed for resume

    def stop(self):
        pass  # No action needed for stop

    def finished(self):
        pass  # No action needed for finished
