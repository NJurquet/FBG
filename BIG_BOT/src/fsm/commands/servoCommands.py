from .command import ICommand
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SetOuterServoAngleCommand(ICommand):
    """Command to set the outer servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[int], time_needed: float = 0.4):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

        self.new_time_needed = time_needed

    def execute(self):
        self.fsm.robot.servoControl.setOuterAngles(self.angles)
        self.time_needed = self.new_time_needed

    def pause(self):
        self.fsm.robot.servoControl.stopOuterServos()

    def resume(self):
        self.fsm.robot.servoControl.setOuterAngles(self.angles)
        self.time_needed = self.new_time_needed

    def stop(self):
        self.fsm.robot.servoControl.stopOuterServos()

    def finished(self):
        self.stop()
        self._is_finished = True

class SetAllServoAnglesCommand(ICommand):
    """Command to set the all servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[int], time_needed: float = 0.4):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

        self.new_time_needed = time_needed

    def execute(self):
        self.fsm.robot.servoControl.setAngles(self.angles)
        self.time_needed = self.new_time_needed

    def pause(self):
        self.fsm.robot.servoControl.stopServos()

    def resume(self):
        self.fsm.robot.servoControl.setAngles(self.angles)
        self.time_needed = self.new_time_needed

    def stop(self):
        self.fsm.robot.servoControl.stopServos()

    def finished(self):
        self.stop()
        self._is_finished = True

class SetPlankPusherServoAnglesCommand(ICommand):

    """Command to set the outer servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[int], time_needed: float = 0.4):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

        self.new_time_needed = time_needed

    def execute(self):
        self.fsm.robot.servoControl.setPlankPusherAngles(self.angles)
        self.time_needed = self.new_time_needed

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
    def __init__(self, fsm: 'RobotFSM', angle: int, time_needed: float = 0.4):
        self._is_finished = False
        self.fsm = fsm
        self.angle = angle

        self.new_time_needed = time_needed

    def execute(self):

        self.fsm.robot.servoControl.setBannerDeployerAngle(self.angle)
        self.time_needed = self.new_time_needed

    def pause(self):
        pass

    def resume(self):
        pass


    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True
