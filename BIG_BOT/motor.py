from gpiozero import Motor
from time import sleep
motor1 = Motor(17,27) #Pin numbers

while True:
    motor1.forward()
    print("T")

