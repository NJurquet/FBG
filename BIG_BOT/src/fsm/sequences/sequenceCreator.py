from ..commands.command import ICommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand
from ..commands.startCommands import InitCommand
from ..commands.ultrasonicCommands import ToggleUltrasonicSensorsCommand
from ..commands.reedswitchCommands import ReedSwitchCommand
from ...constants import USPosition
from ...config import OUTER_RIGHT_CLAW_NAME
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceCreator():
    def __init__(self, fsm: 'RobotFSM'):
        speed = 0.5
        rotation = 100

        self._Init: list[ICommand] = [
                ReedSwitchCommand(fsm),
                InitCommand(fsm),
                StopCommand(fsm)
            ]
        
        self._FirstCanMove: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            MoveForwardCommand(fsm, 50),
            RotateLeftCommand(fsm, rotation),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Enable front sensors
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 30),
        ]
        
        self._FirstCanBuildMove: list[ICommand] = [
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 15),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 40)
            ]
        
        self._Sprint4Yellow: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),  # Disable back sensors
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 95),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 130),
        ]

        self._Sprint4Blue: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 95),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 130),
        ]

        self.clawtest: list[ICommand] = [
            SetAllServoAnglesCommand(fsm, [150,150,150,150]),
            SetAllServoAnglesCommand(fsm, [90,90,90,90]),
            SetAllServoAnglesCommand(fsm, [150,150,150,150]),

            SetOuterServoAngleCommand(fsm, [40,40,40,40]),

            ]
        
        self._Sprint4CansBlue: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 55),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),

            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),

            MoveBackwardCommand(fsm, 60),


            RotateLeftCommand(fsm, rotation),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),

            MoveForwardCommand(fsm, 40),
            RotateLeftCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self._Sprint4CansYellows: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 55),

            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),

            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),

            MoveBackwardCommand(fsm, 60),

            RotateRightCommand(fsm, rotation),
            ToggleUltrasonicSensorsCommand(fsm, positions= [USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),

            MoveForwardCommand(fsm, 40),
            RotateRightCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self.wheeltest: list[ICommand] = [
            RotateLeftCommand(fsm, 10),
        ]

        self.reedswitchTest: list[ICommand] = [
            ReedSwitchCommand(fsm)
        ]

    def get_Init(self) -> list[ICommand]:
        return self._Init

    def get_FirstCanMove(self) -> list[ICommand]:
        return self._FirstCanMove
    
    def get_FirstCanBuildMove(self) -> list[ICommand]:
        return self._FirstCanBuildMove
    
    def get_Sprint4Yellow(self) -> list[ICommand]:
        return self._Sprint4Yellow
    
    def get_Sprint4Blue(self) -> list[ICommand]:
        return self._Sprint4Blue
    
    def get_Sprint4CansBlue(self) -> list[ICommand]:    
        return self._Sprint4CansBlue
    
    def get_Sprint4CansYellows(self) -> list[ICommand]:
        return self._Sprint4CansYellows
    
