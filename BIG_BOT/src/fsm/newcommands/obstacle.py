from BIG_BOT.src.robot import Robot
from .commands import CommandSequence, ForwardCommand, BackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand, WaitCommand

def demo_obstacle_detection():
    # Initialize robot
    robot = Robot("blue")
    
    # Create sequences that are obstacle-aware
    safe_sequence = robot.create_obstacle_aware_sequence("safe_square")
    
    print("Starting robot with obstacle detection...")
    
    # Start the robot's FSM
    robot.run()  # This will run the main loop until match ends or interrupted


# Alternative approach using the FSM's obstacle detection
def setup_obstacle_aware_robot():
    # Initialize robot
    robot = Robot("blue")
    
    # Create regular sequences - the FSM will handle obstacle detection
    square_path = robot.command_invoker.create_sequence("square_path")
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.stop())
    
    print("Starting robot with FSM obstacle detection...")
    
    # Start the robot's FSM, which will check for obstacles during updates
    robot.run()


if __name__ == "__main__":
    # Choose which approach to use
    demo_obstacle_detection()  # Command-level obstacle detection
    # setup_obstacle_aware_robot()  # FSM-level obstacle detection