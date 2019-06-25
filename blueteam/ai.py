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

from environment import Map, Environment

landform_0 = [
            [Map.LAND, Map.START, Map.LAND,   Map.DANGER],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND, Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND, Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.DANGER],
            [Map.GOAL, Map.LAND,  Map.LAND,   Map.DANGER]
        ]

playground_0 = [
    ["START", "LAND", "LAND", "LAND"],
    ["DANGER", "DANGER", "DANGER", "LAND"],
    ["DANGER", "DANGER", "DANGER", "GOAL"],
]

playground_1 = [
    ["DANGER", "START", "DANGER", "DANGER"],
    ["DANGER", "LAND", "LAND", "LAND"],
    ["DANGER", "DANGER", "DANGER", "LAND"],
    ["DANGER", "DANGER", "DANGER", "LAND"],
    ["DANGER", "DANGER", "LAND", "LAND"],
    ["DANGER", "DANGER", "LAND", "DANGER"],
    ["GOAL", "LAND", "LAND", "DANGER"]
]

playground_2 = [
    ['START', 'LAND', 'LAND'],
    ['LAND', 'DANGER', 'LAND'],
    ['LAND', 'GOAL', 'LAND'],
    ['DANGER', 'DANGER', 'LAND'],
    ['DANGER', 'LAND', 'LAND'],
]

playground_3 = [
    ['LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND'],
    ['LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND'],
    ['LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND', 'LAND'],
    ['START', 'DANGER', 'DANGER', 'DANGER', 'DANGER', 'DANGER', 'DANGER', 'GOAL'],
]


def get_reward_for_cell(cell_content):
    if cell_content == "DANGER":
        return -10
    elif cell_content == "GOAL":
        return 10
    elif cell_content == "LAND":
        return -1
    elif cell_content == "START":
        return -1


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


def print_matrix(reward_matrix, matrix_name):
    print("########################################")
    print("#######  " + matrix_name + "  MATRIX     ###########")
    print("########################################")
    for i in range(0, len(reward_matrix)):
        print(reward_matrix[i])
    print("########################################")


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

def get_next_action(state, flat_reward_matrix, calculated_valid_actions_matrix, random_choice_rate=0.1):
    if(np.random.random() < random_choice_rate):
        return random.choice(calculated_valid_actions_matrix[state])
    else:
        index = flat_reward_matrix[state].index(max(flat_reward_matrix[state]))
        if(index in calculated_valid_actions_matrix[state]):
            return index
        else:
            return random.choice(calculated_valid_actions_matrix[state])





calculated_reward_matrix = calculate_reward_matrix(landform_0)
calculated_flat_reward_matrix = get_flat_matrix(calculated_reward_matrix)
calculated_transition_matrix = calculate_transition_matrix(landform_0)
calculated_valid_actions_matrix = calculate_valid_actions_matrix(calculated_transition_matrix)
calculated_lava_states_matrix = get_lava_states_matrix(landform_0)
calculated_goal_states_matrix = get_goal_states_matrix(landform_0)

print_matrix(calculated_reward_matrix, "REWARD")
print_matrix(calculated_transition_matrix, "TRANSITION")
print_matrix(calculated_valid_actions_matrix, "VALID ACTIONS")
# replace 32 by number of cells
# 4 is the number of possible states
def launch_qlearning(calculated_reward_matrix, calculated_transition_matrix, calculated_valid_actions_matrix):
    q_matrix = np.zeros((28, 4))

    gamma = 0.8

    episodes = 1000

    for i in range(episodes):
        # replace starting state depending on playground (TODO code function to automate it)
        start_state = 1
        current_state = start_state
        # While diamond not found
        while not is_lava_or_goal(current_state, calculated_lava_states_matrix, calculated_goal_states_matrix):
            action = get_next_action(current_state, calculated_flat_reward_matrix, calculated_valid_actions_matrix)
            #action = random.choice(calculated_valid_actions_matrix[current_state])
            next_state = calculated_transition_matrix[current_state][action]
            future_rewards = []
            for next_action in calculated_valid_actions_matrix[next_state]:
                future_rewards.append(q_matrix[next_state][next_action])
            q_state = calculated_reward_matrix[current_state][action] + gamma * max(future_rewards)
            q_matrix[current_state][action] = q_state
            print(q_matrix)
            current_state = next_state

    print("Final q_matrix : ")
    print(q_matrix)


launch_qlearning(calculated_reward_matrix, calculated_transition_matrix, calculated_valid_actions_matrix)