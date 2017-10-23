# Author: Bilal Elezi

# Date: 3/24/2016

# Class: Adv Robotics Final Project.

# Code to Analyze path and map creation

import pygame
import sys
import serial
import math
import server

from socket import *

#scaling down 10 times.
def mm_to_pixels(mm):
    return mm//10

#convert angle to radians.
def convert_to_radians(x):
    return math.radians(x)
    
#computing the new coordinates.
def compute_new_coordinates(x, y, distance, angle):
    angle = convert_to_radians(angle)

    x += (math.cos(angle) * distance)
    #subtract y because screen is the fourth part of a cartigean plane.
    y -= (math.sin(angle) * distance)
    
    return (round(x), round(y))

#Quit event
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit 
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
                
#draw robot name on the circle.
def draw_robot_name(robot):
    font = pygame.font.Font(None, 18)  # default font
    
    # robot label inside circle
    label_text = font.render(("R"+ str(robot+1)), True, WHITE)
    label_size = label_text.get_rect()
    
    (x, y) = init_pos[robot]
    
    # Compute position to center label
    label_pos = ( x - (label_size.width // 2), y - (label_size.height // 2))
        
    screen.blit(label_text, label_pos)

#Draw the circles on the screen
def draw_on_screen(data, x , y):
    for distance in data:
        float_dist = float(distance)
        coord = compute_new_coordinates(x, y, float_dist, init_angle[0])     
        pygame.draw.circle(screen, BLACK, coord, radius, 0)
        pygame.draw.line(screen, BLACK, (x, y), coord, 2)
        (x, y) = coord
        print ("x: ",x, "y: ", y)
        init_angle[0] += 90

        pygame.display.update()
        pygame.display.flip()

        
def receive_data():
    return server.client_data  
        
        
    
pygame.init()  # initialize all imported Pygame modules

#Initialize dimentions of screen, radius, compute center on dimentions and colors
width = 900
height = 900
radius = 18
screen_size = (width, height)
BLACK = (0, 0, 0)  # RGB color black
WHITE = (255, 255, 255) #RGB color white
center_x = width // 2
center_y = height // 2

#Store the initial position for each robot.
init_pos = [((radius),(center_y - radius)),
            ((width - radius),(center_y + radius))
            ]

init_angle = [ 0, 180 ]



# Set up Pygame screen
screen = pygame.display.set_mode(screen_size)
screen.fill(WHITE)
pygame.display.update()
pygame.display.flip()

pygame.display.set_caption('Default room space!')
pygame.display.update()
pygame.display.flip()

#Initially draw the two robots on the center of the screen.
for i in range (0, 2):
    pygame.draw.circle(screen, BLACK, init_pos[i], radius, 0)
    draw_robot_name(i)

    #update screen
    pygame.display.update()
    #pygame.display.flip()


data = receive_data()
for x in range (0, 2)
    data[x] 

(x , y) = init_pos[0]
print ("Initially  x: ",x, "y: ", y)

draw_on_screen(data, x, y)

