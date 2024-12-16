// #include <Arduino.h>
#include <SoftwareSerial.h>
#include "FSM_groupie.h"
#include "FSM_star.h"
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
const int HallSensorPin = 2;

// RX/TX pins of Bluetooth module
const int TX_Debug = 9;
const int RX_Debug = 10;
SoftwareSerial mySerial(TX_Debug, RX_Debug);

HallSensor hallSensor(HallSensorPin);
UltrasonicSensor ultrasonicSensor(trigPin, echoPin);
IRSensor leftIRSensor(leftIRPin);
IRSensor rightIRSensor(rightIRPin);
MotorControl motorControl;
Debugger debugger(TX_Debug, RX_Debug);

FSM fsm(ultrasonicSensor, leftIRSensor, rightIRSensor, motorControl);
FSM_dev fsm_dev(ultrasonicSensor, motorControl);

void debug()
{
  if (rotationChanged)
  {
    if (rotatingLeft)
    {
      mySerial.println(F("Changed rotation to left"));
    }
    else
    {
      mySerial.println(F("Changed rotation to right"));
    }
    rotationChanged = false; // Reset the flag
  }

  if (Serial.available())
  {
    mySerial.write(Serial.read()); // Forward what Serial received to Software Serial Port
  }
  if (mySerial.available())
  {
    Serial.write(mySerial.read()); // Forward what Software Serial received to Serial Port
  }
}

void setup()
{
  delay(1000);
  while (!Serial)
    ;
  Serial.begin(9600);
  mySerial.begin(9600);
  Serial.println(F("Initializing..."));

  motorControl.init();
  ultrasonicSensor.init();
  leftIRSensor.init();
  rightIRSensor.init();
  hallSensor.init();
}

void loop()
{
  // fsm.update();
  fsm_dev.update();
  debug();
}