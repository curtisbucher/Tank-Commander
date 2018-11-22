""" The goal of this game is to destroy the enemy tank on the screen, by
    programming your own tank to shoot the enemy. The program the user
    submits is written in python, and the purpose of this game is to help
    teach general programming properties such as functions, conditionals
    and data types to the inexepirianced user in a fun, easy to learn way"""

## Importing the necessary libraries for drawing the game on the screen
import pygame
from pygame.locals import *
from PIL import Image

## Importing libraries to run the game on Windows
from sys import exc_info, platform
from os import system
import traceback

## Importing Libraries for timing and random generation
import random
import time

# Set the width and height of the screen
pygame.init()
infoObject = pygame.display.Info()
size = (infoObject.current_w, infoObject.current_h - 30)
clock = pygame.time.Clock()
time_delay = 0.001

# Setting global variables for object rotation (in degrees)
NORTH = 0
SOUTH = 180
EAST = 90
WEST = 270

# These rotations are reletive to the the tanks current position
CLOCKWISE = -90
COUNTERCLOCKWISE = 90

# This is the tank class, that is used to draw, move, command, and update both the
# player's tank and the enemy tank, which are both 'tank' objects
class tank:
    """A sprite object that can move around the map when using the tank's
    functions listed under player.help(). The tank's position, rotation, image,
    and state are all updated using the _update function"""
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

    def info(self,keyword=""):
        """ Provides an interactive, helpful list of commands for the tank actions"""
        keywords = {"move()" : """Syntax: player.move(distance)\nMoves the tank, [distance] forward. Type a negetive number to go backward.""",
            "turnLeft()" : """Syntax: player.turnLeft()\nRotates the tank 90 degrees clockwise.""",
            "turnRight()" : """Syntax: player.turnRight()\nRotates the tank 90 degrees clockwise.""",
            "fire()" : """Syntax: player.fire()\nFires a bullet from the gun of the player. Bullets kill enemy tanks.""",
            "delay()" : """Syntax: player.delay(milliseconds)\nStops the tank for [milliseconds] milliseconds. There are 1000 milliseconds to a second."""
            }
        if "()" not in keyword and keyword != "":
            keyword += "()"
            
        if(keyword == ""):
            print("List of Tank Commands\n"
                "---------------------\n"
                "player.move()\n"
                "player.turnLeft()\n"
                "player.turnRight()\n"
                "player.fire()\n"
                "player.delay()\n\n"

                "For help with a specific function,\n"
                "type player.info('function').\n"
                "(function is in quotes)\n")
            
        elif keyword not in keywords and keyword != "":
            print("Command not recognized:\n" + player.help())
            
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
        """ This program will move [movement_speed] pixels everytime called, untill it has
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
        """ Returns True if the player's bullet would hit the enemy, otherwise it returns false"""
        if can_hit_target(self, enemy):
            return True
        else:
            return False
    
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
        """ Goes through all of the tank's bullets on the screen and 1)moves
        them forward and 2) destroys anything they touch
        """
        for bullet in self.bullet_list:
            bullet._update()
            
    def delay(self, milliseconds):
        """Stops the tank for [milliseconds] milliseconds. There are 1000 milliseconds to a second."""
        self.desired_delay = milliseconds/(0.01/time_delay)

    def _delay_step(self):
        """Delays the tank's movement 1 clock cycle"""
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
        """Animates an explosion frame by frame, updating the frame everytime it
        is called.
        """
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
        """Rotate and move the tank, if it has not reached it's
        [desired_rotation] and [desired_coords]. Then draw it
        """
        ## Will keep iterating untill it is done moving
        if not self.explode:
            rotated = self._rotate_step()
            moved = self._move_step()
            delayed  = self._delay_step()
            
            self._update_bullets()
            self._draw()

            ## Will get the next command from the player or computer if it is
            ## where it needs to be, otherwise it will continue moving
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

