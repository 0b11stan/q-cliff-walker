from environment import Action
from main import launch_qlearning


class AI():
    def __init__(self, env):
        calculated_reward_matrix = calculate_reward_matrix(playground_0)
        calculated_transition_matrix = calculate_transition_matrix(playground_0)
        calculated_valid_actions_matrix = calculate_valid_actions_matrix(calculated_transition_matrix)
        calculated_lava_states_matrix = get_lava_states_matrix(playground_0)
        calculated_goal_states_matrix = get_goal_states_matrix(playground_0)

        print_matrix(calculated_reward_matrix, "REWARD")
        print_matrix(calculated_transition_matrix, "TRANSITION")
        print_matrix(calculated_valid_actions_matrix, "VALID ACTIONS")

    def learn(self, steps, display=None):
        launch_qlearning(calculated_reward_matrix, calculated_transition_matrix, calculated_valid_actions_matrix)
