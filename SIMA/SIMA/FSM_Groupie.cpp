#include <Arduino.h>
#include "FSM_groupie.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM_groupie::FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS) : ultrasonicSensor(us), leftIRSensor(leftIR), rightIRSensor(rightIR), motorControl(mc), ledCelebretion(lc), servoCelebretion(sc), zoneNumber(zN), leftStart(lS)
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
        if (currentTime >= startDelay)
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

    case ENTER_ZONE:
        enterZone();
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
    currentState = distance < 10 ? AVOID_OBSTACLE : FOLLOW_LINE;
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
        motorControl.moveForward();

        // TODO: Implement crossings and perpendicular line behaviour
        zoneCounter++;
        if (zoneCounter == zoneNumber)
        {
            currentState = ENTER_ZONE;
            enterZoneTime = millis();
        }
        Serial.println("Detected perpendicular line");
    }

    currentState = CHECK_OBSTACLE;
}

void FSM_groupie::enterZone()
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