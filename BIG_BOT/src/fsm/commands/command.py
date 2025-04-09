from abc import ABC, abstractmethod
from ..myTimer import MyTimer

class ICommand(ABC):
    """Abstract base class for all commands."""

    timer: MyTimer | None = None
    _is_finished: bool = False

    @property
    def is_finished(self) -> bool:
        """Check if the command is finished."""
        return self.is_finished

    @abstractmethod
    def execute(self) -> MyTimer | None:
        """Execute the command and return the time needed for completion"""
        pass
    
    @abstractmethod
    def pause(self):
        """Pause the command."""
        pass

    @abstractmethod
    def resume(self):
        """Resume the command."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the command."""
        pass

    @abstractmethod
    def finished(self):
        """Check if the command is finished."""
        pass