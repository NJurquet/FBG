from abc import ABC, abstractmethod
from .states.movementStates import (
    FastMoveState,
    RotateLeftState,
    RotateRightState,
    StopState
)
from ..constants import StateEnum
from .myTimer import MyTimer
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .FSM import RobotFSM

class ICommand(ABC):
    @abstractmethod
    def execute(self) -> float:
        """Execute the command and return the time needed for completion"""
        pass

class MoveForwardCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', distance: float, speed: float):
        self.fsm = fsm
        self.distance = distance
        self.speed = speed

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.FAST_MOVE, distance=self.distance, speed=self.speed)
        return self.distance / (self.speed * 100)  # Estimated time

class RotateLeftCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', degrees: float, speed: float):
        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.ROTATE_LEFT, degrees=self.degrees, speed=self.speed)
        return self.degrees / (self.speed * 90)  # Estimated time

class RotateRightCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', degrees: float, speed: float):
        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.ROTATE_RIGHT, degrees=self.degrees, speed=self.speed)
        return self.degrees / (self.speed * 90)  # Estimated time

class StopCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.STOP)
        return 0.1  # Minimal time for stop

class FirstCanMoveBuilder:
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        self._sequence: list[ICommand] = []
        self._current_idx: int = 0
        self._is_finished: bool = False
        self._timer: MyTimer | None = None

    def create_sequence(self):
        speed = 0.5
        distance = 20.0  # cm
        rotation = 90.0  # degrees

        self._sequence = [
            MoveForwardCommand(self.fsm, distance, speed),
            RotateRightCommand(self.fsm, rotation, speed),
            MoveForwardCommand(self.fsm, distance, speed),
            RotateLeftCommand(self.fsm, rotation, speed),
            StopCommand(self.fsm)
        ]
        self.fsm.set_state(StateEnum.FAST_MOVE, distance=distance, speed=speed)

    def execute_step(self):
        # If timer is running, check if it's completed
        if self._timer:
            if self._timer.is_finished():
                self._timer = None
            else:
                return

        # Start next command if there is one
        if self._current_idx < len(self._sequence):
            command = self._sequence[self._current_idx]
            print(f"Executing Step {self._current_idx + 1}")
            time_needed = command.execute()
            self._timer = MyTimer(time_needed, self._on_step_complete)
        else:
            self._is_finished = True
            print("FirstCanMove sequence complete")

    def _on_step_complete(self):
        """Callback when a step completes"""
        self._current_idx += 1

    @property
    def is_finished(self) -> bool:
        return self._is_finished
