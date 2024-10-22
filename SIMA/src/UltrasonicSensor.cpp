#include <Arduino.h>
#include "UltrasonicSensor.h"

UltrasonicSensor::UltrasonicSensor(int tPin, int ePin) : trigPin(tPin), echoPin(ePin) {}

void UltrasonicSensor::init()
{
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

long UltrasonicSensor::readDistance()
{
    digitalWrite(trigPin, LOW); // Clears the trigPin
    delayMicroseconds(2);

    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    long distance = (duration / 2) * 0.034; // Speed of sound wave divided by 2 (go and back)
    return distance;
}