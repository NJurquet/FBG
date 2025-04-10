from .command import ICommand
from ...constants import StateEnum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SetServoAngleCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', name: str, angle: float):
        self._is_finished = False
        self.fsm = fsm
        self.name = name
        self.angle = angle

    def execute(self) -> float:
        # Set the angle of the specific servo motor
        self.fsm.robot.servoControl.setAngle(self.name, self.angle)
        time_needed = 2.0  
        return time_needed

    def pause(self):
        # Stop the specific servo motor
        self.fsm.robot.servo_control.stop(self.name)

    def resume(self):
        # Resume setting the angle of the specific servo motor
        self.fsm.robot.servoControl.setAngle(self.name, self.angle)
        time_needed = 2.0 
        return time_needed

    def stop(self):
        # Stop the specific servo motor
        pass

    def finished(self):
        self.stop()
        self._is_finished = True

class SetAllServoAnglesCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', angles: List[float]):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

    def execute(self) -> float:
        # Set the angles of ALL the servo motors
        self.fsm.robot.servoControl.setAngles(self.angles)
        time_needed = 2.0  
        return time_needed

    def pause(self):
        # Stop all servo motors
        pass

    def resume(self):
        # Resume setting the angles of the servo motors
        pass

    def stop(self):
        # Stop all servo motors
        pass

    def finished(self):
        self.stop()
        self._is_finished = True