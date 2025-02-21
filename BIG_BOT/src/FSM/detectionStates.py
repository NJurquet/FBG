from .State import State


class DetectTargetsState(State):    # Detection & Mapping of the environment
    def __init__(self, fsm, command, components):
        super().__init__(fsm)
        self.command = command
        self.components = components
        self.testIterations = 0

    def on_event(self, event):
        if event == 'targets_detected':
            from .movementStates import MoveState
            move_command = {"forward_speed": 0.5}
            return MoveState(self.fsm, move_command, self.components)
        return self

    def enter(self):
        pass

    def execute(self):
        from .movementStates import MoveState
        from .movementStates import StopState

        if self.testIterations == 0:
            move_command = {"forward_speed": 0.5}
            self.testIterations += 1
            moveState = MoveState(self.fsm, move_command, self.components)
            moveState.execute()
        
        if self.testIterations in [1, 2, 3]:
            move_command = {"forward_speed": 1}
            self.testIterations += 1
            return MoveState(self.fsm, move_command, self.components)
        
        if self.testIterations == 4:
            move_command = {"backward_speed": 0.5}
            self.testIterations += 1
            return MoveState(self.fsm, move_command, self.components)
        
        if self.testIterations in [5, 6, 7]:
            move_command = {"backward_speed": 1}
            self.testIterations += 1
            return MoveState(self.fsm, move_command, self.components)
        
        if self.testIterations == 8:
            self.testIterations += 1
            return StopState(self.fsm, {}, self.components)
        
        else:
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
