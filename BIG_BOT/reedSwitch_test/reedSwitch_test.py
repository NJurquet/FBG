from BIG_BOT.src.hardware.reedSwitch import reedSwitch
from time import sleep


reed = reedSwitch(4)
while True:
    print(reed.read())
    sleep(1)
    

