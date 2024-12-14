# Superstar & Groupies

## Overview

The superstar and groupies are Small Independent Mobile Actuators (SIMA) capable of navigating its environment while avoiding obstacles. They both have specific roles but they use an ultrasonic sensor to detect obstacles, IR sensors to follow lines drawn on the table, Bluetooth module for remote debugging and a finite state machine (FSM) to manage its states and behaviors.

## Depedencies

-   `Adafruit Motor Shield V2 Library` : v1.1.3

## Components

-   **Arduino Uno**: The microcontroller used to control the robot.
-   **Adafruit Motor Shield V2**: Used to control the motors of the robot.
-   **Ultrasonic Sensor HC-SR04**: Used to detect obstacles in the robot's path.
-   **IR sensor**: Used to follow lines drawn on the table.
-   **HC-05 Bluetooth module** : Used to debug robot actions.

## Setup

### Hardware Setup

-   **Motors** : First, place the motor shield on the Arduino. Then, connect the left motor to `M4`, and the right motor to `M3`.
-   **Ultrasonic sensor** : Connect the VCC to `5V`, GND to `GND`, Trig to pin `11`, and Echo to pin `12`.
-   **IR sensors** : Connect the VCC to `5V`, GND to `GND`, and the left sensor to pin `A0` and the right sensor to pin `A1`.
-   **Bluetooth** : Connect the VCC to `5V`, GND to `GND`, RX to pin `10`, and TX to pin `9`.

### Software Setup

-   Open Arduino IDE and install the necessary libraries (e.g., Adafruit Motor Shield V2 library).
-   Open the `.ino` file (`.cpp` and `.h` files should open automatically).
-   Build & upload the code to the Arduino.
