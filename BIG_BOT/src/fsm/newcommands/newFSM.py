from typing import TYPE_CHECKING, Dict, Optional, List
import time
from BIG_BOT.src.constants import MAX_TIME  # Adjusted to an absolute import path
from BIG_BOT.src.fsm.newcommands.commands import Command  # Adjusted to an absolute import path

if TYPE_CHECKING:
    from BIG_BOT.src.robot import Robot

class RobotFSM:
    """
    Finite State Machine (FSM) of the robot using a command pattern approach.
    
    This class manages robot behavior using command sequences rather than traditional states.

    Parameters
    ----------
    `robot` : Robot
        The robot instance that uses the FSM.
    """

    def __init__(self, robot: 'Robot'):
        self.robot = robot
        
        # Match control variables
        self.start_match: bool = False
        self.start_time: float = 0.0
        self.end_of_match: bool = False
        
        # Current sequence tracking
        self.current_sequence_name: Optional[str] = None
        self.current_command_index: int = 0
        self.executing_command: bool = False
        self.command_start_time: float = 0.0
        self.command_duration: float = 0.0
        
        # Initialize predefined sequences
        self.initialize_sequences()
    
    def initialize_sequences(self) -> None:
        """
        Initialize all predefined command sequences for the robot.
        This creates the basic movement patterns the robot can execute.
        """
        # First can sequence
        first_can = self.robot.command_invoker.create_sequence("first_can")
        first_can.add_command(self.robot.move_forward(60.0, 0.5))
        first_can.add_command(self.robot.stop())
        first_can.add_command(self.robot.rotate_left(270.0, 0.5))
        
        # Add more predefined sequences as needed
        avoid_obstacle = self.robot.command_invoker.create_sequence("avoid_obstacle")
        avoid_obstacle.add_command(self.robot.stop())
        avoid_obstacle.add_command(self.robot.rotate_right(45, 0.4))
        avoid_obstacle.add_command(self.robot.move_forward(20, 0.5))
        avoid_obstacle.add_command(self.robot.rotate_left(45, 0.4))
        
        # Add a sequence for ending the match
        end_match = self.robot.command_invoker.create_sequence("end_match")
        end_match.add_command(self.robot.stop())
    
    def start(self) -> None:
        """
        Start the robot's match operations.
        """
        self.start_match = True
        self.start_time = time.time()
        
        # Start with the first sequence
        self.start_sequence("first_can")
    
    def start_sequence(self, sequence_name: str) -> bool:
        """
        Start executing a named sequence.
        
        Parameters
        ----------
        sequence_name : str
            Name of the sequence to execute
            
        Returns
        -------
        bool
            True if sequence was found and started, False otherwise
        """
        sequence = self.robot.command_invoker.get_sequence(sequence_name)
        if not sequence:
            print(f"Sequence '{sequence_name}' not found")
            return False
            
        self.current_sequence_name = sequence_name
        self.current_command_index = 0
        self.executing_command = False
        
        print(f"Starting sequence: {sequence_name}")
        return True
    
    def handle_obstacle_detection(self) -> None:
        """
        Handle obstacle detection by interrupting the current sequence
        and starting the avoid_obstacle sequence.
        
        This method saves the current sequence state to resume later.
        """
        # Save current sequence state before handling obstacle
        interrupted_sequence = self.current_sequence_name
        interrupted_index = self.current_command_index
        
        # Start obstacle avoidance sequence
        self.start_sequence("avoid_obstacle")
        
        # After avoiding obstacle, we'd want to resume the previous sequence
        # This could be handled in update() when avoid_obstacle completes
        # For now, we store the information in the FSM instance
        self.interrupted_sequence = interrupted_sequence
        self.interrupted_index = interrupted_index
    
    def update(self) -> None:
        """
        Update the FSM, executing commands from the current sequence.
        This should be called repeatedly in the main control loop.
        """
        # Check if match has ended
        if self.end_of_match or (self.start_match and time.time() - self.start_time >= MAX_TIME):
            if not self.end_of_match:
                self.end_of_match = True
                self.start_sequence("end_match")
            return
            
        # If no match started, nothing to do
        if not self.start_match:
            return
            
        # Check for obstacles (you would integrate your ultrasonic sensor logic here)
        # Example:
        # if self.check_for_obstacles():
        #     self.handle_obstacle_detection()
        #     return
            
        # Execute the current sequence if one is active
        self.execute_current_sequence()
    
    def execute_current_sequence(self) -> None:
        """
        Execute the current command sequence, handling timing and progression.
        """
        if not self.current_sequence_name:
            return
            
        sequence = self.robot.command_invoker.get_sequence(self.current_sequence_name)
        if not sequence or self.current_command_index >= len(sequence.commands):
            # Sequence is complete or not found
            self.current_sequence_name = None
            return
            
        # Get the current command
        current_command = sequence.commands[self.current_command_index]
        
        # If not currently executing a command, start the next one
        if not self.executing_command:
            print(f"Executing command: {current_command.get_name()}")
            self.command_duration = current_command.execute()
            self.command_start_time = time.time()
            self.executing_command = True
            return
            
        # Check if the current command has completed
        if self.command_duration > 0 and time.time() - self.command_start_time >= self.command_duration:
            # Command completed, move to next command
            self.current_command_index += 1
            self.executing_command = False
            
            # If we've completed all commands in the sequence
            if self.current_command_index >= len(sequence.commands):
                print(f"Sequence '{self.current_sequence_name}' completed")
                
                # Check if we need to resume an interrupted sequence
                if hasattr(self, 'interrupted_sequence') and self.interrupted_sequence:
                    print(f"Resuming interrupted sequence: {self.interrupted_sequence}")
                    self.current_sequence_name = self.interrupted_sequence
                    self.current_command_index = self.interrupted_index
                    self.interrupted_sequence = None
                    self.interrupted_index = 0
                else:
                    self.current_sequence_name = None
    
    def check_for_obstacles(self) -> bool:
        """
        Check if there are obstacles in the robot's path.
        
        Returns
        -------
        bool
            True if an obstacle is detected, False otherwise
        """
        # This would integrate with your ultrasonic sensor logic
        # Example implementation:
        # distances = self.robot.ultrasonicController.measure_distances()
        # return min(distances.values()) < OBSTACLE_THRESHOLD
        return False  # Placeholder