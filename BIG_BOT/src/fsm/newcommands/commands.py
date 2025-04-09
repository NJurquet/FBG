import time
from abc import ABC, abstractmethod
from typing import List, Optional, Callable
from BIG_BOT.src.constants import USEvent


class Command(ABC):
    """Base command interface"""
    
    @abstractmethod
    def execute(self) -> float:
        """Execute the command and return the time taken"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the command for logging/display"""
        pass


class ForwardCommand(Command):
    def __init__(self, robot, distance_cm: float, speed: float = 0.5):
        self.robot = robot
        self.distance_cm = distance_cm
        self.speed = speed
    
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        return self.robot.motor.moveForward(self.distance_cm, self.speed)
    
    def get_name(self) -> str:
        return f"Move forward {self.distance_cm}cm at speed {self.speed}"


class BackwardCommand(Command):
    def __init__(self, robot, distance_cm: float, speed: float = 0.5):
        self.robot = robot
        self.distance_cm = distance_cm
        self.speed = speed
    
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        return self.robot.motor.moveBackward(self.distance_cm, self.speed)
    
    def get_name(self) -> str:
        return f"Move backward {self.distance_cm}cm at speed {self.speed}"


class RotateLeftCommand(Command):
    def __init__(self, robot, degrees: float, speed: float = 0.5):
        self.robot = robot
        self.degrees = degrees
        self.speed = speed
    
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        return self.robot.motor.rotateLeftDegrees(self.degrees, self.speed)
    
    def get_name(self) -> str:
        return f"Rotate left {self.degrees} degrees at speed {self.speed}"


class RotateRightCommand(Command):
    def __init__(self, robot, degrees: float, speed: float = 0.5):
        self.robot = robot
        self.degrees = degrees
        self.speed = speed
    
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        return self.robot.motor.rotateRightDegrees(self.degrees, self.speed)
    
    def get_name(self) -> str:
        return f"Rotate right {self.degrees} degrees at speed {self.speed}"


class StopCommand(Command):
    def __init__(self, robot):
        self.robot = robot
    
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        self.robot.motor.stop()
        return 0
    
    def get_name(self) -> str:
        return "Stop"


class WaitCommand(Command):
    def __init__(self, duration: float):
        self.duration = duration
    
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        time.sleep(self.duration)
        return self.duration
    
    def get_name(self) -> str:
        return f"Wait for {self.duration} seconds"


class CommandSequence:
    """Class to manage sequences of commands"""
    
    def __init__(self, name: str = "Command Sequence"):
        self.commands: List[Command] = []
        self.name = name
    
    def add_command(self, command: Command) -> 'CommandSequence':
        """Add a command to the sequence and return self for chaining"""
        self.commands.append(command)
        return self
    
    def execute(self, wait_between_commands: bool = True) -> None:
        """Execute all commands in sequence"""
        print(f"Starting command sequence: {self.name}")
        
        for i, command in enumerate(self.commands):
            execution_time = command.execute()
            
            # If this is a timed movement and we want to wait between commands
            if wait_between_commands and execution_time > 0 and i < len(self.commands) - 1:
                # Wait for the command to finish (the motors are running in a separate thread)
                time.sleep(execution_time)
        
        print(f"Command sequence {self.name} completed")
    
    def clear(self) -> None:
        """Clear all commands from the sequence"""
        self.commands = []


# Add this to your Robot class
class CommandInvoker:
    """Command invoker that stores and executes command sequences"""
    
    def __init__(self):
        self.sequences: dict[str, CommandSequence] = {}
        self.current_sequence: Optional[CommandSequence] = None
    
    def create_sequence(self, name: str) -> CommandSequence:
        """Create a new command sequence"""
        sequence = CommandSequence(name)
        self.sequences[name] = sequence
        self.current_sequence = sequence
        return sequence
    
    def get_sequence(self, name: str) -> Optional[CommandSequence]:
        """Get a sequence by name"""
        return self.sequences.get(name)
    
    def execute_sequence(self, name: str, wait_between_commands: bool = True) -> None:
        """Execute a sequence by name"""
        sequence = self.get_sequence(name)
        if sequence:
            sequence.execute(wait_between_commands)
        else:
            print(f"Sequence '{name}' not found")
    
    def list_sequences(self) -> List[str]:
        """List all available sequences"""
        return list(self.sequences.keys())
    
    from abc import ABC, abstractmethod

