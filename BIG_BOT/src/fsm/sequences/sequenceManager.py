from ..commands.command import ICommand, ITimeBasedCommand
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceManager():
    def __init__(self, fsm: 'RobotFSM', sequences: list[list[ICommand | ITimeBasedCommand]]) -> None:
        self.fsm = fsm
        self._sequences = sequences
        self._current_sequence: list[ICommand | ITimeBasedCommand] = self._sequences[0]
        self._current_sequence_idx: int = 0
        self._current_command_idx: int = -1
        self._command: ICommand | ITimeBasedCommand | None = self.get_next_command()
        self._execution_in_progress: bool = False
        self._all_sequences_completed: bool = False
    
    def get_next_sequence(self) -> list[ICommand | ITimeBasedCommand] | None:
        """Get the next sequence to execute"""
        if self._current_sequence_idx < len(self._sequences):
            return self._sequences[self._current_sequence_idx]
        return None

    def get_next_command(self) -> ICommand | ITimeBasedCommand | None:
        """Get the next command to execute"""

        self._current_command_idx += 1

        if self._current_command_idx >= len(self._current_sequence):
            # Move to the next sequence if available
            self._current_sequence_idx += 1

            # Check if we've gone through all sequences
            if self._current_sequence_idx >= len(self._sequences):
                # If there are no more sequences, mark all as completed
                self._all_sequences_completed = True
                print("All sequences completed")
                return None

            self._current_command_idx = 0
            next_sequence = self.get_next_sequence()
            self.fsm.robot.logger.info(f"Moving to Sequence {self._current_sequence_idx + 1}")

            # Set the next sequence as the current sequence
            if next_sequence is not None:
                self._current_sequence = next_sequence

        # Return the next command in the current sequence
        return self._current_sequence[self._current_command_idx]
    
    def execute_step(self):
        # First check if all sequences are completed & pass if so
        if self._all_sequences_completed :
            return
        
        if self._command is not None:
            # If a command is in progress, pass or recalculate the time
            if self._execution_in_progress:
                if isinstance(self._command, ITimeBasedCommand):
                    # Recalculate the current time based on the pause and resume times
                    if self._command.start_time and self._command.time_needed:
                        shifted_time = self._command.resume_time - self._command.pause_time
                        self._command.current_progress_time = time.time() - self._command.start_time - shifted_time
                        
                        if self._command.current_progress_time >= self._command.time_needed:
                            self._on_step_complete()                    
                return

            # Set the execution flag to prevent duplicate calls
            self._execution_in_progress = True

            if self._command and isinstance(self._command, ICommand):
                # If the command is a regular command, execute it
                self._command.execute()
                self._on_step_complete()

            elif self._command and isinstance(self._command, ITimeBasedCommand):
                # If the command is time-based, execute it & Get a new time base
                self._command.execute()
                self._command.start_time = time.time()

    def _on_step_complete(self):
        """Callback when a step completes"""
        if self._command:
            self._command.finished()

        self._execution_in_progress = False        
        # Only print "Moving to Step X" if there are more steps in this sequence
        if self._current_command_idx < len(self._current_sequence):
            self.fsm.robot.logger.info(f"Moving to Step {self._current_command_idx + 1} in Sequence {self._current_sequence_idx + 1}")

        self._command = self.get_next_command()
        
    def reset(self):
        """Reset the sequence manager to start from the beginning"""
        self._current_sequence_idx = 0
        self._current_command_idx = 0
        self._command = None
        self._execution_in_progress = False
        self._all_sequences_completed = False
        self._current_sequence = self._sequences[0]

    def pause(self):
        if self._execution_in_progress:
            if self._command:
                if isinstance(self._command, ITimeBasedCommand) and self._command.start_time:
                    shifted_time = self._command.resume_time - self._command.pause_time
                    self._command.current_progress_time = time.time() - self._command.start_time - shifted_time
 
                    self._command.pause_time = time.time()

                # Pause the command
                self._command.pause()

    def resume(self):
        if self._execution_in_progress:
            if self._command:
                if isinstance(self._command, ITimeBasedCommand) and self._command.start_time:
                    self._command.resume_time = time.time()
                # Resume the command
                self._command.resume()