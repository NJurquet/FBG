#include <Arduino.h>
#include "FSM.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM::FSM(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR)
    : ultrasonicSensor(us), leftIRSensor(leftIR), rightIRSensor(rightIR), currentState(INIT) {}

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

    case FOLLOW_LINE:
        if (currentTime < stopTime)
        {
            followLine();
            currentState = CHECK_OBSTACLE;
        }
        else
        {
            currentState = STOP;
        }
        break;

    case AVOID_OBSTACLE:
        if (currentTime < stopTime)
        {
            avoidObstacle();
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

void FSM::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    if (distance < 20) // If obstacle is closer than 20 cm
    {
        currentState = AVOID_OBSTACLE;
    }
    else
    {
        currentState = FOLLOW_LINE;
    }
}

void FSM::avoidObstacle()
{
    // TODO: Implement obstacle avoidance
    currentState = CHECK_OBSTACLE;
}

void FSM::followLine()
{
    bool leftIR = leftIRSensor.read();
    bool rightIR = rightIRSensor.read();

    if (leftIR == 0 && rightIR == 0) // If both sensors do not detect the black line (detect white lines)
    {
        MotorControl::moveForward();
        Serial.println("Moving forward");
    }
    else if (leftIR && !rightIR) // If left sensor detects the black line
    {
        MotorControl::rotateLeft();
        Serial.println("Rotating left");
    }
    else if (!leftIR && rightIR) // If right sensor detects the black line
    {
        MotorControl::rotateRight();
        Serial.println("Rotating right");
    }
    else if (leftIR && rightIR) // If both sensors detect the black line
    {
        // TODO: Implement a solution for line reunion
        MotorControl::stop();
    }
}

void FSM::stopMotors()
{
    MotorControl::stop();
}