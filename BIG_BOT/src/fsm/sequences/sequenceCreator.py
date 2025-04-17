from ..commands.command import ICommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand, SetPlankPusherServoAnglesCommand, SetBannerDeployerServoAngleCommand
from ..commands.startCommands import InitCommand
from ..commands.ultrasonicCommands import ToggleUltrasonicSensorsCommand, DisableUltrasonicSensorsCommand, EnableUltrasonicSensorsCommand
from ..commands.reedswitchCommands import ReedSwitchCommand
from ..commands.frontPlateCommands import RaiseFrontPlateCommand, LowerFrontPlateCommand, InitFrontPlateCommand, MoveFrontPlateCommand
from ...constants import USPosition
from ...config import OUTER_RIGHT_CLAW_NAME, ALL_CLOSED, ALL_OPEN, SERVO_IDLE, SERVO_INIT, OUTER_OPEN, OUTER_INIT, PLANK_PUSHER_BLOCKING, PLANK_PUSHER_MIDDLE, PLANK_PUSHER_INIT, PLANK_PUSHER_PUSH, BANNER_DEPLOYER_DEPLOY_STAGE_1, BANNER_DEPLOYER_IDLE, BANNER_DEPLOYER_DEPLOY_STAGE_2
from ...config import STEPPER_MIDDLE_POINT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FSM import RobotFSM

