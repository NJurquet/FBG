from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import OpenClawCommand, CloseClawCommand
from ..commands.startCommands import InitCommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceCreator():
    def __init__(self, fsm: 'RobotFSM'):
        speed = 0.5
        rotation = 90

        self.Init = [
                InitCommand(fsm, "yellow"),
                StopCommand(fsm)
            ]
        
        self.FirstCanMove = [
            MoveForwardCommand(fsm, 40),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 15),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 30),
        ]
        
        self.FirstCanBuildMove = [
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 15),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 40)
            ]