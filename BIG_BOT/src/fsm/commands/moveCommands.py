from .command import IMoveCommand, ITimeBasedCommand
from ...constants import USPosition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


class MoveForwardCommand(ITimeBasedCommand):
    """Command to move the robot forward a certain distance at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', distance: float = 0.0, speed: float = 0.5, enable_direction_sensors = True, re_enable_us_sensors = True):
        self._is_finished = False

        self.fsm = fsm
        self.distance = distance
        self.speed = speed
        self.enable_direction_sensors = enable_direction_sensors
        self.re_enable_us_sensors = re_enable_us_sensors
        time_needed = self.fsm.robot.motor.computeTimeNeeded(direction="forward", distance_cm=self.distance, speed=self.speed)
        self.time_needed = time_needed + 0.1

    def execute(self):
        print(f"Moving forward")

        # Enable US sensors in the direction of movement
        if self.enable_direction_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)
        else:
            # Disable US sensors in the direction of movement
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_LEFT)

        # Disable US sensors in other directions
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_LEFT)
        
        self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.stop()
        
        if self.re_enable_us_sensors:
            # Re-enable US sensors in other directions
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)

        self._is_finished = True
        
class MoveBackwardCommand(ITimeBasedCommand):
    """Command to move the robot backward a certain distance at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', distance: float = 0.0, speed: float = 0.5, enable_direction_sensors = True, re_enable_us_sensors = True):
        self._is_finished = False

        self.fsm = fsm
        self.distance = distance
        self.speed = speed
        self.enable_direction_sensors = enable_direction_sensors
        self.enable_us_sensors = re_enable_us_sensors
        time_needed = self.fsm.robot.motor.computeTimeNeeded(direction="backward", distance_cm=self.distance, speed=self.speed)
        self.time_needed = time_needed + 0.1

    def execute(self):
        print(f"Moving backward")

        # Enable US sensors in the direction of movement
        if self.enable_direction_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)
        else:
            # Disable US sensors in the direction of movement
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_LEFT)

        # Disable US sensors in other directions
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_LEFT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)

        self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)

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

class RotateLeftCommand(ITimeBasedCommand):
    """Command to rotate the robot to the left a certain number of degrees at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', degrees: float = 0.0, speed: float = 0.5, enable_front_sensors = True, enable_back_sensors = True, enable_side_sensors = True):
        self._is_finished = False

        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed
        self.enable_front_sensors = enable_front_sensors
        self.enable_back_sensors = enable_back_sensors
        self.enable_side_sensors = enable_side_sensors

        time_needed = self.fsm.robot.motor.computeTimeNeeded(direction="rotateLeft", degrees=self.degrees, speed=self.speed)
        self.time_needed = time_needed + 0.1

    def execute(self):
        print(f"Rotating left")

        if self.enable_front_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_LEFT)
        if self.enable_back_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_LEFT)
        if self.enable_side_sensors:    
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)

        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)
        
        self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_MIDDLE)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)

        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)

        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)

        self.stop()
        self._is_finished = True

class RotateRightCommand(ITimeBasedCommand):
    """Command to rotate the robot to the right a certain number of degrees at a certain speed."""
    def __init__(self, fsm: 'RobotFSM', degrees: float = 0.0, speed: float = 0.5, enable_front_sensors = True, enable_back_sensors = True, enable_side_sensors = True):
        self._is_finished = False

        self.fsm = fsm
        self.degrees = degrees
        self.speed = speed

        self.enable_front_sensors = enable_front_sensors
        self.enable_back_sensors = enable_back_sensors
        self.enable_side_sensors = enable_side_sensors

        time_needed = self.fsm.robot.motor.computeTimeNeeded(direction="rotateRight", degrees=self.degrees, speed=self.speed)
        self.time_needed = time_needed + 0.1

    def execute(self):
        print(f"Rotating right")

        if self.enable_front_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_RIGHT)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_MIDDLE)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.FRONT_LEFT)
        if self.enable_back_sensors:
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_RIGHT)
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.BACK_LEFT)
        if self.enable_side_sensors:    
            self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)
        else:
            self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_RIGHT)
        
        self.fsm.robot.ultrasonicController.disable_sensor(USPosition.CENTER_LEFT)

        self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)
    
    def pause(self):
        self.fsm.robot.motor.stop()

    def resume(self):
        self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)

    def stop(self):
        self.fsm.robot.motor.stop()

    def finished(self):
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_RIGHT)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_MIDDLE)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.FRONT_LEFT)

        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_RIGHT)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.BACK_LEFT)

        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_RIGHT)
        self.fsm.robot.ultrasonicController.enable_sensor(USPosition.CENTER_LEFT)

        self.stop()
        self._is_finished = True

class StopCommand(ITimeBasedCommand):
    """Command to stop the motors and wait a time 0.1 to be sure of the complete stop of movement (can be tuned up if needed)."""
    def __init__(self, fsm: 'RobotFSM', time_needed: float = 0.2):
        self._is_finished = False

        self.fsm = fsm
        self.time_needed = time_needed

    def execute(self):
        # 0.1 seconds is the minimum of a stop in our logic
        self.fsm.robot.motor.stop()
    
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