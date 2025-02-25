from gpiozero import Robot, Motor
from time import sleep

robot = Robot(left=Motor(17, 27), right=Motor(22, 23))

for i in range(4):
    robot.forward()
    sleep(10)
    robot.right()
    sleep(1)