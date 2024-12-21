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
FSM_star::FSM_star(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc) : ultrasonicSensor(us),
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

        followLine();
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
    bool leftIR = leftIRSensor.read();     // Is 1 if it detects white
    bool centerIR = centerIRSensor.read(); // Is 1 if it detects white
    bool rightIR = rightIRSensor.read();   // Is 1 if it detects white

    static unsigned long blackStartTime = 0; // Start time when all sensors detect black
    static bool checkingBlack = false;       // Whether we are in the process of checking for continuous black

    // If all sensors detect black
    if (leftIR && centerIR && rightIR)
    {
        motorControl.moveForward();
        if (!checkingBlack)
        {
            // Start timing the continuous black detection
            blackStartTime = millis();
            checkingBlack = true;
        }
        else
        {
            // Check if 1.5 seconds (1500 ms) have passed
            if (millis() - blackStartTime >= 750)
            {
                // If black is detected for 1.5 seconds continuously, stop
                motorControl.stop();
                Serial.println("All sensors detect black for 1.5s. Stopping.");
                while (millis() - blackStartTime < 30000)
                {
                    celebrate();
                }
                celebrate();

                return;
            }
        }
    }
    else
    {
        // If not all sensors are on black, reset the black detection timer
        checkingBlack = false;
    }

    // Normal line-following logic
    if (!leftIR && !rightIR && !centerIR) // If all sensors are on white
    {
        motorControl.moveForward();
        Serial.println("Moving forward");
    }
    else if (!leftIR && !rightIR && centerIR) // If Left and Right sensors are on white and center sensor is on black
    {
        motorControl.moveForward();
        Serial.println("Moving forward");
    }
    else if (leftIR && !centerIR)
    {
        motorControl.rotateRight();
        Serial.println("Rotating right");
    }
    else if (rightIR && !centerIR)
    {
        motorControl.rotateLeft();
        Serial.println("Rotating left");
    }
    /*
    else if (leftIR && centerIR) // If left & center sensors detect the black line -> potentially on the left curved part of the line
    {
        motorControl.rotateLeft();
        Serial.println("Left curve detected, rotating left");
    }*/
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
    while (true)
    {
        ledCelebretion.turnOn();
        servoCelebretion.setPosition(35);
        delay(500);
        ledCelebretion.turnOff();
        servoCelebretion.setPosition(-35);
        delay(500);
    }
}