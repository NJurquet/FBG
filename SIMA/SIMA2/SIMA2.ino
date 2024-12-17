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
const int centerIRPin = A2;
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
IRSensor centerIRSensor(centerIRPin);
IRSensor rightIRSensor(rightIRPin);
MotorControl motorControl;
Debugger debugger(TX_Debug, RX_Debug);

bool groupie = false;
int zoneNumber = 2;
bool leftStart = true;

FSM_groupie fsm_groupie(ultrasonicSensor, leftIRSensor, centerIRSensor, rightIRSensor, motorControl, zoneNumber, leftStart);
FSM_star fsm_star(ultrasonicSensor, leftIRSensor, centerIRSensor, rightIRSensor, motorControl);

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
  mySerial.println(F("Starting..."));

  motorControl.init();
  ultrasonicSensor.init();
  leftIRSensor.init();
  centerIRSensor.init();
  rightIRSensor.init();
  hallSensor.init();
}

void loop()
{
  if (groupie)
  {
    fsm_groupie.update();
  }
  else
  {
    fsm_star.update();
  }
  // fsm_dev.update();
  debug();
} 