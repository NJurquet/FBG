#ifndef FSM_star_H
#define FSM_star_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "MotorControl.h"
#include "Led.h"
#include "ServoMotor.h"

/**
 * @brief State Machine (FSM) for controlling a robot's behavior based on sensor inputs.
 *
 * The class includes methods to update the state, check for obstacles, avoid obstacles, stop the motors, and follow a line.
 *
 * @param ultrasonicSensor An instance of the UltrasonicSensor class for detecting obstacles.
 * @param leftIRSensor An instance of the IRSensor class for detecting the left line.
 * @param centerIRSensor An instance of the IRSensor class for detecting the center line.
 * @param rightIRSensor An instance of the IRSensor class for detecting the right line.
 * @param motorControl An instance of the MotorControl class for controlling the robot's motors/movements.
 */
class FSM_star
{
public:
    /**
     * @brief Constructor for the FSM_star class.
     */
    FSM_star(UltrasonicSensor us, IRSensor leftIR, IRSensor centerIR, IRSensor rightIR, MotorControl mc, Led lc, ServoMotor sc);

    /**
     * @brief Updates the state of the FSM_star.
     */
    void update();

    /**
     * @brief Follow the white lines.
     */
    void followLine();

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
        ON_THE_EDGE,
        AVOID_OBSTACLE,
        STOP,
        CELEBRATE
    } currentState;
    const unsigned long startDelay = 5000; // 85 seconds in milliseconds
    const unsigned long stopTime = 15000;  // 100 seconds in milliseconds
    unsigned long onTheEdgeStartTime;
    unsigned long currentTime;
    unsigned long onTheEdgeTime = 1000;
    unsigned long avoidTime;

    /**
     * @brief Go forward a certain time to be as close to the edge as possible.
     */
    void onTheEdge();

    /**
     * @brief Checks for obstacles for a distance in front of the robot using ultrasonic sensor.
     */
    void checkObstacle();

    /**
     * @brief Avoids obstacles in front of the robot.
     */
    void avoidObstacle();

    /**
     * @brief Stops the motors of the robot.
     */
    void stopMotors();

    /**
     * @brief Celebrates for the show.
     */
    void celebrate();
};

#endif // FSM_star_H