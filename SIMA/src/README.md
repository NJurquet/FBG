# Robotic Software Homework

This homework is about creating a simple FSM for a SIMA to move, rotate, and avoid an obstacle when one is detected.
When the obstacle is detected, the robot will rotate in the opposite direction of the last rotation until it is clear to move forward.
Rotation direction is also send by Bluetooth for debugging purposes.

The goal of this homework is to follow code good practices, with a correct git versionning flow, and review peers code via pull requests before merging.

> **Note:**
>
> The homework was made in the already existing repository for the Eurobot robotic project, thus the files needed for the homework are `main.cpp`, `FSM_dev.cpp/.h`, `MotorControl.cpp/.h`, `UltrasonicSensor.cpp/.h`, and `Debug.cpp/.h`.

To use this FSM, make sure the `main.cpp` file is correctly set up by uncommenting the `fsm_dev.update()` method:

```cpp
void loop()
{
    // fsm.update();
    fsm_dev.update();
}
```

## FSM

The FSM is composed of 6 states:

```cpp
enum State
    {
        INIT,
        MOVE,
        CHECK_OBSTACLE,
        AVOID_OBSTACLE,
        ROTATING,
        STOP
    };
```

The state `INIT` will first set the state to `MOVE` (An initial obstacle check has not been done because "When we start the system, there is nothing in front of the senor").

The `MOVE` state will move the robot forward and change the state to `CHECK_OBSTACLE` to check if there is an obstacle before continuing to move.

The `CHECK_OBSTACLE` state will check if there is an obstacle within a distance of 20cm in front of the robot. If there is an obstacle, the state will change to `AVOID_OBSTACLE`, otherwise, it will change to `MOVE`.

The `AVOID_OBSTACLE` state will define the rotation direction based on the last rotation direction (rotates in the opposite direction) and change the state to `ROTATING`.

The `ROTATING` state will rotate the robot in the specified direction for a defined amount of time and send Bluetooth message with the direction, then change the state back to `CHECK_OBSTACLE`.

At any time, if the robot has changed his rotation direction 5 times (6 total rotations/avoidances), or after running for 30 seconds, the state will change to `STOP` and will need a reboot to restart the FSM.
