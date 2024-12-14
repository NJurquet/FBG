#ifndef ULTRASONICSENSOR_H
#define ULTRASONICSENSOR_H

/**
 * @brief A class to interface with an ultrasonic sensor.
 *
 * This class provides methods to initialize and read data from an ultrasonic sensor.
 *
 * @param trigPin The pin number to which the trigger pin of the ultrasonic sensor is connected.
 * @param echoPin The pin number to which the echo pin of the ultrasonic sensor is connected.
 */
class UltrasonicSensor
{
public:
    /**
     * @brief Constructor for the UltrasonicSensor class.
     */
    UltrasonicSensor(int trigPin, int echoPin);

    /**
     * @brief Initializes the ultrasonic sensor.
     *
     * This method sets up the necessary configurations for the ultrasonic sensor.
     */
    void init();

    /**
     * @brief Reads the distance from the ultrasonic sensor.
     *
     * @return The distance in centimeters.
     */
    long readDistance();

private:
    int trigPin;
    int echoPin;
};

#endif // ULTRASONICSENSOR_H