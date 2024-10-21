# Superstar & Groupies

## Overview

The superstar and groupies are Small Independent Mobile Actuators (SIMA) capable of navigating its environment while avoiding obstacles. They both have specific roles but they use an ultrasonic sensor to detect obstacles, IR sensors to follow lines drawn on the table and a finite state machine (FSM) to manage its states and behaviors.

## Depedencies

-   `Adafruit Motor Shield V2 Library`

## Components

-   **Arduino Uno**: The microcontroller used to control the robot.
-   **Adafruit Motor Shield V2**: Used to control the motors of the robot.
-   **Ultrasonic Sensor HC-SR04**: Used to detect obstacles in the robot's path.
-   **IR sensor**: Used to follow lines drawn on the table.

## Setup

1. **Hardware Setup**:

    - Connect the ultrasonic sensor to the specified pins on the Arduino.
    - Connect the IR sensors to the specified pins on the Arduino.
    - Connect the motors to the Adafruit Motor Shield V2.
    - Attach the Motor Shield to the Arduino.

2. **Software Setup**:
    - Install the necessary libraries (e.g., Adafruit Motor Shield library).
    - Build & upload the code to the Arduino.

## Finite State Machine (FSM)

The FSM manages the following states:

-   `INIT`: Initial state, transitions to WAIT.
-   `WAIT`: Waits for a specified delay before starting obstacle detection.
-   `CHECK_OBSTACLE`: Checks for obstacles using the ultrasonic sensor.
-   `MOVE_FORWARD`: Moves the robot forward if no obstacles are detected.
-   `ROTATE`: Rotates the robot if an obstacle is detected.
-   `STOP`: Stops the robot.

## License

This project is licensed under the MIT License.
