from gpiozero import Motor
from time import sleep

motor1 = Motor(13, 19)
speed = 1.0

while True:
    motor1.forward(speed)

