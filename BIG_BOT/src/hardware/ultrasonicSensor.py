from gpiozero import DistanceSensor

class UltrasonicSensor:
    """
        Manages one ultrasonic sensor.

        Parameters:
            name: A string representing the sensor's name.
            echoPin: An integer representing the GPIO pin connected to the sensor's echo pin.
            trigPin: An integer representing the GPIO pin connected to the sensor's trigger pin.

        Methods:
            getDistance(): Returns a float of the distance in meters.
    """
    def __init__(self, name: str, echoPin: int, trigPin: int):
        self.name = name
        self.sensor = DistanceSensor(echo=echoPin, trigger=trigPin)

    def getDistance(self): 
        """
        Returns the distance in meters.

        Returns:
            float: The distance in meters.
        """
        return self.sensor.distance
    
