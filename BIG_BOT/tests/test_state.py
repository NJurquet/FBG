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


def test_state_cannot_be_instantiated():
    """Test that an instance of the abstract class `State` cannot be created directly."""
    mock_fsm = Mock(spec=RobotFSM)

    with pytest.raises(TypeError, match="Can't instantiate abstract class State"):
        State(mock_fsm)


def test_state_requires_abstract_methods():
    """Test that a subclass of `State` must implement all abstract methods."""
    mock_fsm = Mock(spec=RobotFSM)

    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteState"):
        IncompleteState(mock_fsm)


@pytest.mark.skip
@pytest.mark.parametrize("method_name", ["enter", "execute", "exit"])
def test_abstract_methods_raise_not_implemented_error(method_name):
    """Test that calling an abstract method in a non-overridden subclass raises NotImplementedError."""
    mock_fsm = Mock(spec=RobotFSM)

    test_state = IncompleteState(mock_fsm)

    with pytest.raises(NotImplementedError, match=f"The '{method_name}' method must be overridden in subclasses of State."):
        getattr(test_state, method_name)()


def test_concrete_state_instantiation():
    """Test that a concrete implementation of `State` can be instantiated."""
    mock_fsm = Mock(spec=RobotFSM)
    state_enum = Mock(spec=StateEnum)

    state = ConcreteState(mock_fsm, state_enum)

    assert state.fsm is mock_fsm
    assert state.enum is state_enum


def test_concrete_state_methods():
    """Ensure a valid subclass implements required methods without errors."""
    mock_fsm = Mock(spec=RobotFSM)
    state = ConcreteState(mock_fsm)

    assert state.enter() is None
    assert state.execute() is None
    assert state.exit() is None
