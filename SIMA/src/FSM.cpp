#include <Arduino.h>
#include "FSM.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"

FSM::FSM() : currentState(INIT), rotateStartTime(0) {}

void FSM::update()
{
    unsigned long currentTime = millis();

    switch (currentState)
    {
    case INIT:
        currentState = WAIT;
        break;
    case WAIT:
        if (currentTime >= startDelay)
        {
            currentState = CHECK_OBSTACLE;
        }
        break;
    case CHECK_OBSTACLE:
        if (currentTime < stopTime)
        {
            checkObstacle();
        }
        else
        {
            currentState = STOP;
        }
        break;
    case MOVE_FORWARD:
        if (currentTime < stopTime)
        {
            moveForward();
            currentState = CHECK_OBSTACLE;
        }
        else
        {
            currentState = STOP;
        }
        break;
    case ROTATE:
        if (currentTime < stopTime)
        {
            rotate();
        }
        else
        {
            currentState = STOP;
        }
        break;
    case STOP:
        stopMotors();
        break;
    }
}

void FSM::moveForward()
{
    MotorControl::moveForward();
}

void FSM::checkObstacle()
{
    long distance = UltrasonicSensor::readDistance();
    if (distance < 20) // If obstacle is closer than 20 cm
    {
        currentState = ROTATE;
        rotateStartTime = millis(); // Record the start time of rotation
    }
    else
    {
        currentState = MOVE_FORWARD;
    }
}

void FSM::rotate()
{
    if (millis() - rotateStartTime < rotateDuration)
    {
        MotorControl::rotate();
    }
    else
    {
        currentState = MOVE_FORWARD;
    }
}

void FSM::stopMotors()
{
    MotorControl::stop();
}