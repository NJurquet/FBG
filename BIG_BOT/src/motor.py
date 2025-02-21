from gpiozero import Motor
from time import sleep
from bigMotorControl import BigMotorControl
motor1 = BigMotorControl(17,27) #Pin numbers
motor2 = BigMotorControl(13,19)

while True:
    motor1.forward(1)
    motor2.forward(1)
    print("T")

