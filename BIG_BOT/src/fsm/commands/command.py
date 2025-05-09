from abc import ABC, abstractmethod

class ICommand(ABC):
    """Abstract base class for all non-time based commands, they execute their work in one go."""

    _is_finished: bool = False

    def is_finished(self, finished) -> bool:
        """Check if the command is finished."""
        if finished is not None:
            self._is_finished = finished
        return self._is_finished

    @abstractmethod
    def execute(self):
        """Execute the command."""
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
        """Called when the command is finished."""
        pass

class ITimeBasedCommand(ABC):
    """Abstract base class for all time based commands, these commands give a time_needed object for the custom timer."""

    time_needed: float | None = None
    start_time: float | None = None
    current_progress_time: float = 0.0
    pause_time: float = 0.0
    resume_time: float = 0.0
    _is_finished: bool = False

    def is_finished(self, finished) -> bool:
        """Check if the command is finished."""
        if finished is not None:
            self._is_finished = finished
        return self._is_finished

    @abstractmethod
    def execute(self):
        """Execute the command."""
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
        """Called when the command is finished."""
        pass
