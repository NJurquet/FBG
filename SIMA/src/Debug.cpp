#include <Arduino.h>
#include "Debug.h"
#include <SoftwareSerial.h>

Debugger::Debugger(int TX, int RX) : TX(TX), RX(RX), mySerial(TX, RX) {}

void Debugger::init()
{
    pinMode(RX, INPUT);
    pinMode(TX, OUTPUT);

    mySerial.begin(9600);
    Serial.begin(38400);
}

void Debugger::write(char message[16])
{
    mySerial.println(message);
}

char Debugger::read(){
    char rx_message;
    while(mySerial.available())
      rx_message= (char)mySerial.read();
      Serial.println(rx_message);
      mySerial.println("Received");
      return rx_message;
}