## All of the bullets fired in this game are objects of class [bullet]
class bullet:
    def __init__(self, coordinates, rotation, owner):
        """Creates the bullet object with the needed hardcoded variables."""
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
        as input, and uses their coordinates to see if a bullet can hit them
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
        """ Draws the image of the bullet on the playing surface"""
        self.image = _rot_center(self.origional_image, self.rotation + 90)
        screen.blit(self.image, self.coords)
        
    def _update(self):
        """Is called by the tank that fired the bullet to move and draw the bullets."""
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
    """ Rotate an image around its center, while keeping the origional size,
    by converting to pil, rotating and converting the image back to pygame
    """

    tank_image_string = pygame.image.tostring(pygame_image, 'RGBA', False)
    new_image = Image.frombytes('RGBA', pygame_image.get_size(),tank_image_string)
    new_image = new_image.rotate(-degrees)
    tank_image_string = new_image.tobytes()
    new_pygame_image = pygame.image.fromstring(tank_image_string,new_image.size, 'RGBA')
    return new_pygame_image


def can_hit_target(self_tank_object, target_tank_object):
    """ This function takes in the self tank object and the target tank object
        as input, and uses their coordinates to see if a bullet can hit them
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
    """ This function returns true if the provided button is pressed. 'button'
    defaults to 'escape'"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT and button == "escape":
            return True
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == button:
                return True
    return False

def clearScreen():
    """ Clears the terminal screen """
    if platform == "win32":
        system('cls')
    else:
        system("clear")

def get_user_program(exception_raised, nest=0):
    """ This function returns a string of the tank program from the user"""
    
    user_in = True
    done = False
    program = ""
    if exception_raised:
        input("\n\n [Press Enter to Continue]")

    if nest == 0:
        clearScreen()
        print("For general help with the game, type 'info' and press enter.\n"
            + "For a list of tank commands and what they do, type player.info()\n\n")
        print(lesson_statements[level] + "\n")

    ## Gets tank commands from user
    while user_in and not done:        
        done = _button_press()
        user_in = input('>>> ' + nest *'    ')
        if user_in == "info":
            print("The purpose of this game is to teach those unfamiliar with coding how to code.\n"
                  "The player will play several levels, where the goal of the level is to kill the\n"
                  "enemy tank, by destroying it with a bullet. The player can manuever their tank\n"
                  "by writing a code for it to follow after the '>>> '. The program is coded in \n"
                  "the python programming language, and all normal python actions are supported by\n" 
                  "the console in addition to several new functions that control the player.\n"
                  "Type 'player.info()' for a list of the tank's commands. Break a leg!")
            user_in = "\n"
        if "player.info(" in user_in:
            exec(user_in)
            user_in = "\n"

        if ":" in user_in:
            user_in += "\n" + get_user_program(False,nest+1)
        
        program += nest *'    ' + user_in + "\n"
        
        #if "player." in user_in and ":" not in user_in:
        program += nest *'    ' + "_update()\n"
    
    return program

def get_enemy_move(level, enemy_tank_object, player_tank_object, game_map):
    """This function is called after every move the player, tank makes when the
    game is being compiled. It takes the map, as well as the level,
    the player tank object and the enemy tank object and outputs the move that
    the tank will make, based on what the level dictates
    """
    player_x, player_y = player_tank_object.coords
    enemy_x, enemy_y = enemy_tank_object.coords

    level +=1
    
    ## Level 1: Do nothing
    if(level == 1):
        return("")

    ## Level 2: Moves up and down the screen:
    elif(level == 2):
