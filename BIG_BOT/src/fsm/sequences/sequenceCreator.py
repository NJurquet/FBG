from ..commands.command import ICommand, ITimeBasedCommand, IMoveCommand
from ..commands.moveCommands import MoveForwardCommand, MoveBackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand
from ..commands.servoCommands import SetOuterServoAngleCommand, SetAllServoAnglesCommand, SetPlankPusherServoAnglesCommand, SetBannerDeployerServoAngleCommand
from ..commands.ultrasonicCommands import ToggleUltrasonicSensorsCommand, DisableUltrasonicSensorsCommand, EnableUltrasonicSensorsCommand
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

        self._IdleState: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.CENTER_LEFT, USPosition.CENTER_RIGHT]),
            #InitFrontPlateCommand(fsm),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_BLOCKING),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE),
            WaitCommand(fsm, 1.0),
            SetAllServoAnglesCommand(fsm, SERVO_IDLE),            
            WaitCommand(fsm, 1.0)
        ]

        self._Init: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            ReedSwitchCommand(fsm),
            WaitCommand(fsm, 1.0),
            InitLCDCommand(fsm),
            WaitCommand(fsm, 0.5),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_MIDDLE),
            WaitCommand(fsm, 0.5),
            SetOuterServoAngleCommand(fsm, OUTER_INIT, time_needed=1.0),
            WaitCommand(fsm, 0.5),
            SetPlankPusherServoAnglesCommand(fsm, PLANK_PUSHER_INIT),
            WaitCommand(fsm, 0.5),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
        ]

        self._DeployBanner: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            WaitCommand(fsm, 1.0),
            MoveForwardCommand(fsm, 15, re_enable_us_sensors=False, enable_direction_sensors=False),
            WaitCommand(fsm, 0.5),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1, time_needed=1.0),
            WaitCommand(fsm, 0.5),
            MoveBackwardCommand(fsm, 10, re_enable_us_sensors=False, enable_direction_sensors=False),           
            WaitCommand(fsm, 1.0),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2, time_needed=1.0),
            # MoveForwardCommand(fsm, 15, re_enable_us_sensors=False, enable_direction_sensors=False),
            WaitCommand(fsm, 0.5),
            MoveForwardCommand(fsm, 30, re_enable_us_sensors=False, enable_direction_sensors=False),
        ]

        self._MoveToSecondCans_Yellow: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            WaitCommand(fsm, 1.0),
            RotateLeftCommand(fsm, 90, ),
            WaitCommand(fsm, 1.0),
            MoveForwardCommand(fsm, 40, ),
            WaitCommand(fsm, 1.0),
            RotateLeftCommand(fsm, 90, ),
            WaitCommand(fsm, 1.0),
            MoveForwardCommand(fsm, 20, ),
        ]

        self._MoveToSecondCans_Blue: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            WaitCommand(fsm, 1.0),
            RotateRightCommand(fsm, 90, ),
            WaitCommand(fsm, 1.0),
            MoveForwardCommand(fsm, 40, ),
            WaitCommand(fsm, 1.0),
            RotateRightCommand(fsm, 90, ),
            WaitCommand(fsm, 1.0),
            MoveForwardCommand(fsm, 20, ),
        ]

        self._CollectCans: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            # LowerFrontPlateCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            MoveForwardCommand(fsm, 20, re_enable_us_sensors=False, enable_direction_sensors=False),
            SetAllServoAnglesCommand(fsm, ALL_CLOSED),
            #MoveFrontPlateCommand(fsm, STEPPER_MIDDLE_POINT),
            MoveBackwardCommand(fsm, 20),
        ]

        self._Build1StoryBleachers: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            MoveForwardCommand(fsm, 20, re_enable_us_sensors=False, enable_direction_sensors=False),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            # LowerFrontPlateCommand(fsm),
            SetAllServoAnglesCommand(fsm, ALL_OPEN),
            MoveBackwardCommand(fsm, 20, re_enable_us_sensors=False),
            # RaiseFrontPlateCommand(fsm),
        ]

        self._Build2StoryBleachers: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
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
        
        # Steps 3 to 7 on graph : Center cans => most accessible ones
        self._FirstCansCollectMove_Yellow: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            EnableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),  # Disable front sensors
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 10),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 10),
        ]

        self._FirstCansCollectMove_Blue: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            MoveForwardCommand(fsm, 20),
            StopCommand(fsm),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 10),
            StopCommand(fsm),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 10),
        ]
        
        # Steps 8 to 11 on graph
        self._FirstCansBuildMove_Yellow: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            MoveBackwardCommand(fsm, 30),
            StopCommand(fsm),
            RotateRightCommand(fsm, rotation),
            MoveBackwardCommand(fsm, 5),
            StopCommand(fsm),
            RotateRightCommand(fsm, rotation),
            MoveForwardCommand(fsm, 50),
        ]

        self._FirstCansBuildMove_Blue: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 10),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 30),
        ]

        # Steps 12 to 17 on graph : Cans to the left (yellow) or right (blue) => just need to push
        self._SecondCansPushMove_Yellow: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            MoveBackwardCommand(fsm, 30),
            RotateRightCommand(fsm, rotation),
        ]

        self._SecondCansPushMove_Blue: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 50),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 80),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 80),
        ]

        # Steps 18 to 21 on graph : Cans on the edge => bring back to spawn
        self._ThirdCansCollectMove_Blue: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 80),
            RotateRightCommand(fsm, 90),
            MoveForwardCommand(fsm, 100),
        ]

        # Steps 22 to 25 on graph : Cans on the edge => bring back to spawn
        self._ThirdCansBuildMove_Blue: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            RotateLeftCommand(fsm, 180),
            MoveForwardCommand(fsm, 150),
            RotateLeftCommand(fsm, 90),
            MoveForwardCommand(fsm, 20),
        ]

        # Step 26 to 31 : Go to the end & wait for a certain moment
        self._GoToEndMove: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
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

        self._HomologationMove: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            MoveForwardCommand(fsm, 100),
            MoveBackwardCommand(fsm, 80),
            RotateLeftCommand(fsm, 180),
            RotateRightCommand(fsm, 180),
        ]

        self._wheeltest: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            #MoveForwardCommand(fsm, 70, re_enable_us_sensors=False),
            WaitCommand(fsm, 1.0),
            RotateLeftCommand(fsm, 90, enable_back_sensors=False, enable_front_sensors=False, enable_side_sensors= False),
            WaitCommand(fsm, 1.0),
            RotateRightCommand(fsm, 90, enable_back_sensors=False, enable_front_sensors=False, enable_side_sensors= False),
        ]

        self._reedswitchTest: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            ReedSwitchCommand(fsm)
        ]

        self._bannerTest: list[ICommand | ITimeBasedCommand | IMoveCommand] = [
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.BACK_LEFT, USPosition.BACK_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.FRONT_LEFT, USPosition.FRONT_RIGHT]),
            DisableUltrasonicSensorsCommand(fsm, positions=[USPosition.CENTER_LEFT, USPosition.CENTER_RIGHT]),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_IDLE, time_needed=1.0),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_1, time_needed=1.0),
            SetBannerDeployerServoAngleCommand(fsm, BANNER_DEPLOYER_DEPLOY_STAGE_2, time_needed=1.0),
        ]

    @property
    def IdleState(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._IdleState
    @IdleState.setter
    def IdleState(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._IdleState = sequence

    @property
    def Init(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Init
    @Init.setter
    def Init(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Init = sequence

    @property
    def DeployBanner(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._DeployBanner
    @DeployBanner.setter
    def DeployBanner(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._DeployBanner = sequence

    @property
    def MoveToSecondCans(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        if self.color == "yellow":
            return self._MoveToSecondCans_Yellow
        else:
            return self._MoveToSecondCans_Blue
    @MoveToSecondCans.setter
    def MoveToSecondCans(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        if self.color == "yellow":
            self._MoveToSecondCans_Yellow = sequence
        else:
            self._MoveToSecondCans_Blue = sequence

    @property
    def CollectCans(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._CollectCans
    @CollectCans.setter
    def CollectCans(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._CollectCans = sequence

    @property
    def Build1StoryBleachers(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Build1StoryBleachers
    @Build1StoryBleachers.setter
    def Build1StoryBleachers(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Build1StoryBleachers = sequence

    @property
    def Build2StoryBleachers(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Build2StoryBleachers
    @Build2StoryBleachers.setter
    def Build2StoryBleachers(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Build2StoryBleachers = sequence

    @property
    def FirstCansCollectMove(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        if self.color == "yellow":
            return self._FirstCansCollectMove_Yellow
        else:
            return self._FirstCansCollectMove_Blue
    @FirstCansCollectMove.setter
    def FirstCansCollectMove(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        if self.color == "yellow":
            self._FirstCansCollectMove_Yellow = sequence
        else:
            self._FirstCansCollectMove_Blue = sequence
    
    @property
    def FirstCansBuildMove(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        if self.color == "yellow":
            return self._FirstCansBuildMove_Yellow
        else:
            return self._FirstCansBuildMove_Blue
    @FirstCansBuildMove.setter
    def FirstCansBuildMove(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        if self.color == "yellow":
            self._FirstCansBuildMove_Yellow = sequence
        else:
            self._FirstCansBuildMove_Blue = sequence

    @property
    def SecondCansPushMove(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        if self.color == "yellow":
            return self._SecondCansPushMove_Yellow
        else:
            return self._SecondCansPushMove_Blue
    @SecondCansPushMove.setter
    def SecondCansPushMove(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        if self.color == "yellow":
            self._SecondCansPushMove_Yellow = sequence
        else:
            self._SecondCansPushMove_Blue = sequence

    @property
    def ThirdCansCollectMove(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        if self.color == "yellow":
            return self._ThirdCansCollectMove_Blue
        else:
            return self._ThirdCansCollectMove_Blue
    @ThirdCansCollectMove.setter
    def ThirdCansCollectMove(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        if self.color == "yellow":
            self._ThirdCansCollectMove_Blue = sequence
        else:
            self._ThirdCansCollectMove_Blue = sequence

    @property
    def ThirdCansBuildMove(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        if self.color == "yellow":
            return self._ThirdCansBuildMove_Blue
        else:
            return self._ThirdCansBuildMove_Blue
    @ThirdCansBuildMove.setter
    def ThirdCansBuildMove(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        if self.color == "yellow":
            self._ThirdCansBuildMove_Blue = sequence
        else:
            self._ThirdCansBuildMove_Blue = sequence

    @property
    def GoToEndMove(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._GoToEndMove
    @GoToEndMove.setter
    def GoToEndMove(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
            self._GoToEndMove = sequence

    @property
    def MainSequence(self) -> list[list[ICommand | ITimeBasedCommand | IMoveCommand]]:
        return [
            self.IdleState,
            self.Init,
            self.DeployBanner,
            self.MoveToSecondCans,
            # self.FirstCansCollectMove,
            # self.CollectCans,
            # self.FirstCansBuildMove,
            # self.Build1StoryBleachers,
            #self.SecondCansPushMove,
            #self.ThirdCansCollectMove,
            #self.CollectCans,
            #self.ThirdCansBuildMove,
            #self.Build1StoryBleachers,
            #self.GoToEndMove
        ]
    # @MainSequence.setter
    # def MainSequence(self, sequence_list: list[list[ICommand | ITimeBasedCommand | IMoveCommand]]):
    #     self.IdleState = sequence_list[0]
    #     self.Init = sequence_list[1]
    #     self.DeployBanner = sequence_list[2]
    #     self.FirstCansCollectMove = sequence_list[3]
    #     self.CollectCans = sequence_list[4]
    #     self.FirstCansBuildMove = sequence_list[5]
    #     self.Build1StoryBleachers = sequence_list[6]
    #     self.SecondCansPushMove = sequence_list[7]
    
    @property
    def Sprint4Yellow(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Sprint4Yellow

    @Sprint4Yellow.setter
    def Sprint4Yellow(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Sprint4Yellow = sequence
    
    @property
    def Sprint4Blue(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Sprint4Blue
    @Sprint4Blue.setter
    def Sprint4Blue(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Sprint4Blue = sequence
    
    @property
    def clawtest(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._clawtest
    @clawtest.setter
    def clawtest(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._clawtest = sequence
    
    @property
    def Sprint4CansBlue(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Sprint4CansBlue
    @Sprint4CansBlue.setter
    def Sprint4CansBlue(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Sprint4CansBlue = sequence
    
    @property
    def Sprint4CansYellows(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._Sprint4CansYellows
    @Sprint4CansYellows.setter
    def Sprint4CansYellows(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._Sprint4CansYellows = sequence
    
    @property
    def wheeltest(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._wheeltest
    @wheeltest.setter
    def wheeltest(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._wheeltest = sequence
    
    @property
    def reedswitchTest(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._reedswitchTest
    @reedswitchTest.setter
    def reedswitchTest(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._reedswitchTest = sequence
    
    @property
    def frontPlateTest(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._frontPlateTest
    @frontPlateTest.setter
    def frontPlateTest(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._frontPlateTest = sequence

    @property
    def frontPlantUp(self) -> list[ICommand | ITimeBasedCommand | IMoveCommand]:
        return self._frontPlantUp
    @frontPlantUp.setter
    def frontPlantUp(self, sequence: list[ICommand | ITimeBasedCommand | IMoveCommand]):
        self._frontPlantUp = sequence