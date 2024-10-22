#include <Arduino.h>
#include "MotorControl.h"
#include <Adafruit_MotorShield.h>
#include <SPI.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *leftMotor = AFMS.getMotor(3);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(4);

namespace MotorControl
{
    void init()
    {
        AFMS.begin();
    }

    void moveForward()
    {
        leftMotor->setSpeed(30);
        rightMotor->setSpeed(30);
        leftMotor->run(FORWARD);
        rightMotor->run(FORWARD);
    }

    void rotateLeft()
    {
        leftMotor->setSpeed(30);
        rightMotor->setSpeed(30);
        leftMotor->run(BACKWARD);
        rightMotor->run(FORWARD);
    }

    void rotateRight()
    {
        leftMotor->setSpeed(30);
        rightMotor->setSpeed(30);
        leftMotor->run(FORWARD);
        rightMotor->run(BACKWARD);
    }

    void stop()
    {
        leftMotor->run(RELEASE);
        rightMotor->run(RELEASE);
    }
}