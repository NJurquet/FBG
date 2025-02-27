from ultrasonicSensor import UltrasonicSensor

"""
    Manages multiple ultrasonic sensors.

    Parameters:
        echoPins (list): A list of echo pins for the sensors.
        trigPins (list): A list of trigger pins for the sensors.

    Attributes:
        sensors (list): A list of UltrasonicSensor objects.

    Methods:
        getDistances(): Returns a list of distance measurements from all sensors.
"""
class UltrasonicController:
    def __init__(self, echoPins, trigPins):
        self.sensors = []
        for i in range(len(echoPins)):
            self.sensors.append(UltrasonicSensor(echoPins[i], trigPins[i]))
    
    def getDistances(self):
        distances = []
        for sensor in self.sensors:
            distances.append(sensor.getDistance())
        return distances