from ultrasonicSensor import UltrasonicSensor

class UltrasonicController:
    """
    Manages multiple ultrasonic sensors.

    Parameters:
        names (list): A list of names for the sensors.
        echoPins (list): A list of echo pins for the sensors.
        trigPins (list): A list of trigger pins for the sensors.

    Methods:
        getDistances(): Returns a list of distance measurements from all sensors.
    """

    def __init__(self, names, echoPins, trigPins):
        self.sensors = []
        for i in range(len(names)):
            self.sensors.append(UltrasonicSensor(names[i], echoPins[i], trigPins[i]))
    
    def getDistances(self):
        """
        Returns a list of distance measurements from all sensors.

        Returns:
            list: A list of floats representing the distances in meters.
        """
        distances = []
        for sensor in self.sensors:
            distances.append(sensor.getDistance())
        return distances
    
    def getDistance(self, name):
        """
        Returns the distance from a specific sensor.

        Parameters:
            name (str): The name of the sensor.

        Returns:
            float: The distance in meters.
        """
        for sensor in self.sensors:
            if sensor.name == name:
                return sensor.getDistance()
        return None