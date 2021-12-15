import torch
import random
import numpy as np

from collections import deque
from snake_game import SnakeGame, Direction, Point, BLOCK_SIZE
from model import linear_QNet, Q_Trainer

from helpers import plot

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.random_epsilon = 0  # randomnessrate
        self.discount_gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = linear_QNet(11, 256, 3)  # the number of one state obj is 11
        self.trainer = Q_Trainer(
            self.model, learning_rate=LR, gamma=self.discount_gamma
        )

    def get_state(self, game):
        head = game.snake[0]

        point_right = Point(head.x + BLOCK_SIZE, head.y)
        point_down = Point(head.x, head.y + BLOCK_SIZE)
        point_left = Point(head.x - BLOCK_SIZE, head.y)
        point_up = Point(head.x, head.y - BLOCK_SIZE)

        direction_right = game.direction == Direction.RIGHT
        direction_down = game.direction == Direction.DOWN
        direction_left = game.direction == Direction.LEFT
        direction_up = game.direction == Direction.UP

        state = [
            # Danger when the snake goes straight
            (direction_right and game.is_collision(point_right))
            or (direction_down and game.is_collision(point_down))
            or (direction_left and game.is_collision(point_left))
            or (direction_up and game.is_collision(point_up)),
            # Danger when the snake turns right
            (direction_right and game.is_collision(point_down))
            or (direction_down and game.is_collision(point_left))
            or (direction_left and game.is_collision(point_up))
            or (direction_up and game.is_collision(point_right)),
            # Danger when the snake turns left
            (direction_right and game.is_collision(point_up))
            or (direction_down and game.is_collision(point_right))
            or (direction_left and game.is_collision(point_down))
            or (direction_up and game.is_collision(point_left)),
            # Current direction
            direction_right,  # right
            direction_down,  # down
            direction_left,  # left
            direction_up,  # up
            # Food direction
            game.food.x > game.head.x,  # food right
            game.food.y > game.head.y,  # food down
            game.food.x < game.head.x,  # food left
            game.food.y < game.head.y,  # food up
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, state_next, done):
        self.memory.append([state, action, reward, state_next, done])

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            sample = self.memory

        states, actions, rewards, state_nexts, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, state_nexts, dones)

    def train_short_memory(self, state, action, reward, state_next, done):
        self.trainer.train_step(state, action, reward, state_next, done)

    def get_action(self, state):
        self.random_epsilon = 70 - self.n_games
        next_move = [0, 0, 0]

        if random.randint(0, 200) < self.random_epsilon:
            next_move_idx = random.randint(0, 2)
            next_move[next_move_idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            next_move_idx = torch.argmax(prediction).item()

            next_move[next_move_idx] = 1

        return next_move


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

        # get next move
        next_move = agent.get_action(state_current)

        # perform next move and get new state
        reward, done, score = game.play_step(next_move)
        state_next = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_current, next_move, reward, state_next, done)

        # remember
        agent.remember(state_current, next_move, reward, state_next, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(
                f"지금까지 한 게임 수 : { agent.n_games }, 이번 게임 점수 : { score }, 지금까지 최대 점수 : { record }"
            )

            # Draw a plot
            episode_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            episode_mean_scores.append(mean_score)

            plot(episode_scores, episode_mean_scores)


if __name__ == "__main__":
    train()
