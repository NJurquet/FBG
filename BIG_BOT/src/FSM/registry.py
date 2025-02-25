from .states.State import State
from typing import TYPE_CHECKING, Callable
from importlib import import_module
from pkgutil import iter_modules
import sys

if TYPE_CHECKING:
    from ..constants import StateEnum


class Registry:
    _registry: dict['StateEnum', type['State']] = {}

    @classmethod
    def register_state(cls, state_enum: 'StateEnum') -> Callable:
        """Decorator to register a state using the Enum."""
        def decorator(wrapped_cls: type['State']) -> Callable:
            if issubclass(wrapped_cls, State):
                cls._registry[state_enum] = wrapped_cls
            else:
                raise TypeError("Registered class must be a subclass of State")
            return wrapped_cls
        return decorator

    @classmethod
    def auto_register_states(cls) -> None:
        """Automatically imports all state modules inside the 'states' package."""
        package_name = __name__.rsplit(".", 1)[0] + ".states"  # Get 'src.fsm.states'
        try:
            package = import_module(package_name)  # Import the states package itself
        except ModuleNotFoundError:
            raise ImportError(f"Could not import state package '{package_name}'")

        for _, module_name, _ in iter_modules(package.__path__, package_name + "."):
            import_module(module_name)  # Import each state module dynamically
