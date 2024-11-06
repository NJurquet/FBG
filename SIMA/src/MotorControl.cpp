#include <Arduino.h>
#include "MotorControl.h"
#include <SPI.h>

MotorControl::MotorControl()
{
    AFMS = Adafruit_MotorShield();
    leftMotor = AFMS.getMotor(4);
    rightMotor = AFMS.getMotor(3);
    motorSpeed = 30;
}

void MotorControl::init()
{
    AFMS.begin();
}

void MotorControl::moveForward()
{
    leftMotor->setSpeed(motorSpeed);
    rightMotor->setSpeed(motorSpeed);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
}

void MotorControl::rotateLeft()
{
    leftMotor->setSpeed(motorSpeed);
    rightMotor->setSpeed(motorSpeed);
    leftMotor->run(BACKWARD);
    rightMotor->run(FORWARD);
}

void MotorControl::rotateRight()
{
    leftMotor->setSpeed(motorSpeed);
    rightMotor->setSpeed(motorSpeed);
    leftMotor->run(FORWARD);
    rightMotor->run(BACKWARD);
}

void MotorControl::stop()
{
    leftMotor->run(RELEASE);
    rightMotor->run(RELEASE);
}

int MotorControl::getSpeed()
{
    return motorSpeed;
}

void MotorControl::setSpeed(int speed)
{
    motorSpeed = speed;
}