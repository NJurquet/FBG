#include "HallSensor.h"
#include <Arduino.h>

// Initialize the static instance pointer to nullptr
HallSensor* HallSensor::instance = nullptr;

// Constructor to initialize the sensor pin
HallSensor::HallSensor(int pin) {
    HallSensorPin = pin;
    SensorState = LOW;
    PreviousState = LOW;
}

// Initialize the sensor and attach the interrupt
void HallSensor::init() {
    pinMode(HallSensorPin, INPUT);
    // Set the static instance pointer to this object
    instance = this;
    attachInterrupt(digitalPinToInterrupt(HallSensorPin), SensorChange, CHANGE);
}

// Function called in the loop to check sensor state and print messages
void HallSensor::ReadState() {
    // Check if the sensor state has changed
    if (SensorState != PreviousState) {
        if (SensorState == HIGH) {
            Serial.println("Détection !");
        } else {
            Serial.println("Aucune détection");
        }

        // Update previous state
        PreviousState = SensorState;
    }
}

// Interrupt function to handle sensor state change
void HallSensor::SensorChange() {
    // Use the static instance pointer to access the actual object
    if (instance != nullptr) {
        instance->SensorState = digitalRead(instance->HallSensorPin); // Read current state of the sensor
    }
}
