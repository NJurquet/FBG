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
        self.fsm.robot.servo_control.setAngle(self.name, self.angle)
        # Assuming the time needed to set the angle is negligible or predefined
        time_needed = 0.0  # You can adjust this based on your requirements
        return time_needed

    def pause(self):
        # Stop the specific servo motor
        self.fsm.robot.servo_control.stop(self.name)

    def resume(self):
        # Resume setting the angle of the specific servo motor
        self.fsm.robot.servo_control.setAngle(self.name, self.angle)
        time_needed = 0.0  # You can adjust this based on your requirements
        return time_needed

    def stop(self):
        # Stop the specific servo motor
        self.fsm.robot.servo_control.stop(self.name)

    def finished(self):
        self.stop()
        self._is_finished = True