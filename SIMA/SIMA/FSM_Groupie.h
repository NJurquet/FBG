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
 * @param centerIR An instance of the IRSensor class for detecting the center line.
 * @param rightIR An instance of the IRSensor class for detecting the right side of the line.
 * @param mc An instance of the MotorControl class for controlling the robot's motors/movements.
 * @param lc An instance of the Led class for controlling the celebration LED.
 * @param sc An instance of the ServoMotor class for controlling the celebration servo motor.
 * @param zN Integer that determines which zone is the target of the groupie (1 or 2).
 * @param lS Boolean that determines if the groupie begins on the left side of the arena.
 */
class FSM_groupie
{
public:
    /**
     * @brief Constructor for the FSM_groupie class.
     */
    FSM_groupie(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc, int zN, bool lS);

    /**
     * @brief Updates the state of the FSM_groupie.
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
    int zoneNumber;
    bool leftStart;
    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        FOLLOW_LINE,
        ENTER_ZONE,
        ENTERING_ZONE,
        AVOID_OBSTACLE,
        STOP,
        CELEBRATE
    } currentState;
    const unsigned long startDelay = 5000; // 85 seconds in milliseconds / 0 seconds for testing
    const unsigned long stopTime = 15000;  // 100 seconds in milliseconds / 15 seconds for testing
    unsigned long currentTime;
    unsigned long avoidTime;
    unsigned long enterZoneTime;
    int zoneCounter = 0;
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
     * @brief Turns to enter a zone when encounters the objective perpendicular line.
     */
    void enterZone();

    /**
     * @brief Moves the robot forward to be in the middle of the zone.
     */
    void enteringZone();

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