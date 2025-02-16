from State import State
from detectionStates import DetectTargetsState


class DropState(State):
    def __init__(self):
        super().__init__("Drop", None)
    
    def on_event(self, event):
        if event == 'targets_detected':
            return DetectTargetsState()
        return self
    
    def enter(self):
        pass

    def exit(self):
        pass

    def drop(self):
        print("Dropping")


class MoveToDrop(State):
    def __init__(self):
        super().__init__("Move to Drop", None)
    
    def on_event(self, event):
        if event == 'drop':
            return DropState()
        return self
    
    def enter(self):
        pass

    def exit(self):
        pass