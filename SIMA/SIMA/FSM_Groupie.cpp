#include <Arduino.h>
#include "FSM_groupie.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM_groupie::FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS)
{
    ultrasonicSensor = us;
    leftIRSensor = leftIR;
    centerIRSensor = centerIR;
    rightIRSensor = rightIR;
    motorControl = mc;
    ledCelebretion = lc;
    servoCelebretion = sc;
    zoneNumber = zN;
    leftStart = lS;

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
    bool leftIR = leftIRSensor.read();
    bool centerIR = centerIRSensor.read();
    bool rightIR = rightIRSensor.read();

    if ((!leftIR && !rightIR && !centerIR) || (!leftIR && !rightIR && centerIR)) // If both extreme sensors do not detect the black line (detect white lines) & center detects black line
    {
        motorControl.moveForward();
        Serial.println("Moving forward");
        currentState = CHECK_OBSTACLE;
    }
    else if (leftIR && !centerIR) // If left detect black & center detect white we turn right
    {
        motorControl.rotateRight();
        Serial.println("Rotating left");
        currentState = CHECK_OBSTACLE;
    }
    else if (rightIR && !centerIR) // If right detect black & center detect white we turn left
    {
        motorControl.rotateLeft();
        Serial.println("Rotating right");
        currentState = CHECK_OBSTACLE;
    }
    else if (leftIR && rightIR && centerIR) // If all sensors detect the black line
    {
        zoneCounter++;
        if (zoneCounter == zoneNumber)
        {
            currentState = ENTER_ZONE;
            enterZoneTime = millis();
        }
        Serial.println("Detected perpendicular line");
    }
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