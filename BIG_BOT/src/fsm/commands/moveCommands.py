from .command import ICommand
from ...constants import StateEnum
from ..myTimer import MyTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class MoveForwardCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', distance: float, speed: float):
        self.fsm = fsm
        self.distance = distance
        self.speed = speed

    def execute(self) -> float:
        # Get the time needed directly from the motor controller
        time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
        self.fsm.set_state(StateEnum.MOVE_FORWARD, distance=self.distance, speed=self.speed)
        return time_needed

class MoveBackwardCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', distance: float, speed: float):
        self.fsm = fsm
        self.distance = distance
        self.speed = speed

    def execute(self) -> float:
        # Get the time needed directly from the motor controller
        time_needed = self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)
        self.fsm.set_state(StateEnum.MOVE_BACKWARD, distance=self.distance, speed=self.speed)
        return time_needed

class RotateLeftCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', degrees: float, speed: float):
        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self) -> float:
        time_needed = self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)
        self.fsm.set_state(StateEnum.ROTATE_LEFT, degrees=self.degrees, speed=self.speed)
        return time_needed

class RotateRightCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', degrees: float, speed: float):
        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self) -> float:
        time_needed = self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)
        self.fsm.set_state(StateEnum.ROTATE_RIGHT, degrees=self.degrees, speed=self.speed)
        return time_needed

class StopCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.STOP)
        return 0.1  # Minimal time for stop


