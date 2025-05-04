from ..commands.command import ICommand, ITimeBasedCommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand, SetPlankPusherServoAnglesCommand, SetBannerDeployerServoAngleCommand
from ..commands.ultrasonicCommands import DisableUltrasonicSensorsCommand, EnableUltrasonicSensorsCommand
from ..commands.reedswitchCommands import ReedSwitchCommand
from ..commands.frontPlateCommands import RaiseFrontPlateCommand, LowerFrontPlateCommand, InitFrontPlateCommand, MoveFrontPlateCommand
from ..commands.timeCommands import WaitCommand, WaitForTargetTimeCommand
from ..commands.initCommands import InitLCDCommand
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

        self._IdleState: list[ICommand | ITimeBasedCommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_MIDDLE, USPosition.FRONT_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.CENTER_LEFT, USPosition.CENTER_RIGHT]),
            #InitFrontPlateCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_BLOCKING),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE),
            WaitCommand(fsm, 1.0),
            SetAllServoAnglesCommand(fsm, SERVO_IDLE),            
            WaitCommand(fsm, 1.0)
        ]

        self._Init: list[ICommand | ITimeBasedCommand] = [
            ReedSwitchCommand(fsm),
            WaitCommand(fsm, 0.5),
            InitLCDCommand(fsm),
            WaitCommand(fsm, 0.5),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_MIDDLE),
            WaitCommand(fsm, 0.5),
            SetOuterServoAngleCommand(fsm, OUTER_INIT),
            WaitCommand(fsm, 0.5),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            WaitCommand(fsm, 0.5),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
        ]

        self._DeployBanner: list[ICommand | ITimeBasedCommand] = [
            WaitCommand(fsm, 0.5,),
            MoveForwardCommand(fsm, 10, re_enable_us_sensors=False, enable_direction_sensors=False),
            WaitCommand(fsm, 1.5),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1),
            WaitCommand(fsm, 0.5),
            MoveBackwardCommand(fsm, 6, re_enable_us_sensors=False, enable_direction_sensors=False),           
            WaitCommand(fsm, 1.5),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 10, re_enable_us_sensors=False, enable_direction_sensors=True),
        ]

        self._MoveToSecondCans_Yellow: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 45),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 35, re_enable_us_sensors=True, enable_direction_sensors=True),
            WaitCommand(fsm, 0.5),
            MoveBackwardCommand(fsm, 20, re_enable_us_sensors=True, enable_direction_sensors=True),
            StopCommand(fsm),
        ]

        self._MoveToSecondCans_Blue: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 45),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 35, re_enable_us_sensors=True, enable_direction_sensors=True),
            WaitCommand(fsm, 0.5),
            MoveBackwardCommand(fsm, 20, re_enable_us_sensors=True, enable_direction_sensors=True),
            StopCommand(fsm),
        ]

        self._CollectCans: list[ICommand | ITimeBasedCommand] = [
            # LowerFrontPlateCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 20, re_enable_us_sensors=True, enable_direction_sensors=True),
            WaitCommand(fsm, 0.5),
            SetAllServoAnglesCommand(fsm, ALL_CLOSED),
            WaitCommand(fsm, 0.5),
            #MoveFrontPlateCommand(fsm, STEPPER_MIDDLE_POINT),
            MoveBackwardCommand(fsm, 20, re_enable_us_sensors=True, enable_direction_sensors=True),
        ]

        self._Build1StoryBleachers: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 20, re_enable_us_sensors=False, enable_direction_sensors=False),
            # LowerFrontPlateCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            MoveBackwardCommand(fsm, 20, re_enable_us_sensors=True),
            # RaiseFrontPlateCommand(fsm),
        ]

        self._Build2StoryBleachers: list[ICommand | ITimeBasedCommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            MoveForwardCommand(fsm, 20),
            #LowerFrontPlateCommand(fsm),
            SetOuterServoAngleCommand(fsm, OUTER_OPEN),
            MoveBackwardCommand(fsm, 15),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_PUSH),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            # RaiseFrontPlateCommand(fsm),
            MoveForwardCommand(fsm, 15),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            # MoveFrontPlateCommand(fsm, 600),
            MoveBackwardCommand(fsm, 20),
            # RaiseFrontPlateCommand(fsm),
            #EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
        ]

        self._RushFromStart_Yellow: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 30),
            WaitCommand(fsm, 1.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 1.5),
            MoveForwardCommand(fsm, 65),
            WaitCommand(fsm, 1.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 1.5),
            MoveForwardCommand(fsm, 50),
            WaitForTargetTimeCommand(fsm, time_target=95.0),
            MoveForwardCommand(fsm, 40),
        ]

        self._RushFromStart_Blue: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 30),
            WaitCommand(fsm, 1.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 1.5),
            MoveForwardCommand(fsm, 65),
            WaitCommand(fsm, 1.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 1.5),
            MoveForwardCommand(fsm, 50),
            WaitForTargetTimeCommand(fsm, time_target=95.0),
            MoveForwardCommand(fsm, 40),
        ]
        
        # Steps 3 to 7 on graph : Center cans => most accessible ones
        self._FirstCansCollectMove_Yellow: list[ICommand | ITimeBasedCommand] = [            
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 8),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 20, re_enable_us_sensors=True, enable_direction_sensors=False),
            StopCommand(fsm),
        ]

        self._FirstCansCollectMove_Blue: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 8),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 20),
            StopCommand(fsm),
        ]
        
        # Steps 8 to 11 on graph
        self._FirstCansBuildMove_Yellow: list[ICommand | ITimeBasedCommand] = [
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 10),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 20),
            StopCommand(fsm),
        ]

        self._FirstCansBuildMove_Blue: list[ICommand | ITimeBasedCommand] = [
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 10),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 40),
            StopCommand(fsm),
        ]

        # Steps 12 to 17 on graph : Cans to the left (yellow) or right (blue) => just need to push
        self._SecondCansPushMove_Yellow: list[ICommand | ITimeBasedCommand] = [
            RotateRightCommand(fsm, 180),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 55),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 55, re_enable_us_sensors=True, enable_direction_sensors=False),
            WaitCommand(fsm, 0.5),
        ]

        self._SecondCansPushMove_Blue: list[ICommand | ITimeBasedCommand] = [
            RotateLeftCommand(fsm, 180),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 55),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 55, re_enable_us_sensors=True, enable_direction_sensors=False),
            WaitCommand(fsm, 0.5),
        ]

        self._RushToEndFromSecondCans_Yellow: list[ICommand | ITimeBasedCommand] = [
            MoveBackwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 180),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 100),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 40),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            WaitForTargetTimeCommand(fsm, time_target=95.0),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 45),
        ]

        self._RushToEndFromSecondCans_Blue: list[ICommand | ITimeBasedCommand] = [
            MoveBackwardCommand(fsm, 20),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 180),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 100),
            WaitCommand(fsm, 0.5),
            RotateRightCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 40),
            WaitCommand(fsm, 0.5),
            RotateLeftCommand(fsm, 90),
            WaitCommand(fsm, 0.5),
            WaitForTargetTimeCommand(fsm, time_target=95.0),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 45),
        ]

        # Steps 18 to 21 on graph : Cans on the edge => bring back to spawn
        self._ThirdCansCollectMove_Blue: list[ICommand | ITimeBasedCommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 80),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
        ]

        # Steps 22 to 25 on graph : Cans on the edge => bring back to spawn
        self._ThirdCansBuildMove_Blue: list[ICommand | ITimeBasedCommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 150),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 20),
        ]

        # Step 26 to 31 : Go to the end & wait for a certain moment
        self._GoToEndMove: list[ICommand | ITimeBasedCommand] = [
            RotateRightCommand(fsm, 180),
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            WaitForTargetTimeCommand(fsm, time_target=95.0),
            MoveForwardCommand(fsm, 50),
        ]

        self._HomologationMove: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 100),
            MoveBackwardCommand(fsm, 80),
            RotateLeftCommand(fsm, 180),
            RotateRightCommand(fsm, 180),
        ]

        self._wheeltest: list[ICommand | ITimeBasedCommand] = [
            MoveForwardCommand(fsm, 20),
            WaitCommand(fsm, 2.0),
            MoveBackwardCommand(fsm, 20),
        ]

        self._timeMoveTest: list[ICommand | ITimeBasedCommand] = [
            WaitCommand(fsm, 2.0),
            MoveForwardCommand(fsm, 20),
            WaitForTargetTimeCommand(fsm, time_target=95.0), 
            MoveForwardCommand(fsm, 20),
        ]

        self._reedswitchTest: list[ICommand | ITimeBasedCommand] = [
            ReedSwitchCommand(fsm)
        ]

        self._bannerTest: list[ICommand | ITimeBasedCommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.CENTER_LEFT, USPosition.CENTER_RIGHT]),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2),
        ]

    @property
    def IdleState(self) -> list[ICommand | ITimeBasedCommand]:
        return self._IdleState

    @property
    def Init(self) -> list[ICommand | ITimeBasedCommand]:
        return self._Init

    @property
    def DeployBanner(self) -> list[ICommand | ITimeBasedCommand]:
        return self._DeployBanner

    @property
    def MoveToSecondCans(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._MoveToSecondCans_Yellow
        else:
            return self._MoveToSecondCans_Blue

    @property
    def CollectCans(self) -> list[ICommand | ITimeBasedCommand]:
        return self._CollectCans

    @property
    def Build1StoryBleachers(self) -> list[ICommand | ITimeBasedCommand]:
        return self._Build1StoryBleachers

    @property
    def Build2StoryBleachers(self) -> list[ICommand | ITimeBasedCommand]:
        return self._Build2StoryBleachers

    @property
    def RushFromStart(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._RushFromStart_Yellow
        else:
            return self._RushFromStart_Blue

    @property
    def FirstCansCollectMove(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._FirstCansCollectMove_Yellow
        else:
            return self._FirstCansCollectMove_Blue
    
    @property
    def FirstCansBuildMove(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._FirstCansBuildMove_Yellow
        else:
            return self._FirstCansBuildMove_Blue

    @property
    def SecondCansPushMove(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._SecondCansPushMove_Yellow
        else:
            return self._SecondCansPushMove_Blue

    @property
    def RushToEndFromSecondCans(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._RushToEndFromSecondCans_Yellow
        else:
            return self._RushToEndFromSecondCans_Blue

    @property
    def ThirdCansCollectMove(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._ThirdCansCollectMove_Blue
        else:
            return self._ThirdCansCollectMove_Blue

    @property
    def ThirdCansBuildMove(self) -> list[ICommand | ITimeBasedCommand]:
        if self.color == "yellow":
            return self._ThirdCansBuildMove_Blue
        else:
            return self._ThirdCansBuildMove_Blue

    @property
    def GoToEndMove(self) -> list[ICommand | ITimeBasedCommand]:
        return self._GoToEndMove

    @property
    def MainSequence(self) -> list[list[ICommand | ITimeBasedCommand]]:
        return [
            self.IdleState,
            self.Init,
            self.DeployBanner,
            self.RushFromStart,
            # self.FirstCansCollectMove,
            # self.CollectCans,
            # self.FirstCansBuildMove,
            # self.Build1StoryBleachers,
            # self.SecondCansPushMove,
            # self.RushToEndFromSecondCans,
            #self.ThirdCansCollectMove,
            #self.CollectCans,
            #self.ThirdCansBuildMove,
            #self.Build1StoryBleachers,
            #self.GoToEndMove
        ]

    @property
    def wheeltest(self) -> list[ICommand | ITimeBasedCommand]:
        return self._wheeltest
    
    @property
    def reedswitchTest(self) -> list[ICommand | ITimeBasedCommand]:
        return self._reedswitchTest