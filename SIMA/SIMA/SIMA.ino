// #include <Arduino.h>
#include <SoftwareSerial.h>
#include "FSM_groupie.h"
#include "FSM_star.h"
#include "MotorControl.h"
#include "UltrasonicSensor.h"
#include "IRSensor.h"
#include "HallSensor.h"
#include "Led.h"
#include "ServoMotor.h"
#include "Debug.h"
#include "MagneticStart.h"

// IR sensor pins
const int leftIRPin = A0;
const int rightIRPin = A1;

// Ultrasonic sensor pins
const int leftTrigPin = 9;  //green cable
const int leftEchoPin = 8;  //blue cable

const int rightTrigPin = 11; //green cable
const int rightEchoPin = 10;  //blue cable

// Celebretion pins
const int celebrationLedPin = 13;
const int celebrationServoPin = 6;

// Hall sensor pin
const int HallSensorPin = 2;

// Magnetic start pin
const int magneticStartPin = 5;

// Groupie start left select pin
const int startLeftPin = 12;

HallSensor hallSensor(HallSensorPin);
UltrasonicSensor leftUltrasonicSensor(leftTrigPin, leftEchoPin);
UltrasonicSensor rightUltrasonicSensor(rightTrigPin, rightEchoPin);
IRSensor leftIRSensor(leftIRPin);
IRSensor rightIRSensor(rightIRPin);
MotorControl motorControl;
Led celebrationLed(celebrationLedPin);
ServoMotor celebretionServo(celebrationServoPin);
MagneticStart magneticStart(magneticStartPin);

// CONFIGURATION CONSTANTS ///////////////////////
const bool groupie = true;
const bool leftStart = digitalRead(startLeftPin);
const bool topStartLine = false;
const int zoneNumber = topStartLine ? 1 : 2;
//////////////////////////////////////////////////

FSM_groupie fsm_groupie(leftUltrasonicSensor, rightUltrasonicSensor, leftIRSensor, rightIRSensor, motorControl, celebrationLed, celebretionServo, magneticStart, zoneNumber, leftStart, topStartLine);
FSM_star fsm_star(leftUltrasonicSensor, rightUltrasonicSensor, leftIRSensor, rightIRSensor, motorControl, magneticStart, celebrationLed, celebretionServo);

void setup()
{
  delay(1000);
  while (!Serial)
    ;
  Serial.begin(9600);

  Serial.println(F("Initializing..."));

  motorControl.init();
  leftUltrasonicSensor.init();
  rightUltrasonicSensor.init();
  leftIRSensor.init();
  rightIRSensor.init();
  hallSensor.init();
  celebrationLed.init();
  celebretionServo.init();
  magneticStart.init();
}

void loop()
{
  groupie ? fsm_groupie.update() : fsm_star.update();
}
