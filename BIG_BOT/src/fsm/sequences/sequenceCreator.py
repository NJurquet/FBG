from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand
from ..commands.startCommands import InitCommand
from ..commands.ultrasonicCommands import UltrasonicSensorCommand
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
        
        self.Sprint4Yellow = [
            UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, False),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, False),
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),
            MoveForwardCommand(fsm, 50),
            UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, True),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, True),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 95),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 130),
        ]

        self.Sprint4Blue = [
            UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, False),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, False),
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),
            MoveForwardCommand(fsm, 50),
            UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, True),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, True),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 95),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 130),
        ]

        self.clawtest = [
            #SetServoAngleCommand(fsm, "centerRightClaw", 0),
            #SetServoAngleCommand(fsm, "centerRightClaw", 90),
            SetAllServoAnglesCommand(fsm, [30,30,30,30]),
            SetAllServoAnglesCommand(fsm, [50,50,50,50]),
            SetAllServoAnglesCommand(fsm, [30,30,30,30]),

            SetOuterServoAngleCommand(fsm, [40,40,40,40]),

            ]
        
        self.Sprint4CansBlue = [
            UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, False),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, False),
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),
            MoveForwardCommand(fsm, 50),
            #UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, True),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, True),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 55),

            UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  
            UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),

            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),

            MoveBackwardCommand(fsm, 60),


            RotateLeftCommand(fsm, rotation),
            UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, True),  
            UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, True),

            MoveForwardCommand(fsm, 40),
            RotateLeftCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self.Sprint4CansYellows = [
            UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, False),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, False),
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  
            # UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),
            MoveForwardCommand(fsm, 50),
            #UltrasonicSensorCommand(fsm, USPosition.BACK_LEFT, True),  
            UltrasonicSensorCommand(fsm, USPosition.BACK_RIGHT, True),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 55),

            UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, False),  
            UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, False),

            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),

            MoveBackwardCommand(fsm, 60),


            RotateRightCommand(fsm, rotation),
            UltrasonicSensorCommand(fsm, USPosition.FRONT_LEFT, True),  
            UltrasonicSensorCommand(fsm, USPosition.FRONT_RIGHT, True),

            MoveForwardCommand(fsm, 40),
            RotateRightCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self.wheeltest = [
            RotateLeftCommand(fsm, 10),
        ]

        self.reedswitchTest = [
            ReedSwitchCommand(fsm),
            MoveForwardCommand(fsm, 40),


        ]