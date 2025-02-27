from gpiozero import DistanceSensor

"""
    Manages one ultrasonic sensor.

    Parameters:
        echoPin: An integer representing the GPIO pin connected to the sensor's echo pin.
        trigPin: An integer representing the GPIO pin connected to the sensor's trigger pin.

    Attributes:
        sensor: A DistanceSensor object (from gpio zero).

    Methods:
        getDistance(): Returns a float of the distance in meters.
"""
class UltrasonicSensor:
    def __init__(self, echoPin, trigPin):
        self.sensor = DistanceSensor(echo=echoPin, trigger=trigPin)

    def getDistance(self):
        return self.sensor.distance
    
