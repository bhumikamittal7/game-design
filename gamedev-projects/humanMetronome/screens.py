import pygame

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Button Example")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

active_screen = "first"


def draw_button(button):
    button.draw(screen)


class FirstScreen:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class SecondScreen:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class ThirdScreen:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


button_width = 200
button_height = 50
button_x = (width - button_width) // 2
button_y = (height - button_height) // 2

button_first = FirstScreen(button_x, button_y, button_width, button_height, BLACK, "Start Game!")
button_second = SecondScreen(button_x, button_y, button_width, button_height, BLACK, "Click Me!")


class Label:
    def __init__(self, x, y, text, font_size=24, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.rendered_text, self.rect)


gamedone = False
