#include <Arduino.h>
#include "FSM_groupie.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "MagneticStart.h"

FSM_groupie::FSM_groupie(UltrasonicSensor usl, UltrasonicSensor usr, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, MagneticStart ms, int zN, bool lS, bool tSL) : 
leftUltrasonicSensor(usl), rightUltrasonicSensor(usr), leftIRSensor(leftIR), rightIRSensor(rightIR), motorControl(mc), ledCelebretion(lc), servoCelebretion(sc), magneticStart(ms), zoneNumber(zN), leftStart(lS), topStartLine(tSL)
{
    currentState = INIT;
    previousState = INIT;
    motorControl.setSpeed(60);
    if (topStartLine)
    {
      motorControl.setRightOffset(5);
      motorControl.setRotationSpeed(topRotationSpeedRatio*1.1);
    }
    else
    {
      leftStart ? motorControl.setLeftOffset(1) : motorControl.setLeftOffset(3);
      leftStart ? motorControl.setRotationSpeed(0.65) : motorControl.setRotationSpeed(0.7);
    }
    // topStartLine ? motorControl.setRotationSpeed(topRotationSpeedRatio*1.1) : motorControl.setRotationSpeed(0.9);
    servoCelebretion.setPosition(90);
    ledCelebretion.turnOff();
}

void FSM_groupie::update()
{
    currentTime = (magneticStartTime > 0) ? (millis() - magneticStartTime) : millis();

    if (currentTime >= stopTime && currentState != CELEBRATE)
    {
        currentState = STOP;
    }

    switch (currentState)
    {
    case INIT:
        while (!magneticStartDetected)
        {
            magneticStartDetected = magneticStart.read();
            digitalWrite(13,HIGH);
        }
        digitalWrite(13,LOW);
        magneticStartTime = millis(); //Time when the rope is pulled
        currentState = WAIT;
        break;

    case WAIT:
        if ((topStartLine && currentTime >= startDelayTop) || (!topStartLine && currentTime >= startDelayBottom))
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

    long distanceL = 100;
    long distanceR = 100;

    if (topStartLine && currentTime - startDelayTop - totalObstacleTime <= turnZoneDelay || !topStartLine && currentTime - startDelayBottom - totalObstacleTime <= turnZoneDelay){
      leftStart ? distanceR = rightUltrasonicSensor.readDistance() : distanceL = leftUltrasonicSensor.readDistance();
    } 
    else {
      distanceL = leftUltrasonicSensor.readDistance();
      distanceR = rightUltrasonicSensor.readDistance();
    }

    // Checks if obstacle is closer than 10 cm
    if (distanceL < obstacleDistance || distanceR < obstacleDistance)
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
                motorControl.setRotationSpeed(topRotationSpeedRatio);
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
                motorControl.setRotationSpeed(bottomRotationSpeedRatio);
                motorControl.setLeftOffset(2);
                enteringZone = true;
                enterZoneTime = currentTime;
                totalObstacleTime = 0;
            }
            // else if (currentTime - startDelayBottom - totalObstacleTime >= 0.6*turnZoneDelay)
            // {
            //   if (leftStart) {motorControl.setRotationSpeed(bottomRotationSpeedRatio*0.8);}
            // }
            else
            { // It's not yet time to detect a zone turn, keep moving forward
                // motorControl.moveForward();
                leftStart ? motorControl.rotateRight() : motorControl.rotateLeft();
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
        if (currentTime - enterZoneTime - totalObstacleTime  <= secondZoneTurnTime)
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
        servoCelebretion.setPosition(90 + celebrationAngle);
        celebrationAngle = -celebrationAngle;
        lastCelebrationTime = currentTime;
    }
}