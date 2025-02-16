from State import State

class DetectTargetsState(State):    # Detection & Mapping of the environment
    def __init__(self):
        super().__init__("Detection", None)

    def on_event(self, event):
        if event == 'targets_detected':
            from movementStates import MoveState
            command = {"distance": 50}
            return MoveState(command)  
        return self

    def enter(self):
        pass

    def exit(self):
        pass

# DetectingObstacleState will be an observer
class CheckObstaclesState(State):    
    def __init__(self):
        super().__init__("Checking Obstacles", None)
    
    def on_event(self, event):
        if event == 'obstacle_detected':
            from movementStates import MoveState
            return MoveState()
        return self
    
    def enter(self):
        pass

    def exit(self):
        pass