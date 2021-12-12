import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font("OpenSans-Regular.ttf", 25)
# font = pygame.font.SysFont('arial.ttf', 25)


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


# colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 40

Point = namedtuple("Point", "x, y")


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
        self.head = Point(self.w // 2, self.h // 2)
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

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def play_step(self):
        # 1. check user input

        # 2. move forward

        # 3. check if user wants to get the game over

        # 4. place new food

        # 5. update UI and Clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. game over and return score
        game_over = False
        return game_over, self.score


if __name__ == "__main__":
    game = SnakeGame()

    # start loop
    while True:
        game_over, score = game.play_step()

        # go to exit if game is over
        if game_over is True:
            break

    print("Final Score", score)

    pygame.quit()
