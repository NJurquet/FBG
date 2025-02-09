#include <Arduino.h>
#include "FSM_groupie.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM_groupie::FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS, bool tSL) : ultrasonicSensor(us), leftIRSensor(leftIR), rightIRSensor(rightIR), motorControl(mc), ledCelebretion(lc), servoCelebretion(sc), zoneNumber(zN), leftStart(lS), topStartLine(tSL)
{
    currentState = INIT;
    servoCelebretion.setPosition(0);
    ledCelebretion.turnOff();
}

void FSM_groupie::update()
{
    currentTime = millis();

    if (currentTime >= stopTime)
    {
        currentState = STOP;
    }

    switch (currentState)
    {
    case INIT:
        currentState = WAIT;
        break;

    case WAIT:
        if ((topStartLine && currentTime >= startDelayTop) || (!topStartLine && currentTime >= startDelayBottom))
        { // Make sure to repect starting delay for each groupie
            currentState = CHECK_OBSTACLE;
        }
        break;

    case CHECK_OBSTACLE:
        checkObstacle();
        break;

    case AVOID_OBSTACLE:
        avoidObstacle();
        break;

    case FOLLOW_LINE:
        followLine();
        break;

    case ENTER_ZONE:
        enterZone();
        break;

    case STOP:
        stopMotors();
        break;

    case CELEBRATE:
        celebrate();
        break;
    }
}

void FSM_groupie::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    // Checks if obstacle is closer than 10 cm
    if (distance < 10)
    {
        currentState = AVOID_OBSTACLE;
    }
    else
    {
        currentState = enteringZone ? ENTER_ZONE : FOLLOW_LINE;
    }
}

void FSM_groupie::avoidObstacle()
{
    motorControl.stop();
    currentState = CHECK_OBSTACLE;
}

void FSM_groupie::followLine()
{
    bool leftIR = leftIRSensor.read();   // Is 1 if it detects black
    bool rightIR = rightIRSensor.read(); // Is 1 if it detects black

    if (leftIR && rightIR) // If all sensors detect black
    {
        motorControl.moveForward();
    }
    else if (!leftIR && rightIR) // If Left on white and right on black
    {
        motorControl.rotateLeft();
    }
    else if (leftIR && !rightIR) // If Left on black and right on white
    {
        motorControl.rotateRight();
    }
    else if (!leftIR && !rightIR) // If all sensors are on white
    {
        if (topStartLine)
        {
            if (currentTime - startDelayTop >= turnZoneDelay)
            { // If at the minimum time for detecting a zone turn, start turning
                enteringZone = true;
                enterZoneTime = currentTime;
            }
            else
            { // It's not yet time to detect a zone turn, keep moving forward
                motorControl.moveForward();
            }
        }
        else
        {
            if (currentTime - startDelayBottom >= turnZoneDelay)
            { // If at the minimum time for detecting a zone turn, start turning
                enteringZone = true;
                enterZoneTime = currentTime;
            }
            else
            { // It's not yet time to detect a zone turn, keep moving forward
                motorControl.moveForward();
            }
        }
    }

    currentState = CHECK_OBSTACLE;
}

void FSM_groupie::enterZone()
{
    if (topStartLine)
    {
        if (currentTime - enterZoneTime <= firstZoneTurnTime)
        { // Turn to the zone for a set of time
            motorControl.setRotationSpeed(0.5);
            leftStart ? motorControl.rotateLeft() : motorControl.rotateRight();
            currentState = CHECK_OBSTACLE;
        }
        else
        { // When reaching the zone, stop
            currentState = STOP;
        }
    }
    else
    {
        if (currentTime - enterZoneTime <= secondZoneTurnTime)
        { // Turn to the zone for a set of time
            motorControl.setRotationSpeed(0.8);
            leftStart ? motorControl.rotateLeft() : motorControl.rotateRight();
            currentState = CHECK_OBSTACLE;
        }
        else
        { // When reaching the zone, stop
            currentState = STOP;
        }
    }
}

void FSM_groupie::stopMotors()
{
    motorControl.stop();
    currentState = CELEBRATE;
}

void FSM_groupie::celebrate()
{
    if (currentTime - lastCelebrationTime >= celebrationDelay)
    {
        ledCelebretion.toggle();
        servoCelebretion.setPosition(celebrationAngle);
        celebrationAngle = -celebrationAngle;
        lastCelebrationTime = currentTime;
    }
}