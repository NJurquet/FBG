#include <Arduino.h>
#include "FSM.h"
#include "FSM_dev.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "HallSensor.h"
#include "Debug.h"

// IR sensor pins
const int leftIRPin = A0;
const int rightIRPin = A1;

// Ultrasonic sensor pins
const int trigPin = 11;
const int echoPin = 12;

// Hall sensor pins
const int HallSensorPin(2);

// Debugging pins
const int TX_Debug = 9;
const int RX_Debug = 10;

HallSensor hallSensor(HallSensorPin);
UltrasonicSensor ultrasonicSensor(trigPin, echoPin);
IRSensor leftIRSensor(leftIRPin);
IRSensor rightIRSensor(rightIRPin);
MotorControl motorControl;
Debugger debugger(TX_Debug, RX_Debug);

FSM fsm(ultrasonicSensor, leftIRSensor, rightIRSensor, motorControl);
FSM_dev fsm_dev(ultrasonicSensor, motorControl, debugger);

void setup()
{
    delay(1000);
    while (!Serial)
        ;
    Serial.begin(9600);
    motorControl.init();
    ultrasonicSensor.init();
    leftIRSensor.init();
    rightIRSensor.init();
    hallSensor.init();
    debugger.init();
}

void loop()
{
    // fsm.update();
    fsm_dev.update();
}