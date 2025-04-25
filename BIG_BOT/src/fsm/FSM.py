from ..constants import USEvent, MAX_TIME
import time
from .sequences.sequenceManager import SequenceManager
from .sequences.sequenceCreator import SequenceCreator

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

        self.us_event: USEvent = USEvent.NO_EVENT
        self.match_time = 0.0
        self.start_match: bool = False
        self.start_time: float = 0.0
        self.end_of_match: bool = False

        self.sequenceCreator = SequenceCreator(self, self.robot.color)
        

        # Main Sequence : Strategy :
        #   - Deploy Banner 
        #   - Move in front of the end zone -> Wait for the PAMIs to move
        #   - Move into the end zone        

        self.sequenceManager = SequenceManager(self, 
                        self.sequenceCreator.MainSequence)
        

        # Test sequences

        # self.sequenceManager = SequenceManager(self, 
        #                 [ 
        #                     self.sequenceCreator.Init,
        #                     self.sequenceCreator._wheeltest,
        #                 ])

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
                    self.robot.logger.info("Obstacle detected")
                    self.sequenceManager.pause()
                    return
                elif self.us_event == USEvent.OBSTACLE_PRESENT:
                    return
                elif self.us_event == USEvent.OBSTACLE_CLEARED:
                    print("Obstacle cleared")
                    self.robot.logger.info("Obstacle cleared")
                    self.sequenceManager.resume()

            if self.us_event == USEvent.NO_EVENT:
                self.sequenceManager.execute_step()
