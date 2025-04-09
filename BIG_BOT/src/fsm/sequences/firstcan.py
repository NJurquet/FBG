from .sequence import Sequence
from ..commands.command import ICommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import OpenClawCommand, CloseClawCommand
from ...constants import StateEnum
from ..myTimer import MyTimer
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class FirstCanMoveBuilder(Sequence):
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
            MoveForwardCommand(self.fsm, 40, speed),
            RotateLeftCommand(self.fsm, rotation, speed),
            MoveForwardCommand(self.fsm, 15, speed),
            RotateRightCommand(self.fsm, rotation, speed),
            MoveForwardCommand(self.fsm, 30, speed),
            # CloseClawCommand(self.fsm),
            MoveBackwardCommand(self.fsm, 30, speed),
            RotateRightCommand(self.fsm, rotation, speed),
            MoveForwardCommand(self.fsm, 15, speed),
            RotateRightCommand(self.fsm, rotation, speed),
            MoveForwardCommand(self.fsm, 40, speed),

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
        
        # Execute command and get timer
        self._timer = command.execute()

    def _on_step_complete(self):
        """Callback when a step completes"""
        print(f"Step {self._current_idx + 1} completed")
        self._current_idx += 1
        self._execution_in_progress = False
        
        # Automatically proceed to next step
        self.execute_step()

    def pause(self):
        if self._execution_in_progress:
            # Pause the current command
            self._sequence[self._current_idx].pause()

    def resume(self):
        if self._execution_in_progress:
            # Resume the current command
            self._sequence[self._current_idx].resume()

    @property
    def is_finished(self) -> bool:
        return self._is_finished