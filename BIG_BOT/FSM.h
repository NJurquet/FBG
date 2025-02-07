#ifndef FSM_H
#define FSM_H

class FSM
{
public:
    FSM();

    void update();

private:
    enum State
    {
        INIT,
        DETECT_TARGETS,
        MOVE,
        ROTATE,
        CHECK_OBSTACLE,
        AVOID_OBSTACLE,
        MOVE_TO_COLLECT,
        COLLECT,
        SLOW_MOVE,
        SLOW_ROTATE,
        DROP,
        RETURN,
        STOP
    } currentState;

    void DetectTargets();

    void move();

    void rotate();

    void checkObstacle();

    void avoidObstacle();

    void collect();

    void slowMove();

    void slowRotate();

    void drop();

    void stopMotors();
};
#endif // FSM_H