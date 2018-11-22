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

# Set the width and height of the screen

infoObject = pygame.display.Info()
size = (infoObject.current_w, infoObject.current_h - 30)

# Used to manage how fast the screen updates

clock = pygame.time.Clock()
class tank:

    def __init__(self):
        self.origional_image = pygame.image.load('KV-2_Tank.png')
        self.image = self.origional_image
        self.rotation = 0
        self.coords = (0, 0)
        self.move_count = 0  # # Counts the number of tims a function is iterated

    def rotate(self, degrees):
        """ This program will rotate 1 degree everytime called, untill it has
            reached the desired rotation, then it will advance the program counter
        """

        global program_counter

        if degrees > 0 and self.move_count < degrees:
            self.rotation += 1
            self.move_count += 1
        elif degrees < 0 and self.move_count > degrees:
            self.rotation -= 1
            self.move_count -= 1
        else:
            self.move_count = 0
            program_counter += 1

            # # Converting large negetive rotations to the corresponding small positive ones

            if abs(self.rotation) > 180:
                if self.rotation < 0:
                    self.rotation = 360 + self.rotation
                elif self.rotation > 0:
                    self.rotation = -360 + self.rotation

    def move(self, distance):
        """ This program will move 10 pixels everytime called, untill it has
            reached the desired position, then it will advance the program counter
        """

        global program_counter

        self.move_count += 1
        (x, y) = self.coords

        if distance < 0:
            factor = -1
        elif distance == 0:
            factor = 0
        else:
            factor = 1

        if self.move_count < abs(distance):
            y += factor * -(5 - abs(self.rotation) / 18)
            if abs(self.rotation) <= 90:
                x -= factor * self.rotation / 18
            elif self.rotation > 0:
                x -= factor * (180 - self.rotation) / 18
            else:
                x -= factor * -(180 - abs(self.rotation)) / 18
        else:

            program_counter += 1
            self.move_count = 0

        self.coords = (x, y)

    def fire(self):
        """ Fires a bullet from the tank"""
        
        global program_counter
        global bullet_list
        x,y = self.coords
        bullet_list.append(bullet((x, y- 1/2 * self.image.get_height()), self.rotation))
        program_counter += 1

    def delay(self, milliseconds):
        """Delays the tank's movement"""
        
        global program_counter
        time.sleep(milliseconds * 0.001)
        program_counter += 1

    def draw(self):
        """ Draws the image of the tank on the playing surface"""

        self.image = _rot_center(self.origional_image, self.rotation)
        screen.blit(self.image, self.coords)


class bullet:

    def __init__(self, coordinates, rotation):
        self.origional_image = \
            pygame.transform.scale(pygame.image.load('bullet.png'),
                                   (20, 10))
        self.image = self.origional_image
        self.rotation = rotation
        self.coords = coordinates
        self.move_count = 0  ## Counts the number of tims a function is iterated

    def move(self, distance):
        """ This program will move 10 pixels everytime called, untill it has
        reached the desired position, then it will advance the program counter
        """

        self.move_count += 1
        (x, y) = self.coords

        if distance < 0:
            factor = -1
        elif distance == 0:
            factor = 0
        else:
            factor = 1

        if self.move_count < abs(distance):
            y += factor * -(5 - abs(self.rotation) / 18)
            if abs(self.rotation) <= 90:
                x -= factor * self.rotation / 18
            elif self.rotation > 0:
                x -= factor * (180 - self.rotation) / 18
            else:
                x -= factor * -(180 - abs(self.rotation)) / 18
        else:

            self.move_count = 0

        self.coords = (x, y)

    def draw(self):
        """ Draws the image of the tank on the playing surface"""

        self.image = _rot_center(self.origional_image, self.rotation
                                 + 90)
        screen.blit(self.image, self.coords)


def _rot_center(pygame_image, degrees):
    """ Rotate an image while keeping its center and size, by converting to pil, rotating and back"""

    image_string = pygame.image.tostring(pygame_image, 'RGBA', False)
    PIL_image = Image.frombytes('RGBA', pygame_image.get_size(),
                                image_string)
    PIL_image = PIL_image.rotate(degrees)
    image_string = PIL_image.tobytes()
    pygame_image = pygame.image.fromstring(image_string,
            PIL_image.size, 'RGBA')
    return pygame_image


def get_program(nest):
    """ This function gets the tank program from the user"""

    user_in = True
    program = []

    # # Gets program from user

    while user_in:
        user_in = input('>>> ' + nest * '  ')
        if 'tank.' in user_in:
            user_in = 'tank_program.append("' + user_in + '")'

        # # If a conditional, it runs 'get_program' to get the conditional
        # # the code under the conditional,and appends it as one string
        # # separated by '\n' to the program list. It counts the number of
        # # 'nests' to print the correct number of tabs.

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

    # # Calculating the moves of the Tank. Compiling

    global program_counter
    while True:
        if program_counter < len(program) - 1:
            exec(program[program_counter])
            program_counter += 1
        else:
            break

    # # Executing the moves of the tank. Interpreting

    program_counter = 0
    while True:
        if program_counter < len(tank_program):
            print(tank_program[program_counter])
            exec(tank_program[program_counter])
        screen.fill((255, 255, 255))
        for bullet in bullet_list:
            bullet.move(10)
            bullet.draw()
            
        tank.draw()
        pygame.display.flip()
        time.sleep(0.001)
        clock.tick(60)


program = get_program(0)
tank_program = []
program_counter = 0
tank = tank()
bullet_list = []

screen = pygame.display.set_mode(size)  # , FULLSCREEN)
start(program)
# Close the window and quit.
pygame.quit()
