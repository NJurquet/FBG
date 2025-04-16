import argparse
from .robot import Robot


def main():
    try:
        parser = argparse.ArgumentParser(usage="python -m BIG_BOT.src.main [-h] --score SCORE --color COLOR",
                                         description="Run the robot, set the current color and set the expected score displayed on the LCD.")
        parser.add_argument("--score", type=int, required=True, help="The expected score displayed on the LCD.")
        parser.add_argument("--color", type=str, required=True, choices=["yellow", "blue"],
                            help="The color assigned to the robot for the game.")
        args = parser.parse_args()

        robot: Robot = Robot(args.color, args.score)

        while True:
            robot.fsm.update()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Cleaning up...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources in the finally block to ensure it always runs
        if robot and hasattr(robot, 'stepper'):
            try:
                robot.stepper.cleanup()
                print("Stepper motor cleaned up successfully")
            except Exception as cleanup_error:
                print(f"Error during cleanup: {cleanup_error}")
        exit(0)

if __name__ == "__main__":
    main()
