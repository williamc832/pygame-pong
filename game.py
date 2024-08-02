import pygame
import sys
from settings import *
from table import Table


# define game object
class Game:
    # initialize window
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.running = True
        self.clock = pygame.time.Clock()
        self.table = Table(self.win)

    # update window
    def update(self):
        self.table.update()
        pygame.display.flip()
        self.clock.tick(FPS)

    # draw window
    def draw(self):
        self.win.fill(BLACK)
        self.table.draw()

    # handle events
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == self.table.RESET_BALL:
                self.table.center_ball()

    # main loop
    def run(self):
        while self.running:
            self.check_events()
            self.draw()
            self.update()
