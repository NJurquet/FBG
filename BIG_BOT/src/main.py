from .fsm.FSM import RobotFSM


def main():
    robot: RobotFSM = RobotFSM()

    while True:
        robot.update()
        # robot.on_event("targets_detected")


if __name__ == "__main__":
    main()
