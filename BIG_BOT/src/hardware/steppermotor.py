#Code taken from here: https://github.com/gfabia/raspberrypi-gpiozero-stepmotor

from gpiozero import OutputDevice
from time import sleep

class Stepper:

    CW = -1
    CCW = 1

    """Constructor"""
    def __init__(self, motor_pins, number_of_steps = 32, step_sequence = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]):
        """
        Class to control a stepper motor
        
        Parameters:
            motor_pins (list): The GPIO pins the motor is connected to.
            number_of_steps (int): The number of steps per internal motor revolution.
            step_sequence (list): The sequence of control signals to control the motor.
            
        Methods:
            set_speed(what_speed): Sets the speed of the motor in RPM.
            step(steps_to_move): Moves the motor a specified number of steps.
            step_motor(): Moves the motor one step.
            forward(): Rotates the motor clockwise indefinitely.
            backward(): Rotates the motor counter-clockwise indefinitely.
        """
        self.motor_pins = [OutputDevice(pin) for pin in motor_pins]  # Control pins
        self.pin_count = len(motor_pins)                             # Number of control pins 
        self.step_sequence = step_sequence                           # Sequence of control signals   
        self.step_number = 0                                         # Which step the motor is on
        self.number_of_steps = number_of_steps                       # Total number of steps per internal motor revolution
        self.direction = self.CW                                     # Rotation direction
        self.step_delay = 60 / self.number_of_steps / 240            # Rotation delay (240rpm == 3.90625ms delay)
        
    def set_speed(self, what_speed):
        self.step_delay = 60 / self.number_of_steps / what_speed     # Step delay in seconds
        print("Step Delay: {}ms".format(self.step_delay * 1000)) 

    def step(self, steps_to_move):
        """Moves the motor steps_to_move steps.
        
        Parameters:
            steps_to_move (int): The number of steps to move. Negative values move the motor in the reverse direction.
        """

        # Determine how many steps to left to take
        steps_left = int(abs(steps_to_move))

        # Determine direction
        self.direction = self.CW if steps_to_move > 0 else self.CCW

        # Decrement the number of steps, moving one step each time
        while steps_left > 0:
            if self.direction == self.CCW:
                self.step_number = (self.step_number + 1) % self.number_of_steps
            else:
                self.step_number = (self.step_number - 1) % self.number_of_steps
                
            steps_left -= 1
            self.step_motor()

    def step_motor(self):
        """Moves the motor one step."""

        # Select the correct control signal sequence
        this_step = self.step_number % len(self.step_sequence)
        seq = self.step_sequence[this_step]

        # Set pin state accordingly
        for pin in range(self.pin_count):
            if seq[pin] == 1:
                self.motor_pins[pin].on()
            else:
                self.motor_pins[pin].off()

        sleep(self.step_delay)

    def forward(self):
        """Rotates the motor clockwise indefinitely."""
        while True:
            self.step_number = (self.step_number - 1) % self.number_of_steps
            self.step_motor()

    """Rotates the motor counter-clockwise indefinitely"""
    def backward(self):
        while True:
            self.step_number = (self.step_number + 1) % self.number_of_steps
            self.step_motor()