from ...constants import StateEnum
from .detectionStates import DetectTargetsState
from .State import State
from ..registry import Registry
from typing import TYPE_CHECKING, override

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
        self.fsm.set_state(StateEnum.MOVE)

    @override
    def exit(self):
        print("Exiting Idle State - Match Started")


@Registry.register_state(StateEnum.MOVE)
class MoveState(State):
    """
    State in which the robot moves.

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
        self.fsm.robot.motor.forward(0.3)

    @override
    def exit(self):
        pass


@Registry.register_state(StateEnum.ROTATE)
class RotateState(State):
    """
    State in which the robot rotates.

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

    def on_event(self, event):
        if event == 'obstacle_cleared':
            return
        return self

    @override
    def enter(self):
        pass

    @override
    def execute(self):
        self.fsm.robot.motor.stop()

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
        pass

    @override
    def execute(self):
        self.fsm.robot.motor.stop()

    @override
    def exit(self):
        pass


class SlowMoveState(State):
    """
    State in which the robot moves slowly.

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

    def slow_forward(self):
        print("Slowly moving forward")

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
