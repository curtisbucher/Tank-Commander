#!/usr/bin/python
# -*- coding: utf-8 -*-
""" A Tank Game to teach coding those unfamiliar with it"""

import pygame
import sys
from pygame.locals import *
from PIL import Image
import random
import time

pygame.init()
pygame.font.init()

# Set the width and height of the screen
infoObject = pygame.display.Info()
size = (infoObject.current_w, infoObject.current_h - 30)
clock = pygame.time.Clock()
time_delay = 0.001
# Setting rotation variables
NORTH = 0
SOUTH = 180
EAST = 90
WEST = 270

CLOCKWISE = -90
COUNTERCLOCKWISE = 90

class tank:
    """A sprite object that can move around the map when using the tank's functions under tank.help()"""
    def __init__(self, coords, rotation):
        """Creates the tank object with hardcoded variables"""
        self.origional_image = pygame.image.load('KV-2_Tank.png')
        self.image = self.origional_image

        self.rotation_speed = 1
        self.rotation = rotation
        self.desired_rotation = 0

        self.movement_speed = 1
        self.coords = coords
        self.desired_coords = self.coords

        self.desired_delay = 0
        self.delay_count = 0
        
        self.bullet_list = []
        self.bullet_fired = False

    def help(self,keyword=""):
        """ Provides an interactive, helpful list of commands for the tank actions"""
        keywords = {"move()" : """Syntax: tank.move(distance)\nMoves the tank, [distance] forward. Type a negetive number to go backward.""",
            "turnLeft()" : """Syntax: tank.turnLeft()\nRotates the tank 90 degrees clockwise.""",
            "turnRight()" : """Syntax: tank.turnRight()\nRotates the tank 90 degrees clockwise.""",
            "fire()" : """Syntax: tank.fire()\nFires a bullet from the gun of the tank. Bullets kill enemy tanks.""",
            "delay()" : """Syntax: tank.delay(milliseconds)\nStops the tank for [milliseconds] milliseconds. There are 1000 milliseconds to a second."""
            }
        if "()" not in keyword and keyword != "":
            keyword += "()"
            
        if(keyword == ""):
            print("List of Tank Commands\n"
                + "---------------------\n"
                + "tank.move()\n"
                + "tank.turnLeft()\n"
                + "tank.turnRight()\n"
                + "tank.fire()\n"
                + "tank.delay()\n\n"

                + "For help with a specific function,\n"
                + "type tank.help('function').\n"
                + "(function is in quotes)\n")
            
        elif keyword not in keywords and keyword != "":
            print("Command not recognized:\n" + tank.help())
            
        else:
            print(keywords[keyword])
                
    
    def turnRight(self):
        """Rotate the tank 90 degrees clockwise."""
        self.desired_rotation = CLOCKWISE
    def turnLeft(self):
        """Rotate the tank 90 degrees counter clockwise."""
        self.desired_rotation = COUNTERCLOCKWISE
        
    def _rotate_step(self):
        """ This program will rotate 1 degree everytime called, untill it has
            reached the desired rotation
        """
        if self.desired_rotation < 0:
            self.rotation += self.rotation_speed
            self.desired_rotation += self.rotation_speed

        elif self.desired_rotation > 0:
            self.rotation -= self.rotation_speed
            self.desired_rotation -= self.rotation_speed
        else:
            return False
        ## Converting large rotations to the corresponding small ones
        self.rotation = self.rotation % 360
        return True
    
    def move(self, distance):
        """Move the tank, [distance] forward. Type a negetive number to go
        backward
        """
        x,y = self.coords
        if self.rotation == NORTH:
            self.desired_coords = (x, y - distance)
        elif self.rotation == SOUTH:
            self.desired_coords = (x, y + distance)
        elif self.rotation == EAST:
            self.desired_coords = (x + distance, y)
        elif self.rotation == WEST:
            self.desired_coords = (x - distance, y)
                    
    def _move_step(self):
        """ This program will move 10 pixels everytime called, untill it has
        reached the desired position.
        """
        (x, y) = self.coords
        (ax,ay) = self.desired_coords
        
        if ax < x:
            x -= self.movement_speed
        elif ax > x:
            x += self.movement_speed
        
        elif ay < y:
            y -= self.movement_speed
        elif ay > y:
            y += self.movement_speed
        else:
            return False
        
        self.coords = (x, y)
        self.desired_coords = (ax, ay)
        return True
    
    def fire(self):
        """ Fires a bullet from the tank"""
        x,y = self.coords
        
        if self.rotation == NORTH:
            (x,y) = (x + tank.image.get_width()/2,y)
        elif self.rotation == SOUTH:
            (x,y) = (x + tank.image.get_width()/2,y + tank.image.get_height())
        elif self.rotation == EAST:
            (x,y) = (x + tank.image.get_width(),y + tank.image.get_height()/2)
        elif self.rotation == WEST:
            (x,y) = (x ,y + tank.image.get_height()/2)

        self.bullet_list.append(bullet((x,y), self.rotation))
        self.bullet_fired = True

    def _update_bullets(self):
        for bullet in self.bullet_list:
            bullet._update()
            
    def delay(self, milliseconds):
        """Stops the tank for [milliseconds] milliseconds. There are 1000 milliseconds to a second."""
        self.desired_delay = milliseconds/(0.01/time_delay)

    def _delay_step(self):
        """Delays the tank's movement"""
        if self.delay_count < self.desired_delay:
            self.delay_count += 1
            return True
        self.delay_count = 0
        self.desired_delay = 0
        return False
    def _draw(self):
        """Draw the image of the tank on the playing surface"""
        
        self.image = _rot_center(self.origional_image, self.rotation)
        screen.blit(self.image, self.coords)
    def _update(self):
        """Rotate the tank, and move it if necessary. Then draw it"""

        rotated = self._rotate_step()
        moved = self._move_step()
        delayed  = self._delay_step()
        self._update_bullets()

        self._draw()
        ## This will move on to the next command if the tank is stopped moving
        ## and delaying or if it just fired a bullet.
        if (not rotated and not moved and not delayed):## or self.bullet_fired:
            ##print("next command")
            return True
        return False
        
