#ifndef LED_H
#define LED_H

class Led
{
public:
    Led(int pin);

    void init();

    void turnOn();

    void turnOff();

    void toggle();

    //void blink();

private:
    int pin;
};

#endif // LED_H