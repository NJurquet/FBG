from .State import State
from .detectionStates import DetectTargetsState, CheckObstaclesState


class MoveState(State):
    
    def __init__(self, fsm, command, components):
        super().__init__(fsm, command)
        self.command = command
        self.components = components
        self.lMotorControl = self.components[0]
        self.rMotorControl = self.components[1]

    def on_event(self, event):
        if event == 'stop':
            return StopState(self.fsm, {})
        elif event == 'obstacle_detected':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        forward_speed = self.command.get("forward_speed")
        backward_speed = self.command.get("backward_speed")
        if forward_speed is not None and forward_speed > 0:
            self.forward(forward_speed)
            print("Moving forward")
            self.fsm.set_state(DetectTargetsState(self.fsm, self.command, self.components))
        if backward_speed is not None and backward_speed > 0:
            self.backward(backward_speed)
            print("Moving backward")
            self.fsm.set_state(DetectTargetsState(self.fsm, self.command, self.components))
        else:
            print("Not moving")
            self.fsm.set_state(DetectTargetsState(self.fsm, self.command, self.components))

    def exit(self):
        pass

    def forward(self, speed):
        self.lMotorControl.forward(speed)
        self.rMotorControl.forward(speed)
        print(f"Moving forward: at speed {speed}")

    def backward(self, speed):
        self.lMotorControl.backward(speed)
        self.rMotorControl.backward(speed)
        print(f"Moving backward: at speed {speed}")


class RotateState(State):
    def __init__(self, fsm, command):
        super().__init__(fsm, command)
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
    def __init__(self, fsm, command):
        super().__init__(fsm, command)
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


class StopState(State):
    def __init__(self, fsm, command, components):
        super().__init__(fsm, command)
        self.command = command
        self.components = components
        self.lMotorControl = self.components[0]
        self.rMotorControl = self.components[1]

    def on_event(self, event):
        if event == 'start_moving':
            return
        return self

    def enter(self):
        pass

    def execute(self):
        self.motor.stop()
        print("Stopped Motors")

    def exit(self):
        pass
        #return DetectTargetsState(self.fsm)

    def stop(self):
        print("Stopping")


class SlowMoveState(State):
    def __init__(self, fsm, command):
        super().__init__(fsm, command)
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
    def __init__(self, fsm, command):
        super().__init__(fsm, command)
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
