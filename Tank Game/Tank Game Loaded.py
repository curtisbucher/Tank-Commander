#!/usr/bin/python
# -*- coding: utf-8 -*-
""" A Tank Game to teach coding those unfamiliar with it"""

import pygame
from pygame.locals import *
from PIL import Image
import time
print("Loading...")


# Setting rotation variables
NORTH = 0
SOUTH = 180
EAST = 90
WEST = 270

CLOCKWISE = -90
COUNTERCLOCKWISE = 90

class tank:
    """A sprite object that can move around the map when using the tank's functions under player.help()"""
    tank_list = []
    def __init__(self, coords, rotation, sprite):
        """Creates the tank object with hardcoded variables"""
        self.origional_image = pygame.transform.rotate(pygame.image.load(sprite),180)
        x,y = self.origional_image.get_size()
        self.size = (x//2,y//2)

        self.explosion_animation = pygame.image.load('explosion_animation.png')
        self.explosion_frame = 0

        self.explosion_sound = pygame.mixer.Sound('Explosion_Shrapnel.ogg')
        self.explosion_sound.set_volume(0.35)

        self.origional_image = pygame.transform.scale(self.origional_image, self.size)
        self.image = self.origional_image
        
        self.rotation_speed = 1.5 ## Must be divisible by the rotation in degrees
        self.rotation = rotation
        self.desired_rotation = 0

        self.movement_speed = 3
        self.coords = coords
        self.desired_coords = self.coords

        self.desired_delay = 0
        self.delay_count = 0
        
        self.bullet_list = []
        self.bullet_fired = False
        self.fire_sound = pygame.mixer.Sound('Bomb.ogg')
        self.fire_sound.set_volume(0.25)
        
        self.alive = True
        self.explode = False
        self.next_move = False
        self.program_counter = 0
    
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
        ## Making sure the number is divisible by the speed
        distance = distance// self.movement_speed * self.movement_speed
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

    def can_hit_enemy(self):
        """ This function takes in the self tank object and the target tank object
        as input, and uses their coordinates (and possibly there rotation and
        velocity) to see if a bullet can hit them
        """     
        target_x, target_y = enemy.coords
        self_x, self_y = self.coords
        ## The radius of the tank's target area in which it will shoot
        bounds = 50
        ## The lower left  coordinate in the target bounding box
        lower_bounds = (self_x - bounds, self_y + bounds)
        ## The upper right coordinate in the target bounding box
        upper_bounds = (self_x + bounds, self_y - bounds)

        ## Checking if the target's tank is within the bounding box, and returning true if so
        if self_tank_object.rotation == EAST or self_tank_object.rotation == WEST:
            if(upper_bounds[1] < target_y < lower_bounds[1]):
                return True
        if self_tank_object.rotation == NORTH or self_tank_object.rotation == SOUTH:
            if(lower_bounds[0] < target_x < upper_bounds[0]):
                return True
        
        return(False)
    def fire(self):
        """ Fires a bullet from the tank"""
        x,y = self.coords
        self.fire_sound.play()
        
        if self.rotation == NORTH:
            (x,y) = (x + self.image.get_width()/2,y)
        elif self.rotation == SOUTH:
            (x,y) = (x + self.image.get_width()/2,y + self.image.get_height())
        elif self.rotation == EAST:
            (x,y) = (x + self.image.get_width(),y + self.image.get_height()/2)
        elif self.rotation == WEST:
            (x,y) = (x ,y + self.image.get_height()/2)

        self.bullet_list.append(bullet((x,y), self.rotation, self))
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
        
    def _animate_explosion(self, frame):
        if self.explosion_frame == 0:
                self.explosion_sound.play()
        sprite_size = (64,64) ## The size of the explosion images on the sprite sheet. width by height
        sheet_size = (5,5) ## The number of image frames in the sprite sheet, width by height

        ## Cutting the spritesheet to get the right image, and blows it up to the right size of the tank
        cropped = pygame.Surface(sprite_size, pygame.SRCALPHA, 32)
        cropped = cropped.convert_alpha()
        cropped.blit(self.explosion_animation, (0, 0), (sprite_size[0]*(frame//sheet_size[0]), sprite_size[1]*(frame%sheet_size[1]), sprite_size[0], sprite_size[1]))
        cropped = pygame.transform.scale(cropped, self.size)
        return(cropped)
        
    def _update(self):
        """Rotate the tank, and move it if necessary. Then draw it"""
        ## Will keep iterating untill it is done moving
        if not self.explode:
            rotated = self._rotate_step()
            moved = self._move_step()
            delayed  = self._delay_step()
            
            self._update_bullets()
            self._draw()

            if not (rotated or delayed or moved):
                self.next_move = True
                return True
            else:
                self.next_move = False
                return False
        
        else:
            self.origional_image = self._animate_explosion(self.explosion_frame)
            self.image = self.origional_image
            time.sleep(0.01)
            if self.explosion_frame < 25:
                self.explosion_frame +=1
            else:
                self.alive = False
 
            self._draw()
            self._update_bullets()
        
class bullet:
    def __init__(self, coordinates, rotation, owner):
        """Creates the tank object with the needed hardcoded variables."""
        self.origional_image = pygame.transform.scale(pygame.image.load('bullet.png'),(20, 10))
        self.image = self.origional_image
        self.owner = owner

        self.rotation = rotation
        self.coords = coordinates
        self.movement_speed = 10

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
    
    def _check_collision(self,enemy_tank_object):
        """ This function takes in the enemy tank object and the player tank object
        as input, and uses their coordinates (and possibly there rotation and
        velocity) to see if a bullet can hit them
        """     
        x, y = self.coords

        enemy_x, enemy_y = enemy_tank_object.coords
        enemy_x += enemy_tank_object.size[0]/2
        enemy_y += enemy_tank_object.size[1]/2
        ## The radius of the tank's target area in which it will shoot
        x_bounds = enemy_tank_object.size[0]/2
        y_bounds = enemy_tank_object.size[1]/2
        ## The lower left  coordinate in the target bounding box
        lower_bounds = (enemy_x - x_bounds, enemy_y + y_bounds)
        ## The upper right coordinate in the target bounding box
        upper_bounds = (enemy_x + x_bounds, enemy_y - y_bounds)

        ## Checking if the player's tank is within the bounding box
        if(lower_bounds[0] < x < upper_bounds[0]):
            if(upper_bounds[1] < y < lower_bounds[1]):
                return(True)
        return(False)

    def _draw(self):
        """ Draws the image of the tank on the playing surface"""
        self.image = _rot_center(self.origional_image, self.rotation + 90)
        screen.blit(self.image, self.coords)
        
    def _update(self):
        """Is called in the program loop to move and draw the bullet."""
        self._move_step()
        self._draw()
        for target in tank.tank_list:
            if self._check_collision(target) and target != self.owner:
                target.explode = True
                self.owner.bullet_list.remove(self)
        ## Destroying the bullet if it goes off screen
        if self.coords[0] < 0 or self.coords[0] > size[0]:
            self.owner.bullet_list.remove(self)
        elif self.coords[1] < 0 or self.coords[1] > size[1]:
            self.owner.bullet_list.remove(self)

def _rot_center(pygame_image, degrees):
    """ Rotate an image while keeping its center and size, by converting to pil, rotating and back"""

    image_string = pygame.image.tostring(pygame_image, 'RGBA', False)
    PIL_image = Image.frombytes('RGBA', pygame_image.get_size(),image_string)
    PIL_image = PIL_image.rotate(-degrees)
    image_string = PIL_image.tobytes()
    pygame_image = pygame.image.fromstring(image_string,PIL_image.size, 'RGBA')
    return pygame_image


def can_hit_target(self_tank_object, target_tank_object):
    """ This function takes in the self tank object and the target tank object
        as input, and uses their coordinates (and possibly there rotation and
        velocity) to see if a bullet can hit them
    """     
    target_x, target_y = target_tank_object.coords
    self_x, self_y = self_tank_object.coords
    ## The radius of the tank's target area in which it will shoot
    bounds = 50
    ## The lower left  coordinate in the target bounding box
    lower_bounds = (self_x - bounds, self_y + bounds)
    ## The upper right coordinate in the target bounding box
    upper_bounds = (self_x + bounds, self_y - bounds)

    ## Checking if the target's tank is within the bounding box, and returning true if so
    if self_tank_object.rotation == EAST or self_tank_object.rotation == WEST:
        if(upper_bounds[1] < target_y < lower_bounds[1]):
            return(True)
    if self_tank_object.rotation == NORTH or self_tank_object.rotation == SOUTH:
        if(lower_bounds[0] < target_x < upper_bounds[0]):
            return(True)
    
    return(False)

def _button_press(button = "escape"):
    for event in pygame.event.get():
        if event.type == pygame.QUIT and button == "escape":
            return True
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == button:
                return True
    return False

def display_title_screen():
    global screen
    title_screen = pygame.transform.scale(pygame.image.load('title_screen2.jpg'),size)

    _done = False

    background_music.play()
    screen = pygame.display.set_mode(size , FULLSCREEN)
    
    while not _done:
        _done = _button_press("return")
        screen.blit(title_screen,(0,0))
        pygame.display.flip()
        clock.tick(60)
    background_music.stop()

def _update(repeat = False):
    global _quit
    backgroundImg = pygame.transform.scale(pygame.image.load('background2.png'),size)
    
    _quit = False
    
    _done = False

    while not _quit and ((not _done) or repeat) and player.alive:
        _quit = _button_press()
        screen.blit(backgroundImg, (0,0))
        
        _done = player._update()

        pygame.display.flip()
        time.sleep(time_delay)
    


# ----- Game Start ----------------------------------
pygame.init()


# Set the width and height of the screen
infoObject = pygame.display.Info()
size = (infoObject.current_w, infoObject.current_h - 30)
clock = pygame.time.Clock()
time_delay = 0.001
screen = pygame.display.set_mode(size , FULLSCREEN)

player = tank((100,240),EAST, 'tank_sprite.png')
tank.tank_list = [player]
done = False

while not done:
    done = _button_press()
    _update()

tank.tank_list = [player]

pygame.quit()
