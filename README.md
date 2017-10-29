# Room-Mapping-Project
Advanced Robotics Final Project  (Spring 2016)

## Description
This project is to use multiple iRobots to detect the boundary of a room.
The iRobots will travel forward and detect the wall by their bumper. 
When a wall detected, the iRobots will turn 90 degrees to the left and drive forward to detect another wall.

## Requirement
Each iRobot should equip Pi with Wi-Fi. 
A desktop program will be collecting data (travel distance) from each iRobots.
Use data to analyze the boundary of the room to create a map.

## Mapping Procedure
Two iRobot will be facing different direction (facing east and west of the room)
If the iRobot's bumper hit the wall, the iRobot will stop and turn left.

![TravelDiagram](https://github.com/CHico-Lee/Room-Mapping-Project/blob/master/iRobot%20Travel%20Diagram.jpg)

Each iRobot has their own territory. The iRobot will not travel across other territories and discovered area.
The iRobot will stop when all the area is discovered inside the boundary.

State 1: Stop and turn when detecting wall by bumper

State 2: Stop and turn before the iRobot enter the discovered area.

State 3: Stop when travel distance is less than robot diameter.

Issue 1:
Physical imperfect on each iRobot: Drive speed and straightness
Solution: Measure and calculate error coefficient on each robot.

Issue 2:
No script command on Create2:
Solution: Use time to sleep to control the angle of rotation and distance of travel.

## Tools used

iRobot Create2, Raspberry Pi 2

## Project Members

Chi Ho Lee, Ilyass Hmamou, Bilal Elezi, Gregory Bushnell
