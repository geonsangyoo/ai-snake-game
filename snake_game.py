import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font("OpenSans-Regular.ttf", 25)

# colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
EMERALD = (80, 200, 120)

BLOCK_SIZE = 20
SPEED = 50

Point = namedtuple("Point", "x, y")


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        # init caption
        pygame.display.set_caption("뱀 게임 테스트")

        # reset game
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        # start point > x, y coordinates
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (BLOCK_SIZE * 2), self.head.y),
        ]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(
                self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                self.display, EMERALD, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        new_direction = None

        if np.array_equal(action, [1, 0, 0]):  # straight
            new_direction = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):  # right turn (clockwise)
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx]
        else:  # [0, 0, 1] # left turn (anti-clockwise)
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        else:
            pass

        self.head = Point(x, y)

    def is_collision(self, point=None):
        if point is None:
            point = self.head

        # the user hits boundary of wall
        if (
            point.x > self.w - BLOCK_SIZE
            or point.x < 0
            or point.y > self.h - BLOCK_SIZE
            or point.y < 0
        ):
            return True

        # the user hits on part of the snake body
        if self.head in self.snake[1:]:
            return True

        return False

    def play_step(self, action):
        self.frame_iteration += 1

        # # 1. check user input
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             self.direction = Direction.LEFT
        #         elif event.key == pygame.K_RIGHT:
        #             self.direction = Direction.RIGHT
        #         elif event.key == pygame.K_UP:
        #             self.direction = Direction.UP
        #         elif event.key == pygame.K_DOWN:
        #             self.direction = Direction.DOWN
        #         else:
        #             pass

        # 2. move forward
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if user's play is over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > len(self.snake) * 500:
            game_over = True
            reward -= 10
            return reward, game_over, self.score

        # 4. place new food
        if self.head == self.food:
            reward = 10
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update UI and Clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. game over and return score
        return reward, game_over, self.score
