from .sequence import Sequence
from ..commands.command import ICommand
from ..commands.moveCommands import MoveForwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import OpenClawCommand, CloseClawCommand
from ...constants import StateEnum
from ..myTimer import MyTimer
import time
from typing import TYPE_CHECKING, override

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
    
    @override
    def create_sequence(self):
        speed = 0.5
        rotation = 90.0  # degrees

        self._sequence = [
            #OpenClawCommand(self.fsm), 
            MoveForwardCommand(self.fsm, 20, speed),
            # CloseClawCommand(self.fsm),
            # RotateLeftCommand(self.fsm, rotation, speed),
            # OpenClawCommand(self.fsm),
            # MoveForwardCommand(self.fsm, 20, speed),
            # CloseClawCommand(self.fsm),

            StopCommand(self.fsm)
        ]
        # Don't automatically execute first command here
        self._current_idx = 0
        self._is_finished = False

    @override
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

    @override
    def _on_step_complete(self):
        """Callback when a step completes"""
        print(f"Step {self._current_idx + 1} completed")
        self._current_idx += 1
        self._execution_in_progress = False
        
        # Automatically proceed to next step
        self.execute_step()

    # @property
    # def is_finished(self) -> bool:
    #     return self._is_finished