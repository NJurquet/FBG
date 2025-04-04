from ...constants import StateEnum
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

    def enter(self, **args):
        print("Entering Avoid Obstacle State")
        self._obstacle_start_time = time.time()
        self.fsm.robot.motor.stop()

    def execute(self):
        obstacle_duration: float = time.time() - self._obstacle_start_time
        if obstacle_duration >= MAX_OBSTACLE_DURATION and obstacle_duration < MAX_OBSTACLE_DURATION + 2.0:
            self.fsm.robot.motor.backward(0.5)
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


@Registry.register_state(StateEnum.SLOW_MOVE)
class SlowMoveState(State):
    """
    State in which the robot moves slowly.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.

    **Methods**:
        slow_forward(): Moves the robot forward slowly
        slow_backward(): Moves the robot backward slowly
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    @override
    def enter(self, **args):
        self.fsm.robot.motor.forward(0.3)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass


class SlowRotateState(State):
    """
    State in which the robot rotates slowly.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.

    **Methods**:
        slow_rotate_left(): Rotates the robot left slowly
        slow_rotate_right(): Rotates the robot right slowly
    """

    def __init__(self, fsm):
        super().__init__(fsm)

    @override
    def enter(self, **args):
        pass

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass


@Registry.register_state(StateEnum.FAST_MOVE)
class FastMoveState(State):
    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    @override
    def enter(self, **args):
        distance = args.get('distance', 0.0)
        speed = args.get('speed', 1.0)
        self.fsm.robot.motor.moveForward(distance_cm=distance, speed=speed)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        return DetectTargetsState(self.fsm)

@Registry.register_state(StateEnum.FIRST_CAN_MOVE)
class FirstCanMoveState(State):
    """
    State in which the robot moves to the first can.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)
        self.substep = 0  # Track the progress of the sequence

    def enter(self, **args):
        print("Entering FirstCanMoveState")
        self.substep = 0  # Reset the substep counter

    def execute(self):
        if self.substep == 0:
            print("Substep 0: Moving forward")
            self.fsm.set_state(StateEnum.FAST_MOVE, distance=20, speed=0.5)
            self.substep += 1
        elif self.substep == 1:
            print("Substep 1: Rotating right")
            self.fsm.set_state(StateEnum.ROTATE_RIGHT, degrees=90, speed=0.5)
            self.substep += 1
        elif self.substep == 2:
            print("Substep 2: Moving forward")
            self.fsm.set_state(StateEnum.FAST_MOVE, distance=20, speed=0.5)
            self.substep += 1
        elif self.substep == 3:
            print("Substep 3: Rotating left")
            self.fsm.set_state(StateEnum.ROTATE_LEFT, degrees=90, speed=0.5)
            self.substep += 1
        else:
            print("FirstCanMoveState sequence complete")
            self.fsm.step += 1  # Increment the FSM step
            self.fsm.set_state(StateEnum.STOP)  # Transition to the STOP state

    def exit(self):
        print("Exiting FirstCanMoveState")