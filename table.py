import pygame
import random
import math
from settings import *
from player import Paddle
from ball import Ball


# define table object
class Table:
    # initialize table object
    def __init__(self, win):
        self.win = win
        self.p1 = Paddle(100, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.p2 = Paddle(WIDTH - 100 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2)
        self.p1_score = 0
        self.p2_score = 0
        self.score_limit = 11
        self.game_over = False
        self.score_font = pygame.font.Font(SCORE_FONT, SCORE_FONT_SIZE)
        self.color = pygame.Color(WHITE)
        self.score_time = pygame.time.get_ticks() - 2000
        self.RESET_BALL = pygame.USEREVENT + 1
        self.RESET_DELAY = 2000
        self.collision_tolerance = 10
        self.collision_count = 0

    # draw net onto table object
    def _draw_net(self):
        for x in range(0, HEIGHT, 20):
            if x % 2 == 1:
                continue
            pygame.draw.rect(self.win, self.color, (WIDTH // 2, x, 1, 10))

    # paddle movement
    def _move_paddle(self):
        # get state of all keyboard buttons
        keys = pygame.key.get_pressed()

        # left paddle movement
        if keys[pygame.K_w] and self.p1.rect.top >= PADDLE_LIMIT:
            self.p1.move_up()
        if keys[pygame.K_s] and self.p1.rect.bottom <= HEIGHT - PADDLE_LIMIT:
            self.p1.move_down()

        # right paddle movement
        if keys[pygame.K_UP] and self.p2.rect.top >= PADDLE_LIMIT:
            self.p2.move_up()
        if keys[pygame.K_DOWN] and self.p2.rect.bottom <= HEIGHT - PADDLE_LIMIT:
            self.p2.move_down()

    # collision between ball and walls
    def _wall_collision(self):
        # collision with top and bottom of window
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.speed_y *= -1

        # collision with left and right side of window
        if self.game_over:
            if self.ball.rect.left <= 0 or self.ball.rect.right >= WIDTH:
                self.ball.speed_x *= -1
        else:
            if self.ball.rect.left >= WIDTH and pygame.time.get_ticks() - self.score_time > self.RESET_DELAY:
                self.p1_score += 1
                self.score_time = pygame.time.get_ticks()
                self._hide_ball()
                self._reset_ball_speed()
                self._check_score()
            if self.ball.rect.right <= 0 and pygame.time.get_ticks() - self.score_time > self.RESET_DELAY:
                self.p2_score += 1
                self.score_time = pygame.time.get_ticks()
                self._hide_ball()
                self._reset_ball_speed()
                self._check_score()

    # check for collision between ball and paddle
    def _paddle_collision(self):
        self._handle_paddle_collision(self.ball, self.p1, self.ball.speed_x)
        self._handle_paddle_collision(self.ball, self.p2, self.ball.speed_x)

    # handle collision between ball and paddles
    def _handle_paddle_collision(self, ball, paddle, ball_direction):
        if self.ball.rect.colliderect(paddle) and not self.game_over:
            # point of collision between ball and paddle
            collision_point = ball.rect.centery - paddle.rect.centery

            # collision with right paddle
            if abs(ball.rect.right - paddle.rect.left) < self.collision_tolerance and ball_direction > 0:
                if abs(collision_point) < 1:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(180))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(180))
                elif 0 < collision_point <= 5:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(160))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(160))
                elif 5 < collision_point <= 10:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(140))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(140))
                elif 10 < collision_point <= 15:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(120))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(120))
                elif 0 > collision_point >= -5:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(200))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(200))
                elif -5 > collision_point >= -10:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(220))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(220))
                elif -10 > collision_point >= -15:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(240))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(240))
                elif collision_point < -15 or collision_point > 15:
                    self._check_ball_speed()
                    ball.speed_x *= -1

            # collision with left paddle
            elif abs(ball.rect.left - paddle.rect.right) < self.collision_tolerance and ball_direction < 0:
                if abs(collision_point) < 1:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(0))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(0))
                elif 0 < collision_point <= 5:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(20))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(20))
                elif 5 < collision_point <= 10:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(40))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(40))
                elif 10 < collision_point <= 15:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(60))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(60))
                elif 0 > collision_point >= -5:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(340))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(340))
                elif -5 > collision_point >= -10:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(320))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(320))
                elif -10 > collision_point >= -15:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(300))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(300))
                elif collision_point < -15 or collision_point > 15:
                    self._check_ball_speed()
                    ball.speed_x *= -1

            # collision between top of paddle and bottom of ball
            elif abs(ball.rect.bottom - paddle.rect.top) < self.collision_tolerance and self.ball.speed_y > 0:
                ball.speed_y *= -1
                ball.rect.bottom = paddle.rect.top

            # collision between top of ball and bottom of paddle
            elif abs(ball.rect.top - paddle.rect.bottom) < self.collision_tolerance and self.ball.speed_y < 0:
                ball.speed_y *= -1
                ball.rect.top = paddle.rect.bottom

    # check number of collisions to increase ball speed
    def _check_ball_speed(self):
        # increment count upon collision with paddle
        self.collision_count += 1

        # increase speed after collision with both paddles
        if self.collision_count % 2 == 0:
            self.ball.increase_speed()
            self.collision_count = 0

    # move ball to center after scoring
    def center_ball(self):
        # move ball to center
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = random.randint(BALL_HEIGHT + PADDLE_LIMIT, HEIGHT - BALL_HEIGHT - PADDLE_LIMIT)

        # set ball movement
        if self.p1_score < self.score_limit and self.p2_score < self.score_limit:
            self.ball.randomize_direction()
        else:
            self._reset_ball_movement()

        # draw ball onto window
        self.ball.moving = True

    # hide ball animation for period after point is scored
    def _hide_ball(self):
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = HEIGHT // 2
        self.ball.moving = False

    # reset collision count and ball speed
    def _reset_ball_speed(self):
        self.collision_count = 0
        self.ball.new_speed = BALL_SPEED

    # ball movement if game over is true
    def _reset_ball_movement(self):
        self.ball.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.ball.speed_y = BALL_SPEED * random.choice([-1, 1])

    # delay ball reset after each score
    def _check_score(self):
        if self.p1_score < self.score_limit and self.p2_score < self.score_limit:
            pygame.time.set_timer(self.RESET_BALL, self.RESET_DELAY, 1)
        else:
            self.center_ball()

    # draw points scored
    def _draw_score(self):
        left_score = self.score_font.render(f"{self.p1_score}", False, self.color)
        right_score = self.score_font.render(f"{self.p2_score}", False, self.color)
        if self.p1_score < 10:
            self.win.blit(left_score, (WIDTH // 4 + 35, 15))
        else:
            self.win.blit(left_score, (WIDTH // 4, 15))
        if self.p2_score < 10:
            self.win.blit(right_score, (WIDTH * 3 // 4 + 10, 15))
        else:
            self.win.blit(right_score, (WIDTH * 3 // 4 - 50, 15))

    # handle game over state
    def _check_game_over(self):
        if self.p1_score == self.score_limit or self.p2_score == self.score_limit:
            self.game_over = True
            self.p1.drawing = False
            self.p2.drawing = False

    # draw objects from table onto window
    def draw(self):
        self._draw_net()

    # update objects on table
    def update(self):
        # update ball and paddles
        self.p1.update(self.win)
        self.p2.update(self.win)
        self.ball.update(self.win)

        # update paddle movement
        self._move_paddle()

        # update collision with walls and paddles
        self._wall_collision()
        self._paddle_collision()

        # update score
        self._draw_score()
        self._check_game_over()
