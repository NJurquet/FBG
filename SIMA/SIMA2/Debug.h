#ifndef DEBUG_H
#define DEBUG_H

#include <Arduino.h>
#include <SoftwareSerial.h>

class Debugger
{
public:
    /**
     * @brief Constructor for the Debugger class.
     * using a HC-05 bluetooth module.
     */
    Debugger(int TX_Debug, int RX_Debug);

    /**
     * @brief Initializes the bluetooth debugger.
     * This method sets up the necessary configurations for the HC-05.
     */
    void init();

    /**
     * @brief Write debug information in bluetooth terminal.
     *
     */
    void write(const char *message);

    /**
     * @brief Read debug information from bluetooth terminal.
     *
     */
    void read();

private:
    int TX_Debug;
    int RX_Debug;
};

#endif // DEBUG_H