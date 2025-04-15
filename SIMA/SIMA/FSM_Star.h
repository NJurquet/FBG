#ifndef FSM_star_H
#define FSM_star_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "MotorControl.h"
#include "Led.h"
#include "ServoMotor.h"
#include "MagneticStart.h"

/**
 * @brief Finite State Machine (FSM) for controlling the Superstar robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param us1 An instance of the UltrasonicSensor class for detecting obstacles.
 * @param us2 An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIR An instance of the IRSensor class for detecting the left line.
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
    FSM_star(UltrasonicSensor us1, UltrasonicSensor us2, IRSensor leftIR, IRSensor rightIR, MotorControl mc, MagneticStart ms, Led lc, ServoMotor sc);

    /**
     * @brief Updates the state of the FSM_star and the robot's actions.
     */
    void update();

private:
    UltrasonicSensor leftUltrasonicSensor;
    UltrasonicSensor rightUltrasonicSensor;
    IRSensor leftIRSensor;
    IRSensor rightIRSensor;
    MotorControl motorControl;
    Led ledCelebretion;
    ServoMotor servoCelebretion;
    MagneticStart magneticStart;

    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        AVOID_OBSTACLE,
        FOLLOW_LINE,
        STOP,
        CELEBRATE
    } currentState;
    State previousState;
    const unsigned long startDelay = 5000;   // 85 seconds in milliseconds / 5 seconds for testing
    const unsigned long stopTime = 15000;    // 100 seconds in milliseconds / 15 seconds for testing
    const unsigned long edgeStopTime = 7800; // 7s35ms seconds in milliseconds
    unsigned long currentTime;               // Time from the start of the program in milliseconds
    unsigned long obstacleStartTime = 0;     // Time when a new obstacle is detected in milliseconds
    unsigned long totalObstacleTime = 0;     // Total time spent avoiding obstacles in milliseconds
    const int obstacleDistance = 10;         // Distance in cm from which it will be detected as an obstacle
    const double rotationSpeedRatio = 0.8;   // Ratio of the main speed to apply for rotation
    bool magneticStartDetected = false;      // Flag to know if the magnetic start was detected
    long magneticStartTime = 0;              // Time when the magnetic start was detected in milliseconds

    const int celebrationDelay = 1000;     // 1 seconds
    unsigned long lastCelebrationTime = 0; // Time when the last celebration happened in milliseconds
    int celebrationAngle = 35;             // Angle at which the servo motor will alternate

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