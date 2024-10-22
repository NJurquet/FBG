#include <Arduino.h>
#include "FSM.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"

// IR sensor pins
const int leftIRPin = A0;
const int rightIRPin = A1;

// Ultrasonic sensor pins
const int trigPin = 11;
const int echoPin = 12;

UltrasonicSensor ultrasonicSensor(trigPin, echoPin);
IRSensor leftIRSensor(leftIRPin);
IRSensor rightIRSensor(rightIRPin);
FSM fsm(ultrasonicSensor, leftIRSensor, rightIRSensor);

void setup()
{
    Serial.begin(9600);
    MotorControl::init();
    ultrasonicSensor.init();
    leftIRSensor.init();
    rightIRSensor.init();
}

void loop()
{
    fsm.update();
}