#ifndef FSM_H
#define FSM_H

#include <Arduino.h>

enum State
{
    INIT,
    WAIT,
    CHECK_OBSTACLE,
    MOVE_FORWARD,
    ROTATE,
    STOP
};

class FSM
{
public:
    FSM();
    void update();

private:
    State currentState;
    unsigned long rotateStartTime;
    const unsigned long rotateDuration = 500; // 500ms
    const unsigned long startDelay = 85000;   // 85 seconds in milliseconds
    const unsigned long stopTime = 100000;    // 100 seconds in milliseconds

    void moveForward();
    void checkObstacle();
    void rotate();
    void stopMotors();
};

#endif // FSM_H