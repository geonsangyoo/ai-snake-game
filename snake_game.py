import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


BLOCK_SIZE = 20
Point = namedtuple("Point", "x", "y")


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        # init caption
        pygame.display.set_caption("蛇ゲーム")

        # init game state
        self.direction = Direction.RIGHT

        # start point > x-coordinate, y-coordinate
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (BLOCK_SIZE * 2), self.head.y),
        ]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        pass


if __name__ == "__main__":
    game = SnakeGame()

    # start loop
    while True:
        game.play_step()

        # go to exit if game is over

    pygame.quit()
