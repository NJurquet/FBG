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
        DETECT_TARGETS,             // These 2 will be called repatedly to detect the targets
        PLAN_ROUTE,                 // and plan the direction of the robot
        MOVE,
        ROTATE,
        CHECK_OBSTACLE,             // Detect the obstacles thanks to the ultrasonic sensors
        AVOID_OBSTACLE,
        MOVE_TO_COLLECT,            // May be redundant but used for precise movement
        COLLECT,            // Uses its own FSM (how to avoid ?)
        SLOW_MOVE,                  // May be redundant but used for
        SLOW_ROTATE,                // deplacement when pushing the planks and cans
        DROP,               // Uses its own FSM (how to avoid ?)
        RETURN,
        STOP
    } currentState;

    void DetectTargets();

    void planRoute();

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