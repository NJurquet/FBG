#include <Arduino.h>
#include <Servo.h>

Servo myServo;
int pos;

void setup() {
  // myServo.attach(9);
  // myServo.writeMicroseconds(1600);
  // delay(1000);
  // myServo.writeMicroseconds(1400);
  // delay(1000);
  // myServo.writeMicroseconds(1500);
  // delay(1000);

  myServo.attach(9);
  myServo.write(50);
  delay(1000);
  myServo.write(15);
  delay(1000);
}

void loop()
{
    
}