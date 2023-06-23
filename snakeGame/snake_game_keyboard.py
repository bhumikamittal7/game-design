import pygame
import random

pygame.init()
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')
FPS=25
fpsClock=pygame.time.Clock()

background_color = (0,139,0)
snake_color=(0,0,255)
snake_mouth = [200,150]
snake_height = 30
snake_width = 30
display.fill(background_color)

SPEED = 5
snake=[]
direction_list=[]
snake.append(snake_mouth)
'''
1:left
2:right
3:up
4:down
'''
direction = 1
direction_list.append(direction)

def move_cell(direction,posn):
    new_x = posn[0]
    new_y = posn[1]
    if direction == 1:
        new_x -= SPEED
    if direction == 2:
        new_x += SPEED
    if direction == 3:
        new_y -= SPEED
    if direction == 4:
        new_y += SPEED
    return [new_x,new_y]


def move(direction,snake):
    updated_mouth = move_cell(direction,snake[0])
    new_snake=[]
    new_snake.append(updated_mouth)
    for i in range(len(snake)-1):
        new_snake.append(snake[i])
    return new_snake


food_color = (139,0,0)
def add_food():
    food_x =random.randint(0,width)
    food_y =random.randint(0,height)
    return [food_x,food_y]

food_posn = add_food()

def update_food(snake,direction):
    last_block = snake[-1]
    if direction == 1:
        new_block = [last_block[0] + snake_width, last_block[1]]
    if direction == 2:
        new_block = [last_block[0] - snake_width, last_block[1]]
    if direction == 3:
        new_block = [last_block[0], last_block[1] + snake_height]
    if direction == 4:
        new_block = [last_block[0], last_block[1] - snake_height]
    snake.append(new_block)
    
    return snake


def is_food_present(snake,food_posn):
    snake_mouth = snake[0]
    snake_mouth_center = [snake_mouth[0],snake_mouth[1]]
    distance = ((food_posn[0]-snake_mouth_center[0])**2 + (food_posn[1]-snake_mouth_center[1])**2)**0.5
    # print(snake_mouth)
    if distance<12:
        return True
    else:
        return False
        
game_over = False
while not game_over:
    display.fill(background_color)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction=1
            if event.key == pygame.K_RIGHT:
                direction=2
            if event.key == pygame.K_UP:
                direction=3
            if event.key == pygame.K_DOWN:
                direction=4
    snake = move(direction,snake)
    #print(snake)
    is_food= is_food_present(snake,food_posn)
    #print('is_food_present:',is_food)
    if (is_food):
        
        snake = update_food(snake,direction)
        food_posn = add_food()
    else:
        pygame.draw.circle(display, food_color, food_posn, 5)
    for snake_posn in snake:
        pygame.draw.rect(display, snake_color, [snake_posn[0]-int(snake_width/2), snake_posn[1]-int(snake_height/2), snake_width, snake_height])
    pygame.draw.rect(display, [255,255,255],[snake[0][0], snake[0][1], 2, 2])

    if(is_food):
        print(snake)
    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
quit()