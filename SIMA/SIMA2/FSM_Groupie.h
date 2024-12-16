#ifndef FSM_groupie_H
#define FSM_groupie_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "MotorControl.h"

/**
 * @brief State Machine (FSM_groupie) for controlling a robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param ultrasonicSensor An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIRSensor An instance of the IRSensor class for detecting the left side of the line.
 * @param rightIRSensor An instance of the IRSensor class for detecting the right side of the line.
 * @param motorControl An instance of the MotorControl class for controlling the robot's motors/movements.
 */
class FSM_groupie
{
public:
    /**
     * @brief Constructor for the FSM_groupie class.
     */
    FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc);

    /**
     * @brief Updates the state of the FSM_groupie.
     */
    void update();

private:
    UltrasonicSensor ultrasonicSensor;
    IRSensor leftIRSensor;
    IRSensor rightIRSensor;
    MotorControl motorControl;
    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        FOLLOW_LINE,
        AVOID_OBSTACLE,
        STOP
    } currentState;
    const unsigned long startDelay = 5000; // 85 seconds in milliseconds
    const unsigned long stopTime = 100000; // 100 seconds in milliseconds

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

#endif // FSM_groupie_H