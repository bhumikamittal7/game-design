import pygame
import time
import random

# Initialize pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
POWERUP_TIME = 60  # 5 minutes in seconds
POWERUP_LIFETIME = 10  # Powerups disappear after 10 seconds
collect_sound = pygame.mixer.Sound('collect_powerup.wav')
kill_sound = pygame.mixer.Sound('kill_enemy.wav')

# Set up window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Different types of powerups
POWERUP_TYPES = ['apple', 'strength', 'speed']

# Set up font
font = pygame.font.Font(None, 36)


# Game classes (Snake, Powerup, Enemy)
class Snake:
    def __init__(self, x, y):
        self.body = [(x, y)]
        self.direction = 'UP'
        self.grow = False
        self.strength = 1
        self.speed = 1
        self.health = 3
        self.projectile_speed = 1
        self.shoot_cooldown = 0
        self.last_shoot_time = None

    def can_shoot(self):
        if self.last_shoot_time is None:
            return True
        delay = max(0.2, 1 - 0.1 * self.speed)  # The delay is at least 0.2 seconds and decreases with the snake's speed
        return time.time() - self.last_shoot_time > delay

    def shoot_projectile(self):
        return Projectile(self.body[0][0], self.body[0][1], self.speed, direction='UP')

    def move(self):
        x, y = self.body[0]
        speed = self.speed if powerup_phase else 2
        if self.direction == 'UP' and powerup_phase:
            y -= speed
        elif self.direction == 'DOWN' and powerup_phase:
            y += speed
        elif self.direction == 'LEFT':
            x -= speed
        elif self.direction == 'RIGHT':
            x += speed

        # Wrap around when moving off the screen
        x %= WINDOW_WIDTH
        if powerup_phase:
            y %= WINDOW_HEIGHT
        else:
            y = WINDOW_HEIGHT - 10  # Place the snake at the bottom of the screen in wave phase

        self.body.insert(0, (x, y))
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        self.direction = direction

    def eat_powerup(self, powerup_type):
        pygame.mixer.Sound.play(collect_sound)
        if powerup_type == 'apple':
            self.health += 1  # Change the apple powerup effect to increase health
        elif powerup_type == 'strength':
            self.strength += 1
        elif powerup_type == 'speed':
            self.speed += 1
            if self.shoot_cooldown > 0:  # If there is a shooting cooldown, decrease it when the snake eats a speed powerup
                self.shoot_cooldown -= 0.1

    def get_head_position(self):
        return self.body[0]

    def get_body(self):
        return self.body

    def draw(self, window):
        for part in self.body:
            pygame.draw.rect(window, (255, 255, 255), pygame.Rect(part[0], part[1], 10, 10))


class Powerup:
    def __init__(self, x, y, powerup_type, size=20):
        self.x = x
        self.y = y
        self.size = size
        self.type = powerup_type
        self.color = self.get_color()
        self.spawn_time = time.time()

    def get_color(self):
        if self.type == 'apple':
            return 0, 255, 0
        elif self.type == 'strength':
            return 0, 0, 255
        elif self.type == 'speed':
            return 255, 255, 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Enemy:
    def __init__(self, x, y, width=30, height=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1  # Velocity at which the enemy moves down the screen
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.projectile_speed = 1

    def shoot_projectile(self):
        return Projectile(self.x, self.y, self.projectile_speed, direction='DOWN')

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), self.shape)  # Draw the enemy as a red rectangle

    def move(self):
        self.y += self.vel  # Move the enemy down the screen
        self.shape.y = self.y  # Update the rectangle position


class Projectile:
    def __init__(self, x, y, speed, direction='UP', color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.color = color

    def move(self):
        if self.direction == 'UP':
            self.y -= self.speed
        elif self.direction == 'DOWN':
            self.y += self.speed

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, 5, 10))


