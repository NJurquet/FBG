from gpiozero import DistanceSensor
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
        self._sensor = DistanceSensor(echo=echoPin, trigger=trigPin)

    @property
    def pos(self) -> USPosition:
        """
        Returns the position of the sensor.

        Returns:
            USPosition: The position of the sensor.
        """
        return self._pos

    @property
    def sensor(self) -> DistanceSensor:
        """
        Returns the DistanceSensor object.

        Returns:
            DistanceSensor: The DistanceSensor object.
        """
        return self._sensor

    def getDistance(self) -> float:
        """
        Returns the distance in meters.

        Returns:
            float: The distance in meters.
        """
        return self._sensor.distance