## OLD CODE:
##        if((enemy_y < 20 and enemy.rotation != SOUTH) or (enemy_y > 1000 and enemy.rotation != NORTH)):
##            return("enemy.turnLeft()")
##        else:
##            return("enemy.move(10)")
        return("")
        
    ## Level 3: Shoot if it can hit you
    elif(level == 3):  
        if(can_hit_target(enemy_tank_object, player_tank_object) and enemy_tank_object.program_counter > 10 and len(enemy_tank_object.bullet_list) == 0):
            return("enemy.fire()")
        return ""
        
    ## Level 4: Circle around the map and try to shoot you whenever possible
    elif(level == 4):
        if(can_hit_target(enemy_tank_object, player_tank_object) and len(enemy_tank_object.bullet_list) == 0):
            enemy_tank_object.program_counter -= 1
            return("enemy.fire()")
        elif(enemy_tank_object.program_counter % 2 == 0 ):
            return("enemy.turnLeft()")
        elif((enemy_tank_object.program_counter -1)%4 == 0):
            return("enemy.move(500)")
        else:
            return("enemy.move(1000)")

    ## Level 5: The tank will use logic and tank coordinates to make it's way toward the
    ## player tank and fire whenever possible. Makes 3 left turns for a right as a handicap   
    elif(level == 5):
        if(can_hit_target(enemy_tank_object, player_tank_object) and len(enemy_tank_object.bullet_list) == 0):
            return("enemy.fire()")
        elif(player_x < enemy_x and enemy.rotation != WEST):
            return("enemy.turnLeft()")
        elif(player_x > enemy_x and enemy.rotation != EAST):
            return("enemy.turnLeft()")
        elif(player_y < enemy_y and player_x == enemy_x and enemy.rotation != NORTH):
            return("enemy.turnLeft()")
        elif(player_y > enemy_y and player_x == enemy_x and enemy.rotation != SOUTH):
            return("enemy.turnLeft()")
        elif(player_x != enemy_x):
            return("enemy.desired_coords = (" + str(player_x) + "," + str(enemy_y) + ")")
        else:
            return("enemy.desired_coords = (" + str(enemy_x) + "," + str(player_y) + ")")

def display_title_screen():
    """ Displays the title screen """
    global screen

    _done = False

    background_music.play()
    screen = pygame.display.set_mode(size , FULLSCREEN)
    
    while not _done:
        _done = _button_press("return")
        screen.blit(title_screen,(0,0))
        pygame.display.flip()
        clock.tick(60)
    background_music.stop()
        
def display_level(level):
    """ Displays the starting game state for the level, so the player knows what to program"""
    _enter = False
    
    pygame.font.init()
    myfont = pygame.font.SysFont('Times New Roman',100)
    textsurface = myfont.render('Level ' + str(level + 1), False, (0,0,0))
    center = (screen.get_width()/2 - textsurface.get_width()/2,screen.get_height()/2 - textsurface.get_height()/2)
    
    while not _enter:
        _enter = _button_press("return")
        screen.blit(backgroundImg, (0,0))

        player._draw()
        enemy._draw()
        screen.blit(textsurface, center)

        pygame.display.flip()
        time.sleep(time_delay)
        
    pygame.display.quit()

def _update(repeat = False):
    """ Heart of the game. This function is called after every line of the player's program to move the
    player's tank as well as updating the enemy tank
    """
    global _quit
    
    _quit = False
    
    _done = False
    _enemy_done = False

    enemy_x, enemy_y = enemy.coords
    enemy_x += enemy.size[0]//2
    enemy_y += enemy.size[1]//2

    while not _quit and ((not _done) or repeat) and (player.alive and enemy.alive):
        _quit = _button_press()
        screen.blit(backgroundImg, (0,0))
        
        _done = player._update()
        _enemy_done = enemy._update()

        if _enemy_done:
            exec(get_enemy_move(level, enemy, player, None))
            print(get_enemy_move(level, enemy, player, None))
            enemy.program_counter+=1

        pygame.display.flip()
        time.sleep(time_delay)
    