class SequenceCreator():
    def __init__(self, fsm: 'RobotFSM', color: str):
        speed = 0.5
        rotation = 100
        if color in ["yellow", "blue"]:
            self.color = color
        else:
            raise ValueError("Invalid color. Please choose 'yellow' or 'blue'.")

        self._IdleState: list[ICommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.CENTER_LEFT, USPosition.CENTER_RIGHT]),
            #InitFrontPlateCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_BLOCKING),
            StopCommand(fsm),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE),
            StopCommand(fsm),
            SetAllServoAnglesCommand(fsm, SERVO_IDLE),
        ]

        self._Init: list[ICommand] = [
            ReedSwitchCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_MIDDLE),
            StopCommand(fsm),
            SetOuterServoAngleCommand(fsm, OUTER_INIT, time_needed=1.0),
            StopCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            StopCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
        ]

        self._DeployBanner: list[ICommand] = [
            MoveForwardCommand(fsm, 15, enable_us_sensors=False),
            StopCommand(fsm),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1, time_needed=1.0),
            MoveBackwardCommand(fsm, 10, enable_us_sensors=False),           
            StopCommand(fsm),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2, time_needed=1.0),
            MoveForwardCommand(fsm, 15, enable_us_sensors=False),
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
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
        
        # Steps 3 to 7 on graph : Center cans => most accessible ones
        self._FirstCansCollectMove_Yellow: list[ICommand] = [
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            MoveForwardCommand(fsm, 50),
            RotateLeftCommand(fsm, rotation),
            #DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Enable front sensors
            MoveForwardCommand(fsm, 5),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 30),
        ]

        self._FirstCansCollectMove_Blue: list[ICommand] = [
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, rotation),
            # DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Enable front sensors
            MoveForwardCommand(fsm, 5),
            RotateLeftCommand(fsm, rotation),
            MoveForwardCommand(fsm, 30),
        ]
        
        # Steps 8 to 11 on graph
        self._FirstCansBuildMove_Yellow: list[ICommand] = [
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT, USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),  # Enable front sensors
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
            MoveBackwardCommand(fsm, 5),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 50),
            # DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT, USPosition.BACK_LEFT, USPosition.BACK_RIGHT] ),
        ]

        self._FirstCansBuildMove_Blue: list[ICommand] = [
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 5),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
        ]

        # Steps 12 to 17 on graph : Cans to the left (yellow) or right (blue) => just need to push
        self._SecondCansPushMove_Yellow: list[ICommand] = [
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
        ]

        self._SecondCansPushMove_Blue: list[ICommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 80),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 80),
        ]

        # Steps 18 to 21 on graph : Cans on the edge => bring back to spawn
        self._ThirdCansCollectMove_Blue: list[ICommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 80),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
        ]

        # Steps 22 to 25 on graph : Cans on the edge => bring back to spawn
        self._ThirdCansBuildMove_Blue: list[ICommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 150),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 20),
        ]

        # Step 26 to 31 : Go to the end & wait for a certain moment
        self._GoToEndMove: list[ICommand] = [
            RotateRightCommand(fsm, 180),
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveForwardCommand(fsm, 50, time_target=95.0),
        ]

        self._HomologationMove: list[ICommand] = [
            MoveForwardCommand(fsm, 100),
            MoveBackwardCommand(fsm, 80),
            RotateLeftCommand(fsm, 180),
            RotateRightCommand(fsm, 180),
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
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE, time_needed=1.0),
            StopCommand(fsm),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1, time_needed=1.0),
            StopCommand(fsm),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2, time_needed=1.0),
            StopCommand(fsm),
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
            return self._FirstCansCollectMove_Yellow
        else:
            return self._FirstCansCollectMove_Blue
    @FirstCansCollectMove.setter
    def FirstCansCollectMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._FirstCansCollectMove_Yellow = sequence
        else:
            self._FirstCansCollectMove_Blue = sequence
    
    @property
    def FirstCansBuildMove(self) -> list[ICommand]:
        if self.color == "yellow":
            return self._FirstCansBuildMove_Yellow
        else:
            return self._FirstCansBuildMove_Blue
    @FirstCansBuildMove.setter
    def FirstCansBuildMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._FirstCansBuildMove_Yellow = sequence
        else:
            self._FirstCansBuildMove_Blue = sequence

    @property
    def SecondCansPushMove(self) -> list[ICommand]:
        if self.color == "yellow":
            return self._SecondCansPushMove_Yellow
        else:
            return self._SecondCansPushMove_Blue
    @SecondCansPushMove.setter
    def SecondCansPushMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._SecondCansPushMove_Yellow = sequence
        else:
            self._SecondCansPushMove_Blue = sequence

    @property
    def ThirdCansCollectMove(self) -> list[ICommand]:
        if self.color == "yellow":
            return self._ThirdCansCollectMove_Blue
        else:
            return self._ThirdCansCollectMove_Blue
    @ThirdCansCollectMove.setter
    def ThirdCansCollectMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._ThirdCansCollectMove_Blue = sequence
        else:
            self._ThirdCansCollectMove_Blue = sequence

    @property
    def ThirdCansBuildMove(self) -> list[ICommand]:
        if self.color == "yellow":
            return self._ThirdCansBuildMove_Blue
        else:
            return self._ThirdCansBuildMove_Blue
    @ThirdCansBuildMove.setter
    def ThirdCansBuildMove(self, sequence: list[ICommand]):
        if self.color == "yellow":
            self._ThirdCansBuildMove_Blue = sequence
        else:
            self._ThirdCansBuildMove_Blue = sequence

    @property
    def GoToEndMove(self) -> list[ICommand]:
        return self._GoToEndMove
    @GoToEndMove.setter
    def GoToEndMove(self, sequence: list[ICommand]):
            self._GoToEndMove = sequence

    @property
    def MainSequence(self) -> list[list[ICommand]]:
        return [
            #self.IdleState,
            #self.Init,
            #self.DeployBanner,
            self.FirstCansCollectMove,
            # self.CollectCans,
            self.FirstCansBuildMove,
            # self.Build1StoryBleachers,
            self.SecondCansPushMove,
            self.ThirdCansCollectMove,
            #self.CollectCans,
            self.ThirdCansBuildMove,
            #self.Build1StoryBleachers,
            self.GoToEndMove
        ]
    # @MainSequence.setter
    # def MainSequence(self, sequence_list: list[list[ICommand]]):
    #     self.IdleState = sequence_list[0]
    #     self.Init = sequence_list[1]
    #     self.DeployBanner = sequence_list[2]
    #     self.FirstCansCollectMove = sequence_list[3]
    #     self.CollectCans = sequence_list[4]
    #     self.FirstCansBuildMove = sequence_list[5]
    #     self.Build1StoryBleachers = sequence_list[6]
    #     self.SecondCansPushMove = sequence_list[7]
    
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