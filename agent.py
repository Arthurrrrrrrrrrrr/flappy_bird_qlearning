import torch
import random
import pygame
import sys
import numpy as np
from collections import deque #must be installed
from model import Linear_QNet, QTrainer
from game import GameAI

MAX_GAMES = 1000
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        #self.game_env = GameAI()
        self.n_games = 0
        self.epsilon = 0  # Initial exploration rate (will decay over time)
        self.gamma = 0    # Discount rate for future rewards
        self.input_size = 7
        self.hidden_size = 256
        self.output_size = 2

        # Initialize the Q-learning model and the QTrainer
        self.model = Linear_QNet(self.input_size, self.hidden_size, self.output_size)  # Input and output size should be defined accordingly
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  # Define the learning rate as needed

        self.memory = deque(maxlen=MAX_MEMORY) # popleft()

    def get_state(self, game):
        # Implement this function to obtain the current state from the game environment
        # It should return the inputs needed for the Q-learning agent (e.g., distances, speeds, etc.)
        state = game.get_game_state()
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        # Store the state, action, reward, and next state in memory for experience replay
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Implement the logic to select the action based on the current state
        # You can use an exploration strategy (e.g., epsilon-greedy) to balance exploration and exploitation
        # Return the action (as an index or label) predicted by the Q-learning model
                # random moves: tradeoff exploration / exploitation
        prediction = 0
        self.epsilon = 200 - self.n_games
        final_move = [0,0] # [1,0] -> jump, [0,1] -> don't jump
        if random.randint(0, 2000) < self.epsilon:
            move = random.randint(0, 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move, prediction

def train():
    game = GameAI()
    agent = Agent()
    record = 0
    frame_iteration_record = 0
    # Implement the training loop for the Q-learning agent
    # In this function, the agent will play the game, store experiences in memory, and periodically train the model
    game.game_active = True
    while True :
        # Get the current state from the game environment
        state_current = agent.get_state(game)
        old_score = game.score
        # Get the action predicted by the Q-learning model
        action, pred = agent.get_action(state_current)
        # Perform the action in the game environment and receive the reward and next state

        done = game.play_step_bot(action) #-> update_counter -> update score
        game.update_ui()
        new_score = game.score

        state_new= agent.get_state(game)

        if done:
            reward = -10
        # elif new_score < 1:
        #     if 400 < game.vertical_distance_to_bottom < 800:
        #         reward = 10
        #     else:
        #         reward = -10
        elif game.score > old_score:
            reward = 10
        else:
            reward = 0

        print("Game n°: %d" % agent.n_games, "Record: %d" % record)

        # Store the experience in memory for experience replay
        agent.remember(state_current, action, reward, state_new, done)

        # Train the Q-learning model using short memory
        agent.train_short_memory(state_current, action, reward, state_new, done)

        # Check if the game has ended and reset the environment for the next game if needed, save model
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if new_score > record:
                record = new_score
                agent.model.save()

        # Stop training after a certain number of games or when other stopping criteria are met
        if agent.n_games >= MAX_GAMES:
            break

train()