from .robot import Robot


def main():
    robot: Robot = Robot()

    while True:
        robot.fsm.update()
        # robot.on_event("targets_detected")


if __name__ == "__main__":
    main()
