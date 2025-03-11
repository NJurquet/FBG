from .ultrasonicSensor import UltrasonicSensor
from ..constants import USPosition


class UltrasonicController:
    """
    Class managing multiple ultrasonic sensors.

    Parameters:
        `sensorsDict` (dict[USPosition, tuple[int, int]]): A dictionary where each key is the position of a sensor and the value is a tuple with the echo and trigger pins.
    """

    def __init__(self, sensorsDict: dict[USPosition, tuple[int, int]]):
        self._sensors: list[UltrasonicSensor] = [UltrasonicSensor(pos, echoPin, trigPin) for pos, (echoPin, trigPin) in sensorsDict.items()]

    def getDistances(self) -> dict[USPosition, float]:
        """
        Get measured distances from all ultrasonic sensors.

        Returns:
            dict: A dictionary with the sensor positions as keys and the distances as values.
        """
        return {sensor.pos: sensor.getDistance() for sensor in self._sensors}

    def getDistance(self, pos: USPosition) -> float:
        """
        Get the measured distance from the specified ultrasonic sensor.

        Parameters:
            `pos` (USPosition): The position of the sensor.

        Returns:
            float: The distance in meters.

        Raises:
            ValueError: If the specified position does not correspond to any sensor.
        """
        for sensor in self._sensors:
            if sensor.pos == pos:
                return sensor.getDistance()
        raise ValueError(f"No sensor found with position {pos}.")
