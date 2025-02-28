#include <Arduino.h>
#include "MagneticStart.h"

MagneticStart::MagneticStart(int p) : pin(p) {}

void MagneticStart::init()
{
    pinMode(pin, INPUT);
}
bool MagneticStart::read()
{
    return digitalRead(pin);
}