import pygame
import time 
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman',30)
textsurface = myfont.render('', False, (0,0,0))
pygame.key.set_repeat(250,30)

infoObject = pygame.display.Info()
size = (infoObject.current_w, infoObject.current_h - 30)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)  # , FULLSCREEN)

done = False
cursor = False
cursor_coord = 0
letter = None
lines = ["|"]
count = 0

def return_letter():
    global done
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if pygame.key.name(event.key) != "escape" :
            return pygame.key.name(event.key)
        else:
            done = True
            return False
      if event.type == pygame.QUIT:
        done = True
        return False

def print_text(next_char):
    global lines
    global textsurface
    global cursor_coord

    this_line = lines[len(lines)-1]
    
    if next_char == "space":
        next_char = " "
    elif next_char == "backspace":
        this_line = this_line[:len(this_line)-1]
        textsurface = myfont.render(this_line, False, (0,0,0))
        next_char = ""
        
    if next_char:
        this_line = this_line.replace("|","")
        this_line += next_char
        this_line = this_line[:cursor_coord+1] + "|" + this_line[cursor_coord:]
        textsurface = myfont.render(this_line, False, (0,0,0))
        cursor_coord += 1
        
    lines[len(lines)-1] = this_line
while not done:
    letter = return_letter()
    print_text(letter)
        
    screen.fill((255, 255, 255))
    screen.blit(textsurface,(0,0))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()



