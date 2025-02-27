from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..FSM import RobotFSM
    from ...constants import StateEnum


class State(ABC):
    """
    Interface for all Finite State Machine (FSM) states.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm

    def on_event(self, event) -> None:
        pass

    @abstractmethod
    def enter(self) -> None:
        """
        Method called by the FSM when entering the state.
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        Method called continuously by the FSM executing the main logic of the state.
        """
        pass

    @abstractmethod
    def exit(self) -> None:
        """
        Method called by the FSM when exiting the state.
        """
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
