#ifndef FSM_DROP_H
#define FSM_DROP_H

class FSM_DROP
{
public:
FSM_DROP();

    void update();

private:
    enum State
    {
        INIT,                       // Maybe use more generic states ?
        CHECK_OBSTACLES,
        RELEASE_OUTTER_CANS,
        SLOW_MOVE,
        PUSH_TOP_PLANK,
        VERTICAL_MOVE_INNER_CANS,
        RELEASE_INNER_CANS,
        VERTICAL_MOVE_FORK,
        
    } currentState;
    
};
#endif // FSM_DROP_H