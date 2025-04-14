#include <Arduino.h>
#include "MotorControl.h"
#include <SPI.h>

MotorControl::MotorControl()
{
    AFMS = Adafruit_MotorShield();
    leftMotor = AFMS.getMotor(4);
    rightMotor = AFMS.getMotor(3);
    motorSpeed = 85;
    motorRotationSpeed = 50;
    leftOffset = 0;
    rightOffset = 0;
}

void MotorControl::init()
{
    AFMS.begin();
}

void MotorControl::moveForward()
{
    leftMotor->setSpeed(motorSpeed + leftOffset);
    rightMotor->setSpeed(motorSpeed + rightOffset);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
}

void MotorControl::moveBackward()
{
    leftMotor->setSpeed(motorSpeed / 2 + leftOffset/2);
    rightMotor->setSpeed(motorSpeed / 2 + rightOffset/2);
    leftMotor->run(BACKWARD);
    rightMotor->run(BACKWARD);
}

void MotorControl::rotateLeft()
{
    leftMotor->setSpeed(motorRotationSpeed + leftOffset);
    rightMotor->setSpeed(motorSpeed + rightOffset);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
}

void MotorControl::rotateRight()
{
    leftMotor->setSpeed(motorSpeed + leftOffset);
    rightMotor->setSpeed(motorRotationSpeed + rightOffset);
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

void MotorControl::setRotationSpeed(double speedRatio)
{
    motorRotationSpeed = motorSpeed * speedRatio;
}

void MotorControl::setLeftOffset(int offset)
{
    leftOffset = offset;
}

void MotorControl::setRightOffset(int offset)
{
    rightOffset = offset;
}