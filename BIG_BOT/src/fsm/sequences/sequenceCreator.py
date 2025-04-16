from ..commands.command import ICommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand, SetPlankPusherServoAnglesCommand, SetBannerDeployerServoAngleCommand
from ..commands.startCommands import InitCommand
from ..commands.ultrasonicCommands import ToggleUltrasonicSensorsCommand, DisableUltrasonicSensorsCommand, EnableUltrasonicSensorsCommand
from ..commands.reedswitchCommands import ReedSwitchCommand
from ..commands.frontPlateCommands import RaiseFrontPlateCommand, LowerFrontPlateCommand, InitFrontPlateCommand, MoveFrontPlateCommand
from ...constants import USPosition
from ...config import OUTER_RIGHT_CLAW_NAME, ALL_CLOSED, ALL_OPEN, OUTER_OPEN, PLANK_PUSHER_BLOCKING, PLANK_PUSHER_MIDDLE, PLANK_PUSHER_INIT, PLANK_PUSHER_PUSH, BANNER_DEPLOYER_DEPLOY_STAGE_1, BANNER_DEPLOYER_IDLE, BANNER_DEPLOYER_DEPLOY_STAGE_2
from ...config import STEPPER_MIDDLE_POINT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceCreator():
    def __init__(self, fsm: 'RobotFSM', color: str):
        speed = 0.5
        rotation = 100
        if color == "yellow" or "blue":
            self.color = color
        else:
            raise ValueError("Invalid color. Please choose 'yellow' or 'blue'.")

        self._IdleState: list[ICommand] = [
            InitFrontPlateCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_BLOCKING),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
        ]

        self._Init: list[ICommand] = [
            ReedSwitchCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_MIDDLE),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            # InitCommand(fsm),
            StopCommand(fsm)
        ]

        self._DeployBanner: list[ICommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveForwardCommand(fsm, 15),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1),
            MoveBackwardCommand(fsm, 10),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2),
            MoveForwardCommand(fsm, 15),
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
        ]

        self._CollectCans: list[ICommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            LowerFrontPlateCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            MoveForwardCommand(fsm, 20),
            SetAllServoAnglesCommand(fsm, ALL_CLOSED),
            #MoveFrontPlateCommand(fsm, STEPPER_MIDDLE_POINT),
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveBackwardCommand(fsm, 20),
        ]

        self._Build1StoryBleachers: list[ICommand] = [
            MoveForwardCommand(fsm, 20),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            LowerFrontPlateCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            MoveBackwardCommand(fsm, 20),
            RaiseFrontPlateCommand(fsm),
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
        ]

        self._Build2StoryBleachers: list[ICommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveForwardCommand(fsm, 20),
            #LowerFrontPlateCommand(fsm),
            SetOuterServoAngleCommand(fsm, OUTER_OPEN),
            MoveBackwardCommand(fsm, 15),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_PUSH),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            RaiseFrontPlateCommand(fsm),
            MoveForwardCommand(fsm, 15),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            MoveFrontPlateCommand(fsm, 600),
            MoveBackwardCommand(fsm, 20),
            RaiseFrontPlateCommand(fsm),
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
        ]
        
        self._CenterCansCollectMove_Yellow: list[ICommand] = [
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            MoveForwardCommand(fsm, 50),
            RotateLeftCommand(fsm, rotation),
            #DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Enable front sensors
            MoveForwardCommand(fsm, 5),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 30),
        ]

        self._CenterCansCollectMove_Blue: list[ICommand] = [
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, rotation),
            # DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Enable front sensors
            MoveForwardCommand(fsm, 5),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 30),
        ]
        
        self._CenterCansBuildMove_Yellow: list[ICommand] = [
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT, USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),  # Enable front sensors
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
            MoveBackwardCommand(fsm, 5),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 50),
            # DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT, USPosition.BACK_LEFT, USPosition.BACK_RIGHT] ),
        ]

        self._CenterCansBuildMove_Blue: list[ICommand] = [
            MoveBackwardCommand(fsm, 30),
            RotateLeftCommand(fsm, rotation),
            MoveBackwardCommand(fsm, 5),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 50),
        ]

        self._InnerLowerCansMove_Yellow: list[ICommand] = [
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
        ]

        self._InnerLowerCansMove_Blue: list[ICommand] = [
            MoveBackwardCommand(fsm, 30),
            RotateLeftCommand(fsm, rotation),
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
            SetBannerDeployerServoAngleCommand(fsm,170),

        ]

        self._clawtest: list[ICommand] = [
            # SetAllServoAnglesCommand(fsm, [150, 150, 150, 150]),
            # MoveFrontPlateCommand(fsm, 200),
            # MoveForwardCommand(fsm, 40),
            
            # SetAllServoAnglesCommand(fsm, [90, 90, 90, 90]),
            # SetAllServoAnglesCommand(fsm, [150, 150, 150, 150]),
            # SetOuterServoAngleCommand(fsm, [40, 40, 40, 40]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT, USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            SetBannerDeployerServoAngleCommand(fsm,170),
            SetBannerDeployerServoAngleCommand(fsm, 130),
            MoveBackwardCommand(fsm, 15),
            SetBannerDeployerServoAngleCommand(fsm, 10),
            MoveForwardCommand(fsm, 10)


            # SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY),
            # SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_END)

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
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 50),
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            RotateLeftCommand(fsm, rotation),
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            MoveForwardCommand(fsm, 55),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 60),
            MoveBackwardCommand(fsm, 60),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 40),
            RotateRightCommand(fsm, 110),
            MoveForwardCommand(fsm, 140),
        ]

        self._frontPlateTest: list[ICommand] = [
            SetAllServoAnglesCommand(fsm, ALL_OPEN),

            InitFrontPlateCommand(fsm),


        ]

        self._frontPlantUp : list[ICommand] = [
            SetAllServoAnglesCommand(fsm, [90, 90, 90, 90]),


            RaiseFrontPlateCommand(fsm),
            MoveForwardCommand(fsm, 25),
        ]


        self._wheeltest: list[ICommand] = [
            RotateLeftCommand(fsm, 10),
        ]

        self._reedswitchTest: list[ICommand] = [
            ReedSwitchCommand(fsm)
        ]

        self._bannerTest: list[ICommand] = [
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE),
        ]

    @property
    def IdleState(self) -> list[ICommand]:
        return self._IdleState

    @IdleState.setter
    def IdleState(self, sequence: list[ICommand]):
        self._IdleState = sequence

    @property
    def Init(self) -> list[ICommand]:
        return self._Init

    @Init.setter
    def Init(self, sequence: list[ICommand]):
        self._Init = sequence

    @property
    def DeployBanner(self) -> list[ICommand]:
        return self._DeployBanner
    
    @DeployBanner.setter
    def DeployBanner(self, sequence: list[ICommand]):
        self._DeployBanner = sequence

    @property
    def CollectCans(self) -> list[ICommand]:
        return self._CollectCans
    
    @CollectCans.setter
    def CollectCans(self, sequence: list[ICommand]):
        self._CollectCans = sequence

    @property
    def Build1StoryBleachers(self) -> list[ICommand]:
        return self._Build1StoryBleachers
    
    @Build1StoryBleachers.setter
    def Build1StoryBleachers(self, sequence: list[ICommand]):
        self._Build1StoryBleachers = sequence

    @property
    def Build2StoryBleachers(self) -> list[ICommand]:
        return self._Build2StoryBleachers
    
    @Build2StoryBleachers.setter
    def Build2StoryBleachers(self, sequence: list[ICommand]):
        self._Build2StoryBleachers = sequence

    @property
    def FirstCansCollectMove(self) -> list[ICommand]:
        if self.color == "yellow":
            return self._CenterCansCollectMove_Yellow
        elif self.color == "blue":
            return self._CenterCansCollectMove_Blue
    
    @FirstCansCollectMove.setter
    def FirstCansCollectMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._CenterCansCollectMove_Yellow = sequence
        elif self.color == "blue":
            self._CenterCansCollectMove_Blue = sequence
    
    @property
    def FirstCanBuildMove(self) -> list[ICommand]:
        if self.color == "yellow":
            return self._CenterCansBuildMove_Yellow
        elif self.color == "blue":
            return self._FirstCanBuildMove_Blue
    
    @FirstCanBuildMove.setter
    def FirstCanBuildMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._CenterCansBuildMove_Yellow = sequence
        elif self.color == "blue":
            self._FirstCanBuildMove_Blue = sequence
    
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
    
    @property
    def frontPlateTest(self) -> list[ICommand]:
        return self._frontPlateTest
    @frontPlateTest.setter
    def frontPlateTest(self, sequence: list[ICommand]):
        self._frontPlateTest = sequence

    @property
    def frontPlantUp(self) -> list[ICommand]:
        return self._frontPlantUp
    @frontPlantUp.setter
    def frontPlantUp(self, sequence: list[ICommand]):
        self._frontPlantUp = sequence