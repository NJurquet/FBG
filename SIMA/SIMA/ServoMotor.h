#ifndef SERVOMOTOR_H
#define SERVOMOTOR_H
#include <Servo.h>

class ServoMotor
{
public:
    ServoMotor(int pin);

    void init();

    /**
     * @brief Set the position of the servo motor.
     *
     * @param angle The angle in degrees (0° to 180°) to which the servo motor should be set.
     */
    void setPosition(int angle);

private:
    int pin;
    Servo servo;
};

#endif // SERVOMOTOR_H