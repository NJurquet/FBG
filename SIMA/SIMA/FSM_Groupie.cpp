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
        {
            currentState = CHECK_OBSTACLE;
        }
        break;

    case CHECK_OBSTACLE:
        checkObstacle();
        break;

    case FOLLOW_LINE:
        followLine();
        break;

    case TURN_TO_ZONE:
        turnToZone();
        break;

    case ENTERING_ZONE:
        enteringZone();
        break;

    case AVOID_OBSTACLE:
        avoidObstacle();
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
        currentState = enterZone ? TURN_TO_ZONE : FOLLOW_LINE;
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
            if (currentTime - startDelayTop >= turnZoneTime)
            {
                enterZone = true;
            }
            else
            {
                motorControl.moveForward();
            }
        }
        else
        {
            if (currentTime - startDelayBottom >= turnZoneTime)
            {
                enterZone = true;
            }
            else
            {
                motorControl.moveForward();
            }
        }
    }

    currentState = CHECK_OBSTACLE;
}

void FSM_groupie::turnToZone()
{
    unsigned long startTime = millis(); // Capture the current time
    while (millis() - startTime < 2000)
    { // Run the loop for 1000 milliseconds (1 second)
        if (leftStart)
        {
            motorControl.rotateLeft();
        }
        else
        {
            motorControl.rotateRight();
        }
        delay(10); // Small delay to reduce CPU usage
    }
    currentState = ENTERING_ZONE;
}

void FSM_groupie::enteringZone()
{
    unsigned long startTime = millis(); // Capture the current time
    while (millis() - startTime < 1500)
    { // Run the loop for 1000 milliseconds (1 second)
        motorControl.moveForward();
        delay(10); // Small delay to reduce CPU usage
    }
    currentState = STOP;
}

void FSM_groupie::stopMotors()
{
    motorControl.stop();

    if (currentTime > stopTime)
    {
        currentState = CELEBRATE;
    }
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