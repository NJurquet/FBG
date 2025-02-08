#ifndef SERVOMOTOR_H
#define SERVOMOTOR_H
#include <Servo.h>

class ServoMotor
{
public:
    ServoMotor(int pin);

    void init();

    void setPosition(int angle);


private:
    int pin;
    Servo servo;
};

#endif // SERVOMOTOR_H