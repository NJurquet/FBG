#ifndef ULTRASONICSENSOR_H
#define ULTRASONICSENSOR_H

namespace UltrasonicSensor
{
    void init(int trigPin, int echoPin);
    long readDistance();
}

#endif // ULTRASONICSENSOR_H