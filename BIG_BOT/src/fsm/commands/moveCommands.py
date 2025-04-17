from .command import ICommand
from ...constants import USPosition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class MoveForwardCommand(ICommand):
    """Command to move the robot forward a certain distance at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', distance: float = 0.0, speed: float = 0.5, time_target = None, enable_us_sensors = True):
        self._is_finished = False

        self.fsm = fsm
        self.distance = distance
        self.speed = speed

        self.time_target = time_target
        self.enable_us_sensors = enable_us_sensors

    def execute(self):
        print(f"Moving forward")
        # Disable US sensors in other directions
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_LEFT)
        
        if self.time_target:
            if self.fsm.match_time >= self.time_target:
                self.time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
        else:   
            # Get the time needed directly from the motor controller
            self.time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.stop()
        
        if self.enable_us_sensors:
            # Re-enable US sensors in other directions
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)

        self._is_finished = True
        
class MoveBackwardCommand(ICommand):
    """Command to move the robot backward a certain distance at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', distance: float = 0.0, speed: float = 0.5, enable_us_sensors = True):
        self._is_finished = False

        self.fsm = fsm
        self.distance = distance
        self.speed = speed
        
        self.enable_us_sensors = enable_us_sensors
        self.time_needed = self.fsm.robot.motor.computeTimeNeeded(direction="backward",distance_cm=self.distance, speed=self.speed)

    def execute(self):
        print(f"Moving backward")
        # Disable US sensors in other directions
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)

        self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.time_needed = self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.stop()
        
        if self.enable_us_sensors:
            # Disable US sensors in other directions
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)

        self._is_finished = True

class RotateLeftCommand(ICommand):
    """Command to rotate the robot to the left a certain number of degrees at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', degrees: float = 0.0, speed: float = 0.5):
        self.timer = None
        self._is_finished = False

        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self):
        self.time_needed = self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.time_needed = self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.stop()
        self._is_finished = True

class RotateRightCommand(ICommand):
    """Command to rotate the robot to the right a certain number of degrees at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', degrees: float = 0.0, speed: float = 0.5):
        self._is_finished = False

        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

    def execute(self):
        self.time_needed = self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.time_needed = self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.stop()
        self._is_finished = True

class StopCommand(ICommand):
    """Command to stop the motors and wait a time 0.1 to be sure of the complete stop of movement (can be tuned up if needed)."""
    def __init__(self, fsm: 'RobotFSM'):
        self._is_finished = False

        self.fsm = fsm

    def execute(self):
        # 0.1 seconds is the minimum of a stop in our logic
        self.fsm.robot.motor.stop()
        self.time_needed = 0.1
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.fsm.robot.motor.stop()
        self.time_needed = 0.1

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.stop()
        self._is_finished = True