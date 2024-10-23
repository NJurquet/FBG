#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

/**
 * @namespace MotorControl
 * @brief Namespace for motor control functions.
 */
namespace MotorControl
{
    /**
     * @brief Initializes the motor control system.
     *
     * This method sets up the necessary configurations for the Motors and Motor Shield.
     */
    void init();

    /**
     * @brief Moves the robot forward.
     */
    void moveForward();

    /**
     * @brief Rotates the robot to the left.
     */
    void rotateLeft();

    /**
     * @brief Rotates the robot to the right.
     */
    void rotateRight();

    /**
     * @brief Stops the robot.
     */
    void stop();
}

#endif // MOTORCONTROL_H