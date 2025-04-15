from .command import ICommand
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SetOuterServoAngleCommand(ICommand):
    """Command to set the outer servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[float]):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

    def execute(self):
        new_angles = [0, 0, self.angles[0], self.angles[1]]
        self.fsm.robot.servoControl.setOuterAngles(new_angles)
        self.time_needed = 2.0  

    def pause(self):
        self.fsm.robot.servoControl.stopOuterServos()

    def resume(self):
        self.fsm.robot.servoControl.setOuterAngles(self.angles)
        self.time_needed = 2.0

    def stop(self):
        self.fsm.robot.servoControl.stopOuterServos()

    def finished(self):
        self.stop()
        self._is_finished = True

class SetAllServoAnglesCommand(ICommand):
    """Command to set the all servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[float]):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

    def execute(self):
        self.fsm.robot.servoControl.setAngles(self.angles)
        self.time_needed = 2.0

    def pause(self):
        self.fsm.robot.servoControl.stopServos()

    def resume(self):
        self.fsm.robot.servoControl.setAngles(self.angles)
        self.time_needed = 2.0

    def stop(self):
        self.fsm.robot.servoControl.stopServos()

    def finished(self):
        self.stop()
        self._is_finished = True

class SetPlankPusherServoAnglesCommand(ICommand):

    """Command to set the outer servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[float]):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

    def execute(self):
        new_angles = [0, 0, 0, 0 , self.angles[0], self.angles[1]]
        self.fsm.robot.servoControl.setPlankPusherAngles(new_angles)
        self.time_needed = 2.0  

    def pause(self):
        pass

    def resume(self):
       pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True

class SetBannerDeployerServoAngleCommand(ICommand):

    """Command to set the outer servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[float]):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

    def execute(self):
        new_angles = [0, 0, 0, 0 , 0, 0, 0, self.angles[0]]
        self.fsm.robot.servoControl.setBannerDeployerAngle(new_angles)
        self.time_needed = 2.0  

    def pause(self):
        pass

    def resume(self):
        pass


    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True