def run_level(level, exception_raised):
    """ This is the game loop that runs whenever a level begins, and ends at the end of the level"""
    global screen
    global enemy
    global player

    enemy.__init__(enemy_coords[level],enemy_direction[level],'enemy_sprite.png')
    player.__init__(player_coords[level],EAST, 'tank_sprite.png')

    if not exception_raised:
        screen = pygame.display.set_mode(size , FULLSCREEN)

        background_music.play()
        display_level(level)
        
    pygame.init()

    user_program = get_user_program(exception_raised)

    screen = pygame.display.set_mode(size , FULLSCREEN)
    
    background_noise.play(-1)

    ## This code segment checks the user's program for bugs, by restarting the level, and reporting the
    ## the bug to the user if there is a syntax error or an exception raised.
    try:
        exec(user_program)
    except SyntaxError as err:
        error_class = err.__class__.__name__
        detail = err.args[0]
        line_number = err.lineno
        print(error_class + " " + detail + "\nLine Number: " + str(line_number//2 + 1))

        exception_raised = True
        pygame.display.quit()
    except Exception as err:
        error_class = err.__class__.__name__
        detail = err.args[0]
        cl, exc, tb = exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        print(error_class + ": " + detail + "\nLine Number: " + str(line_number//2 + 1))

        exception_raised = True
        pygame.display.quit()
    else:
        exception_raised = False
        _update(True)
    
    pygame.mixer.stop()

    ## Returning the next level for the computer to play, based on if anybody died.
    
    ## If the player did not die and the user did, advance the level
    if enemy.explode and not player.explode:
        return level + 1, exception_raised
    ## otherwise don't advance the level
    else:
        return level, exception_raised
    
def game_loop():
    """ This is the game loop that calls 'run_level' for each individual level """
    global level
    global _quit
    exception_raised = False

    display_title_screen()
    
    while level < 5 and not _quit:
        level, exception_raised = run_level(level, exception_raised)
     
    pygame.quit()

## Defining global variables for the game, such as...
level = 0

_quit = False

## 1) starting positions and rotations of the tanks
enemy_coords = [(1000,250),(1000,250),(1000,250),(1000,500),(1000,500)]
enemy_direction = [WEST,WEST,WEST,EAST,NORTH]

player_coords = [(100,240),(100,240),(100,240),(10,10),(10,10)]

## 2) media for the entire game, including images and music
title_screen = pygame.transform.scale(pygame.image.load('title_screen2.jpg'),size)

backgroundImg = pygame.transform.scale(pygame.image.load('background2.png'),size)

background_noise = pygame.mixer.Sound('Battlefeild Background Noise.wav')
background_noise.set_volume(1)
background_music = pygame.mixer.Sound('The_Circus_Bee.ogg')
background_music.set_volume(1)

## 3) The lessons for each level

lesson_statements = ["Level One: You can command your tank by writing a python program that includes "
                   + "the game's special tank methods found under\nplayer.help(). In this first level, "
                   + "the enemy tank will not move. Your job is to try destroying the tank, by "
                   + "firing at it using the \nplayer.fire() method. So try typing player.fire() and then "
                   + "pressing [enter] twice.",
                     "Level Two: In python, 'if' statements are very helpful. An if statement "
                   + "executes a certain portion of code only if a certain condition is met. To do this "
                   + "you type 'if( [condition] ): and then type your code. Anything you type now will be "
                   + "run if that condition is met. Let's try using our tanks built in 'can_hit_enemy' "
                   + "function so that our tank only fires if it can hit the enemy. So try typing if(player. "
                   + "can_hit_enemy): player.fire() and see what happens",
                     "Level Three: Now we are going to try using our other built in tank methods. Type play "
                   + "er.help() for a list of players built in movement methods. Have fun with it and try to "
                   + "kill the enemy tank! Hint: You are going to want to turn around and move before the "
                   + "enemy bullet can hit you!)",
                     "Level Four: Just go for it!",
                     "Level Five"]
                     
                

## 4) Creating the tank objects
enemy = tank((1000,500),EAST,'enemy_sprite.png')
player = tank((100,240),EAST, 'tank_sprite.png')

tank.tank_list = [player, enemy]

## Starting the Game
game_loop()
