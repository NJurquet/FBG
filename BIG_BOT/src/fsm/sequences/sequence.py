from abc import ABC, abstractmethod

class Sequence(ABC):
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

    @property
    def is_finished(self) -> bool:
        """Check if the sequence is finished"""
        pass