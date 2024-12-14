#ifndef FSM_dev_H
#define FSM_dev_H

#include "UltrasonicSensor.h"
#include "MotorControl.h"

extern bool rotatingLeft;    // Flag to indicate if the robot is rotating left
extern bool rotationChanged; // Flag to indicate if the rotation direction has changed

/**
 * @brief State Machine (FSM) for controlling a SIMA behavior based on sensor inputs.
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
     * @brief Constructor for the FSM_dev class.
     *
     * @param us UltrasonicSensor object for distance measurement
     * @param mc MotorControl object for robot movement
     */
    FSM_dev(UltrasonicSensor us, MotorControl mc);

    /**
     * @brief Main update method for the Finite State Machine.
     *
     * Manages state transitions and actions based on current state,
     * elapsed time, and number of obstacle avoidances.
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
    const unsigned long stopTime = 30000;    // Stops after 30 seconds
    const unsigned long rotatingTime = 2500; // Rotates for 2.5 second
    unsigned long rotatingStartTime;         // Start time for rotating
    unsigned short avoided = 0;              // Number of avoided objects
    const unsigned short maxAvoided = 5;     // Avoid 5 objects max
    unsigned long currentTime;               // Current time in milliseconds

    /**
     * @brief Moves the robot forward.
     */
    void move();

    /**
     * @brief Checks for obstacles for a distance in front of the robot using ultrasonic sensor.
     *
     * If an obstacle is detected, transitions to `AVOID_OBSTACLE` state, otherwise to `MOVE` state.
     */
    void checkObstacle();

    /**
     * @brief Prepares the robot for obstacle avoidance.
     *
     * Alternates between left and right rotation based on
     * the number of obstacles avoided.
     * Transitions to `ROTATING` state.
     */
    void avoidObstacle();

    /**
     * @brief Handles robot rotation during obstacle avoidance.
     *
     * Rotates the robot left or right for a predetermined time
     * based on the previous `avoidObstacle()` method configuration.
     * Transitions back to `CHECK_OBSTACLE` state after rotation is complete.
     */
    void rotating();

    /**
     * @brief Stops the robot's motors.
     */
    void stopMotors();
};

#endif // FSM_H