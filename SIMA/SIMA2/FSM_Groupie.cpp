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
 * @param rightIR Right IR sensor for line tracking
 * @param mc MotorControl object for robot movement
 */
FSM_groupie::FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc)
    : ultrasonicSensor(us), leftIRSensor(leftIR), rightIRSensor(rightIR), motorControl(mc), currentState(INIT) {}

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
    unsigned long currentTime = millis();

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
        if (currentTime < stopTime)
        {
            checkObstacle();
        }
        else
        {
            currentState = STOP;
        }
        break;

    case FOLLOW_LINE:
        if (currentTime < stopTime)
        {
            followLine();
            currentState = CHECK_OBSTACLE;
        }
        else
        {
            currentState = STOP;
        }
        break;

    case AVOID_OBSTACLE:
        if (currentTime < stopTime)
        {
            avoidObstacle();
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
 * @brief Checks for obstacles using the ultrasonic sensor.
 * 
 * Reads the distance from the ultrasonic sensor and determines
 * the next state based on the measured distance:
 * - If an obstacle is closer than 20 cm, transitions to AVOID_OBSTACLE
 * - Otherwise, transitions to FOLLOW_LINE
 */
void FSM_groupie::checkObstacle()
{
    long distance = ultrasonicSensor.readDistance();
    if (distance < 20) // If obstacle is closer than 20 cm
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
    // TODO: Implement obstacle avoidance
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
    bool rightIR = rightIRSensor.read();

    if (leftIR == 0 && rightIR == 0) // If both sensors do not detect the black line (detect white lines)
    {
        motorControl.moveForward();
        Serial.println("Moving forward");
    }
    else if (leftIR && !rightIR) // If left sensor detects the black line
    {
        motorControl.rotateLeft();
        Serial.println("Rotating left");
    }
    else if (!leftIR && rightIR) // If right sensor detects the black line
    {
        motorControl.rotateRight();
        Serial.println("Rotating right");
    }
    else if (leftIR && rightIR) // If both sensors detect the black line
    {
        // TODO: Implement a solution for line reunion
        motorControl.stop();
    }
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
}