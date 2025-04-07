from hardware import reedSwitch

rs = reedSwitch(26)

while True:
    # Check if the reed switch is pressed (0 means not pressed, 1 means pressed)
    if rs.read() == 0:
        print("Reed switch is pressed!")
    else:
        print("Reed switch is not pressed.")