#include <Arduino.h>
#include "FSM_groupie.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

/**
 * @brief Constructor for the Finite State Machine (FSM_groupie) class.
 * 
 * Initializes the FSM_groupie with ultrasonic and IR sensors, motor control,
 * and sets the initial state to INIT.
 * 
 * @param us UltrasonicSensor object for distance measurement
 * @param leftIR Left IR sensor for line tracking
 * @param centerIR Center IR sensor for lint tracking
 * @param rightIR Right IR sensor for line tracking
 * @param mc MotorControl object for robot movement
 * @param zN Integer that determines which zone is the target of the groupie
 * @param lS Boolean that determines if the groupie starts on the left side of the arena
 */
FSM_groupie::FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS): 
    ultrasonicSensor(us), 
    leftIRSensor(leftIR), 
    centerIRSensor(centerIR), 
    rightIRSensor(rightIR), 
    motorControl(mc),
    ledCelebretion(lc),
    servoCelebretion(sc),
    zoneNumber(zN), 
    leftStart(lS) 
{
    currentState = INIT;
    servoCelebretion.setPosition(0);
    ledCelebretion.turnOff();
}

/**
 * @brief Main update method for the Finite State Machine.
 * 
 * Manages the state transitions and actions based on the current state
 * and elapsed time. Controls the robot's behavior through different states
 * such as initialization, waiting, obstacle checking, line following,
 * obstacle avoidance, and stopping.
 */
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

/**
 * @brief Checks for obstacles using the ultrasonic sensor.
 * 
 * Reads the distance from the ultrasonic sensor and determines
 * the next state based on the measured distance:
 * - If an obstacle is closer than 10 cm, transitions to AVOID_OBSTACLE
 * - Otherwise, transitions to FOLLOW_LINE
 */
void FSM_groupie::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    if (distance < 10) // If obstacle is closer than 10 cm
    {
        currentState = AVOID_OBSTACLE;
    }
    else
    {
        currentState = FOLLOW_LINE;
    }
}

/**
 * @brief Handles obstacle avoidance behavior.
 * 
 * Currently a placeholder method for implementing obstacle avoidance strategy.
 * Temporarily transitions back to CHECK_OBSTACLE state.
 * 
 * @todo Implement a comprehensive obstacle avoidance algorithm
 */
void FSM_groupie::avoidObstacle()
{
    motorControl.stop();
    currentState = CHECK_OBSTACLE;
}

/**
 * @brief Manages line-following behavior using IR sensors.
 * 
 * Reads the state of left and right IR sensors and controls
 * the robot's movement accordingly:
 * - If both sensors are on white: move forward
 * - If left sensor detects black line: rotate left
 * - If right sensor detects black line: rotate right
 * - If both sensors detect black line: stop (to be improved)
 */
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

/**
 * @brief Turns the robot in the right direction to begin entering the zone.
 */
void FSM_groupie::enterZone()
{
    unsigned long startTime = millis();  // Capture the current time
    while (millis() - startTime < 2000) {  // Run the loop for 1000 milliseconds (1 second)
        if (leftStart) {
            motorControl.rotateLeft();
        } else {
            motorControl.rotateRight();
        }
    delay(10);  // Small delay to reduce CPU usage
    }
    currentState = ENTERING_ZONE;
}

/**
 * @brief Drives the robot forward to be in the middle of the zone.
 */
void FSM_groupie::enteringZone()
{
    unsigned long startTime = millis();  // Capture the current time
    while (millis() - startTime < 1500) {  // Run the loop for 1000 milliseconds (1 second)
        motorControl.moveForward();
        delay(10);  // Small delay to reduce CPU usage
    }
    currentState = STOP;
}

/**
 * @brief Stops the robot's motors.
 * 
 * Calls the stop method of the motor control object
 * to halt all motor movement.
 */
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