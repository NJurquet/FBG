from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..FSM import RobotFSM
    from ...constants import StateEnum


class State(ABC):
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        # self.name = name

    def on_event(self, event) -> None:
        pass

    @abstractmethod
    def enter(self) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass


STATE_REGISTRY: dict['StateEnum', type[State]] = {}
"""Registry of all allowed states. Maps the StateEnum to the class of the state."""


def register_state(state_enum: 'StateEnum') -> Callable:
    """Decorator to register a state using the Enum."""
    def decorator(cls: type[State]) -> Callable:
        if issubclass(type[cls], State):
            STATE_REGISTRY[state_enum] = cls
        else:
            raise TypeError("Registered class must be a subclass of State")
        return cls
    return decorator
