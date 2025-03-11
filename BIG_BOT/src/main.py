from .logger import logger
from .robot import Robot


def main():
    robot: Robot = Robot()

    try:
        while True:
            robot.fsm.update()
            # robot.on_event("targets_detected")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")


if __name__ == "__main__":
    main()
