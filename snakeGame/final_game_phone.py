import pygame
import random
import socket
import threading
pygame.init()
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')
FPS=60
fpsClock=pygame.time.Clock()

background_color = (0,139,0)
snake_color=(0,0,255)
snake_mouth = [200,150]
snake_height = 50
snake_width = 50
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
direction = 0
direction_list.append(direction)

host = "10.1.17.153"  # '#'127.0.0.1'
port = 8080
global soc
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host, port))


def get_min_max(window):
    min_window = min(window)
    max_window = max(window)
    min_index = window.index(min_window)
    max_index = window.index(max_window)
    diff = max_window - min_window
    return diff,max_index,min_index

def read_process_live_data():
    x_data = []
    y_data = []
    z_data = []
    count=0
    window_size=50
    skip_size=30
    thresh = 18.0
    last_checked=0
    start_w = 0
    end_w = window_size
    is_valid = False
    global direction
    global game_over
    while not game_over:
        message, address = soc.recvfrom(1024)
        # print(message)
        # print("received message: %s" % message)
        res = message
        res = (res.rstrip()).lstrip()
        res = res.decode("utf-8")
        data = res.split(",")

        data = [float(x) for x in data[2:5]]
        #print(data)
        x_data.append(data[0])
        y_data.append(data[1])
        z_data.append(data[2])
        count+=1
        if(count>window_size and (end_w-start_w)>=window_size and len(x_data)>=end_w):
            window_x = x_data[start_w:end_w]
            window_z = z_data[start_w:end_w]
            print("window length:", len(window_x))
            delta_x,max_i_x,min_i_x = get_min_max(window_x)
            delta_z,max_i_z,min_i_z = get_min_max(window_z)

            if delta_x > delta_z:
                dir='x'
                delta = delta_x
                min_index = min_i_x
                max_index = max_i_x
            else:
                dir='z'
                delta = delta_z
                min_index = min_i_z
                max_index = max_i_z

            if delta > thresh :
                if min_index<max_index:
                    if dir=='x':
                        print("left", delta)
                        direction=1
                    else:
                        print("down",delta)
                        direction=4
                else:
                    if dir=='x':
                        print("right", delta)
                        direction=2
                    else:
                        print("up",delta)
                        direction=3
                is_valid=True
            last_checked=count
            if is_valid:
                start_w += window_size
                end_w += window_size
            else:
                start_w += skip_size
                end_w += skip_size


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
    #print(snake_mouth)
    if distance<20:
        return True
    else:
        return False

game_over = False
thread1 = threading.Thread(target=read_process_live_data, args=())
thread1.start()
while not game_over:
    display.fill(background_color)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

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

