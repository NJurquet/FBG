#ifndef FSM_H
#define FSM_H

#include "UltrasonicSensor.h"
#include "IRSensor.h"

class FSM
{
public:
    FSM(UltrasonicSensor ultrasonicSensor, IRSensor leftIRSensor, IRSensor rightIRSensor);
    void update();

private:
    enum State
    {
        INIT,
        WAIT,
        CHECK_OBSTACLE,
        FOLLOW_LINE,
        AVOID_OBSTACLE,
        STOP
    };
    UltrasonicSensor ultrasonicSensor;
    IRSensor leftIRSensor;
    IRSensor rightIRSensor;
    State currentState;
    const unsigned long startDelay = 85000; // 85 seconds in milliseconds
    const unsigned long stopTime = 100000;  // 100 seconds in milliseconds

    void checkObstacle();
    void avoidObstacle();
    void stopMotors();
    void followLine();
};

#endif // FSM_H