# Game state
snake = Snake(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
powerups = []
enemies = []
powerup_phase = True
start_time = time.time()
snake_projectiles = []
enemy_projectiles = []
last_wave = time.time()
wave_interval = 30  # Every 30 seconds, a new wave of enemies will come
start_time = time.time()
last_wave = time.time()
enemy_speed = 1
score = 0  #
wave_number = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    if powerup_phase:
        if keys[pygame.K_LEFT]:
            snake.change_direction('LEFT')
        elif keys[pygame.K_RIGHT]:
            snake.change_direction('RIGHT')
        elif keys[pygame.K_UP]:
            snake.change_direction('UP')
        elif keys[pygame.K_DOWN]:
            snake.change_direction('DOWN')
    else:  # In wave phase, snake can only move left and right
        if keys[pygame.K_LEFT]:
            snake.change_direction('LEFT')
        elif keys[pygame.K_RIGHT]:
            snake.change_direction('RIGHT')
        if not powerup_phase and keys[pygame.K_SPACE] and snake.can_shoot():
            snake_projectiles.append(snake.shoot_projectile())
            snake.last_shoot_time = time.time()

    snake.move()

    if powerup_phase:
        if random.randint(0, 100) < 2:  # Decreased the spawn rate a bit
            powerup_type = random.choice(POWERUP_TYPES)
            powerups.append(Powerup(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), powerup_type))

        snake_head_rect = pygame.Rect(*snake.get_head_position(), 10, 10)
        for powerup in powerups[:]:
            if powerup.get_rect().colliderect(snake_head_rect):
                snake.eat_powerup(powerup.type)
                powerups.remove(powerup)
            elif time.time() - powerup.spawn_time >= POWERUP_LIFETIME:
                powerups.remove(powerup)  # Remove powerup if it has been on the screen for too long

        if time.time() - start_time >= POWERUP_TIME:
            powerup_phase = False


    else:  # Wave phase

        if time.time() - last_wave >= wave_interval:
            wave_number += 1
            last_wave = time.time()
            enemy_speed += 0.1  # Gradually increase the enemy's projectile speed
            powerups = []  # Clear all powerups

            if len(enemies) == 0 and len(
                    enemy_projectiles) == 0:  # If all enemies and their projectiles are gone, start a new wave
                last_wave = time.time()
                enemy_speed += 0.1  # Gradually increase the enemy's projectile speed
                powerups = []  # Clear all powerups

                for _ in range(len(enemies) + 5):  # Each wave has 5 more enemies than the previous one

                    enemy = Enemy(random.randint(0, WINDOW_WIDTH), 0)

                    enemy.projectile_speed = enemy_speed

                    enemies.append(enemy)

        for enemy in enemies:
            if random.randint(0, 100) < 1:  # % chance for each enemy to shoot a projectile each frame
                enemy_projectiles.append(enemy.shoot_projectile())

        for projectile in snake_projectiles:
            projectile.move()
            if projectile.y < 0:
                snake_projectiles.remove(projectile)
            else:
                for enemy in enemies:
                    if pygame.Rect(projectile.x, projectile.y, 5, 10).colliderect(enemy.shape):
                        enemies.remove(enemy)
                        snake_projectiles.remove(projectile)
                        score += 1
                        pygame.mixer.Sound.play(kill_sound)
                        break

        for projectile in enemy_projectiles:
            projectile.move()
            if projectile.y > WINDOW_HEIGHT:
                enemy_projectiles.remove(projectile)
            else:
                if pygame.Rect(projectile.x, projectile.y, 5, 10).colliderect(
                        pygame.Rect(*snake.get_head_position(), 10, 10)):
                    snake.health -= 1
                    enemy_projectiles.remove(projectile)
                    if snake.health <= 0:
                        print("Game Over!")
                        pygame.quit()

    # Draw everything
    window.fill((0, 0, 0))

    # Draw counters
    pygame.display.set_caption("Snake Invaders")

    # Set window icon
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)

    health_text = font.render(f'Health: {snake.health}', True, (255, 255, 255))
    speed_text = font.render(f'Speed: {snake.speed}', True, (255, 255, 255))
    strength_text = font.render(f'Strength: {snake.strength}', True, (255, 255, 255))
    window.blit(health_text, (10, 450))
    window.blit(speed_text, (10, 500))
    window.blit(strength_text, (10, 550))
    time_left = max(0, int(POWERUP_TIME - (time.time() - start_time)))
    timer_text = font.render(f'Time left: {time_left}', True, (255, 255, 255))
    window.blit(timer_text, (600, 550))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    wave_number_text = font.render(f'Wave number: {wave_number}', True, (255, 255, 255))
    window.blit(score_text, (600, 500))
    window.blit(wave_number_text, (600, 450))

    snake.draw(window)
    for powerup in powerups:
        powerup.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    for projectile in snake_projectiles:
        projectile.draw(window)
    for projectile in enemy_projectiles:
        projectile.draw(window)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
