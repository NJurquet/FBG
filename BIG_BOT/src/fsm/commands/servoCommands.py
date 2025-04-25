from .command import ITimeBasedCommand
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SetOuterServoAngleCommand(ITimeBasedCommand):
    """Command to set the outer servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[int], time_needed: float = 1.0):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

        self.time_needed = self.fsm.robot.servoControl.computeTimeNeeded(servos="outer", angles=self.angles)

    def execute(self):
        self.fsm.robot.servoControl.setOuterAngles(self.angles)

    def pause(self):
        self.fsm.robot.servoControl.stopOuterServos()

    def resume(self):
        self.fsm.robot.servoControl.setOuterAngles(self.angles)

    def stop(self):
        self.fsm.robot.servoControl.stopOuterServos()

    def finished(self):
        self.stop()
        self._is_finished = True

class SetAllServoAnglesCommand(ITimeBasedCommand):
    """Command to set the all servo angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[int], time_needed: float = 1.0):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

        self.time_needed = self.fsm.robot.servoControl.computeTimeNeeded(servos="all", angles=self.angles)

    def execute(self):
        self.fsm.robot.servoControl.setAngles(self.angles)

    def pause(self):
        self.fsm.robot.servoControl.stopServos()

    def resume(self):
        self.fsm.robot.servoControl.setAngles(self.angles)

    def stop(self):
        self.fsm.robot.servoControl.stopServos()

    def finished(self):
        self.stop()
        self._is_finished = True

class SetPlankPusherServoAnglesCommand(ITimeBasedCommand):
    """Command to set the plank pushers angles."""
    def __init__(self, fsm: 'RobotFSM', angles: List[int], time_needed: float = 1.0):
        self._is_finished = False
        self.fsm = fsm
        self.angles = angles

        self.time_needed = self.fsm.robot.servoControl.computeTimeNeeded(servos="plankPushers", angles=self.angles)

    def execute(self):
        self.fsm.robot.servoControl.setPlankPusherAngles(self.angles)

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True

class SetBannerDeployerServoAngleCommand(ITimeBasedCommand):
    """Command to set the banner deployer angle."""
    def __init__(self, fsm: 'RobotFSM', angle: int, time_needed: float = 1.0):
        self._is_finished = False
        self.fsm = fsm
        self.angle = angle

        self.time_needed = self.fsm.robot.servoControl.computeTimeNeeded(servos="bannerDeployer", angles=[self.angle])

    def execute(self):
        self.fsm.robot.servoControl.setBannerDeployerAngle(self.angle)

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def finished(self):
        self.stop()
        self._is_finished = True
