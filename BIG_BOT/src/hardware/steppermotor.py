from gpiozero import DigitalOutputDevice, Button
from ..utils import precise_sleep


class StepperMotor:
    """
    Interfaces with a NEMA stepper via an A4988 driver.

    The following pins are used:
      - step: pulses for each step.
      - dir: controls direction (clockwise or counter-clockwise).
      - MS1, MS2, MS3: define the microstepping resolution.

    Limit switches:
      - Optionally, you can provide top_limit_pin and bottom_limit_pin.
        These are used for homing and safe operation to stop rotation
        when a mechanical limit is reached.

    Microstepping settings supported (resolution: multiplier):
      - 1    → Full step    (MS1=LOW, MS2=LOW, MS3=LOW)    → 200 steps/rev
      - 1/2  → Half step    (MS1=HIGH, MS2=LOW, MS3=LOW)   → 400 steps/rev
      - 1/4  → Quarter step (MS1=LOW, MS2=HIGH, MS3=LOW)   → 800 steps/rev
      - 1/8  → Eighth step  (MS1=HIGH, MS2=HIGH, MS3=LOW)  → 1600 steps/rev
      - 1/16 → Sixteenth    (MS1=HIGH, MS2=HIGH, MS3=HIGH) → 3200 steps/rev (if supported)

    A simple position tracking (in steps) is implemented so that after homing the vertical position can be monitored and controlled.

    **Note:** The reset and sleep pins on your A4988 are assumed to be wired together to keep the stepper motor at full power.
    """

    # Microstepping mapping: resolution → (MS1, MS2, MS3)
    _MICROSTEP_RESOLUTION = {
        1:  (0, 0, 0),
        2:  (1, 0, 0),
        4:  (0, 1, 0),
        8:  (1, 1, 0),
        16: (1, 1, 1),
    }
    _BASE_STEPS_PER_REV = 200  # Full step base (1.8° per step)

    def __init__(self, step: int, dir: int, ms1: int, ms2: int, ms3: int,
                 step_delay: float = 0.002, microstep: int = 1,
                 top_limit_pin: int | None = None, bottom_limit_pin: int | None = None):
        """
        Initialize the stepper motor and, optionally, limit switches.

        Parameters:
            `step` (int):   GPIO pin for STEP.
            `dir` (int):    GPIO pin for DIR.
            `ms1` (int):  GPIO pin for MS1.
            `ms2` (int):  GPIO pin for MS2.
            `ms3` (int):  GPIO pin for MS3.
            `step_delay` (float): Delay between high and low transitions (in seconds), default is 0.002s. Step delay must be higher or equal to 0.002s.
            `microstep` (int): Number of microsteps to perform per full step, default is 1. The corresponding microstepping resolution is (1, 1/2, 1/4, 1/8, 1/16).
            `top_limit_pin` (int): Optional GPIO pin for the top limit switch, default is None.
            `bottom_limit_pin` (int): Optional GPIO pin for the bottom limit switch, default is None.
        """
        # Create gpiozero devices for A4988 control.
        self._step_device = DigitalOutputDevice(step)
        self._dir_device = DigitalOutputDevice(dir)
        self._ms1_device = DigitalOutputDevice(ms1)
        self._ms2_device = DigitalOutputDevice(ms2)
        self._ms3_device = DigitalOutputDevice(ms3)
        try:
            self._top_switch = Button(top_limit_pin) if top_limit_pin is not None else None
            self._bottom_switch = Button(bottom_limit_pin) if bottom_limit_pin is not None else None
        except ValueError as e:
            self._top_switch = None
            self._bottom_switch = None
            import warnings
            warnings.warn(f"Top or bottom limit switches are invalid or not connected.\nError: {e}", stacklevel=2)
        precise_sleep(0.001)

        if step_delay < 0.002:
            raise ValueError("step_delay must be >= 0.002 seconds.")
        self._step_delay = step_delay
        self._current_resolution = microstep
        self._steps_per_rev = self._BASE_STEPS_PER_REV * microstep
        self.set_microstepping(self._current_resolution)

        self.current_position: int | None = None  # Vertical position in steps (None until homed).

        self.stop_flag = False  # Call this Flag to stop the motor.

    def set_microstepping(self, resolution: int) -> None:
        """
        Set the microstepping resolution to apply on MS1, MS2, MS3 pins.

        Parameters:
            `resolution` (int): The resolution to set, one of (1, 2, 4, 8, 16).
                - 1: Full step (200 steps/rev).
                - 2: Half step (400 steps/rev).
                - 4: Quarter step (800 steps/rev).
                - 8: Eighth step (1600 steps/rev).
                - 16: Sixteenth step (3200 steps/rev).
        Raises:
            `ValueError`: If the resolution is unsupported.
        """
        if resolution not in self._MICROSTEP_RESOLUTION:
            raise ValueError(f"Unsupported resolution: {resolution}. Choose from {list(self._MICROSTEP_RESOLUTION.keys())}")
        ms1_state, ms2_state, ms3_state = self._MICROSTEP_RESOLUTION[resolution]
        self._ms1_device.on() if ms1_state else self._ms1_device.off()
        self._ms2_device.on() if ms2_state else self._ms2_device.off()
        self._ms3_device.on() if ms3_state else self._ms3_device.off()
        self._current_resolution = resolution
        self._steps_per_rev = self._BASE_STEPS_PER_REV * resolution

    @property
    def steps_per_rev(self) -> int:
        """Return the full number of steps per revolution, including the current microstepping resolution."""
        return self._steps_per_rev

    def step(self, steps: int, clockwise: bool = False, update_position: bool = True) -> None:
        """
        Pulse the STEP pin a specific number of times to rotate the motor by a given number of steps.
        The direction is controlled by the DIR pin.

        Parameters:
            `steps` (int): Number of steps to move (absolute count).
            `clockwise` (bool): Direction flag, default is False. Clockwise rotation increases vertical position.
            `update_position` (bool): If True and if current_position is set, update the internal position count.
        """
        self._dir_device.value = clockwise  # Set direction.
        for _ in range(abs(steps)):
            if self.stop_flag:
                print("Stepper Motor stopped.")
                break

            self._step_device.on()
            precise_sleep(self._step_delay)  # Precise sleep to avoid timing issues.
            self._step_device.off()
            precise_sleep(self._step_delay)  # Precise sleep to avoid timing issues.
            if update_position and self.current_position is not None:
                self.current_position += 1 if clockwise else -1

    def rotate(self, rotations: float, clockwise: bool = True) -> None:
        """
        Rotate the motor a specific number of rotations (full or fractional).

        Parameters:
            `rotations` (float): Number of full or fractional rotations.
            `clockwise` (bool): Direction of rotation, default is True. Clockwise rotation increases vertical position.
        """
        total_steps = int(self._steps_per_rev * rotations)
        print(f"Rotating {rotations} rotations ({total_steps} steps) {'clockwise' if clockwise else 'counter-clockwise'}.")
        self.step(total_steps, clockwise=clockwise, update_position=True)

    def home_bottom(self) -> None:
        """
        Move the motor downward until the bottom limit switch is triggered.
        After homing, the vertical position is set to 0.

        Raises:
            `Exception`: If the bottom limit switch is not configured.
        """
        if self._bottom_switch is None:
            raise Exception("Bottom limit switch not configured.")
        while not self._bottom_switch.is_active:
            if self.stop_flag:
                print("Stepper Motor stopped.")
                break

            self.step(1, clockwise=False, update_position=False)
        self.current_position = 0
        print("Homed: bottom limit reached. Current position set to 0.")

    def move_to_top(self) -> None:
        """
        Step upward one step at a time until the top limit switch is activated.
        Updates the current position as it moves.

        Raises:
            `Exception`: If the top limit switch is not configured.
        """
        if self._top_switch is None:
            raise Exception("Top limit switch not configured.")
        while not self._top_switch.is_active:
            if self.stop_flag:
                print("Stepper Motor stopped.")
                break

            self.step(1, clockwise=True, update_position=True)
        print("Reached top limit.")

    def move_to_bottom(self):
        """
        Step downward one step at a time until the bottom limit switch is activated.
        Updates the current position as it moves.

        Raises:
            `Exception`: If the bottom limit switch is not configured.
        """
        if self._bottom_switch is None:
            raise Exception("Bottom limit switch not configured.")
        while not self._bottom_switch.is_active:
            if self.stop_flag:
                print("Stepper Motor stopped.")
                break

            self.step(1, clockwise=False, update_position=True)
        print("Reached bottom limit.")
        self.current_position = 0

    def move_to_position(self, target_position: int) -> None:
        """
        Move the motor one step at a time to a target vertical position.
        Current position is tracked in steps. It is assumed that the motor has been homed,
        so current_position is not None.

        Parameters:
            `target_position` (int): The desired vertical position in step counts.

        Raises:
            `Exception`: If current_position is undefined (None).
        """
        if self.current_position is None:
            raise Exception("Current position is undefined. Please home the motor first.")

        print(f"Moving from position {self.current_position} to target {target_position}.")
        while abs(self.current_position - target_position) > 0:
            if self.stop_flag:
                print("Stepper Motor stopped.")
                break

            # If going upward, check if top limit is reached.
            if self.current_position < target_position:
                if self._top_switch is not None and self._top_switch.is_active:
                    print("Top limit reached; cannot move further upward.")
                    break
                self.step(1, clockwise=True, update_position=True)
            # If going downward, check if bottom limit is reached.
            elif self.current_position > target_position:
                if self._bottom_switch is not None and self._bottom_switch.is_active:
                    print("Bottom limit reached; cannot move further downward.")
                    break
                self.step(1, clockwise=False, update_position=True)
        print(f"Target reached. Current position: {self.current_position}")

    def cleanup(self) -> None:
        """
        Clean up all gpiozero stepper devices.
        """
        self._step_device.close()
        self._dir_device.close()
        self._ms1_device.close()
        self._ms2_device.close()
        self._ms3_device.close()
        if self._top_switch:
            self._top_switch.close()
        if self._bottom_switch:
            self._bottom_switch.close()

    def stop(self) -> None:
        """
        Stop the motor immediately by setting the stop flag.
        """
        self.stop_flag = True
        print("Stepper Motor stop flag set.")


