from ...constants import StateEnum, USPosition
from ...config import MAX_OBSTACLE_DURATION
from .detectionStates import DetectTargetsState
from .State import State
from ..registry import Registry
from ..myTimer import MyTimer
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from ..FSM import RobotFSM


@Registry.register_state(StateEnum.IDLE)
class IdleState(State):
    """
    Initial state of the robot. The robot will stay in this state until the match starts.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    def enter(self, **args):
        pass

    def execute(self):
        # if not self.fsm.robot.reedSwitch.read():  # The reedSwitch is a button so it's 0 when not pressed and 1 when pressed
        self.fsm.start_time = time.time()
        self.fsm.start_match = True

    def exit(self):
        print("Exiting Idle State - Match Started")


@Registry.register_state(StateEnum.MOVE_FORWARD)
class MoveForwardState(State):
    """
    State in which the robot moves forward.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.distance = 0.0
        self.speed = 0.5

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    def enter(self, **args):
        self.distance = args.get('distance', self.distance)
        self.speed = args.get('speed', self.speed)
        time_needed = self.fsm.robot.motor.moveForward(distance_cm=self.distance, speed=self.speed)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(time_needed, self.increment_step)

    def execute(self):
        pass

    def exit(self):
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.MOVE_BACKWARD)
class MoveBackwardState(State):
    """
    State in which the robot moves backward.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.distance = 0.0
        self.speed = 0.5

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    def enter(self, **args):
        self.distance = args.get('distance', self.distance)
        self.speed = args.get('speed', self.speed)
        time_needed = self.fsm.robot.motor.moveBackward(distance_cm=self.distance, speed=self.speed)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(time_needed, self.increment_step)

    def execute(self):
        pass

    def exit(self):
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.ROTATE_LEFT)
class RotateLeftState(State):
    """
    State in which the robot rotates left.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.

    **Methods**:
        execute(): Makes the robot move forward
        on_event(event): stops the robot if an obstacle is detected
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.degrees = 0.0
        self.speed = 0.5

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    def enter(self, **args):
        self.degrees = args.get('degrees', self.degrees)
        self.speed = args.get('speed', self.speed)

        time_needed = self.fsm.robot.motor.rotateLeftDegrees(degrees=self.degrees, speed=self.speed)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(time_needed, self.increment_step)

    def execute(self):
        pass

    def exit(self):
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.ROTATE_RIGHT)
class RotateRightState(State):
    """
    State in which the robot rotates right.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.

    **Methods**:
        enter(): Rotates the robot right
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.degrees = 0.0
        self.speed = 0.5

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    def enter(self, **args):
        self.degrees = args.get('degrees', self.degrees)
        self.speed = args.get('speed', self.speed)

        time_needed = self.fsm.robot.motor.rotateRightDegrees(degrees=self.degrees, speed=self.speed)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(time_needed, self.increment_step)

    def execute(self):
        pass

    def exit(self):
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.AVOID_OBSTACLE)
class AvoidObstacleState(State):
    """
    State in which the robot uses an obstacle avoidance algorithm to avoid obstacles.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)
        self._obstacle_start_time: float = 0.0
        self._detecting_sensors: list[USPosition] = []

    def enter(self, **args):
        print("Entering Avoid Obstacle State")
        self._detecting_sensors = args.get('sensors', [])
        self._obstacle_start_time = time.time()
        self.fsm.robot.motor.stop()

    def execute(self):
        obstacle_duration: float = time.time() - self._obstacle_start_time
        if obstacle_duration >= MAX_OBSTACLE_DURATION and obstacle_duration < MAX_OBSTACLE_DURATION + 2.0:
            if (USPosition.FRONT_RIGHT in self._detecting_sensors or USPosition.FRONT_LEFT in self._detecting_sensors) and (USPosition.BACK_RIGHT in self._detecting_sensors or USPosition.BACK_LEFT in self._detecting_sensors):
                # When detecting in front and back, stop the robot
                self.fsm.robot.motor.stop()
            elif USPosition.FRONT_RIGHT in self._detecting_sensors or USPosition.FRONT_LEFT in self._detecting_sensors:
                # When detecting in front, move backward
                self.fsm.robot.motor.backward(0.5)
            elif USPosition.BACK_RIGHT in self._detecting_sensors or USPosition.BACK_LEFT in self._detecting_sensors:
                # When detecting in back, move forward
                self.fsm.robot.motor.forward(0.5)
        elif obstacle_duration >= MAX_OBSTACLE_DURATION + 2.0:
            self.fsm.robot.motor.stop()
            self._obstacle_start_time = time.time()

    def exit(self):
        pass


@Registry.register_state(StateEnum.STOP)
class StopState(State):
    """
    State in which the robot stops the motors.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum, **args):
        super().__init__(fsm, enum)

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    def enter(self, **args):
        print("Entering Stop State")
        self.fsm.robot.motor.stop()

        stopTime = args.get('stopTime', 0.1)
        self.fsm.timer = MyTimer(stopTime, self.increment_step)

    def execute(self):
        pass

    def exit(self):
        print("Exiting Stop State")
        print(self.fsm.step)
