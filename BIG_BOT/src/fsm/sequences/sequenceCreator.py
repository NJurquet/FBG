from ..commands.command import ICommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand, setPlankPusherServoAnglesCommand
from ..commands.startCommands import InitCommand
from ..commands.ultrasonicCommands import ToggleUltrasonicSensorsCommand
from ..commands.reedswitchCommands import ReedSwitchCommand
from ...constants import USPosition
from ...config import OUTER_RIGHT_CLAW_NAME, ALL_CLOSED, ALL_OPEN, OUTER_OPEN, PLANK_PUSHER_INIT, PLANK_PUSHER_PUSH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceCreator():
    def __init__(self, fsm: 'RobotFSM'):
        speed = 0.5
        rotation = 100

        self._Init = [
            ReedSwitchCommand(fsm),
            InitCommand(fsm),
            StopCommand(fsm)
        ]
        
        self._FirstCanMove: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            MoveForwardCommand(fsm, 50),
            RotateLeftCommand(fsm, rotation),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Enable front sensors
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
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),  # Disable back sensors
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 95),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 130),
        ]

        self._Sprint4Blue: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 95),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 130),
        ]

        self._clawtest: list[ICommand] = [
            # SetAllServoAnglesCommand(fsm, ALL_OPEN ),

            # SetAllServoAnglesCommand(fsm, ALL_CLOSED),
            # SetAllServoAnglesCommand(fsm, ALL_OPEN),

            #SetOuterServoAngleCommand(fsm, [100, 100]), 
            setPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            setPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT)


        ]
        
        self._Sprint4CansBlue: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 55),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),
            MoveBackwardCommand(fsm, 60),
            RotateLeftCommand(fsm, rotation),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveForwardCommand(fsm, 40),
            RotateLeftCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self._Sprint4CansYellows: list[ICommand] = [
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 55),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),
            MoveBackwardCommand(fsm, 60),
            RotateRightCommand(fsm, rotation),
            ToggleUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveForwardCommand(fsm, 40),
            RotateRightCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self._wheeltest: list[ICommand] = [
            RotateLeftCommand(fsm, 10),
        ]

        self._reedswitchTest: list[ICommand] = [
            ReedSwitchCommand(fsm)
        ]

    @property
    def Init(self) -> list[ICommand]:
        return self._Init

    @Init.setter
    def Init(self, sequence: list[ICommand]):
        self._Init = sequence

    @property
    def FirstCanMove(self) -> list[ICommand]:
        return self._FirstCanMove
    
    @FirstCanMove.setter
    def FirstCanMove(self, sequence: list[ICommand]):
        self._FirstCanMove = sequence
    
    @property
    def FirstCanBuildMove(self) -> list[ICommand]:
        return self._FirstCanBuildMove
    
    @FirstCanBuildMove.setter
    def FirstCanBuildMove(self, sequence: list[ICommand]):
        self._FirstCanBuildMove = sequence
    
    @property
    def Sprint4Yellow(self) -> list[ICommand]:
        return self._Sprint4Yellow
    
    @Sprint4Yellow.setter
    def Sprint4Yellow(self, sequence: list[ICommand]):
        self._Sprint4Yellow = sequence
    
    @property
    def Sprint4Blue(self) -> list[ICommand]:
        return self._Sprint4Blue
    
    @Sprint4Blue.setter
    def Sprint4Blue(self, sequence: list[ICommand]):
        self._Sprint4Blue = sequence
    
    @property
    def clawtest(self) -> list[ICommand]:
        return self._clawtest
    
    @clawtest.setter
    def clawtest(self, sequence: list[ICommand]):
        self._clawtest = sequence
    
    @property
    def Sprint4CansBlue(self) -> list[ICommand]:
        return self._Sprint4CansBlue
    
    @Sprint4CansBlue.setter
    def Sprint4CansBlue(self, sequence: list[ICommand]):
        self._Sprint4CansBlue = sequence
    
    @property
    def Sprint4CansYellows(self) -> list[ICommand]:
        return self._Sprint4CansYellows
    
    @Sprint4CansYellows.setter
    def Sprint4CansYellows(self, sequence: list[ICommand]):
        self._Sprint4CansYellows = sequence
    
    @property
    def wheeltest(self) -> list[ICommand]:
        return self._wheeltest
    
    @wheeltest.setter
    def wheeltest(self, sequence: list[ICommand]):
        self._wheeltest = sequence
    
    @property
    def reedswitchTest(self) -> list[ICommand]:
        return self._reedswitchTest
    
    @reedswitchTest.setter
    def reedswitchTest(self, sequence: list[ICommand]):
        self._reedswitchTest = sequence