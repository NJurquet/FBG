#ifndef IRSENSOR_H
#define IRSENSOR_H

class IRSensor
{
public:
    IRSensor(int pin);
    void init();
    bool read();

private:
    int pin;
};

#endif // IRSENSOR_H