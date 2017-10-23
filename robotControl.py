# Name: ilyass hmamou, Chi Ho Lee
# Course: CSI262 (Spring 2016)
# Description: Adv Robotics Final Project
#	Code to control iRobot behavior, include guide robot to undiscovery area.
# 	iRobot will facing different direction
#	For example, 2 robots, one will facing east and the other will facing west of the room)
# 	If the iRobot's bumper hit the wall, the iRobot will stop and turn left.
# 	The iRobot will continue to drive through undiscovery area and then stop.

import serial   # PySerial: https://pypi.python.org/pypi/pyserial
import time     # for sleep()
import sys      # for exit()
import math
import client
from socket import *

# adjustment constants (by Chico)
R_ERR_COEF = 1.35 # for robot # 8
#R_ERR_COEF = 1.2 # for robot # 6
#R_ERR_COEF = 1.23 # for robot #  9

V_ERR_COEF = 1.317 # for robot # 8
#V_ERR_COEF = 1.31 # for robot # 6
#V_ERR_COEF = 1.31 # for robot #9

ADJUSTED_STRAIGHT = [253, 18] # for robot # 8
#ADJUSTED_STRAIGHT = [2, 218]  # for robot # 6
#ADJUSTED_STRAIGHT = [128, 0]  # for robot # 9

ROBOT_DIAMETER = 350

# Connect server by call method form client.
server = client.connect()

# Function to convert distance to string
# and call method from modules (by Chico)
def sendDistance(s,distance):
    client.send_data(s, distance)

def int_as_2bytes(num):
    "Converts 16-bit signed integer to 2 unsigned bytes"
    # Mask off high bytes.
    low = num & 0xFF

    # Shift high byte(s) down on byte, then
    # mask off any additional high byte(s).
    high = (num >> 8) & 0xFF 

    return [high, low]

def sleep_time_for90degrees(velocity, rotation_deg):
    wheel_dist = 235 # distance between wheels in mm
    PI = math.pi
    R = velocity* R_ERR_COEF* 360/(wheel_dist * PI)    
    t = rotation_deg/R
    return t 

def convert_in_to_mm(num):
    result = num * 25.4
    return result

def convert_2bytes_ToInt(byte_list):
    from ctypes import c_short

    high_byte = byte_list[0]
    low_byte =  byte_list[1]

    # Combine bytes by shifting high byte
    # into position and adding bits for
    # low byte.
    num = (high_byte << 8) | low_byte

    # return as 2-byte signed number (using
    # "ctypes" module).
    if num > 2**15:
        num -= 2**16
    return num


# Setup serial port for communication.
COM_PORT = 8                # COM port #
ser = serial.Serial()
ser.baudrate = 115200
#ser.baudrate = 57600
#ser.port = COM_PORT - 1     # COM port names start from 0
ser.port = "/dev/ttyUSB0" 
ser.timeout = 10
ser.open()

# Determine whether port open or closed.
if ser.isOpen():
    print('Open: ' + ser.portstr)
else:
    sys.exit()

# Put robot in Safe Mode.       
ser.write(bytearray([128, 131]))
time.sleep(1)  # need to pause after send mode

# Velocity for robot movements.
V = 50
velocity = int_as_2bytes(V)
#TIME_ROBOT_WIDTH = ROBOT_DIAMETER / V / V_ERR_COEF
TIME_ROBOT_WIDTH = 4

while True:
    if(client.recv_data(server) == "start"):
        break

# Command to stop the robot.
stop = [137, 0, 0, 0, 0]
cmd = [137] + velocity + ADJUSTED_STRAIGHT
ser.write(bytearray(cmd))
stTime = time.time() # start time
# get the needed time to sleep to get a rotation of 90 degrees
t = sleep_time_for90degrees(V, 90)
i = 0
dist = [0,0]
ti= [0,0]
dist_list = [0,0]

# get the lentgh and width travled by a robot and the time needed for each distance
# save data in "dist[]" for distances and "ti[]" for times (index 0: for lenght, index 1: for width)
while (i < 2): # using 2 because we have just 2 real boundry for each robot
    #query data for bumpers
    ser.write(bytearray([149, 1, 7]))
    a = ser.read(1)
    #if any of the bumpers pressed, turn for 90 degrees
    if (a == b'\x03') or (a == b'\x02') or (a == b'\x01'):
        #stop robot
        ser.write(bytearray(stop))
        # if a bumper is pressed save end time
        endTime = time.time()
        # get the time from the start of the drive until the bumper is pressed 
        ti[i] = endTime - stTime
        # calculate distance (velocity * time)
        dist[i] = V * ti[i] * V_ERR_COEF
        # back up the robot a little bit to release the bumper (by Chico)
        cmd = [137, 255, 206, 128, 0]
        ser.write(bytearray(cmd))
        time.sleep(0.2)                           
        # turn robot for 90 degrees
        cmd = [137] + velocity + [0, 1]
        ser.write(bytearray(cmd))
        # see the comment about "t" above
        time.sleep(t)
        # stop before sending data
        ser.write(bytearray(stop))
        # call function to send distance and angle data (by Chico)
        sendDistance(server, "{0:6.1f}".format(dist[i]))
        print (dist[i])
        # drive straight after rotating for 90 degree
        cmd = [137] + velocity + ADJUSTED_STRAIGHT
        ser.write(bytearray(cmd))
        # initialise starting time 
        stTime = time.time()
        # icriment lists index
        i += 1

ser.write(bytearray(stop))
done = False
cmd = [137] + velocity + ADJUSTED_STRAIGHT
ser.write(bytearray(cmd))
j = 0
# Robot will turn before acoss any discovered area.
while (done == False):
    if (ti[j] - TIME_ROBOT_WIDTH < 0):
        done = True
        break
    if (j == 0):
        time.sleep(ti[j])
    else :
        time.sleep(ti[j] - TIME_ROBOT_WIDTH)
    #stop robot
    ser.write(bytearray(stop))
    # if a bumper is pressed save end time
    endTime = time.time()
    # get the time from the start of the drive until the bumper is pressed 
    ti.append(endTime - stTime)
    # calculate distance (velocity * time)
    dist.append(V * ti[i] * V_ERR_COEF)
    # turn robot for 90 degrees
    cmd = [137] + velocity + [0, 1]
    ser.write(bytearray(cmd))
    # see the comment about "t" above
    time.sleep(t)
    # stop before sending data
    ser.write(bytearray(stop))
    # call function to send distance and angle data (by Chico)
    sendDistance(server, "{0:6.1f".format(dist[i]))
    print (dist[i])
    # drive straight after rotating for 90 degree
    cmd = [137] + velocity + ADJUSTED_STRAIGHT
    ser.write(bytearray(cmd))
    # initialise starting time 
    stTime = time.time()
    # icriment lists index
    i += 1
    j += 1
    if (ti[j] <= TIME_ROBOT_WIDTH):
        done = True

ser.write(bytearray(stop))

print ("before finish")
# call function to send "finish" signal to indicate mapping is done (by Chico)
sendDistance(server, "finish")

print ("after finish")

# Disconnect from port so another program (e.g., RealTerm)
# can connect.
ser.close()
# disconnect from server
client.disconnect(server)
