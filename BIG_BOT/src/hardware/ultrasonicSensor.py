from gpiozero import DistanceSensor, Pin
from gpiozero.pins.pigpio import PiGPIOFactory
from ..constants import USPosition


class UltrasonicSensor:
    """
    Class representing an ultrasonic sensor.

    Parameters:
        `pos` (USPosition): The position of the sensor.
        `echoPin` (int): The GPIO pin connected to the sensor's echo pin.
        `trigPin` (int): The GPIO pin connected to the sensor's trigger pin.
    """

    def __init__(self, pos: USPosition, echoPin: int, trigPin: int):
        self._pos = pos
        self._echoPin = echoPin
        self._trigPin = trigPin
        self._sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=1, pin_factory=PiGPIOFactory())

    @property
    def sensor(self) -> DistanceSensor:
        """
        The `DistanceSensor` instance of the ultrasonic sensor.
        """
        return self._sensor

    @property
    def pos(self) -> USPosition:
        """
        The `USPosition` position of the sensor.
        """
        return self._pos

    @property
    def echoGPIO(self) -> Pin:
        """
        The GPIO Pin object connected to the sensor's echo pin.
        """
        if self._sensor.echo is None:
            raise ValueError(f"Echo pin is not set for sensor at position {self._pos}")
        return self._sensor.echo

    @property
    def echoPin(self) -> int:
        """
        The GPIO pin number (int) connected to the sensor's echo pin.
        """
        return self._echoPin

    @property
    def trigGPIO(self) -> Pin:
        """
        The GPIO Pin object connected to the sensor's trigger pin.
        """
        if self._sensor.trigger is None:
            raise ValueError(f"Trigger pin is not set for sensor at position {self._pos}")
        return self._sensor.trigger

    @property
    def trigPin(self) -> int:
        """
        The GPIO pin number (int) connected to the sensor's trigger pin.
        """
        return self._trigPin

    @property
    def max_distance(self) -> int:
        """
        The maximum distance in meters that the sensor can measure.
        """
        return self._sensor.max_distance

    @max_distance.setter
    def max_distance(self, distance: int):
        if not isinstance(distance, int):
            raise TypeError("Distance must be integer.")
        if distance <= 0:
            raise ValueError("Distance must be positive.")
        self._sensor.max_distance = distance

    def getDistance(self) -> float:
        """
        Returns the distance measured in centimeters.

        Returns:
            float: The distance in centimeters.
        """
        return self._sensor.distance * 100


if __name__ == "__main__":
    import time

    # Example usage
    us_sensor = UltrasonicSensor(USPosition.FRONT_RIGHT, 7, 8)
    # print(f"Sensor Position: {us_sensor.pos}")
    while True:
        print(f"Distance: {us_sensor.getDistance():.2f} cm")
        time.sleep(1)
