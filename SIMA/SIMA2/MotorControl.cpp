#include <Arduino.h>
#include "MotorControl.h"
#include <SPI.h>

MotorControl::MotorControl()
{
    AFMS = Adafruit_MotorShield();
    leftMotor = AFMS.getMotor(4);
    rightMotor = AFMS.getMotor(3);
    motorSpeed = 80;
    motorRotationSpeed = 60;
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

void MotorControl::moveBackward()
{
    leftMotor->setSpeed(motorSpeed / 2);
    rightMotor->setSpeed(motorSpeed / 2);
    leftMotor->run(BACKWARD);
    rightMotor->run(BACKWARD);
}

void MotorControl::rotateLeft()
{
    leftMotor->setSpeed(motorRotationSpeed);
    rightMotor->setSpeed(motorSpeed);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
}

void MotorControl::rotateRight()
{
    leftMotor->setSpeed(motorSpeed);
    rightMotor->setSpeed(motorRotationSpeed);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
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