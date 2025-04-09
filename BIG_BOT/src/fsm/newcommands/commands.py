import time
from abc import ABC, abstractmethod
from typing import List, Optional

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