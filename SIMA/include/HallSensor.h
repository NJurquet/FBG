#ifndef HallSensor_H
#define HallSensor_H

/**
 * @brief A class to interface with a Hall sensor.
 *
 * This class provides methods to initialize and read data from a Hall sensor. 
 * It also handles interrupts to detect changes in the sensor state.
 *
 * @param pin The pin number to which the Hall sensor is connected.
 */
class HallSensor {
public:
    /**
     * @brief Constructor to initialize the HallSensor class.
     *
     * @param pin The pin number to which the Hall sensor is connected.
     */
    HallSensor(int pin);

    /**
     * @brief Initializes the Hall sensor.
     *
     * Sets up the pin as an input and configures any necessary interrupts.
     */
    void init();

    /**
     * @brief Reads and prints the current state of the sensor.
     *
     * This method reads the sensor's state and logs the value to aid debugging
     * or for regular monitoring.
     */
    void ReadState();

private:
    int HallSensorPin;          ///< Pin number for the Hall sensor.
    volatile int SensorState;   ///< Current state of the Hall sensor, volatile for use in interrupts.
    int PreviousState;          ///< Stores the previous state of the Hall sensor.

    /**
     * @brief Static pointer to the class instance.
     *
     * This is used to reference the class from static interrupt functions.
     */
    static HallSensor* instance;

    /**
     * @brief Interrupt handler for sensor state changes.
     *
     * This static function is triggered when the sensor state changes, updating
     * the `SensorState` variable and invoking relevant actions.
     */
    static void SensorChange();
};

#endif
