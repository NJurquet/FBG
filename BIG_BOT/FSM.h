#ifndef FSM_H
#define FSM_H

// Decision making algorithm:

// 1. Detect the targets (drop area, cans, planks)
// 2. Plan the route => Most efficient route + oriented perpendicular to the planks
//                      + If possible : avoid adversary (if balise placed on top)
// 3. Standard movement FSM
// 4. Always check for obstacles => if any => avoid mode (to determine)
// 5. Precise movement to collect the cans + FSM to collect the cans
// 6. Slow movement to push the planks and cans to target area
// 7. Precise movement to drop the cans + FSM to drop the cans and planks
// 8. Repeat until time is up (margin of 10? seconds) => return to starting area
// 9. Stop the motors + Party time

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
        MOVE_TO_DROP,
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