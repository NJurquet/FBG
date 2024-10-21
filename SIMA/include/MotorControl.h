#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

#include <Adafruit_MotorShield.h>

namespace MotorControl
{
    void init();
    void moveForward();
    void rotate();
    void stop();
}

#endif // MOTORCONTROL_H