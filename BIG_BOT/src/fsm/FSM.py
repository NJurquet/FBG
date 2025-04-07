from .state_factory import StateFactory
from .myTimer import MyTimer
from ..constants import StateEnum, USEvent, MAX_TIME
import time
from .firstcan import FirstCanMoveBuilder

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .states.State import State
    from ..robot import Robot

class RobotFSM:
    """
    Finite State Machine (FSM) of the robot.

    Parameters
    ----------
    `robot` : Robot
        The robot instance that uses the FSM.
    """

    def __init__(self, robot: 'Robot'):
        self.robot = robot
        self.state_factory = StateFactory(self)

        self.current_state: 'State' = self.state_factory.get_state(StateEnum.IDLE)
        self.current_state.enter()
        self.paused_state: StateEnum | None = None

        self.start_match: bool = False
        self.start_time: float = 0.0
        self.end_of_match: bool = False

        self.timer: MyTimer | None = None
        self.step = 0
        self.maxStep = 15

        self.first_can_builder = FirstCanMoveBuilder(self)

    def set_state(self, new_state: StateEnum, **args) -> None:
        """
        Set the current state of the FSM to the new specified state.

        Parameters
        ----------
        new_state : StateEnum
            The new state to switch to.
        """
        if self.current_state.enum != new_state:
            self.current_state.exit()
            self.current_state = self.state_factory.get_state(new_state)
            self.current_state.enter(**args)

    def update(self) -> None:
        """
        Execute the current state of the FSM.
        """


            #         elif self.start_match and self.step == 2:
            #     self.set_state(StateEnum.ROTATE_LEFT, 
            #                    degrees = 270.0, speed = 0.5)   

            # elif self.start_match and self.step == 1:
            #    self.set_state(StateEnum.STOP)

            # elif self.start_match and self.step == 0:
            #     self.set_state(StateEnum.MOVE_FORWARD,
            #                    distance = 60.0, speed = 0.5)
        if self.start_match and (time.time() - self.start_time >= MAX_TIME):
            self.set_state(StateEnum.STOP)
            self.end_of_match = True




        if not self.end_of_match:
            if self.start_match and self.step == 0:
                # Only initialize the sequence once when step is 0
                self.first_can_builder.create_sequence()
                self.first_can_builder.execute_step()
            elif self.start_match and not self.first_can_builder.is_finished:
                # Continue executing sequence steps until finished
                self.first_can_builder.execute_step()


            self.current_state.execute()
