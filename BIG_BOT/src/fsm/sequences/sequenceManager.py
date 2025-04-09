from .sequence import Sequence
from ..commands.command import ICommand
from ...constants import StateEnum
from ..myTimer import MyTimer
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceManager():
    def __init__(self, fsm: 'RobotFSM', sequences: list[list[ICommand]]) -> None:
        self.fsm = fsm
        self._sequences = sequences
        self._current_sequence: list[ICommand] = self._sequences[0]
        self._current_sequence_idx: int = 0
        self._current_command_idx: int = 0
        self._command: ICommand | None = None
        self._timer: MyTimer | None = None
        self._execution_in_progress: bool = False
        self._all_sequences_completed: bool = False

    def execute_step(self):
        # First check if all sequences are completed
        if self._all_sequences_completed:
            return

        # Don't do anything if we're already executing a command
        if self._execution_in_progress:
            return

        # Check if we've finished the current sequence
        if self._current_command_idx >= len(self._current_sequence):
            self._current_sequence_idx += 1
            self._current_command_idx = 0
            
            # Check if we've finished all sequences
            if self._current_sequence_idx >= len(self._sequences):
                print("All sequences completed")
                self._all_sequences_completed = True
                return
                
            self._current_sequence = self._sequences[self._current_sequence_idx]

        # Start next command
        self._command = self._current_sequence[self._current_command_idx]
        
        # Set the execution flag to prevent duplicate calls
        self._execution_in_progress = True
        
        # Execute command and get timer
        time_needed = self._command.execute()
        self._timer = MyTimer(time_needed, self._on_step_complete)

    def _on_step_complete(self):
        """Callback when a step completes"""
        if self._command:
            self._command.finished()
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self._current_command_idx += 1
        
        # Only print "Moving to Step X" if there are more steps in this sequence
        if self._current_command_idx < len(self._current_sequence):
            print(f"Moving to Step {self._current_command_idx + 1}")
        self._execution_in_progress = False
        
    def reset(self):
        """Reset the sequence manager to start from the beginning"""
        self._current_sequence_idx = 0
        self._current_command_idx = 0
        self._command = None
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self._execution_in_progress = False
        self._all_sequences_completed = False
        self._current_sequence = self._sequences[0]

    def pause(self):
        if self._execution_in_progress:
            # Pause the current command
            if self._timer:
                self._timer.pause()

            if self._command:
                # Pause the command
                self._command.pause()

    def resume(self):
        if self._execution_in_progress:
            # Resume the current command
            if self._timer and self._command:
                # Get the time needed for resuming
                remaining_time = self._timer.resume(self._on_step_complete)
                self._command.resume()