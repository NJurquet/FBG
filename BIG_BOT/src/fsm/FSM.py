from .state_factory import StateFactory
from ..constants import StateEnum, USEvent, MAX_TIME
import time
from .sequences.sequenceManager import SequenceManager
from .sequences.sequenceCreator import SequenceCreator
from ..utils import precise_sleep

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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

        print(f"Robot color: {self.robot.color}")  # Debugging line

        self.us_event: USEvent = USEvent.NO_EVENT
        self.match_time = 0.0
        self.start_match: bool = False
        self.start_time: float = 0.0
        self.end_of_match: bool = False

        self.sequenceCreator = SequenceCreator(self, self.robot.color)
        
        self.sequenceManager = SequenceManager(self, 
                        # [ 
                        #     # self.sequenceCreator._bannerTest
                        #     # self.sequenceCreator.IdleState, 
                        #     # self.sequenceCreator.Init,
                        #     # self.sequenceCreator.DeployBanner,
                        #     # self.sequenceCreator.CollectCans,
                        #     # self.sequenceCreator.Build2StoryBleachers,
                        #     # self.sequenceCreator._timeMoveTest,
                        #     # self.sequenceCreator._wheeltest,
                        # ])

                        self.sequenceCreator.MainSequence)
        
        # self.start_match = True

        self.start_time = time.time()

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
        self.match_time = time.time() - self.start_time

        if self.start_match and (self.match_time >= MAX_TIME) and not self.end_of_match:
            self.sequenceManager.pause()
            self.robot.motor.stop()
            #self.robot.stepper.stop()
            self.end_of_match = True

        if not self.end_of_match:
            if self.start_match and self.sequenceManager._execution_in_progress:
                self.robot.ultrasonicController.measure_distances()
                self.us_event = self.robot.ultrasonicController.check_obstacles()
                if self.us_event == USEvent.OBSTACLE_DETECTED:
                    print("Obstacle detected")
                    self.sequenceManager.pause()
                    return
                elif self.us_event == USEvent.OBSTACLE_PRESENT:
                    return
                elif self.us_event == USEvent.OBSTACLE_CLEARED:
                    print("Obstacle cleared")
                    self.sequenceManager.resume()

            if self.us_event == USEvent.NO_EVENT:
                self.sequenceManager.execute_step()
