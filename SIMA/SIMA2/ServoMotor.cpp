#include <Arduino.h>
#include "ServoMotor.h"

ServoMotor::ServoMotor(int p) : pin(p) {}

void ServoMotor::init()
{
    servo.attach(pin);
}

void ServoMotor::setPosition(int angle)
{
    servo.write(angle);
}
