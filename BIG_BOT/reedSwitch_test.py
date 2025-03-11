from src.hardware.reedSwitch import reedSwitch
from time import sleep


reed = reedSwitch(16)
while True:
    print(reed.read())
    sleep(1)


 