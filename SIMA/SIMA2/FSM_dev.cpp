#include <SoftwareSerial.h>
#include <Arduino.h>
#include "FSM_dev.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"

bool rotationChanged = false;
bool rotatingLeft = false;

FSM_dev::FSM_dev(UltrasonicSensor us, MotorControl mc)
    : ultrasonicSensor(us), motorControl(mc), currentState(INIT) {}

void FSM_dev::update()
{
    currentTime = millis();
    Serial.println("Hello");

    if (currentTime >= stopTime || avoided > maxAvoided)
    {
        currentState = STOP;
    }

    switch (currentState)
    {
    case INIT:
        currentState = CHECK_OBSTACLE;
        break;

    case MOVE:
        move();
        break;

    case CHECK_OBSTACLE:
        checkObstacle();
        break;

    case AVOID_OBSTACLE:
        avoidObstacle();
        break;

    case ROTATING:
        rotating();
        break;

    case STOP:
        stopMotors();
        break;
    }
}

void FSM_dev::move()
{
    motorControl.moveForward();
    currentState = CHECK_OBSTACLE;
}

void FSM_dev::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    if (distance < 10) // If obstacle is closer than 10 cm
    {
        currentState = AVOID_OBSTACLE;
    }
    else
    {
        currentState = MOVE;
    }
}

void FSM_dev::avoidObstacle()
{
    if (avoided % 2 == 0)
    {
        rotatingLeft = false;
    }
    else
    {
        rotatingLeft = true;
    }
    rotationChanged = (avoided != 0);
    rotatingStartTime = millis();
    currentState = ROTATING;
}

void FSM_dev::rotating()
{
    if (currentTime - rotatingStartTime < rotatingTime)
    {
        if (rotatingLeft)
        {
            motorControl.rotateLeft();
        }
        else
        {
            motorControl.rotateRight();
        }
    }
    else
    {
        avoided++;
        currentState = CHECK_OBSTACLE;
    }
}

void FSM_dev::stopMotors()
{
    motorControl.stop();
}