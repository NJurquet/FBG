from .command import ICommand
from ...constants import USPosition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class ToggleUltrasonicSensorsCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', positions: list[USPosition]):
        self._is_finished = False
        self.fsm = fsm
        self.initialStates = fsm.robot.ultrasonicController.get_enabled_sensors()
        self.positions = positions

    def execute(self):
        for i in range(len(self.positions)):
            self.fsm.robot.ultrasonicController.toggle_sensor(self.positions[i])


    def pause(self):
        pass  # No action needed for pause

    def resume(self):
        current_states = self.fsm.robot.ultrasonicController.get_enabled_sensors()
    
        for position in self.positions:
            # Check if the current state is different from the initial state
            current_state = current_states[position]
            initial_state = self.initialStates[position]

            if current_state == initial_state:
                # Toggle the neeeded sensor to the opposite state
                self.fsm.robot.ultrasonicController.toggle_sensor(position)

    def stop(self):
        pass  # No action needed for stop

    def finished(self):
        self._is_finished = True

class  DisableUltrasonicSensorsCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', positions: list[USPosition]):
        self._is_finished = False
        self.fsm = fsm
        self.positions = positions

    def execute(self):
        for position in self.positions:
            self.fsm.robot.ultrasonicController.disable_sensor(position)
        self.fsm.robot.logger.info(f"Sensors : {self.positions} have been disabled")
        self.finished()

    def pause(self):
        pass  # No action needed for pause

    def resume(self):
        pass

    def stop(self):
        pass  # No action needed for stop

    def finished(self):
        self._is_finished = True

class EnableUltrasonicSensorsCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', positions: list[USPosition]):
        self._is_finished = False
        self.fsm = fsm
        self.positions = positions

    def execute(self):
        for position in self.positions:
            self.fsm.robot.ultrasonicController.enable_sensor(position)
        self.fsm.robot.logger.info(f"Sensors : {self.positions} have been enabled")
        self.finished()

    def pause(self):
        pass  # No action needed for pause

    def resume(self):
        pass

    def stop(self):
        pass  # No action needed for stop

    def finished(self):
        self._is_finished = True

