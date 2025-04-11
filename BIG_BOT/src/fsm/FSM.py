from .state_factory import StateFactory
from .myTimer import MyTimer
from ..constants import StateEnum, USEvent, MAX_TIME
import time
from .sequences.sequenceManager import SequenceManager
from .sequences.sequenceCreator import SequenceCreator

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

        self.sequenceCreator = SequenceCreator(self)

        print(f"Robot color: {self.robot.color}")  # Debugging line

        if self.robot.color == "yellow": 

            self.sequenceManager = SequenceManager(self, 
                        [ self.sequenceCreator.reedswitchTest, self.sequenceCreator.clawtest])  
        else:

            self.sequenceManager = SequenceManager(self, 
                        [ self.sequenceCreator.reedswitchTest, self.sequenceCreator.clawtest])  

                                 
        
        self.us_event: USEvent = USEvent.NO_EVENT

        self.current_state: 'State' = self.state_factory.get_state(StateEnum.IDLE)
        # self.current_state.enter()
        # self.paused_state: StateEnum | None = None

        self.start_match: bool = False
        self.start_time: float = 0.0
        self.end_of_match: bool = False

        # self.timer: MyTimer | None = None
        self.step = 0
        self.maxStep = 15

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

        if not self.end_of_match:
            if self.start_match:
                
                self.robot.ultrasonicController.measure_distances()
                self.us_event = self.robot.ultrasonicController.check_obstacles()
                if self.us_event == USEvent.OBSTACLE_DETECTED:
                    self.sequenceManager.pause()
                    return
                elif self.us_event == USEvent.OBSTACLE_PRESENT:
                    
                    return
                elif self.us_event == USEvent.OBSTACLE_CLEARED:
                    self.sequenceManager.resume()

            if self.us_event == USEvent.NO_EVENT:
                self.sequenceManager.execute_step()
