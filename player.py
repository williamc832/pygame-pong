import pygame
from settings import *


# define paddle object as player
class Paddle:
    # initialize paddle
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = pygame.Color(WHITE)
        self.v = PADDLE_SPEED
        self.drawing = True

    # upward movement of paddle
    def move_up(self):
        self.rect.y -= self.v

    # downward movement of paddle
    def move_down(self):
        self.rect.y += self.v

    # update paddle object until game over
    def update(self, win):
        if self.drawing:
            pygame.draw.rect(win, self.color, self.rect)
