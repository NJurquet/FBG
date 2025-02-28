from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


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
        raise NotImplementedError("The 'enter' method must be overridden in subclasses of State.")

    @abstractmethod
    def execute(self) -> None:
        """
        Method called continuously by the FSM executing the main logic of the state.
        """
        raise NotImplementedError("The 'execute' method must be overridden in subclasses of State.")

    @abstractmethod
    def exit(self) -> None:
        """
        Method called by the FSM when exiting the state.
        """
        raise NotImplementedError("The 'exit' method must be overridden in subclasses of State.")
