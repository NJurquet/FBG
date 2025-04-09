from abc import ABC, abstractmethod
from ..myTimer import MyTimer

class ICommand(ABC):
    """Abstract base class for all commands."""

    time_needed: float | None = None
    _is_finished: bool = False

    def is_finished(self, finished) -> bool:
        """Check if the command is finished."""
        if finished is not None:
            self._is_finished = finished
        return self._is_finished

    @abstractmethod
    def execute(self) -> float | None:
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