class bullet:
    def __init__(self, coordinates, rotation):
        """Creates the tank object with the needed hardcoded variables."""
        self.origional_image = pygame.transform.scale(pygame.image.load('bullet.png'),(20, 10))
        self.image = self.origional_image

        self.rotation = rotation
        self.coords = coordinates
        self.movement_speed = 5

    def _move_step(self):
        """ This program will move movement_speed pixels everytime called, untill it has
        gone off the screen.
        """
        (x, y) = self.coords        
        if self.rotation == NORTH:
            y -= self.movement_speed
        elif self.rotation == SOUTH:
            y += self.movement_speed
        elif self.rotation == EAST:
            x += self.movement_speed
        elif self.rotation == WEST:
            x -= self.movement_speed 

        else:
            return False
        self.coords = (x, y)
        return True

    def _draw(self):
        """ Draws the image of the tank on the playing surface"""
        self.image = _rot_center(self.origional_image, self.rotation + 90)
        screen.blit(self.image, self.coords)
        
    def _update(self):
        """Is called in the program loop to move and draw the bullet."""
        self._move_step()
        self._draw()

def _rot_center(pygame_image, degrees):
    """ Rotate an image while keeping its center and size, by converting to pil, rotating and back"""

    image_string = pygame.image.tostring(pygame_image, 'RGBA', False)
    PIL_image = Image.frombytes('RGBA', pygame_image.get_size(),image_string)
    PIL_image = PIL_image.rotate(-degrees)
    image_string = PIL_image.tobytes()
    pygame_image = pygame.image.fromstring(image_string,PIL_image.size, 'RGBA')
    return pygame_image

def enemy_move(level, time, enemy_tank_object, player_tank_object, bullet_list,game_map):
    """ This function is called after every move the player, tank makes when the
        game is being compiled. It takes the game state, as well as the level,
        the player tank object (in order to get coordinates and rotation)
        and the enemy tank object (in order to get its own variables)as imput,
        and outputs the move that the tank will make. Before this is
        implimented, I must get the timing right with moving the player's tank,
        and the enemies tank so that the tank does not attempt a new move
        before it finished the old one.

        Should the Enemy tank move one space at a time for timing purposes?
    """
    player_x, player_y = player_tank_object.coords
    enemy_x, enemy_y = enemy_tank_object.coords
    
    ## 1: Does nothing
    if(level == 1):
        return("")
    ## 2: Rotates slowely, and shoots if it can hit you
    if(level == 2):
        if(can_hit_player(enemy_tank_object, player_tank_object)):
            return("enemy.fire()")
        
    ## 3: Turns 90 degrees every second, otherwise drives. Shoots if it can hit you
    if(level == 3):
        if(time% 1000 == 0):
            return("enemy.turn(90)")
        elif(can_hit_player(enemy_tank_object, player_tank_object)):
            return("enemy.fire()")
        elif(time%100 == 0):
            return("enemy.move(100)")
        else:
            return("")

