#ifndef FSM_H
#define FSM_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"

/**
 * @brief State Machine (FSM) for controlling a robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param ultrasonicSensor An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIRSensor An instance of the IRSensor class for detecting the left side of the line.
 * @param rightIRSensor An instance of the IRSensor class for detecting the right side of the line.
 */
class FSM
{
public:
    /**
     * @brief Constructor for the FSM class.
     */
    FSM(UltrasonicSensor ultrasonicSensor, IRSensor leftIRSensor, IRSensor rightIRSensor);

    /**
     * @brief Updates the state of the FSM.
     */
    void update();

private:
    UltrasonicSensor ultrasonicSensor;
    IRSensor leftIRSensor;
    IRSensor rightIRSensor;
    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        FOLLOW_LINE,
        AVOID_OBSTACLE,
        STOP
    } currentState;
    const unsigned long startDelay = 85000; // 85 seconds in milliseconds
    const unsigned long stopTime = 100000;  // 100 seconds in milliseconds

    /**
     * @brief Checks for obstacles for a distance in front of the robot using ultrasonic sensor.
     */
    void checkObstacle();

    /**
     * @brief Avoids obstacles in front of the robot.
     */
    void avoidObstacle();

    /**
     * @brief Follows a line based on the IR sensors readings.
     */
    void followLine();

    /**
     * @brief Stops the motors of the robot.
     */
    void stopMotors();
};

#endif // FSM_H