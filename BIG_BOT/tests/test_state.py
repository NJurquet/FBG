import pytest
from unittest.mock import Mock
from ..src.fsm.states.State import State
from ..src.fsm.FSM import RobotFSM
from ..src.constants import StateEnum


class IncompleteState(State):
    """A subclass of State that does not implement required methods."""
    pass


class ConcreteState(State):
    """Minimal concrete implementation of State for testing purposes."""

    def enter(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def exit(self) -> None:
        pass


@pytest.fixture
def mock_fsm():
    return Mock(spec=RobotFSM)


@pytest.fixture
def concrete_state(mock_fsm):
    return ConcreteState(mock_fsm, StateEnum.IDLE)


def test_abstract_state_cannot_be_instantiated(mock_fsm):
    """Test that an abstract class cannot be instantiated."""

    with pytest.raises(TypeError, match="Can't instantiate abstract class State"):
        State(mock_fsm)


def test_state_requires_abstract_methods(mock_fsm):
    """Test that a subclass of `State` must implement all abstract methods."""

    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteState"):
        IncompleteState(mock_fsm)


def test_concrete_state_instantiation(concrete_state):
    """Test that a concrete implementation of `State` can be instantiated."""

    state = concrete_state

    assert state.fsm is not None
    assert state.enum == StateEnum.IDLE


@pytest.mark.parametrize("method_name", ["enter", "execute", "exit"])
def test_concrete_state_methods_return_none(method_name, concrete_state):
    """Test that the methods of a concrete implementation of `State` return None."""

    result = getattr(concrete_state, method_name)()
    assert result is None
