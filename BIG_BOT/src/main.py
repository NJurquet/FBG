import argparse
from .robot import Robot


def main():
    parser = argparse.ArgumentParser(usage="python -m BIG_BOT.src.main [-h] --score SCORE",
                                     description="Run the robot and set the expected score displayed on the LCD.")
    parser.add_argument("--score", type=int, required=True, help="The expected score displayed on the LCD.")
    args = parser.parse_args()

    robot: Robot = Robot(args.score)

    while True:
        robot.fsm.update()


if __name__ == "__main__":
    main()
