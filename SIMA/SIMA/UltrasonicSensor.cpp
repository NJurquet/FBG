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
    long distance = (duration / 2) * 34300 * 1e-6; // Speed of sound [cm/s] wave divided by 2 (go and back) [cm]
    return abs(distance);
}