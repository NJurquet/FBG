from gpiozero import Motor
from time import sleep

motor1 = Motor(13, 19)
speed = 1.0
motor2 = Motor(17,27)

while True:
    motor1.forward(speed)
    motor2.forward(speed)
    sleep(5)
    motor1.stop()
    sleep(2)
    motor1.forward(speed)
    motor2.forward(speed)

