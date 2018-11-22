""" A Tank Game to teach coding those unfamiliar with it"""
import pygame, sys
from pygame.locals import *
from PIL import Image
import random
import time

pygame.init()
# Set the width and height of the screen
infoObject = pygame.display.Info()
size = (infoObject.current_w,  infoObject.current_h-30)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

class tank():
    def __init__(self):
        self.origional_image = pygame.image.load("KV-2_Tank.png")
        self.image = self.origional_image
        self.rotation = 0
        self.coords = (0,0)
        self.move_count = 0 ## Counts the number of tims a function is iterated
        
    def rotate(self, degrees):
        """ This program will rotate 1 degree everytime called, untill it has
            reached the desired rotation, then it will advance the program counter
        """
        global program_counter
        
        if degrees > 0 and self.move_count < degrees:
            self.rotation += 1
            self.move_count +=1
        elif degrees < 0 and self.move_count > degrees:
            self.rotation -= 1
            self.move_count -=1
        else:
            self.move_count = 0
            program_counter +=1
            
    def move(self, distance):
        """ This program will move 10 pixels everytime called, untill it has
            reached the desired position, then it will advance the program counter
        """
        global program_counter
        self.move_count+=1
        (x,y) = self.coords
        
        if distance > 0 and self.move_count < distance:
            x += 10
        elif distance < 0 and self.move_count < distance:
            x -= 10
        else:
            program_counter+=1
            self.move_count = 0
            
        self.coords = (x,y)
        
        
    def draw(self):
        self.image = self._rot_center(self.origional_image,self.rotation)
        screen.blit(self.image,self.coords)

    def _rot_center(self,pygame_image,degrees):
        """rotate an image while keeping its center and size, by converting to pil, rotating and back"""
        image_string = pygame.image.tostring(pygame_image, "RGBA", False)
        PIL_image = Image.frombytes("RGBA",pygame_image.get_size(),image_string)
        PIL_image = PIL_image.rotate(degrees)
        image_string = PIL_image.tobytes()
        pygame_image = pygame.image.fromstring(image_string, PIL_image.size, "RGBA")
        return(pygame_image)
            
def get_program(nest):
    """ This function gets the tank program from the user"""
    user_in = True
    program = []
    
    ## Gets program from user
    while user_in:
        user_in = input(">>> " + (nest * "  "))
        ## If a conditional, it runs 'get_program' to get the conditional
        ## the code under the conditional,and appends it as one string
        ## separated by '\n' to the program list. It counts the number of
        ## 'nests' to print the correct number of tabs.
        if ":" in user_in:
            nested_program = get_program(nest + 1)
            for command in nested_program:
                user_in += ("\n" + ((nest + 1) * "  ") + command)
##            user_in += "\n" + ((nest + 1) * "   ") + "start(" + str(nested_program) + ")"
        program.append(user_in)
    return(program)

def start(program):
    done = False
    global program_counter
    program_counter = 0
    
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
                
        # --- Game logic should go here
        if(program_counter < len(program)-1):
            print(program_counter, len(program))
            print(program[program_counter])
            exec(program[program_counter])
            if "tank." not in program[program_counter]:
                program_counter += 1
                print("flag")
        else:
            done = True
            
        # --- Screen-clearing code goes here
        screen.fill((255,255,255))
     
        # --- Drawing code should go here
        tank.draw()
     
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        time.sleep(0.001)
        clock.tick(60)

program = get_program(0)
program_counter = 0
tank = tank()
done = False
screen = pygame.display.set_mode(size)#, FULLSCREEN)
start(program)

# Close the window and quit.
pygame.quit()
