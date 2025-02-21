from time import sleep
from .fsm.FSM import RobotFSM
from .bigMotorControl import BigMotorControl


def main():
    LMotorFpin = 18
    LMotorBpin = 19
    RMotorFpin = 20
    RMotorBpin = 21
    lMotorControl: BigMotorControl = BigMotorControl(LMotorFpin, LMotorBpin)
    rMotorControl: BigMotorControl = BigMotorControl(RMotorFpin, RMotorBpin)

    
    robot: RobotFSM = RobotFSM(lMotorControl, rMotorControl)

    while True:
        robot.update()


if __name__ == "__main__":
    main()
