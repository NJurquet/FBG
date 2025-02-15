#include <SoftwareSerial.h>
#include <Arduino.h>
#include "FSM_star.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

FSM_star::FSM_star(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc) : ultrasonicSensor(us), leftIRSensor(leftIR), rightIRSensor(rightIR), motorControl(mc), ledCelebretion(lc), servoCelebretion(sc)
{
    currentState = INIT;
    previousState = INIT;
    servoCelebretion.setPosition(90);
    ledCelebretion.turnOff();
    motorControl.setRotationSpeed(rotationSpeedRatio);
}

void FSM_star::update()
{
    currentTime = millis();

    if (currentTime >= stopTime && currentState != CELEBRATE)
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
    if (distance < obstacleDistance)
    { // If a new obstacle is detected, start counting the time
        if (previousState != AVOID_OBSTACLE)
        {
            obstacleStartTime = currentTime;
        }
        previousState = currentState;
        currentState = AVOID_OBSTACLE;
    }
    else
    { // If the robot finished avoiding the obstacle, add the time to the total obstacle time
        if (previousState == AVOID_OBSTACLE)
        {
            totalObstacleTime += currentTime - obstacleStartTime;
        }
        previousState = currentState;
        currentState = FOLLOW_LINE;
    }
}

void FSM_star::avoidObstacle()
{
    motorControl.stop();
    previousState = currentState;
    currentState = CHECK_OBSTACLE;
}

void FSM_star::followLine()
{
    // If it is the time at which the superstar should reach the edge (removing the time spent avoiding obstacles), stop
    if (currentTime - startDelay - totalObstacleTime >= edgeStopTime)
    {
        previousState = currentState;
        currentState = STOP;
        return;
    }

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

    previousState = currentState;
    currentState = CHECK_OBSTACLE;
}

void FSM_star::stopMotors()
{
    motorControl.stop();
    currentState = CELEBRATE;
    Serial.println(F("Celebration"));
}

void FSM_star::celebrate()
{
    if (currentTime - lastCelebrationTime >= celebrationDelay)
    {
        ledCelebretion.toggle();
        servoCelebretion.setPosition(90 + celebrationAngle);
        celebrationAngle = -celebrationAngle;
        lastCelebrationTime = currentTime;
    }
}