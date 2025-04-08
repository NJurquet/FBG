from abc import ABC, abstractmethod

class ICommand(ABC):
    @abstractmethod
    def execute(self) -> float:
        """Execute the command and return the time needed for completion"""
        pass