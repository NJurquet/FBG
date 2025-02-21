from gpiozero import Motor
from time import sleep
from BigMotorControl import BigMotorControl

motor1 = BigMotorControl(17, 27)

while True:
    motor1.forward(0.5)
    sleep(5)
    motor1.forward(1)
    sleep(5)
    motor1.backward(0.5)


