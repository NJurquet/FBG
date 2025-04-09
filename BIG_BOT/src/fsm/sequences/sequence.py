from abc import ABC, abstractmethod

class Sequence(ABC):
    _is_finished: bool = False

    @abstractmethod
    def create_sequence(self):
        """Create the sequence of commands"""
        pass

    @abstractmethod
    def execute_step(self):
        """Execute the next step in the sequence"""
        pass

    @abstractmethod
    def _on_step_complete(self):
        """Callback for when a step is complete"""
        pass

    @abstractmethod
    def pause(self):
        """Pause the sequence"""
        pass

    @abstractmethod
    def resume(self):
        """Resume the sequence"""
        pass

    @property
    def is_finished(self) -> bool:
        """Check if the sequence is finished"""
        return self._is_finished