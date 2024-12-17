#include <SoftwareSerial.h>
#include <Arduino.h>
#include "FSM_star.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

/**
 * @brief Constructor for the Finite State Machine (FSM_star) class.
 * 
 * Initializes the FSM_star with ultrasonic and IR sensors, motor control,
 * and sets the initial state to INIT.
 * 
 * @param us UltrasonicSensor object for distance measurement
 * @param leftIR Left IR sensor for line tracking
 * @param centerIR center IR sensor for line tracking
 * @param rightIR Right IR sensor for line tracking
 * @param mc MotorControl object for robot movement
 */
FSM_star::FSM_star(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc): 
    ultrasonicSensor(us), 
    leftIRSensor(leftIR), 
    centerIRSensor(centerIR), 
    rightIRSensor(rightIR), 
    motorControl(mc), 
    ledCelebretion(lc), 
    servoCelebretion(sc), 
    currentState(INIT) {}

/**
 * @brief Main update method for the Finite State Machine.
 * 
 * Manages the state transitions and actions based on the current state
 * and elapsed time. Controls the robot's behavior through different states
 * such as initialization, waiting, obstacle checking, line following,
 * obstacle avoidance, and stopping.
 */
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

    case ON_THE_EDGE:
        if (currentTime < stopTime)
        {
            if (currentTime > onTheEdgeTime + 1000)
            {
                currentState = STOP;
            }
            else 
            {
                onTheEdge();
            }
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
        stopMotors ();
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
 * - If an obstacle is closer than 20 cm, transitions to AVOID_OBSTACLE
 * - Otherwise, transitions to FOLLOW_LINE
 */
void FSM_star::checkObstacle()
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
void FSM_star::avoidObstacle()
{
    currentTime = millis(); 
    while (currentTime < avoidTime + 1500)
    {
        motorControl.moveBackward();
        motorControl.rotateRight();
        currentTime = millis();
    }

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
void FSM_star::followLine()
{
    bool leftIR = leftIRSensor.read(); //Is 1 if it detects white
    bool centerIR = centerIRSensor.read(); //Is 1 if it detects white
    bool rightIR = rightIRSensor.read(); //Is 1 if it detects white

    if (leftIR  && rightIR  && !centerIR) // If Left and Right sensors are on white and center sensor is on black
    {
        motorControl.moveForward();
        Serial.println("Moving forward");
    }
    else if (!leftIR && centerIR)  // If left sensor detects the black line and the center sensor detect the white line
    {
        motorControl.rotateRight();
        Serial.println("Rotating left");
    }
    else if (!rightIR && centerIR) // If right sensor detects the black line
    {
        motorControl.rotateLeft();
        Serial.println("Rotating right");
    }
    else if (!leftIR && !rightIR & !centerIR) // If both sensors detect the black line
    {
        // TODO: Implement a solution for line reunion
        motorControl.stop();
    }

}

/**
 * @brief Go forward a certain time to be as close to the edge as possible.
 */
void FSM_star::onTheEdge()
{
    motorControl.moveForward();
}

/**
 * @brief Stops the robot's motors.
 * 
 * Calls the stop method of the motor control object
 * to halt all motor movement.
 */
void FSM_star::stopMotors()
{
    motorControl.stop();

    if (currentTime > stopTime)
    {
        currentState = CELEBRATE;
    }
}

void FSM_star::celebrate()
{
    servoCelebretion.setPosition(0);
    while(true){
        ledCelebretion.turnOn();
        servoCelebretion.setPosition(35);
        delay(500);
        ledCelebretion.turnOff();
        servoCelebretion.setPosition(-35);
        delay(500);
    }
}