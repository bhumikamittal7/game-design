import websocket
import json
import threading
import time
import pygame
import random

pygame.init()
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')
FPS = 60
fpsClock = pygame.time.Clock()

background_color = (0, 139, 0)
snake_color = (0, 0, 255)
snake_mouth = [200, 150]
snake_height = 50
snake_width = 50
display.fill(background_color)

SPEED = 5
snake = []
direction_list = []
snake.append(snake_mouth)
'''
1: left
2: right
3: up
4: down
'''
direction = 0
direction_list.append(direction)

class Sensor:
    # constructor
    def __init__(self, address, sensor_type):
        self.address = address
        self.sensor_type = sensor_type
        self.x_data = []
        self.y_data = []
        self.z_data = []

    # called each time when sensor data is received
    def on_message(self, ws, message):
        values = json.loads(message)['values']

        self.x_data.append(values[0])
        self.y_data.append(values[1])
        self.z_data.append(values[2])

    def get_x_data(self):
        return self.x_data

    def get_y_data(self):
        return self.y_data

    def get_z_data(self):
        return self.z_data

    def on_error(self, ws, error):
        print("Error occurred")
        print(error)

    def on_close(self, ws, close_code, reason):
        print("Connection closed")
        print("Close code:", close_code)
        print("Reason:", reason)

    def on_open(self, ws):
        print(f"Connected to: {self.address}")

    # Call this method on a separate Thread
    def make_websocket_connection(self):
        ws = websocket.WebSocketApp(f"ws://{self.address}/sensor/connect?type={self.sensor_type}",
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        # blocking call
        ws.run_forever()

    # Make connection and start receiving data on a separate thread
    def connect(self):
        thread = threading.Thread(target=self.make_websocket_connection)
        thread.start()


sensor = Sensor(address="10.1.17.153:8081", sensor_type="android.sensor.accelerometer")

def get_min_max(window):
    min_window = min(window)
    max_window = max(window)
    min_index = window.index(min_window)
    max_index = window.index(max_window)
    diff = max_window - min_window
    return diff, max_index, min_index

def read_process_live_data():
    global direction
    while not game_over:
        x_data = sensor.get_x_data()
        y_data = sensor.get_y_data()
        z_data = sensor.get_z_data()

        if len(x_data) > 0:
            print("x_data:", x_data[-1])
        else:
            print("No x_data available yet.")

        count = 0
        window_size = 50
        skip_size = 30
        thresh = 18.0
        last_checked = 0
        start_w = 0
        end_w = window_size
        is_valid = False

        count += 1
        if count > window_size and (end_w - start_w) >= window_size and len(x_data) >= end_w:
            window_x = x_data[start_w:end_w]
            window_z = z_data[start_w:end_w]
            print("window length:", len(window_x))
            delta_x, max_i_x, min_i_x = get_min_max(window_x)
            delta_z, max_i_z, min_i_z = get_min_max(window_z)

            if delta_x > delta_z:
                dir = 'x'
                delta = delta_x
                min_index = min_i_x
                max_index = max_i_x
            else:
                dir = 'z'
                delta = delta_z
                min_index = min_i_z
                max_index = max_i_z

            if delta > thresh:
                if min_index < max_index:
                    if dir == 'x':
                        print("left", delta)
                        direction = 1
                    else:
                        print("down", delta)
                        direction = 4
                else:
                    if dir == 'x':
                        print("right", delta)
                        direction = 2
                    else:
                        print("up", delta)
                        direction = 3
                is_valid = True

            last_checked = count

            if is_valid:
                start_w += window_size
                end_w += window_size
            else:
                start_w += skip_size
                end_w += skip_size

        data_received_event.set()

def move_cell(direction, posn):
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
    return [new_x, new_y]

def move(direction, snake):
    updated_mouth = move_cell(direction, snake[0])
    new_snake = []
    new_snake.append(updated_mouth)
    for i in range(len(snake) - 2, -1, -1):
        new_snake.append(snake[i])
    return new_snake

food_color = (139, 0, 0)

def add_food():
    food_x = random.randint(0, width)
    food_y = random.randint(0, height)
    return [food_x, food_y]

food_posn = add_food()

def update_food(snake, direction):
    last_block = snake[-1]
    if direction == 1:
        new_block = [last_block[0] + snake_width, last_block[1]]
    if direction == 2:
        new_block = [last_block[0] - snake_width, last_block[1]]
    if direction == 3:
        new_block = [last_block[0], last_block[1] + snake_height]
    if direction == 4:
        new_block = [last_block[0], last_block[1] - snake_height]
    snake.insert(1, new_block)
    return snake

def is_food_present(snake, food_posn):
    snake_mouth = snake[0]
    distance = abs(food_posn[0] - snake_mouth[0]) + abs(food_posn[1] - snake_mouth[1])
    return distance < 20

def handle_events():
    global direction
    global game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 1
            elif event.key == pygame.K_RIGHT and direction != 1:
                direction = 2
            elif event.key == pygame.K_UP and direction != 4:
                direction = 3
            elif event.key == pygame.K_DOWN and direction != 3:
                direction = 4

# Main game loop
game_over = False
data_received_event = threading.Event()

while not game_over:
    handle_events()
    display.fill(background_color)

    if is_food_present(snake, food_posn):
        snake = update_food(snake, direction)
        food_posn = add_food()

    snake = move(direction, snake)

    for block in snake:
        pygame.draw.rect(display, snake_color, [block[0], block[1], snake_width, snake_height])

    pygame.draw.rect(display, food_color, [food_posn[0], food_posn[1], snake_width, snake_height])
    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
