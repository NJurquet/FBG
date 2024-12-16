#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

#include <Adafruit_MotorShield.h>

/**
 * @brief A class to control the motors of a SAMI.
 *
 * Defines all required methods for controlling the robot's movements.
 */
class MotorControl
{
private:
    Adafruit_MotorShield AFMS;
    Adafruit_DCMotor *leftMotor;
    Adafruit_DCMotor *rightMotor;

    /**
     * @brief The speed of the motors.
     */
    int motorSpeed;

public:
    /**
     * @brief Constructor for the MotorControl class.
     */
    MotorControl();

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
     * @brief Moves the robot backward.
     */
    void moveBackward();

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

    /**
     * @brief Gets the speed of the motors.
     *
     * @return The 8-bit PWM value, 0 is off, 255 is on.
     */
    int getSpeed();

    /**
     * @brief Sets the speed of the motors.
     *
     * @param speed The 8-bit PWM value, 0 is off, 255 is on.
     */
    void setSpeed(int speed);
};

#endif // MOTORCONTROL_H