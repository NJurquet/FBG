from .State import State


class DetectTargetsState(State):    # Detection & Mapping of the environment
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Detection", None)

    def on_event(self, event):
        if event == 'targets_detected':
            from .movementStates import MoveState
            command = {"distance": 50}
            return MoveState(self.fsm, command)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass

# DetectingObstacleState will be an observer


class CheckObstaclesState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Checking Obstacles", None)

    def on_event(self, event):
        if event == 'obstacle_detected':
            from movementStates import MoveState
            return MoveState(self.fsm, {})
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass
