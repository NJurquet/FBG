from .command import ICommand
from ...constants import StateEnum
from ..myTimer import MyTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class MoveForwardCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', distance: float = 0.0, speed: float = 0.5):
        self.timer = None
        self._is_finished = False

        self.fsm = fsm
        self.distance = distance
        self.speed = speed

    def execute(self) -> MyTimer:
        # Get the time needed directly from the motor controller
        time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
        self.timer = MyTimer(time_needed, self.finished)
        return self.timer
    
    def pause(self):
        if self.timer:
            self.timer.pause()
        self.fsm.robot.motor.stop()

    def resume(self):
        if self.timer:
            self.timer.resume(self.finished)
        time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
        return time_needed

    def stop(self):
        self.fsm.robot.motor.stop()
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def finished(self):
        self.stop()
        self._is_finished = True

class MoveBackwardCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', distance: float = 0.0, speed: float = 0.5):
        self.timer = None
        self._is_finished = False

        self.fsm = fsm
        self.distance = distance
        self.speed = speed

    def execute(self) -> MyTimer:
        time_needed = self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)
        self.timer = MyTimer(time_needed, self.finished)
        return self.timer
    
    def pause(self):
        if self.timer:
            self.timer.pause()
        self.fsm.robot.motor.stop()

    def resume(self):
        if self.timer:
            self.timer.resume(self.finished)
        time_needed = self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)
        return time_needed

    def stop(self):
        self.fsm.robot.motor.stop()
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def finished(self):
        self.stop()
        self._is_finished = True

class RotateLeftCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', degrees: float = 0.0, speed: float = 0.5):
        self.timer = None
        self._is_finished = False

        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self) -> MyTimer:
        time_needed = self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)
        self.timer = MyTimer(time_needed, self.finished)
        return self.timer
    
    def pause(self):
        if self.timer:
            self.timer.pause()
        self.fsm.robot.motor.stop()

    def resume(self):
        if self.timer:
            self.timer.resume(self.finished)
        time_needed = self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)
        return time_needed

    def stop(self):
        self.fsm.robot.motor.stop()
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def finished(self):
        self.stop()
        self._is_finished = True

class RotateRightCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM', degrees: float = 0.0, speed: float = 0.5):
        self.timer = None
        self._is_finished = False

        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self) -> MyTimer:
        time_needed = self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)
        self.timer = MyTimer(time_needed, self.finished)
        return self.timer
    
    def pause(self):
        if self.timer:
            self.timer.pause()
        self.fsm.robot.motor.stop()

    def resume(self):
        if self.timer:
            self.timer.resume(self.finished)
        time_needed = self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)
        return time_needed

    def stop(self):
        self.fsm.robot.motor.stop()
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def finished(self):
        self.stop()
        self._is_finished = True

class StopCommand(ICommand):
    def __init__(self, fsm: 'RobotFSM'):
        self.timer = None
        self._is_finished = False

        self.fsm = fsm

    def execute(self) -> MyTimer:
        # 0.1 seconds is the minimum of a stop in our logic
        self.fsm.robot.motor.stop()
        self.timer = MyTimer(0.1, self.finished)
        return self.timer
    
    def pause(self):
        if self.timer:
            self.timer.pause()
        self.fsm.robot.motor.stop()

    def resume(self):
        if self.timer:
            self.timer.resume(self.finished)
        self.fsm.robot.motor.stop()
        time_needed = 0.1
        return time_needed

    def stop(self):
        self.fsm.robot.motor.stop()
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def finished(self):
        self.stop()
        self._is_finished = True