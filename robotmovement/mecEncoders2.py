import sys
from movementFiles.roboclaw import Roboclaw
from time import sleep
from imageCapture import *
from lightSwitch import *
import sys
import time

roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()

def resetEncoders():
    # Reset encoders and read and print value to test operation
    roboclaw.ResetEncoders(0x80)
    motor_1_count = roboclaw.ReadEncM1(0x80)
    print ("After resetting:")
    print (motor_1_count)

    roboclaw.ResetEncoders(0x80)
    motor_2_count = roboclaw.ReadEncM2(0x80)
    print ("After resetting:")
    print (motor_2_count)

    roboclaw.ResetEncoders(0x81)
    motor_1_count = roboclaw.ReadEncM1(0x81)
    print ("After resetting:")
    print (motor_1_count)

    roboclaw.ResetEncoders(0x81)
    motor_2_count = roboclaw.ReadEncM2(0x81)
    print ("After resetting:")
    print (motor_2_count)

    sleep(2)

# Position motor, these values may have to be changed to suit the motor/encoder combination in use

# forward 
def forward(d):
    distance = d
    roboclaw.SpeedAccelDeccelPositionM1M2(0x80,500,500,500,distance,500,500,500,distance,0)
    roboclaw.SpeedAccelDeccelPositionM1M2(0x81,500,500,500,distance,500,500,500,distance,1)
    reading()

# backward
def backward(d):
    distance = d #1000
    roboclaw.SetEncM2(0x80,distance)
    roboclaw.SetEncM1(0x80,distance)
    roboclaw.SetEncM2(0x81,distance)
    roboclaw.SetEncM1(0x81,distance)
    sleep(1)

    roboclaw.SpeedAccelDeccelPositionM1M2(0x80,500,500,500,0,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM1M2(0x81,500,500,500,0,500,500,500,0,1)
    reading()
    
# right
def right(d):
    distance = d #3000
    roboclaw.SetEncM2(0x80,distance)
    roboclaw.SetEncM1(0x81,distance)
    sleep(1)

    roboclaw.SpeedAccelDeccelPositionM1M2(0x80,500,500,500,distance,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM1M2(0x81,500,500,500,0,500,500,500,distance,1)
    reading()
    
# left
def left(d):
    distance1 = d
    distance2 = d #+ 200
    roboclaw.SetEncM2(0x81,distance2)
    roboclaw.SetEncM1(0x80,distance1)
    sleep(1)

    roboclaw.SpeedAccelDeccelPositionM1(0x80,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x80,500,500,500,distance1,0)
    roboclaw.SpeedAccelDeccelPositionM1(0x81,500,500,500,distance2,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x81,500,500,500,0,1)
    #roboclaw.SpeedAccelDeccelPositionM1M2(0x80,500,500,500,0,500,500,500,5000,0)
    #roboclaw.SpeedAccelDeccelPositionM1M2(0x81,500,500,500,5000,500,500,500,0,1)
    reading()

# rotate right 90
def rotateRight():
    roboclaw.SetEncM2(0x81,915)
    roboclaw.SetEncM2(0x80,915)

    roboclaw.SpeedAccelDeccelPositionM1(0x80,500,500,500,915,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x80,500,500,500,0,0) #500,-500,0,0
    roboclaw.SpeedAccelDeccelPositionM1(0x81,500,500,500,915,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x81,500,500,500,0,1) #500,-500,0,1
    reading()

# rotate right 360
def rotateRight360():
    roboclaw.SetEncM2(0x81,3660)
    roboclaw.SetEncM2(0x80,3660)

    roboclaw.SpeedAccelDeccelPositionM1(0x80,500,500,500,3660,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x80,500,500,500,0,0) #500,-500,0,0
    roboclaw.SpeedAccelDeccelPositionM1(0x81,500,500,500,3660,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x81,500,500,500,0,1) #500,-500,0,1
    reading()

# rotate left 90
def rotateLeft():
    roboclaw.SetEncM1(0x81,921)
    roboclaw.SetEncM1(0x80,921)

    roboclaw.SpeedAccelDeccelPositionM1(0x80,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x80,500,500,500,921,0)
    roboclaw.SpeedAccelDeccelPositionM1(0x81,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x81,500,500,500,921,1)
    reading()

# rotate left 360
def rotateLeft360():
    roboclaw.SetEncM1(0x81,3684)
    roboclaw.SetEncM1(0x80,3684)

    roboclaw.SpeedAccelDeccelPositionM1(0x80,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x80,500,500,500,3684,0)
    roboclaw.SpeedAccelDeccelPositionM1(0x81,500,500,500,0,0)
    roboclaw.SpeedAccelDeccelPositionM2(0x81,500,500,500,3684,1)
    reading()


def reading():
    address = 0x80
    address2 = 0x81
    speed1 = 1000
    speed2 = 1000
    distance = 6000

    sleep(2)
    print()
    print(roboclaw.ReadSpeedM1(address))
    print(roboclaw.ReadSpeedM2(address))
    print(roboclaw.ReadSpeedM1(address2))
    print(roboclaw.ReadSpeedM2(address2))
    print()
    print(roboclaw.ReadEncM1(address)[1])
    print(roboclaw.ReadEncM2(address)[1])
    print(roboclaw.ReadEncM1(address2)[1])
    print(roboclaw.ReadEncM2(address2)[1])

def scenario1(x,y):
    resetEncoders()
    l = 1800 - y
    b = 2300 + x
    left(l)
    sleep(8)
    resetEncoders()
    backward(b)
    sleep(8)
    resetEncoders()
    right(1800)

def scenario2(x,y):
    resetEncoders()
    r = 3000 + y
    b = 2300 + x
    right(r)
    sleep(8)
    resetEncoders()
    backward(b)
    sleep(8)
    resetEncoders()
    left(3200)

def path():
    #take picture
    print("Taking picture 1")
    lightOn()
    takePhoto(0, "p1")
    # time.sleep(2)
    lightOff()
    sleep(2)
    
    print("Moving left")
    resetEncoders()
    left(1400)
    sleep(3)
    print("Moving forward")
    resetEncoders()
    forward(2800)
    sleep(5)
    
    #take picture
    print("Taking picture 2")
    lightOn()
    takePhoto(0, "p2")
    # time.sleep(2)
    lightOff()
    sleep(2)
    print("Moving right")
    resetEncoders()
    right(1400)
    sleep(3)
    
    #take picture
    print("Taking picture 3")
    lightOn()
    takePhoto(0, "p3")
    # time.sleep(2)
    lightOff()
    sleep(2)
    print("Moving right")
    resetEncoders()
    right(1400)
    sleep(3)
    
    #take picture
    print("Taking picture 4")
    lightOn()
    takePhoto(0, "p4")
    # time.sleep(2)
    lightOff()
    sleep(2)
    print("Moving forward")
    resetEncoders()
    forward(2400)
    sleep(5)
    print("Moving left")
    resetEncoders()
    left(1700)
    sleep(3)
    
    #take picture
    print("Taking picture 5")
    lightOn()
    takePhoto(0, "p5")
    # time.sleep(2)
    lightOff()
    sleep(2)

if __name__ == '__main__':
    #scenario2(150,-20)
    #path()
    resetEncoders()
    backward(3000)

