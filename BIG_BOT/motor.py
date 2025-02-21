from gpiozero import Motor
from time import sleep
from BigMotorControl import BigMotorControl

motor1 = BigMotorControl(13, 19)
speed = 0.0

while speed <1.0:
    motor1.forward(speed)
    speed+= 0.01
    sleep(0.1)


