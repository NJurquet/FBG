from State import State
from detectionStates import DetectTargetsState, CheckObstaclesState


class MoveState(State):
    def __init__(self, command):
        super().__init__("Move", command)

    def on_event(self, event):
        if event == 'stop':
            return 
        elif event == 'obstacle_detected':
            return 
        return self

    def enter(self):
        distance = self.command.get("distance")
        if distance > 0:
            self.forward(distance)
        if distance == 0:
            print("Not moving")
        if distance < 0:
            self.backward(distance)

    def exit(self):
        return DetectTargetsState()

    def forward(self, distance):
        print(f"Moving forward: distance {distance}")

    def backward(self, distance):
        print(f"Moving backward: distance {distance}")


class RotateState(State):
    def __init__(self, command):
        super().__init__("Rotate", command)

    def on_event(self, event):
        if event == 'stop':
            return 
        elif event == 'obstacle_detected':
            return 
        return self

    def enter(self):
        pass

    def exit(self):
        return DetectTargetsState()

    def rotate_left(self):
        print("Rotating left")

    def rotate_right(self):
        print("Rotating right")


class AvoidObstacleState(State):
    def __init__(self, command):
        super().__init__("Avoid Obstacle", command)

    def on_event(self, event):
        if event == 'obstacle_cleared':
            return 
        return self

    def enter(self):
        pass

    def exit(self):
        return DetectTargetsState()

    def avoid_obstacle(self):
        print("Avoiding obstacle")


class StopState(State):
    def __init__(self, command):
        super().__init__("Stop", command)

    def on_event(self, event):
        if event == 'start_moving':
            return 
        return self

    def enter(self):
        pass

    def exit(self):
        return DetectTargetsState()

    def stop(self):
        print("Stopping")


class SlowMoveState(State):
    def __init__(self, command):
        super().__init__("Slow Move", command)

    def on_event(self, event):
        if event == 'stop':
            return 
        elif event == 'obstacle_detected':
            return 
        return self

    def enter(self):
        pass

    def exit(self):
        return DetectTargetsState()

    def slow_forward(self):
        print("Slowly moving forward")

    def slow_backward(self):
        print("Slowly moving backward")


class SlowRotateState(State):
    def __init__(self, command):
        super().__init__("Slow Rotate", command)

    def on_event(self, event):
        if event == 'stop':
            return 
        elif event == 'obstacle_detected':
            return 
        return self

    def enter(self):
        pass

    def exit(self):
        return DetectTargetsState()

    def slow_rotate_left(self):
        print("Slowly rotating left")

    def slow_rotate_right(self):
        print("Slowly rotating right")


