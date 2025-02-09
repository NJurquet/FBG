#include <Arduino.h>
#include "FSM_groupie.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM_groupie::FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS, bool tSL) : ultrasonicSensor(us), leftIRSensor(leftIR), rightIRSensor(rightIR), motorControl(mc), ledCelebretion(lc), servoCelebretion(sc), zoneNumber(zN), leftStart(lS), topStartLine(tSL)
{
    currentState = INIT;
    previousState = INIT;
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
            previousState = currentState;
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
    if (distance < obstacleDistance)
    {
        // If a new obstacle is detected, start counting the time
        if (previousState != AVOID_OBSTACLE)
        {
            obstacleStartTime = currentTime;
        }
        previousState = currentState;
        currentState = AVOID_OBSTACLE;
    }
    else
    {
        // If the robot finished avoiding the obstacle, add the time to the total obstacle time
        if (previousState == AVOID_OBSTACLE)
        {
            totalObstacleTime += currentTime - obstacleStartTime;
        }
        previousState = currentState;
        currentState = enteringZone ? ENTER_ZONE : FOLLOW_LINE;
    }
}

void FSM_groupie::avoidObstacle()
{
    motorControl.stop();
    previousState = currentState;
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
            if (currentTime - startDelayTop - totalObstacleTime >= turnZoneDelay)
            { // If at the minimum time for detecting a zone turn (considering time elapsed during obstacle avoidance), start turning
                enteringZone = true;
                enterZoneTime = currentTime;
                totalObstacleTime = 0;
            }
            else
            { // It's not yet time to detect a zone turn, keep moving forward
                motorControl.moveForward();
            }
        }
        else
        {
            if (currentTime - startDelayBottom - totalObstacleTime >= turnZoneDelay)
            { // If at the minimum time for detecting a zone turn (considering time elapsed during obstacle avoidance), start turning
                enteringZone = true;
                enterZoneTime = currentTime;
                totalObstacleTime = 0;
            }
            else
            { // It's not yet time to detect a zone turn, keep moving forward
                motorControl.moveForward();
            }
        }
    }

    previousState = currentState;
    currentState = CHECK_OBSTACLE;
}

void FSM_groupie::enterZone()
{
    if (topStartLine)
    {
        if (currentTime - enterZoneTime - totalObstacleTime <= firstZoneTurnTime)
        { // Turn to the zone for a set of time (removing the time spent avoiding obstacles)
            motorControl.setRotationSpeed(topRotationSpeedRatio);
            leftStart ? motorControl.rotateLeft() : motorControl.rotateRight();
            previousState = currentState;
            currentState = CHECK_OBSTACLE;
        }
        else
        { // When reaching the zone, stop
            previousState = currentState;
            currentState = STOP;
        }
    }
    else
    {
        if (currentTime - enterZoneTime - totalObstacleTime <= secondZoneTurnTime)
        { // Turn to the zone for a set of time (removing the time spent avoiding obstacles)
            motorControl.setRotationSpeed(bottomRotationSpeedRatio);
            leftStart ? motorControl.rotateLeft() : motorControl.rotateRight();
            previousState = currentState;
            currentState = CHECK_OBSTACLE;
        }
        else
        { // When reaching the zone, stop
            previousState = currentState;
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