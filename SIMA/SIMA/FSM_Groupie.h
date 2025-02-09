#ifndef FSM_groupie_H
#define FSM_groupie_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "MotorControl.h"
#include "Led.h"
#include "ServoMotor.h"

/**
 * @brief State Machine (FSM_groupie) for controlling the Groupies robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param us An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIR An instance of the IRSensor class for detecting the left side of the line.
 * @param rightIR An instance of the IRSensor class for detecting the right side of the line.
 * @param mc An instance of the MotorControl class for controlling the robot's motors/movements.
 * @param lc An instance of the Led class for controlling the celebration LED.
 * @param sc An instance of the ServoMotor class for controlling the celebration servo motor.
 * @param zN Integer that determines which zone is the target of the groupie (1 or 2).
 * @param lS Boolean that determines if the groupie begins on the left side of the arena.
 * @param tSL Boolean that determines if the groupie begins on the top or bottom start line.
 */
class FSM_groupie
{
public:
    /**
     * @brief Constructor for the FSM_groupie class.
     */
    FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS, bool tSL);

    /**
     * @brief Updates the state of the FSM_groupie.
     */
    void update();

private:
    UltrasonicSensor ultrasonicSensor;
    IRSensor leftIRSensor;
    IRSensor rightIRSensor;
    MotorControl motorControl;
    Led ledCelebretion;
    ServoMotor servoCelebretion;
    const int zoneNumber;
    const bool leftStart;
    const bool topStartLine;

    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        AVOID_OBSTACLE,
        FOLLOW_LINE,
        ENTER_ZONE,
        STOP,
        CELEBRATE
    } currentState;
    State previousState;
    const unsigned long startDelayBottom = 5000; // 85 seconds in milliseconds / 5 seconds for testing
    const unsigned long startDelayTop = 7000;    // 87 seconds in milliseconds / 7 seconds for testing
    const unsigned long stopTime = 15000;        // 100 seconds in milliseconds / 15 seconds for testing
    unsigned long currentTime;                   // Time from the start of the program in milliseconds
    unsigned long obstacleStartTime = 0;         // Time when a new obstacle is detected in milliseconds
    unsigned long totalObstacleTime = 0;         // Total time spent avoiding obstacles in milliseconds

    const int turnZoneDelay = 6000;      // Time after start at which it can start detecting a zone turn in milliseconds
    const int firstZoneTurnTime = 1000;  // Time needed to turn to the first zone in milliseconds
    const int secondZoneTurnTime = 3000; // Time needed to turn to the second zone in milliseconds
    unsigned long enterZoneTime;         // Time when the robot starts turning to the zone in milliseconds
    bool enteringZone = false;           // Flag to know if the robot is turning to the zone

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
     * @brief Moves the robot to be in the middle of the aimed zone.
     */
    void enterZone();

    /**
     * @brief Stops the motors of the robot.
     */
    void stopMotors();

    /**
     * @brief Celebrates for the show by moving the servo motor and toggling the LED.
     */
    void celebrate();
};

#endif // FSM_groupie_H