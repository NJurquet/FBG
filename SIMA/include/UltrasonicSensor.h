#ifndef ULTRASONICSENSOR_H
#define ULTRASONICSENSOR_H

class UltrasonicSensor
{
public:
    UltrasonicSensor(int trigPin, int echoPin);
    void init();
    long readDistance();

private:
    int trigPin;
    int echoPin;
};

#endif // ULTRASONICSENSOR_H