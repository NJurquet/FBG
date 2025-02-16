from State import State
from detectionStates import DetectTargetsState

class CollectState(State):
    def __init__(self):
        super().__init__("Collect", None)

    def on_event(self, event):
        if event == 'collected':
            return DetectTargetsState()
        return self

    def enter(self):
        pass

    def exit(self):
        pass

    def collect(self):
        print("Collecting")


class MoveToCollectState(State):
    def __init__(self):
        super().__init__("Move to Collect", None)

    def on_event(self, event):
        if event == 'on_position':
            return CollectState()
        return self

    def enter(self):
        pass

    def exit(self):
        pass