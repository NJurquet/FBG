from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from newFSM import RobotFSM

class FirstCanMoveBuilder:
    """
    Builder for creating movement sequences related to the first can operation.
    Demonstrates how to create specialized sequence builders with the command pattern.
    """
    
    def __init__(self, fsm: 'RobotFSM'):
        self.fsm = fsm
        self.robot = fsm.robot
        self.sequence_created = False
        
    def create_sequence(self) -> None:
        """
        Create the first can movement sequence if it doesn't already exist.
        """
        if self.sequence_created:
            return
            
        # Clear any existing sequence with this name
        if "first_can_detailed" in self.robot.command_invoker.sequences:
            self.robot.command_invoker.sequences.pop("first_can_detailed")
        
        # Create a more detailed sequence than the basic one in RobotFSM
        sequence = self.robot.command_invoker.create_sequence("first_can_detailed")
        
        # Build the sequence step by step
        sequence.add_command(self.robot.move_forward(30.0, 0.5))
        sequence.add_command(self.robot.wait(0.5))
        sequence.add_command(self.robot.rotate_right(45.0, 0.4))
        sequence.add_command(self.robot.move_forward(15.0, 0.6))
        sequence.add_command(self.robot.rotate_left(45.0, 0.4))
        sequence.add_command(self.robot.move_forward(15.0, 0.5))
        sequence.add_command(self.robot.stop())
        # ...
        
        self.sequence_created = True
        
    def execute_sequence(self) -> None:
        """
        Execute the first can movement sequence.
        """
        self.create_sequence()  # Ensure sequence exists
        self.fsm.start_sequence("first_can_detailed")
    
    # For backward compatibility with your current code:
    def execute_step(self) -> None:
        """
        Legacy method to maintain backward compatibility.
        """
        self.execute_sequence()