class ObstacleAwareCommand(ABC):
    """
    Base class for commands that are aware of obstacles and can pause/resume execution.
    """
    @abstractmethod
    def execute(self) -> float:
        """Execute the command and return the expected duration"""
        pass
    
    @abstractmethod
    def pause(self) -> None:
        """Pause the command execution"""
        pass
    
    @abstractmethod
    def resume(self) -> None:
        """Resume the command execution"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the command"""
        pass
    
    @abstractmethod
    def get_elapsed_time(self) -> float:
        """Get the elapsed execution time"""
        pass


class SafeMoveForwardCommand(ObstacleAwareCommand):
    """
    A forward movement command that checks for obstacles during execution.
    """
    def __init__(self, robot, distance_cm: float, speed: float = 0.5, 
                 on_obstacle_detected: Optional[Callable] = None,
                 check_interval: float = 0.1):
        self.robot = robot
        self.distance_cm = distance_cm
        self.speed = speed
        self.on_obstacle_detected = on_obstacle_detected
        self.check_interval = check_interval
        
        self.is_paused = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.total_duration = 0.0
        self.last_check_time = 0.0
    
    def execute(self) -> float:
        """Start moving forward and check for obstacles periodically"""
        print(f"Executing: {self.get_name()}")
        
        # Calculate the expected duration based on distance and speed
        coeff = self.robot.motor.distance_per_second / self.speed
        self.total_duration = self.distance_cm / (self.speed * coeff)
        
        # Start the motors
        self.robot.motor.forward(self.speed)
        
        # Set up timing
        self.start_time = time.time()
        self.last_check_time = self.start_time
        
        # Start a background thread to check for obstacles
        self._start_obstacle_checking()
        
        return self.total_duration
    
    def _start_obstacle_checking(self) -> None:
        """Start a thread to check for obstacles during execution"""
        import threading
        
        def check_obstacles():
            while time.time() - self.start_time < self.total_duration and not self.is_paused:
                # Check for obstacles periodically
                if time.time() - self.last_check_time >= self.check_interval:
                    self.last_check_time = time.time()
                    
                    # Measure distances and check for obstacles
                    self.robot.ultrasonicController.measure_distances()
                    us_event = self.robot.ultrasonicController.check_obstacles()
                    
                    if us_event == USEvent.OBSTACLE_DETECTED:
                        print("Obstacle detected during SafeMoveForward!")
                        
                        # Pause the command
                        self.pause()
                        
                        # Call the obstacle detection callback if provided
                        if self.on_obstacle_detected:
                            self.on_obstacle_detected()
                        
                        break  # Exit the thread
                
                # Sleep a short time to avoid hogging CPU
                time.sleep(0.01)
        
        # Start the obstacle checking thread
        obstacle_thread = threading.Thread(target=check_obstacles)
        obstacle_thread.daemon = True
        obstacle_thread.start()
    
    def pause(self) -> None:
        """Pause the forward movement"""
        if not self.is_paused:
            self.is_paused = True
            # Calculate elapsed time so far
            self.elapsed_time = time.time() - self.start_time
            # Stop the motors
            self.robot.motor.stop()
            print(f"SafeMoveForward paused after {self.elapsed_time:.2f}s")
    
    def resume(self) -> None:
        """Resume the forward movement from where it left off"""
        if self.is_paused:
            self.is_paused = False
            # Calculate remaining distance
            coeff = self.robot.motor.distance_per_second / self.speed
            elapsed_distance = self.elapsed_time * self.speed * coeff
            remaining_distance = self.distance_cm - elapsed_distance
            
            print(f"Resuming SafeMoveForward with {remaining_distance:.2f}cm remaining")
            
            if remaining_distance > 0:
                # Reset the start time
                self.start_time = time.time()
                # Restart the motors
                self.robot.motor.forward(self.speed)
                # Recalculate total duration
                self.total_duration = remaining_distance / (self.speed * coeff)
                # Restart obstacle checking
                self._start_obstacle_checking()
    
    def get_name(self) -> str:
        return f"SafeMoveForward {self.distance_cm}cm at speed {self.speed}"
    
    def get_elapsed_time(self) -> float:
        if self.is_paused:
            return self.elapsed_time
        else:
            return time.time() - self.start_time


