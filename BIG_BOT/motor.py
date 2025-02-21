from gpiozero import Motor
from time import sleep
motor1 = Motor(forward=4, backward=14) #Pin numbers


motor1.forward()
test = 0 
while test <3:
    sleep(5)
    motor1.reverse()
    
    test +=1

motor1.stop()



