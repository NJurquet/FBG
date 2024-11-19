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
    Debugger(int TX, int RX);

    /**
     * @brief Initializes the bluetooth debugger.
     * This method sets up the necessary configurations for the HC-05.
     */
    void init();

    /**
     * @brief Write debug information in bluetooth terminal.
     *
     */
    void write(char message[16]);

    /**
     * @brief Read debug information in bluetooth terminal.
     *
     */
    char read();

private:
    int TX;
    int RX;
    char lastmessageSent[16];
    char lastmessageReceived[16];
    SoftwareSerial mySerial;

};

#endif // DEBUG_H