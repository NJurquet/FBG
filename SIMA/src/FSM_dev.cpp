#include <Arduino.h>
#include "FSM_dev.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"

FSM_dev::FSM_dev(UltrasonicSensor us, MotorControl mc)
    : ultrasonicSensor(us), motorControl(mc), currentState(INIT) {}

void FSM_dev::update()
{
    currentTime = millis();

    switch (currentState)
    {
    case INIT:
        currentState = MOVE;
        break;

    case MOVE:
        if (currentTime < stopTime && avoided < maxAvoided)
        {
            move();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case CHECK_OBSTACLE:
        if (currentTime < stopTime && avoided < maxAvoided)
        {
            checkObstacle();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case AVOID_OBSTACLE:
        if (currentTime < stopTime && avoided < maxAvoided)
        {
            avoidObstacle();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case ROTATING:
        if (currentTime < stopTime && avoided < maxAvoided)
        {
            rotating();
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

void FSM_dev::move()
{
    motorControl.moveForward();
    Serial.println("Moving forward");
    currentState = CHECK_OBSTACLE;
}

void FSM_dev::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    if (distance < 20) // If obstacle is closer than 20 cm
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
    if (avoided % 2 == 0){
        avoided++;
        rotatingLeft = false;
    }
    else{
        avoided++;
        rotatingLeft = true;
    }
    rotatingStartTime = millis();
    currentState = ROTATING;
}

void FSM_dev::rotating(){
    if(currentTime - rotatingStartTime < rotatingTime){
        if (rotatingLeft){
            motorControl.rotateLeft();
            Serial.println("Rotating left");
        }
        else{
            motorControl.rotateRight();
            Serial.println("Rotating right");
        }
    }
    else{
        currentState = MOVE;
    }
}

void FSM_dev::stopMotors()
{
    motorControl.stop();
}