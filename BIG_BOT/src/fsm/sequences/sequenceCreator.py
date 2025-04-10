from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import OpenClawCommand, CloseClawCommand
from ..commands.startCommands import InitCommand
from ..commands.ultrasonicCommands import UltrasonicSensorCommand
from ...constants import USPosition
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
            UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  # Disable front left sensor
            UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),
            MoveForwardCommand(fsm, 50),
            RotateLeftCommand(fsm, rotation),
            UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, True),  # Enable front left sensor
            UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, True),
            MoveForwardCommand(fsm, 50),
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