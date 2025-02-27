from ...constants import StateEnum
from .detectionStates import DetectTargetsState, CheckObstaclesState
from .State import State
from ..registry import Registry
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM


@Registry.register_state(StateEnum.IDLE)
class IdleState(State):
    def __init__(self, fsm: 'RobotFSM'):
        super().__init__(fsm)
        # super().__init__("Idle", command)

    def enter(self):
        pass

    def execute(self):
        self.fsm.set_state(StateEnum.MOVE)

    def exit(self):
        print("Exiting Idle State - Match Started")


@Registry.register_state(StateEnum.MOVE)
class MoveState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Move", command)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    def enter(self):
        # distance = self.command.get("distance")
        # if distance is not None and distance > 0:
        #     self.forward(distance)
        # if distance == 0:
        #     print("Not moving")
        # if distance is not None and distance < 0:
        #     self.backward(distance)
        pass

    def execute(self):
        self.fsm.robot.motor.forward(0.2)

    def exit(self):
        pass

    # def forward(self, distance):
    #     print(f"Moving forward: distance {distance}")

    # def backward(self, distance):
    #     print(f"Moving backward: distance {distance}")


class RotateState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Rotate", command)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        return DetectTargetsState(self.fsm)

    def rotate_left(self):
        print("Rotating left")

    def rotate_right(self):
        print("Rotating right")


class AvoidObstacleState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Avoid Obstacle", command)

    def on_event(self, event):
        if event == 'obstacle_cleared':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        return DetectTargetsState(self.fsm)

    def avoid_obstacle(self):
        print("Avoiding obstacle")


@Registry.register_state(StateEnum.STOP)
class StopState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Stop", command)

    def on_event(self, event):
        if event == 'start_moving':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        self.fsm.robot.motor.stop()

    def exit(self):
        pass


class SlowMoveState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Slow Move", command)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        return DetectTargetsState(self.fsm)

    def slow_forward(self):
        print("Slowly moving forward")

    def slow_backward(self):
        print("Slowly moving backward")


class SlowRotateState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Slow Rotate", command)

    def on_event(self, event):
        if event == 'stop':
            return
        elif event == 'obstacle_detected':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        return DetectTargetsState(self.fsm)

    def slow_rotate_left(self):
        print("Slowly rotating left")

    def slow_rotate_right(self):
        print("Slowly rotating right")