def can_hit_player(enemy_tank_object, time, player_tank_object):
    """ This function takes in the enemy tank object and the player tank object
        as input, and uses their coordinates (and possibly there rotation and
        velocity) to see if a bullet can hit them
    """     
    player_x, player_y = player_tank_object.coords
    enemy_x, enemy_y = enemy_tank_object.coords
    ## The radius of the tank's target area in which it will shoot
    bounds = 10
    ## The lower left  coordinate in the target bounding box
    lower_bounds = (enemy_x - bounds, enemy_y - bounds)
    ## The upper right coordinate in the target bounding box
    upper_bounds = (enemy_x + bounds, enemy_y + bounds)

    ## Checking if the player's tank is within the bounding box
    if(lower_bounds[0] < player_x < upper_bounds[0]):
           if(upper_bounds[1] < player_y < lower_bound[1]):
               return(True)
    return(False)

def quit_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape" :
                return True
    return False

def get_program(nest):
    """ This function gets the tank program from the user"""

    user_in = True
    done = False
    program = []

    if nest == 0:
        print("For general help with the game, type 'help' and press enter.\n"
            + "For a list of tank commands and what they do, type tank.help()")

    ## Gets tank commands from user
    while user_in and not done:        
        done = quit_input()
        user_in = input('>>> ' + nest * '  ')
        if user_in == "help":
            print(   "The purpose of this game is to teach those unfamiliar with coding how to code.\n"
                   + "The player will play several levels, where the goal of the level is to kill the\n"
                   + "enemy tank, by destroying it with a bullet. The player can manuever their tank\n"
                   + "by writing a code for it to follow after the '>>> '. The program is coded in \n"
                   + "the python programming language, and all normal python actions are supported by\n" 
                   + "the console in addition to several new functions that control the tank.\n"
                   + "Type 'tank.help() for a list of the tank's commands. Break a leg!")
            user_in = "\n"
        if "tank.help(" in user_in:
            exec(user_in)
            user_in = "\n"
        
        elif 'tank.' in user_in:
            user_in = 'tank_program.append("' + user_in + '")'

        # If a conditional, it runs 'get_program' to get the conditional
        # the code under the conditional,and appends it as one string
        # separated by '\n' to the program list. It counts the number of
        # 'nests' to print the correct number of tabs.

        if ':' in user_in:
            nested_program = get_program(nest + 1)
            for command in nested_program:
                user_in += '\n' + (nest + 1) * '  ' + command
        program.append(user_in)
    return program




def start(program):
    """ This function is called, given the input data, collected from the user
        and processed by 'get_program'. Given this list of commands, the computer
        moves the tank on the screen.
    """

    # Calculating the moves of the Tank. Compiling
    done = False
    program_counter = 0
    
    while True:
        if program_counter < len(program) - 1:
            exec(program[program_counter])
            program_counter += 1
        else:
            break

    # Executing the moves of the tank. Interpreting
    done = False
    program_counter = 0
    next_command = False
    
    while not done:
        if next_command:
            if program_counter < len(tank_program):
                print(tank_program[program_counter])
                exec(tank_program[program_counter])
                next_command = False
                program_counter+=1
            else:
                break
            
        done = quit_input()
        
        screen.fill((255, 255, 255))
        next_enemy_command = enemy._update()
        next_command = tank._update()
        
        pygame.display.flip()
        time.sleep(time_delay)


    # Waiting untill game is done to stop animating bullets and such
    while not done:
        done = quit_input()
        screen.fill((255, 255, 255))
        tank._update()
        pygame.display.flip()
        time.sleep(0.0005) 

enemy = tank((500,10),WEST)
tank = tank((10,10),EAST)
program = get_program(0)
tank_program = []
program_counter = 0

screen = pygame.display.set_mode(size)  # , FULLSCREEN)
start(program)
# Close the window and quit.
pygame.quit()
