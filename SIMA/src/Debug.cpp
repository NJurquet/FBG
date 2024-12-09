#include "Debug.h"

Debugger::Debugger(int TX_Debug, int RX_Debug) : TX_Debug(TX_Debug), RX_Debug(RX_Debug), mySerial(TX_Debug, RX_Debug) {}

void Debugger::init()
{
    pinMode(RX_Debug, INPUT);
    pinMode(TX_Debug, OUTPUT);

    mySerial.begin(9600);
    // Serial.begin(38400);
}

void Debugger::write(String message)
{
    mySerial.println(message);
}

String Debugger::read()
{
    String rx_message = "";
    while (mySerial.available())
        rx_message += (char)mySerial.read();
    Serial.println(rx_message);
    mySerial.println(F("Received"));
    return rx_message;
}
