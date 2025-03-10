#ifndef MAGNETICSTART_H
#define MAGNETICSTART_H

/**
 * @brief A class to interface with an magnetic sensor to start the robot
 *
 * This class provides methods to initialize and read data from an magnetic sensor
 *
 * @param pin The pin number to which the magnetic sensor is connected.
 */
class MagneticStart
{
public:
    /**
     * @brief Constructor for the MagneticStart class.
     */
    MagneticStart(int pin);

    /**
     * @brief Initializes the magnetic sensor.
     *
     * This method sets up the necessary configurations for the magnetic sensor.
     */
    void init();

    /**
     * @brief Reads the value from the magnetic sensor.
     *
     * @return `true` if the sensor does not detect the magnetic top.
     */
    bool read();

private:
    int pin;
};

#endif // MagneticStart_H