from ...constants import StateEnum
from ...config import MAX_OBSTACLE_DURATION
from .detectionStates import DetectTargetsState
from .State import State
from ..registry import Registry
from typing import TYPE_CHECKING, override
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

    @override
    def enter(self):
        pass

    @override
    def execute(self):
        # if not self.fsm.robot.reedSwitch.read():  # The reedSwitch is a button so it's 0 when not pressed and 1 when pressed
            self.fsm.start_time = time.time()
            self.fsm.start_match = True
            self.fsm.set_state(StateEnum.MOVE_FORWARD)

    @override
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

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    @override
    def enter(self):
        self.fsm.robot.motor.forward(0.5)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass

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

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    @override
    def enter(self):
        self.fsm.robot.motor.backward(0.5)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass

@Registry.register_state(StateEnum.ROTATE_LEFT)
class RotateLeftState(State):
    """
    State in which the robot rotates left.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    @override
    def enter(self):
        self.fsm.robot.motor.rotateLeft(0.5)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        return DetectTargetsState(self.fsm)
    
@Registry.register_state(StateEnum.ROTATE_RIGHT)
class RotateRightState(State):
    """
    State in which the robot rotates right.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    @override
    def enter(self):
        self.fsm.robot.motor.rotateRight(0.5)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        return DetectTargetsState(self.fsm)

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

    @override
    def enter(self):
        print("Entering Avoid Obstacle State")
        self._obstacle_start_time = time.time()
        self.fsm.robot.motor.stop()

    @override
    def execute(self):
        obstacle_duration: float = time.time() - self._obstacle_start_time
        if obstacle_duration >= MAX_OBSTACLE_DURATION and obstacle_duration < MAX_OBSTACLE_DURATION + 2.0:
            self.fsm.robot.motor.backward(0.5)
        elif obstacle_duration >= MAX_OBSTACLE_DURATION + 2.0:
            self.fsm.robot.motor.stop()
            self._obstacle_start_time = time.time()

    @override
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

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    def on_event(self, event):
        if event == 'start_moving':
            return
        return self

    @override
    def enter(self):
        self.fsm.robot.motor.stop()

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass


@Registry.register_state(StateEnum.SLOW_MOVE)
class SlowMoveState(State):
    """
    State in which the robot moves slowly.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    @override
    def enter(self):
        pass

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        pass

    def slow_forward(self):
        self.fsm.robot.motor.forward(0.3)

    def slow_backward(self):
        print("Slowly moving backward")


class SlowRotateState(State):
    """
    State in which the robot rotates slowly.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    @override
    def enter(self):
        pass

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        return DetectTargetsState(self.fsm)

    def slow_rotate_left(self):
        print("Slowly rotating left")

    def slow_rotate_right(self):
        print("Slowly rotating right")


@Registry.register_state(StateEnum.FAST_MOVE)
class FastMoveState(State):
    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

    def on_event(self, event):
        return self

    @override
    def enter(self):
        self.fsm.robot.motor.forward(1.0)

    @override
    def execute(self):
        pass

    @override
    def exit(self):
        return DetectTargetsState(self.fsm)