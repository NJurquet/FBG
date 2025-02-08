#include "Debug.h"

Debugger::Debugger(int TX_Debug, int RX_Debug) : TX_Debug(TX_Debug), RX_Debug(RX_Debug) {}

void Debugger::init()
{
    // pinMode(RX_Debug, INPUT);
    // pinMode(TX_Debug, OUTPUT);
}

void Debugger::write(const char *message)
{
    // dbgSerial.println(message);
}

void Debugger::read()
{
    // String rx_message = "";
    // while (mySerial.available())
    //     rx_message += (char)mySerial.read();
    // Serial.println(rx_message);
    // mySerial.println(F("Received"));
    // if (mySerial.available())
    // {
    //     char incomingChar = mySerial.read();
    //     // if (incomingChar != '\n')
    //     // {
    //     //     rx_message += String(incomingChar);
    //     // }
    //     // else
    //     // {
    //     //     rx_message = "";
    //     // }
    //     Serial.write(mySerial.read());
    // }
    // if (Serial.available())
    // {
    //     dbgSerial.write(Serial.read()); // Forward what Serial received to Software Serial Port
    // }
    // if (dbgSerial.available())
    // {
    //     Serial.write(dbgSerial.read()); // Forward what Software Serial received to Serial Port
    // }
}
