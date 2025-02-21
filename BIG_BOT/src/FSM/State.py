from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, fsm, command: dict[str, int] = {}):
        self.fsm = fsm
        # self.name = name
        self.command = command

    @abstractmethod
    def on_event(self, event):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def exit(self):
        pass
