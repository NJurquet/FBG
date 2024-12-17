#include <Arduino.h>
#include "Led.h"

Led::Led(int p) : pin(p) {}

void Led::init()
{
    pinMode(pin, OUTPUT);
}

void Led::turnOn()
{
    digitalWrite(pin, HIGH);
}

void Led::turnOff()
{
    digitalWrite(pin, LOW);
}

void Led::toggle()
{
    digitalWrite(pin, !digitalRead(pin));
}
