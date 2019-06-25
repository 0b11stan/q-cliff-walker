# Simple implementation of the Qlearning algorithm
# inspired by Minecraft Cliffwalking.
# S.Marchal - 2019
#
#
# s = spawn
# e = empty
# l = lava
# d = diamond
#
# Possible actions are in order (for the reward matrix columns):
#   Up(U):0, Down(D):1, Left(L):2, Right(R):3
#
# Rewards:
# - stepping on empty cell: -1
# - staying on the same cell: -1
# - stepping on lava cell: -10
# - stepping on diamond: +10
#
# Starting reward is -1
#

import numpy as np
import random

from environment import Action, Map, Environment, get_state


def calculate_reward_matrix(playground):
    reward_matrix = []
    # iterate over rows
    for i in range(0, len(playground)):
        # iterate over columns
        for j in range(0, len(playground[i])):
            reward_row = []
            # UP
            if 0 <= i - 1 <= len(playground):
                reward_row.append(playground[i - 1][j].get_reward())
            else:
                reward_row.append(0)
            # DOWN
            if 0 <= i + 1 < len(playground):
                reward_row.append(playground[i + 1][j].get_reward())
            else:
                reward_row.append(0)
            # LEFT
            if 0 <= j - 1 < len(playground[i]):
                reward_row.append(playground[i][j - 1].get_reward())
            else:
                reward_row.append(0)
            # RIGHT
            if 0 <= j + 1 < len(playground[i]):
                reward_row.append(playground[i][j + 1].get_reward())
            else:
                reward_row.append(0)
            reward_matrix.append(reward_row)
    return reward_matrix


def calculate_transition_matrix(playground):
    transition_matrix = []
    # iterate over rows
    for i in range(0, len(playground)):
        # iterate over columns
        for j in range(0, len(playground[i])):
            transition_row = []
            # UP
            if 0 <= i - 1 <= len(playground):
                transition_row.append(((i - 1) * len(playground[i])) + j)
            else:
                transition_row.append(-1)
            # DOWN
            if 0 <= i + 1 < len(playground):
                transition_row.append(((i + 1) * len(playground[i])) + j)
            else:
                transition_row.append(-1)
            # LEFT
            if 0 <= j - 1 < len(playground[i]):
                transition_row.append((i * len(playground[i])) + j - 1)
            else:
                transition_row.append(-1)
            # RIGHT
            if 0 <= j + 1 < len(playground[i]):
                transition_row.append((i * len(playground[i])) + j + 1)
            else:
                transition_row.append(-1)

            transition_matrix.append(transition_row)
    return transition_matrix


def calculate_valid_actions_matrix(transition_matrix):
    # iterate over rows
    valid_actions_matrix = []
    for i in range(0, len(transition_matrix)):
        valid_action_row = []
        for j in range(0, len(transition_matrix[i])):
            if transition_matrix[i][j] != -1:
                valid_action_row.append(j)
        valid_actions_matrix.append(valid_action_row)
    return valid_actions_matrix

def get_lava_states_matrix(playground):
    lava_states_matrix = []
    for i in range(0, len(playground)):
        for j in range(0, len(playground[i])):
            if playground[i][j] == Map.DANGER:
                lava_states_matrix.append((i * len(playground[i])) + j)
    return lava_states_matrix


def get_goal_states_matrix(playground):
    goal_states_matrix = []
    for i in range(0, len(playground)):
        for j in range(0, len(playground[i])):
            if playground[i][j] == Map.GOAL:
                goal_states_matrix.append((i * len(playground[i])) + j)
    return goal_states_matrix


def is_lava_or_goal(state, lava_states_matrix, goal_states_matrix):
    if state in lava_states_matrix or state in goal_states_matrix:
        return True
    else:
        return False


def get_flat_matrix(matrix):
    flat_matrix = []
    for i in range(0, len(matrix)):
        flat_matrix.append(matrix[i])
    return flat_matrix

def get_next_action(state, flat_q_matrix, calculated_valid_actions_matrix, stepratio, random_choice_rate=0.1):
    if(stepratio <= 1.3):
        random_choice_rate /= 8
    elif(stepratio <= 2 ):
        random_choice_rate /= 4
    if(np.random.random() < random_choice_rate):
        return random.choice(calculated_valid_actions_matrix[state])
    else:
        max_val = max(flat_q_matrix[state])
        indexes = [index for index, x in enumerate(flat_q_matrix[state]) if x == max_val]
        index = random.choice(indexes)
        if(index in calculated_valid_actions_matrix[state]):
            return index
        else:
            return random.choice(calculated_valid_actions_matrix[state])

def launch_qlearning(
        env,
        episodes,
        display,
        calculated_reward_matrix,
        calculated_transition_matrix,
        calculated_valid_actions_matrix,
        calculated_lava_states_matrix,
        calculated_goal_states_matrix
):
    # Iinitalisation de la qmatrix avec des 0
    # (Nombres de cases sur la carte, nombre d'actions possibles)
    q_matrix = np.zeros((env.COLS * env.ROWS, 4))
    gamma = 0.8
    for step in range(episodes):
        env.reset()
        start_state = get_state(env.position, env.COLS)
        future_rewards = []
        current_state = start_state
        # While diamond or lava not found
        while not is_lava_or_goal(current_state, calculated_lava_states_matrix, calculated_goal_states_matrix):
            action = get_next_action(current_state, get_flat_matrix(q_matrix), calculated_valid_actions_matrix, (episodes / (step + 1)))
            next_state = calculated_transition_matrix[current_state][action]
            future_rewards.append(q_matrix[next_state][get_next_action(next_state, get_flat_matrix(q_matrix), calculated_valid_actions_matrix, (episodes / (step + 1)))])
            # Bellman Equation
            q_state = calculated_reward_matrix[current_state][action] + gamma * max(future_rewards)
            q_matrix[current_state][action] = q_state
            reward, done = env.step(Action(action))
            display(calculated_reward_matrix[current_state][action], Action(action), done, "## {} ##".format(step))
            current_state = next_state

    #print("Final q_matrix : ")
    #print(q_matrix)
