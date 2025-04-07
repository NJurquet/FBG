from .state_factory import StateFactory
from .myTimer import MyTimer
from ..constants import StateEnum, USEvent, MAX_TIME
import time

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
        if self.start_match and (time.time() - self.start_time >= MAX_TIME):
            self.set_state(StateEnum.STOP)
            self.end_of_match = True

        if not self.end_of_match:
            # self.robot.ultrasonicController.measure_distances()
            # us_event = self.robot.ultrasonicController.check_obstacles()
            # if us_event == USEvent.OBSTACLE_DETECTED:
            #     self.paused_state = self.current_state.enum
            #     if self.timer:
            #         self.timer.pause()
            #     self.set_state(StateEnum.AVOID_OBSTACLE)
            #     return
            # elif us_event == USEvent.OBSTACLE_PRESENT:
            #     self.current_state.execute()
            #     return
            # elif us_event == USEvent.OBSTACLE_CLEARED:
            #     if self.paused_state is not None:
            #         if self.timer:
            #             self.timer.resume()
            #             self.step -= 1
            #             print("newstep", self.step)
            #         self.set_state(self.paused_state)  # Return to pre-obstacle state
            #         self.paused_state = None

            # if self.start_match and (time.time() - self.start_time >= 22.0):
            #     self.set_state(StateEnum.OPEN_CLAW)

            # elif self.start_match and (time.time() - self.start_time >= 4.0):
            #     self.set_state(StateEnum.CLOSE_CLAW)

            # elif self.start_match and (time.time() - self.start_time >= 2.0):
            #     self.set_state(StateEnum.OPEN_CLAW)

            # if self.start_match and (time.time() - self.start_time >= 6.0):
            #     self.set_state(StateEnum.STOP)    

            # elif self.start_match and (time.time() - self.start_time >= 5.0):
            #     self.set_state(StateEnum.MOVE_FORWARD)
            
            # elif self.start_match and (time.time() - self.start_time >= 4.0):
            #     self.set_state(StateEnum.STOP)    

            # elif self.start_match and (time.time() - self.start_time >= 3.0):
            #     self.set_state(StateEnum.MOVE_FORWARD)

            if self.start_match and self.step == 6:
                self.set_state(StateEnum.ROTATE_LEFT, 
                               degrees = 90.0, speed = 0.5)   

            elif self.start_match and self.step == 5:
                self.set_state(StateEnum.STOP)

            elif self.start_match and self.step == 4:
                self.set_state(StateEnum.MOVE_FORWARD, 
                               distance = 10.0, speed = 0.5)  

            elif self.start_match and self.step == 3:
                self.set_state(StateEnum.STOP) 

            elif self.start_match and self.step == 2:
                self.set_state(StateEnum.ROTATE_LEFT, 
                               degrees = 270.0, speed = 0.5)   

            elif self.start_match and self.step == 1:
               self.set_state(StateEnum.STOP)

            elif self.start_match and self.step == 0:
                self.set_state(StateEnum.MOVE_FORWARD,
                               distance = 60.0, speed = 0.5)

            # if self.start_match and (time.time() - self.start_time >= 7.6):
            #     self.set_state(StateEnum.STOP)  

            # elif self.start_match and (time.time() - self.start_time >= 0.0):
            #     self.set_state(StateEnum.ROTATE_LEFT)   
   

        self.current_state.execute()
