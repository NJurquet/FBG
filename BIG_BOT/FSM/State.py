class State:
    def __init__(self, name, command):
        self.name = name
        self.command = command

    def on_event(self, event):
        pass

    def enter(self):
        pass

    def exit(self):
        pass