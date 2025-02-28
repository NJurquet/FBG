from .states.State import State
from typing import TYPE_CHECKING, Callable
from importlib import import_module
from pkgutil import iter_modules

if TYPE_CHECKING:
    from ..constants import StateEnum


class Registry:
    """
    Registry storing the association between StateEnum enumeration and the corresponding State class.
    """
    _registry: dict['StateEnum', type['State']] = {}

    @classmethod
    def register_state(cls, state_enum: 'StateEnum') -> Callable:
        """
        Decorator to register a subclass of the State interface using a defined StateEnum.

        Parameters
        ----------
        `state_enum` : StateEnum
            The StateEnum to associate with the decorated State class.

        Returns
        -------
        `Callable`
            The decorator function to register the State class.

        Raises
        ------
        `TypeError`
            If the registered class is not a subclass of the State interface.
        """
        def decorator(wrapped_cls: type['State']) -> Callable:
            if issubclass(wrapped_cls, State):
                cls._registry[state_enum] = wrapped_cls
            else:
                raise TypeError("Registered class must be a subclass of State")
            return wrapped_cls
        return decorator

    @classmethod
    def auto_register_states(cls) -> None:
        """
        Automatically import all state modules inside the 'states' package to make state registration decorators work. 

        Raises
        ------
        ImportError
            If a module or package could not be imported.
        """
        package_name = __name__.rsplit(".", 1)[0] + ".states"  # Get 'src.fsm.states'
        try:
            package = import_module(package_name)  # Import the 'states' package itself
        except ModuleNotFoundError:
            raise ImportError(f"Could not import state package '{package_name}'")

        for _, module_name, _ in iter_modules(package.__path__, package_name + "."):
            import_module(module_name)  # Import each state module dynamically
