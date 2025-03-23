from .registry import Registry
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..constants import StateEnum
    from .FSM import RobotFSM
    from .states.State import State


class StateFactory:
    """
    Factory class to create and cache State instances.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that uses the factory.
    """

    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        self._state_cache: dict['StateEnum', 'State'] = {}
        Registry.auto_register_states()

    def get_state(self, state_enum: 'StateEnum') -> 'State':
        """
        Retrieve a state instance from the cache or create it if not present.

        Parameters
        ----------
        `state_enum` : StateEnum
            The State enumeration value corresponding to the state to retrieve.

        Returns
        -------
        State
            The state instance corresponding to the StateEnum enumeration value.

        Raises
        ------
        ValueError
            If the state is not found in the registry, meaning the enumeration value is not associated with a state class.
        """
        # If the state is not yet in cache, create it and add it to the cache
        if state_enum not in self._state_cache:
            # If the state is not part of the allowed states (does not have been decorated), raise an error
            if state_enum not in Registry._registry:
                raise ValueError(f"State '{state_enum.name}' not found in registry.")
            state_class = Registry._registry[state_enum]
            self._state_cache[state_enum] = state_class(self.fsm, state_enum)  # Create the state instance and add it to the cache
        return self._state_cache[state_enum]
