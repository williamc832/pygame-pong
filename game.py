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
        self.playing = False

    # check for game over event
    def check_game_over(self):
        if self.table.game_over:
            self.draw_text("GAME OVER", TEXT_FONT, GAME_OVER_FONT_SIZE, 0, 1/3)

    # draw text onto window
    def draw_text(self, text, font, size, x, y):
        text_font = pygame.font.Font(font, size)
        text_surf = text_font.render(text, False, WHITE)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (WIDTH // 2 - text_surf.get_width() // 2 + x, HEIGHT * y - text_surf.get_height() * y)
        self.win.blit(text_surf, text_rect)

    # start new game
    def new_game(self):
        self.table.draw()
        self.table.update()

    # update window
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)

    # draw window
    def draw(self):
        self.win.fill(BLACK)

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
        self.check_events()
        self.draw()
        self.check_game_over()
        self.new_game()
        self.update()
