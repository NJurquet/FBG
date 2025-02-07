#ifndef FSM_COLLECT_H
#define FSM_COLLECT_H

class FSM_COLLECT
{
public:
    FSM_COLLECT();

    void update();

private:
    enum State
    {
        INIT,
        ELEVATE_FORK,
        GRAB_CANS
        
    } currentState;
    
};
#endif // FSM_COLLECT_H