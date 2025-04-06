from .ultrasonicSensor import UltrasonicSensor
from ..constants import USPosition, USEvent
from ..config import OBSTACLE_DISTANCE


class UltrasonicController:
    """
    Class managing multiple ultrasonic sensors.

    Parameters:
        `sensorsDict` (dict[USPosition, tuple[int, int]]): A dictionary where each key is the position of a sensor and the value is a tuple with the echo and trigger pins.
    """

    def __init__(self):
        self._sensors: list[UltrasonicSensor] = []
        self._last_obstacle: bool = False
        self._distances: dict[USPosition, float] = {}

    def add_sensor(self, pos: USPosition, echoPin: int, trigPin: int) -> None:
        """
        Add a new ultrasonic sensor to the controller.

        Parameters:
            `pos` (USPosition): The position of the sensor.
            `echoPin` (int): The GPIO pin connected to the sensor's echo pin.
            `trigPin` (int): The GPIO pin connected to the sensor's trigger pin.
        """
        if not isinstance(pos, USPosition):
            raise TypeError(f"Expected pos to be of type USPosition, got {type(pos).__name__}.")
        if not isinstance(echoPin, int) or not isinstance(trigPin, int):
            raise TypeError("echoPin and trigPin must be integers.")
        if echoPin < 0 or trigPin < 0 or echoPin == trigPin:
            raise ValueError("echoPin and trigPin must be positive integers and not equal.")

        if any(sensor.pos == pos for sensor in self._sensors):
            raise ValueError(f"Sensor with position {pos} already exists in the controller.")
        self._sensors.append(UltrasonicSensor(pos, echoPin, trigPin))

    def check_obstacles(self) -> tuple[USEvent, list[USPosition]]:
        """
        Check if any of the ultrasonic sensors detects an obstacle.
        Make sure to call `measure_distances()` before calling this method.

        Returns:
            tuple:

            `USEvent`: The event that occurred.

                - `OBSTACLE_DETECTED`: If a new obstacle is detected.
                - `OBSTACLE_PRESENT`: If the same obstacle is still detected.
                - `OBSTACLE_CLEARED`: If the previously detected obstacle is no longer detected.
                - `NO_EVENT`: If no obstacle is detected.

            `list[USPosition]`: The USPositions of sensors that detected an obstacle.
        """
        # If no sensors provided or no distances measured
        if len(self._sensors) == 0 or len(self._distances) == 0:
            return USEvent.NO_EVENT, []

        detecting_sensors = [pos for pos, d in self._distances.items() if d < OBSTACLE_DISTANCE]

        # If any sensor detects an obstacle within range
        if detecting_sensors:
            # If the obstacle was not detected before
            if not self._last_obstacle:
                self._last_obstacle = True
                return USEvent.OBSTACLE_DETECTED, detecting_sensors
            return USEvent.OBSTACLE_PRESENT, detecting_sensors  # Still detecting the same obstacle
        else:
            # If the previously detected obstacle is no longer in range
            if self._last_obstacle:
                self._last_obstacle = False
                return USEvent.OBSTACLE_CLEARED, []

        # If no obstacle detected
        return USEvent.NO_EVENT, []

    def measure_distances(self) -> None:
        """
        Measure distances from all ultrasonic sensors.
        """
        self._distances = {sensor.pos: sensor.getDistance() for sensor in self._sensors}

    def get_distance(self, pos: USPosition) -> float:
        """
        Get the measured distance from the specified ultrasonic sensor.

        Parameters:
            `pos` (USPosition): The position of the sensor.

        Returns:
            float: The distance in centimeters.

        Raises:
            ValueError: If the specified position does not correspond to any sensor.
        """
        if not isinstance(pos, USPosition):
            raise TypeError(f"Expected pos to be of type USPosition, got {type(pos).__name__}.")
        for sensor in self._sensors:
            if sensor.pos == pos:
                return sensor.getDistance()
        raise ValueError(f"No sensor found with position {pos}.")


if __name__ == "__main__":
    from gpiozero import Device
    from gpiozero.pins.mock import MockFactory, MockTriggerPin
    from time import sleep, perf_counter

    class PreciseMockTriggerPin(MockTriggerPin):
        def _echo(self):
            if self.echo_pin is None:
                raise ValueError("echo_pin is not initialized")

            sleep(0.001)
            self.echo_pin.drive_high()

            # sleep(), time() and monotonic() dont have enough precision!
            init_time = perf_counter()
            while True:
                if perf_counter() - init_time >= self.echo_time:
                    break

            self.echo_pin.drive_low()

    Device.pin_factory = MockFactory()
    echoPin1 = Device.pin_factory.pin(8)
    echoPin2 = Device.pin_factory.pin(21)
    echoPin3 = Device.pin_factory.pin(25)
    echoPin4 = Device.pin_factory.pin(24)
    trigPin1 = Device.pin_factory.pin(7, pin_class=PreciseMockTriggerPin, echo_pin=echoPin1, echo_time=0.0)
    trigPin2 = Device.pin_factory.pin(20, pin_class=PreciseMockTriggerPin, echo_pin=echoPin2, echo_time=0.005)
    trigPin3 = Device.pin_factory.pin(16, pin_class=PreciseMockTriggerPin, echo_pin=echoPin3, echo_time=0.02)
    trigPin4 = Device.pin_factory.pin(23, pin_class=PreciseMockTriggerPin, echo_pin=echoPin4, echo_time=0.03)

    usController = UltrasonicController()
    usController.add_sensor(USPosition.FRONT_RIGHT, 8, 7)
    usController.add_sensor(USPosition.FRONT_LEFT, 21, 20)
    usController.add_sensor(USPosition.BACK_RIGHT, 25, 16)
    usController.add_sensor(USPosition.BACK_LEFT, 24, 23)

    usController.measure_distances()
    print(f"Sensors: {usController._distances}")
    print(f"Obstacle Event: {usController.check_obstacles()}")
