#ifndef FSM_dev_H
#define FSM_dev_H

#include "UltrasonicSensor.h"
#include "MotorControl.h"

/**
 * @brief State Machine (FSM) for controlling a robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param ultrasonicSensor An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIRSensor An instance of the IRSensor class for detecting the left side of the line.
 * @param rightIRSensor An instance of the IRSensor class for detecting the right side of the line.
 * @param motorControl An instance of the MotorControl class for controlling the robot's motors/movements.
 */
class FSM_dev
{
public:
    /**
     * @brief Constructor for the FSM class.
     */
    FSM_dev(UltrasonicSensor us, MotorControl mc);

    /**
     * @brief Updates the state of the FSM.
     */
    void update();

private:
    UltrasonicSensor ultrasonicSensor;
    MotorControl motorControl;
    enum State
    {
        INIT,
        MOVE,
        CHECK_OBSTACLE,
        AVOID_OBSTACLE,
        ROTATING,
        STOP
    } currentState;
    const unsigned long stopTime = 30000; // Stops after 30 seconds
    const unsigned long rotatingTime = 1000; // Rotates for 1 second
    unsigned long rotatingStartTime; // Start time for rotating
    unsigned short avoided = 0; // Number of avoided objects
    const unsigned short maxAvoided = 5; // Avoid 5 objects max
    bool rotatingLeft; // Flag to indicate if the robot is rotating left
    unsigned long currentTime; // Current time in milliseconds

    /**
     * @brief Moves the robot forward.
     */
    void move();

    /**
     * @brief Checks for obstacles for a distance in front of the robot using ultrasonic sensor.
     */
    void checkObstacle();

    /**
     * @brief Avoids obstacles in front of the robot.
     */
    void avoidObstacle();

    /**
     * @brief Rotates the robot in the given direction.
     */
    void rotating();

    /**
     * @brief Stops the motors of the robot.
     */
    void stopMotors();
};

#endif // FSM_H