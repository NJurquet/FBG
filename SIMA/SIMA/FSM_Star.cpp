#include <SoftwareSerial.h>
#include <Arduino.h>
#include "FSM_star.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM_star::FSM_star(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc)
{
    ultrasonicSensor = us;
    leftIRSensor = leftIR;
    rightIRSensor = rightIR;
    motorControl = mc;
    ledCelebretion = lc;
    servoCelebretion = sc;

    currentState = INIT;
    servoCelebretion.setPosition(0);
    ledCelebretion.turnOff();
}

void FSM_star::update()
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

void FSM_star::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    // Checks if obstacle is closer than 10 cm
    currentState = distance < 10 ? AVOID_OBSTACLE : FOLLOW_LINE;
}

void FSM_star::avoidObstacle()
{
    motorControl.stop();
    currentState = CHECK_OBSTACLE;
}

void FSM_star::followLine()
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
    }

    currentState = CHECK_OBSTACLE;
}

void FSM_star::stopMotors()
{
    motorControl.stop();
    currentState = CELEBRATE;
}

void FSM_star::celebrate()
{
    if (currentTime - lastCelebrationTime >= celebrationDelay)
    {
        ledCelebretion.toggle();
        servoCelebretion.setPosition(celebrationAngle);
        celebrationAngle = -celebrationAngle;
        lastCelebrationTime = currentTime;
    }
}