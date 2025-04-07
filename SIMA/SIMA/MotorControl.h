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
    int motorRotationSpeed;
    int leftOffset;
    int rightOffset;

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

    /**
     * @brief Sets the rotation speed of the motors as a ratio of the main speed.
     *
     * @param speedRatio The ratio of the main speed to apply.
     */
    void setRotationSpeed(double speedRatio);

    /**
     * @brief Sets the speed offset to add to the left motor.
     *
     * @param offset The offset to apply.
     */
    void setLeftOffset(int offset);

    /**
     * @brief Sets the speed offset to add to the right motor.
     *
     * @param offset The offset to apply.
     */
    void setRightOffset(int offset);
};

#endif // MOTORCONTROL_H