from BIG_BOT.src.robot import Robot
from .commands import CommandSequence, ForwardCommand, BackwardCommand, RotateLeftCommand, RotateRightCommand, StopCommand, WaitCommand

def create_predefined_sequences(robot):
    """Create some predefined command sequences for the robot"""
    
    # Create a sequence for navigating a simple square path
    square_path = robot.command_invoker.create_sequence("square_path")
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.move_forward(30))
    square_path.add_command(robot.rotate_right(90))
    square_path.add_command(robot.stop())
    
    # Create a sequence for zigzag movement
    zigzag = robot.command_invoker.create_sequence("zigzag")
    zigzag.add_command(robot.move_forward(20))
    zigzag.add_command(robot.rotate_left(45))
    zigzag.add_command(robot.move_forward(15))
    zigzag.add_command(robot.rotate_right(90))
    zigzag.add_command(robot.move_forward(15))
    zigzag.add_command(robot.rotate_left(45))
    zigzag.add_command(robot.move_forward(20))
    zigzag.add_command(robot.stop())
    
    # Create a dance sequence (just for fun)
    dance = robot.command_invoker.create_sequence("dance")
    dance.add_command(robot.rotate_left(360, 0.7))
    dance.add_command(robot.wait(0.5))
    dance.add_command(robot.rotate_right(360, 0.7))
    dance.add_command(robot.wait(0.5))
    dance.add_command(robot.move_forward(10, 0.8))
    dance.add_command(robot.move_backward(10, 0.8))
    dance.add_command(robot.wait(0.5))
    dance.add_command(robot.rotate_left(180, 0.9))
    dance.add_command(robot.rotate_right(180, 0.9))
    dance.add_command(robot.stop())



# Main program example
def nm():
    # Initialize robot
    robot = Robot("blue")
    
    # Create predefined sequences
    create_predefined_sequences(robot)
    
    # Execute a predefined sequence
    robot.command_invoker.execute_sequence("square_path")
    
    # Create a custom sequence at runtime
    custom_sequence = robot.command_invoker.create_sequence("navigate_obstacle")
    custom_sequence.add_command(robot.move_forward(15))
    custom_sequence.add_command(robot.rotate_right(45))
    custom_sequence.add_command(robot.move_forward(10))
    custom_sequence.add_command(robot.rotate_left(45))
    custom_sequence.add_command(robot.move_forward(20))
    custom_sequence.add_command(robot.stop())
    
    # Execute the custom sequence
    robot.command_invoker.execute_sequence("navigate_obstacle")
    
    # List all available sequences
    print("Available sequences:", robot.command_invoker.list_sequences())


if __name__ == "__main__":
    nm()