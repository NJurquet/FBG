from .State import State
from ...constants import StateEnum
from ...config import CENTER_RIGHT_CLAW_NAME, CENTER_LEFT_CLAW_NAME, OUTER_RIGHT_CLAW_NAME, OUTER_LEFT_CLAW_NAME
from ...config import PLANK_PUSHER_RIGHT_NAME, PLANK_PUSHER_LEFT_NAME, HINGE_NAME, BANNER_DEPLOYER_NAME
from ..registry import Registry
from ..myTimer import MyTimer
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from ..FSM import RobotFSM


@Registry.register_state(StateEnum.OPEN_CENTRAL_CLAWS)
class OpenCentralClawsState(State):
    """
    State in which the robot opens his central claws to drop the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 120

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(CENTER_RIGHT_CLAW_NAME, self.angle)
        self.fsm.robot.servoControl.setAngle(CENTER_LEFT_CLAW_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.CLOSE_CENTRAL_CLAWS)
class CloseCentralClawsState(State):
    """
    State in which the robot closes his central claws to collect the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 75

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(CENTER_RIGHT_CLAW_NAME, self.angle)
        self.fsm.robot.servoControl.setAngle(CENTER_LEFT_CLAW_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.OPEN_OUTER_CLAWS)
class OpenOuterClawsState(State):
    """
    State in which the robot opens his outer claws to drop the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 120

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(OUTER_RIGHT_CLAW_NAME, self.angle)
        self.fsm.robot.servoControl.setAngle(OUTER_LEFT_CLAW_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.CLOSE_OUTER_CLAWS)
class CloseOuterClawsState(State):
    """
    State in which the robot closes his outer claws to collect the cans.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 75

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(CENTER_RIGHT_CLAW_NAME, self.angle)
        self.fsm.robot.servoControl.setAngle(CENTER_LEFT_CLAW_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.DEPLOY_PLANK_PUSHERS)
class DeployPankPushersState(State):
    """
    State in which the robot pushes the plank by deploying turning 2 servomotors.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 90

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(PLANK_PUSHER_RIGHT_NAME, self.angle)
        self.fsm.robot.servoControl.setAngle(PLANK_PUSHER_LEFT_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.RETRACT_PLANK_PUSHERS)
class DeployPankPushersState(State):
    """
    State in which the robot retracts his "plank pushers" by turning 2 servomotors.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 90

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(PLANK_PUSHER_RIGHT_NAME, self.angle)
        self.fsm.robot.servoControl.setAngle(PLANK_PUSHER_LEFT_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.DEPLOY_BANNER)
class DeployClawsState(State):
    """
    State in which the robot turns the back servo to deploy a banner.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 90

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(BANNER_DEPLOYER_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.RETRACT_BANNER_PUSHER)
class DeployClawsState(State):
    """
    State in which the robot turns the back servo to retract the banner pusher.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 90

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(BANNER_DEPLOYER_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None



@Registry.register_state(StateEnum.DEPLOY_CLAWS)
class DeployClawsState(State):
    """
    State in which the robot turns the central hinge to deploy the claws.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 90

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(HINGE_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


@Registry.register_state(StateEnum.RETRACT_CLAWS)
class RetractClawsState(State):
    """
    State in which the robot turns the central hinge to retract the claws.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    'enum' : StateEnum
        The enumeration from which the state comes from.
    """

    def __init__(self, fsm: 'RobotFSM', enum: StateEnum):
        super().__init__(fsm, enum)

        self.angle = 180

    def increment_step(self):
        if self.fsm.step < self.fsm.maxStep:
            self.fsm.step += 1

    @override
    def enter(self, **args) -> None:
        self.angle = args.get('angle', self.angle)

        self.fsm.robot.servoControl.setAngle(HINGE_NAME, self.angle)

        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None

        self.fsm.timer = MyTimer(0.5, self.increment_step)

    @override
    def execute(self) -> None:
        pass

    @override
    def exit(self) -> None:
        if self.fsm.timer:
            self.fsm.timer.cancel()
            self.fsm.timer = None


