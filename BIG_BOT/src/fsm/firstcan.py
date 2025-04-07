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
        # Get the time needed directly from the motor controller
        time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
        self.fsm.set_state(StateEnum.FAST_MOVE, distance=self.distance, speed=self.speed)
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
        self.fsm.set_state(StateEnum.ROTATE_RIGHT, degrees=self.degrees, speed=self.speed)

class StopCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.STOP)
        return 0.1  # Minimal time for stop


class OpenClawCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.OPEN_CLAW)
        return 2   # Minimal time for opening claw

class CloseClawCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        
        self.fsm = fsm

    def execute(self) -> float:
        self.fsm.set_state(StateEnum.CLOSE_CLAW)
        return 2  # Minimal time for closing claw

class FirstCanMoveBuilder:
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        self._sequence: list[ICommand] = []
        self._current_idx: int = 0
        self._is_finished: bool = False
        self._timer: MyTimer | None = None
        self._execution_in_progress: bool = False

    def create_sequence(self):
        speed = 0.5
        rotation = 90.0  # degrees

        self._sequence = [
            #OpenClawCommand(self.fsm), 
            MoveForwardCommand(self.fsm, 20, speed),
            # CloseClawCommand(self.fsm),
            # #RotateLeftCommand(self.fsm, rotation, speed),
            # OpenClawCommand(self.fsm),
            # #MoveForwardCommand(self.fsm, 20, speed),
            # CloseClawCommand(self.fsm),

            StopCommand(self.fsm)
        ]
        # Don't automatically execute first command here
        self._current_idx = 0
        self._is_finished = False

    def execute_step(self):
        # Don't do anything if we're already executing a command
        if self._execution_in_progress:
            return

        # Check if we've finished the sequence (so no list error)
        if self._current_idx >= len(self._sequence):
            self._is_finished = True
            print("FirstCanMove sequence complete")
            return

        # Start next command
        command = self._sequence[self._current_idx]
        print(f"Executing Step {self._current_idx + 1}")
        
        # Set the execution flag to prevent duplicate calls
        self._execution_in_progress = True
        
        # Execute command and get time needed
        time_needed = command.execute()
        
        # Create timer with callback to move to next step
        self._timer = MyTimer(time_needed, self._on_step_complete)

    def _on_step_complete(self):
        """Callback when a step completes"""
        print(f"Step {self._current_idx + 1} completed")
        self._current_idx += 1
        self._execution_in_progress = False
        
        # Automatically proceed to next step
        self.execute_step()

    @property
    def is_finished(self) -> bool:
        return self._is_finished