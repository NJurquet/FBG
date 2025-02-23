from .State import STATE_REGISTRY
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..constants import StateEnum
    from .FSM import RobotFSM
    from .State import State


class StateFactory:
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        self._state_cache: dict['StateEnum', 'State'] = {}

    def get_state(self, state_enum: 'StateEnum') -> 'State':
        """Retrieve a state instance from the cache or create it if not present."""
        # If the state is not yet in cache, create it and add it to the cache
        if state_enum not in self._state_cache:
            # If the state is not part of the allowed states (does not have been decorated), raise an error
            if state_enum not in STATE_REGISTRY:
                raise ValueError(f"State '{state_enum.name}' not found in registry.")
            state_class = STATE_REGISTRY[state_enum]
            self._state_cache[state_enum] = state_class(self.fsm)  # Create the state instance and add it to the cache
        return self._state_cache[state_enum]
