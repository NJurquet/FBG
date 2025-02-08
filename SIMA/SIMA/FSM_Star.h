#ifndef FSM_star_H
#define FSM_star_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "MotorControl.h"
#include "Led.h"
#include "ServoMotor.h"

/**
 * @brief Finite State Machine (FSM) for controlling the Superstar robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param us An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIR An instance of the IRSensor class for detecting the left line.
 * @param centerIR An instance of the IRSensor class for detecting the center line.
 * @param rightIR An instance of the IRSensor class for detecting the right line.
 * @param mc An instance of the MotorControl class for controlling the robot's motors/movements.
 * @param lc An instance of the Led class for controlling the celebration LED.
 * @param sc An instance of the ServoMotor class for controlling the celebration servo motor.
 */
class FSM_star
{
public:
    /**
     * @brief Constructor for the FSM_star class.
     */
    FSM_star(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc);

    /**
     * @brief Updates the state of the FSM_star and the robot's actions.
     */
    void update();

private:
    UltrasonicSensor ultrasonicSensor;
    IRSensor leftIRSensor;
    IRSensor centerIRSensor;
    IRSensor rightIRSensor;
    MotorControl motorControl;
    Led ledCelebretion;
    ServoMotor servoCelebretion;
    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        FOLLOW_LINE,
        AVOID_OBSTACLE,
        STOP,
        CELEBRATE
    } currentState;
    const unsigned long startDelay = 5000; // 85 seconds in milliseconds
    const unsigned long stopTime = 15000;  // 100 seconds in milliseconds
    unsigned long currentTime;
    unsigned long blackStartTime = 0; // Start time when all sensors detect black
    bool checkingBlack = false;       // Whether we are in the process of checking for continuous black
    const int celebrationDelay = 500; // 0.5 seconds
    unsigned long lastCelebrationTime = 0;
    int celebrationAngle = 35;

    /**
     * @brief Checks for obstacles for a distance in front of the robot using ultrasonic sensor.
     */
    void checkObstacle();

    /**
     * @brief Avoids obstacles in front of the robot.
     *
     * @todo Implement a correct obstacle avoidance algorithm
     */
    void avoidObstacle();

    /**
     * @brief Manages line-following behavior using IR sensors.
     */
    void followLine();

    /**
     * @brief Stops the motors of the robot.
     */
    void stopMotors();

    /**
     * @brief Celebrates for the show by moving the servo motor and toggling the LED.
     */
    void celebrate();
};

#endif // FSM_star_H