from .State import State
from .detectionStates import DetectTargetsState


class DropState(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Drop", None)

    def on_event(self, event):
        if event == 'targets_detected':
            return DetectTargetsState(self.fsm)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass

    def drop(self):
        print("Dropping")


class MoveToDrop(State):
    def __init__(self, fsm):
        super().__init__(fsm)
        # super().__init__("Move to Drop", None)

    def on_event(self, event):
        if event == 'drop':
            return DropState(self.fsm)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass
