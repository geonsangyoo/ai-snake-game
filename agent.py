import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGame, Direction, Point

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.random_epsilon = 0  # randomnessrate
        self.discount_gamma = 0  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)

        # TODO: model, trainer

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass


def train():
    episode_scores = []
    episode_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()

    while True:
        # get current state
        state_current = agent.get_state(game)


if __name__ == "__main__":
    train()
