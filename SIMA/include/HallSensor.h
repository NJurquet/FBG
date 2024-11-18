#ifndef HallSensor_H
#define HallSensor_H

class HallSensor {
public:
    // Constructor to initialize the sensor pin
    HallSensor(int pin);

    // Method to initialize the sensor
    void init();

    // Method to read and print sensor state
    void ReadState();

private:
    int HallSensorPin;  // Pin du capteur
    volatile int SensorState;  // État du capteur, volatile car utilisé dans l'interruption
    int PreviousState;  // Précédent état du capteur

    // Static pointer to the instance of the class
    static HallSensor* instance;

    // Fonction appelée lors du changement d'état du capteur
    static void SensorChange(); 
};

#endif
