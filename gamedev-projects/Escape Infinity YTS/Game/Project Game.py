#Escape Infinity

import pygame
from pygame.locals import *
from time import sleep as wait
import re

pygame.init()
width = 1275
height = 650
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Story')

pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 1300, 1300))

image1 = pygame.image.load('1.png').convert()
image2 = pygame.image.load('2.png').convert()
image3 = pygame.image.load('3.png').convert()
image4 = pygame.image.load('4.png').convert()

image1 = pygame.transform.scale(image1, (350, 200))
image2 = pygame.transform.scale(image2, (350, 200))
image3 = pygame.transform.scale(image3, (400, 250))
image4 = pygame.transform.scale(image4, (400, 250))

screen.blit(image1, (50, 10))
screen.blit(image2, (850, 10))
screen.blit(image3, (150, 350))
screen.blit(image4, (850, 350))

story = '''In a dimly lit room, the boy sits engrossed in his video game, his eyes fixed on the screen.
Suddenly, a surge of electricity crackles and he finds himself inexplicably pulled into the digital realm.
The room transforms into a virtual landscape as he becomes one with the game, his surroundings coming alive.
The screen fades to black leaving only the echoing sound of his startled gasp.
Now, armed with his controller he must navigate this realm to find a way back, his adrenaline surging as reality blurs with fantasy.
'''
story = story.split('\n')

base_font = pygame.font.Font(None, 22)

for y in range(0,len(story),1):
    text_surface = base_font.render(story[y], True, (0, 0, 0))
    screen.blit(text_surface, (250 + 5, 250 + y * 25))

pygame.display.flip()
gameOn = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
            pygame.quit()
            break
    if gameOn == False:
        break
pygame.quit()

For = re.compile(r'for (.*?) in')

lvlsize = 15
boxsize = 25

hint = [
'''Hint:
move(amount)
point(0|90|180|270)
''',
'''Hint:
for var in range(number):
  #code

turnLeft90() => requires no argument
''',
'''Hint:
use loop() 4 times
loop() => requires no argument
''',
'''Hint:
use for loop with set of movements
halfLoop => moves around a wall above the player
''',
'''Hint:
move5turnLeft() => requires no argument
'''
]

allowed = [
'''_move(); _point()''',
'''_move(); _turnLeft90()''',
'''_loop()''',
'''_move(); _point(); _halfLoop()''',
'''_move5turnLeft(); _point()'''
]

level = [
'''
# # # # # # # # # # # # # # #
# O # # # # # # # # # # # # #
# - - - - - # # - - - - - # #
# - # # # - # # - - # # # # #
# - # - - - - - - - # - - # #
# - # - - # - # - - # - - # #
# - # - - # - # - - # - - # #
# - # - - # - # - - # - - # #
# - # - - # - # - - # - - # #
# - # - - # - # - - # - - # #
# - # - - # - # - - # - - # #
# - # - - - - - # - - - - - #
# - - # # # # # - - - - - - #
# - - - - - - - - - - - - - #
# # # # # # # # # # # # @ # #
'''.strip('\n').replace('\n',' ').split(' '),
'''
# # # # # # # # # # # # # # #
# O # - - - - - - - - - - - #
# - # - # # # # # # # # # - #
# - # - # - - - - - - - # - #
# - # - # - # # # # # - # - #
# - # - # - # - - - # - # - #
# - # - # - # - # - # - # - #
# - # - # - # @ # - # - # - #
# - # - # - # # # - # - # - #
# - # - # - - - - - # - # - #
# - # - # # # # # # # - # - #
# - # - - - - - - - - - # - #
# - # # # # # # # # # # # - #
# - - - - - - - - - - - - - #
# # # # # # # # # # # # # # #
'''.strip('\n').replace('\n',' ').split(' '),
'''
# # # # # # # # # # # # # # #
# O # - - - # - - - - - - - #
# - # - # - # - - - # - # - #
# - - - - - # # # - - - - - #
# # # - # - - - # - # # # - #
# - # - # - # - # - - - - - #
# - # - - - - - # # # - - - #
# - # # # - # - - - # - - - #
# - - - # - # - # - # - - - #
# - - - # - - - - - # # # - #
# - - - # # # - # - - - # - #
# - - - - - # - # - # - # - #
# - - - - - # - - - - - # - #
# - - - - - # # # @ # # # - #
# # # # # # # # # # # # # # #
'''.strip('\n').replace('\n',' ').split(' '),
'''
# # # # # # # # # # # # # # #
# # - - - - - - - - - - - - #
# - - - # - # # # # # - - - #
# - # - # - # - - - # - - - #
# - - - # - # - - - # - - - #
# # - # # - # # # # # - - - #
# - - - # - # - - - - - - - #
# - # - # - # - # - @ - # - #
# - - - # - # - # - - - # - #
# # - # # - # - - # - # - - #
# - - - # - - - - - # - - - #
# - # - # - - - - - # - - - #
# - - - # - - - - - @ - - - #
# # O # # - - - - - - - - - #
# # # # # # # # # # # # # # #
'''.strip('\n').replace('\n',' ').split(' '),
'''
# # # # # # # # # # # # # # #
# @ # - - - - # - - - - - - #
# @ # - - - - - - - # - # - #
# # # - - - - - - - - - # - #
# - - - # # # # # # - - # - #
# - - - # - - - - # - - # - #
# - - - # - # # - # - - # - #
# - - - # - # O - # - - # - #
# - - @ # - # # # # - - # - #
# # - # # - # - - # - - # - #
# # # # # - - - - - - - # - #
# - - - # - # # # # - - # - #
# - @ - # - # # # # # # # - #
# - - - # - - - - - - - - - #
# # # # # # # # # # # # # # #
'''.strip('\n').replace('\n',' ').split(' ')
]

