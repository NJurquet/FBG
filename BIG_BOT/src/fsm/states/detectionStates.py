from .State import State


class DetectTargetsState(State):
    """
    State in which the robot maps the environment and detects the tribunes positions.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'targets_detected':
            from .movementStates import MoveState
            command = {"distance": 50}
            return MoveState(self.fsm)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass


class CheckObstaclesState(State):
    """
    State in which the robot checks for obstacles with the ultrasonic sensor.

    Parameters
    ----------
    `fsm` : RobotFSM
        The Finite State Machine (FSM) instance that the state belongs to.
    """

    def __init__(self, fsm):
        super().__init__(fsm)

    def on_event(self, event):
        if event == 'obstacle_detected':
            from BIG_BOT.src.fsm.states.movementStates import MoveState
            return MoveState(self.fsm)
        return self

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass
