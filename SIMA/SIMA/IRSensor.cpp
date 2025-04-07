#include <Arduino.h>
#include "IRSensor.h"

IRSensor::IRSensor(int p) : pin(p) {}

void IRSensor::init()
{
    pinMode(pin, INPUT);
}

bool IRSensor::read()
{
    return digitalRead(pin);
}

bool IRSensor::readAccurate()
{
    return digitalRead(pin) || digitalRead(pin);
}