class SafeRotateCommand(ObstacleAwareCommand):
    """Base class for safe rotation commands"""
    def __init__(self, robot, degrees: float, speed: float = 0.5):
        self.robot = robot
        self.degrees = degrees
        self.speed = speed
        
        self.is_paused = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.total_duration = 0.0
    
    def get_elapsed_time(self) -> float:
        if self.is_paused:
            return self.elapsed_time
        else:
            return time.time() - self.start_time


class SafeRotateLeftCommand(SafeRotateCommand):
    """A left rotation command that can be paused and resumed"""
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        
        # Calculate the expected duration
        coeff = self.robot.motor.degrees_per_second_left / self.speed
        self.total_duration = self.degrees / (self.speed * coeff)
        
        # Start rotation
        self.robot.motor.rotateLeft(self.speed)
        self.start_time = time.time()
        
        return self.total_duration
    
    def pause(self) -> None:
        if not self.is_paused:
            self.is_paused = True
            self.elapsed_time = time.time() - self.start_time
            self.robot.motor.stop()
            print(f"SafeRotateLeft paused after {self.elapsed_time:.2f}s")
    
    def resume(self) -> None:
        if self.is_paused:
            self.is_paused = False
            
            # Calculate remaining degrees
            coeff = self.robot.motor.degrees_per_second_left / self.speed
            elapsed_degrees = self.elapsed_time * self.speed * coeff
            remaining_degrees = self.degrees - elapsed_degrees
            
            print(f"Resuming SafeRotateLeft with {remaining_degrees:.2f}° remaining")
            
            if remaining_degrees > 0:
                self.start_time = time.time()
                self.robot.motor.rotateLeft(self.speed)
                self.total_duration = remaining_degrees / (self.speed * coeff)
    
    def get_name(self) -> str:
        return f"SafeRotateLeft {self.degrees}° at speed {self.speed}"


class SafeRotateRightCommand(SafeRotateCommand):
    """A right rotation command that can be paused and resumed"""
    def execute(self) -> float:
        print(f"Executing: {self.get_name()}")
        
        # Calculate the expected duration
        coeff = self.robot.motor.degrees_per_second_right / self.speed
        self.total_duration = self.degrees / (self.speed * coeff)
        
        # Start rotation
        self.robot.motor.rotateRight(self.speed)
        self.start_time = time.time()
        
        return self.total_duration
    
    def pause(self) -> None:
        if not self.is_paused:
            self.is_paused = True
            self.elapsed_time = time.time() - self.start_time
            self.robot.motor.stop()
            print(f"SafeRotateRight paused after {self.elapsed_time:.2f}s")
    
    def resume(self) -> None:
        if self.is_paused:
            self.is_paused = False
            
            # Calculate remaining degrees
            coeff = self.robot.motor.degrees_per_second_right / self.speed
            elapsed_degrees = self.elapsed_time * self.speed * coeff
            remaining_degrees = self.degrees - elapsed_degrees
            
            print(f"Resuming SafeRotateRight with {remaining_degrees:.2f}° remaining")
            
            if remaining_degrees > 0:
                self.start_time = time.time()
                self.robot.motor.rotateRight(self.speed)
                self.total_duration = remaining_degrees / (self.speed * coeff)
    
    def get_name(self) -> str:
        return f"SafeRotateRight {self.degrees}° at speed {self.speed}"