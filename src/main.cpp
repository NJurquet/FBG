#include <Arduino.h>
#include "FSM.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"

// Ultrasonic sensor pins
const int trigPin = 11;
const int echoPin = 12;

FSM fsm;

void setup()
{
    Serial.begin(9600);
    MotorControl::init();
    UltrasonicSensor::init(trigPin, echoPin);
}

void loop()
{
    fsm.update();
}