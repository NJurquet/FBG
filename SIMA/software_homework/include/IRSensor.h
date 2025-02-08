#ifndef IRSENSOR_H
#define IRSENSOR_H

/**
 * @brief A class to interface with an infrared sensor.
 *
 * This class provides methods to initialize and read data from an infrared sensor.
 *
 * @param pin The pin number to which the infrared sensor is connected.
 */
class IRSensor
{
public:
    /**
     * @brief Constructor for the IRSensor class.
     */
    IRSensor(int pin);

    /**
     * @brief Initializes the infrared sensor.
     *
     * This method sets up the necessary configurations for the infrared sensor.
     */
    void init();

    /**
     * @brief Reads the value from the infrared sensor.
     *
     * @return `true` if the sensor detects a black line, `false` if it detect the while line.
     */
    bool read();

private:
    int pin;
};

#endif // IRSENSOR_H