C_pos = []
def _move():
    global move
    def move(amount):#[right/left,up/down]
        global C_pos, dir
        tmp = dir
        for d in range(0,len(C_pos),1):
            if C_pos[d][0] in ['=','+','-']:
                if C_pos[d][0] == '=':
                    tmp = C_pos[d][1]
                elif  C_pos[d][0] == '+':
                    tmp = (tmp + C_pos[d][1]) % 360
                elif C_pos[d][0] == '-':
                    tmp = (tmp - C_pos[d][1]) % 360
        if tmp == 0:
            C_pos += [[amount,0]]
        elif tmp == 90:
            C_pos += [[0,amount * -1]]
        elif tmp == 180:
            C_pos += [[amount * -1,0]]
        elif tmp == 270:
            C_pos += [[0,amount]]
def _point():
    global point
    def point(direction):
        global C_pos
        if direction % 90 != 0:
            print('Error! Only accepts 0, 90, 180, 270!!')
        else:
            C_pos += [['=',direction % 360]]

def _turnLeft90():
    global turnLeft90
    def turnLeft90():
        global C_pos
        C_pos += [['+',90]]

def _loop():
    global loop
    def loop():
        global C_pos
        def move(amount):
            global C_pos, dir
            tmp = dir
            for d in range(0, len(C_pos), 1):
                if C_pos[d][0] in ['=', '+', '-']:
                    if C_pos[d][0] == '=':
                        tmp = C_pos[d][1]
                    elif C_pos[d][0] == '+':
                        tmp = (tmp + C_pos[d][1]) % 360
                    elif C_pos[d][0] == '-':
                        tmp = (tmp - C_pos[d][1]) % 360
            if tmp == 0:
                C_pos += [[amount, 0]]
            elif tmp == 90:
                C_pos += [[0, amount * -1]]
            elif tmp == 180:
                C_pos += [[amount * -1, 0]]
            elif tmp == 270:
                C_pos += [[0, amount]]

        move(2)
        C_pos += [['=', 0]]
        move(4)
        C_pos += [['=', 90]]
        move(2)
        C_pos += [['=', 180]]
        move(2)
        C_pos += [['=', 270]]
        move(3)



def _move5turnLeft():
    global move5turnLeft
    def move5turnLeft():
        global C_pos, dir
        tmp = dir
        for d in range(0, len(C_pos), 1):
            if C_pos[d][0] in ['=', '+', '-']:
                if C_pos[d][0] == '=':
                    tmp = C_pos[d][1]
                elif C_pos[d][0] == '+':
                    tmp = (tmp + C_pos[d][1]) % 360
                elif C_pos[d][0] == '-':
                    tmp = (tmp - C_pos[d][1]) % 360
        if tmp == 0:
            C_pos += [[5, 0]]
        elif tmp == 90:
            C_pos += [[0, 5 * -1]]
        elif tmp == 180:
            C_pos += [[5 * -1, 0]]
        elif tmp == 270:
            C_pos += [[0, 5]]
        C_pos += [['+', 90]]

def _halfLoop():
    global halfLoop
    def halfLoop():
        global C_pos
        def move(amount):
            global C_pos, dir
            tmp = dir
            for d in range(0, len(C_pos), 1):
                if C_pos[d][0] in ['=', '+', '-']:
                    if C_pos[d][0] == '=':
                        tmp = C_pos[d][1]
                    elif C_pos[d][0] == '+':
                        tmp = (tmp + C_pos[d][1]) % 360
                    elif C_pos[d][0] == '-':
                        tmp = (tmp - C_pos[d][1]) % 360
            if tmp == 0:
                C_pos += [[amount, 0]]
            elif tmp == 90:
                C_pos += [[0, amount * -1]]
            elif tmp == 180:
                C_pos += [[amount * -1, 0]]
            elif tmp == 270:
                C_pos += [[0, amount]]
        C_pos += [['=', 0]]
        move(1)
        C_pos += [['=', 90]]
        move(2)
        C_pos += [['=', 180]]
        move(1)

wall = pygame.Surface((boxsize,boxsize))
wall.fill((0,255,255)) #cyan

p = pygame.Surface((boxsize,boxsize))
p.fill((50,205,50)) #lime green

blank = pygame.Surface((boxsize,boxsize))
blank.fill((0,0,0))

goal = pygame.Surface((boxsize,boxsize))
goal.fill((255,255,0))

box = {
    '#':wall,
    'O':p,
    '-':blank,
    '@':goal
}

print('''--How to Play--
You are the GREEN square along with the direction of the square...

Input the allowed functions on the screen and include () with the values inside it...

GOAL : REACH the YELLOW tile!
''')
wait(3)
for i in range(0,len(level),1):
    player = level[i].index('O')
    dir = 270#0 => right, 90 => up, 180 => left, 270 => down
    print(hint[i],'\n')
    while True:
        print('Allowed funtions:\n' + allowed[i].replace('_','').replace(';','\n').replace('()','').replace(' ',''))
        exec(allowed[i].replace('; ','\n'))
        file = open('Print.py','r')
        exec(file.read())
        file.close()
        if gameOn == False:
            dir = 270
        if win == True:
            break
    print('\n'*10)
    exec('del ' + allowed[i].replace('; ',';del ').replace('()','').replace('_',''))
print('You ESCAPED out of the INFINITE virtual reality!!')