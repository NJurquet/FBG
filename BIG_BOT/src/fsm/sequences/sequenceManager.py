from ..commands.command import ICommand, ITimeBasedCommand, IMoveCommand
from ...constants import StateEnum
from ..myTimer import MyTimer
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceManager():
    def __init__(self, fsm: 'RobotFSM', sequences: list[list[ICommand | ITimeBasedCommand | IMoveCommand]]) -> None:
        self.fsm = fsm
        self._sequences = sequences
        self._current_sequence: list[ICommand | ITimeBasedCommand | IMoveCommand] = self._sequences[0]
        self._current_sequence_idx: int = -1
        self._current_command_idx: int = 0
        self._command: ICommand | ITimeBasedCommand | IMoveCommand | None = self.get_next_command()
        self._timer: MyTimer | None = None
        self._execution_in_progress: bool = False
        self._all_sequences_completed: bool = False
    
    def get_next_sequence(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand] | None:
        """Get the next sequence to execute"""
        if self._current_sequence_idx < len(self._sequences):
            return self._sequences[self._current_sequence_idx]
        print("All sequences completed")
        return None

    def get_next_command(self) -> ICommand | ITimeBasedCommand | IMoveCommand | None:
        """Get the next command to execute"""
        
        self._current_command_idx += 1

        if self._current_command_idx >= len(self._current_sequence):
            # Move to the next sequence if available
            if self._current_sequence_idx >= len(self._sequences) - 1:
                # If there are no more sequences, mark all as completed
                self._all_sequences_completed = True
                return None
            
            self._current_sequence_idx += 1
            self._current_command_idx = 0
            next_sequence = self.get_next_sequence()
            print(f"Moving to Sequence {self._current_sequence_idx + 1}")

            # If there is a next sequence, set it as the current sequence
            if next_sequence is not None:
                self._current_sequence = next_sequence
            else:
                # If there are no more sequences, mark all as completed
                self._all_sequences_completed = True
                return None
            
        # If there are still commands in the current sequence, return the next command
        if self._current_command_idx < len(self._current_sequence):
            return self._current_sequence[self._current_command_idx]
    
    def execute_step(self):
        # First check if all sequences are completed
        if self._all_sequences_completed:
            return
        
        if self._command is not None:
            if self._execution_in_progress:
                # If a command is finished, we can execute the next command
                # if self._command._is_finished == True:
                #     self._on_step_complete()
                # else: 
                #     # Don't do anything if we're already executing a command
                #     return
                return

            # Set the execution flag to prevent duplicate calls
            self._execution_in_progress = True

            if isinstance(self._command, ICommand):
                # If the command is a regular command, execute it
                self._timer = None  # No timer needed for non-time-based commands
                self.fsm.robot.motor.movement_timer = None
                self._command.execute()
                self._on_step_complete()

            elif isinstance(self._command, ITimeBasedCommand):
                # If the command is time-based, execute it & Get a new timer
                self.fsm.robot.motor.movement_timer = None
                self._timer = MyTimer(self._command.time_needed, self._on_step_complete)
                self._command.execute()

    def _on_step_complete(self):
        """Callback when a step completes"""
        if self._command:
            self._command.finished()
        if self._timer:
            self._timer.cancel()
            self._timer = None

        self._execution_in_progress = False        
        # Only print "Moving to Step X" if there are more steps in this sequence
        if self._current_command_idx < len(self._current_sequence):
            print(f"Moving to Step {self._current_command_idx + 1}")

        self._command = self.get_next_command()
        
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