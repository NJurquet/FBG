from .ultrasonicSensor import UltrasonicSensor
from ..constants import USPosition, USEvent


class UltrasonicController:
    """
    Class managing multiple ultrasonic sensors.

    Parameters:
        `sensorsDict` (dict[USPosition, tuple[int, int]]): A dictionary where each key is the position of a sensor and the value is a tuple with the echo and trigger pins.
    """

    def __init__(self, sensorsDict: dict[USPosition, tuple[int, int]]):
        self._sensors: list[UltrasonicSensor] = [UltrasonicSensor(pos, echoPin, trigPin) for pos, (echoPin, trigPin) in sensorsDict.items()]
        self._last_obstacle: bool = False

    # return an event depending if any sensor detects an obstacle
    def checkObstacle(self) -> USEvent:
        """
        Check if any of the ultrasonic sensors detects an obstacle.

        Returns:
            USEvent: The event that occurred.
        """
        # If any sensor detects an obstacle within range
        if min(self.getDistances().values()) < 0.2:
            # If the obstacle was not detected before
            if not self._last_obstacle:
                self._last_obstacle = True
                return USEvent.OBSTACLE_DETECTED
        else:
            # If the previously detected obstacle is no longer in range
            if self._last_obstacle:
                self._last_obstacle = False
                return USEvent.OBSTACLE_CLEARED

        # If no obstacle detected or still detecting the same obstacle
        return USEvent.NO_EVENT

    def getDistances(self) -> dict[USPosition, float]:
        """
        Get measured distances from all ultrasonic sensors.

        Returns:
            dict: A dictionary with the sensor positions as keys and the distances in meters as values.
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
