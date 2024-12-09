#include <Arduino.h>
#include "FSM_dev.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"

/**
 * @brief Constructor for the Development Finite State Machine (FSM_dev) class.
 * 
 * Initializes the FSM with an ultrasonic sensor and motor control,
 * setting the initial state to INIT.
 * 
 * @param us UltrasonicSensor object for distance measurement
 * @param mc MotorControl object for robot movement
 */
FSM_dev::FSM_dev(UltrasonicSensor us, MotorControl mc)
    : ultrasonicSensor(us), motorControl(mc), currentState(INIT) {}

/**
 * @brief Main update method for the Finite State Machine.
 * 
 * Manages state transitions and actions based on current state,
 * elapsed time, and number of obstacle avoidances.
 * Controls robot behavior through states: initialization, 
 * moving, obstacle checking, obstacle avoidance, rotating, and stopping.
 */
void FSM_dev::update()
{
    currentTime = millis();

    switch (currentState)
    {
    case INIT:
        currentState = MOVE;
        break;

    case MOVE:
        if (currentTime < stopTime && avoided <= maxAvoided)
        {
            move();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case CHECK_OBSTACLE:
        if (currentTime < stopTime && avoided <= maxAvoided)
        {
            checkObstacle();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case AVOID_OBSTACLE:
        if (currentTime < stopTime && avoided <= maxAvoided)
        {
            avoidObstacle();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case ROTATING:
        if (currentTime < stopTime && avoided <= maxAvoided)
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

/**
 * @brief Moves the robot forward and transitions to obstacle checking.
 * 
 * Sends a move forward command to the motor control and
 * prints a debug message. Immediately transitions to 
 * CHECK_OBSTACLE state.
 */
void FSM_dev::move()
{
    motorControl.moveForward();
    Serial.println("Moving forward");
    currentState = CHECK_OBSTACLE;
}

/**
 * @brief Checks for obstacles using the ultrasonic sensor.
 * 
 * Reads the distance from the ultrasonic sensor and determines
 * the next state:
 * - If an obstacle is closer than 20 cm, transitions to AVOID_OBSTACLE
 * - Otherwise, remains in or returns to MOVE state
 */
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

/**
 * @brief Prepares the robot for obstacle avoidance.
 * 
 * Alternates between left and right rotation based on 
 * the number of obstacles avoided. Increments the avoided
 * counter and sets up for rotating state.
 */
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

/**
 * @brief Handles robot rotation during obstacle avoidance.
 * 
 * Rotates the robot left or right for a predetermined time
 * based on the previous avoidObstacle() method configuration.
 * Transitions back to MOVE state after rotation is complete.
 */
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

/**
 * @brief Stops the robot's motors.
 * 
 * Calls the stop method of the motor control object
 * to halt all motor movement.
 */
void FSM_dev::stopMotors()
{
    motorControl.stop();
}