if __name__ == '__main__':
    from ..config import STEPPER_DIR_PIN, STEPPER_STEP_PIN, STEPPER_MS1_PIN, STEPPER_MS2_PIN, STEPPER_MS3_PIN, STEPPER_BOTTOM_LIMIT_PIN, STEPPER_TOP_LIMIT_PIN
    from gpiozero import Device
    from gpiozero.pins.mock import MockFactory
    Device.pin_factory = MockFactory()

    stepper = StepperMotor(step=STEPPER_STEP_PIN, dir=STEPPER_DIR_PIN,
                           ms1=STEPPER_MS1_PIN, ms2=STEPPER_MS2_PIN, ms3=STEPPER_MS3_PIN,
                           step_delay=0.005, microstep=1,
                           top_limit_pin=STEPPER_TOP_LIMIT_PIN, bottom_limit_pin=STEPPER_BOTTOM_LIMIT_PIN)

    try:
        # Home the motor at the bottom.
        # stepper.home_bottom()

        # Now, move until the top limit is reached.
        # stepper.move_to_top()

        # Move to a target position of 1000 steps (if within the allowed range).
        # stepper.move_to_position(target_position=1000)

        stepper.rotate(rotations=4, clockwise=True)

    finally:
        # Always clean up the devices.
        stepper.cleanup()
