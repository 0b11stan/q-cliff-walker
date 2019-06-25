from environment import Action
from blueteam.bluemain import *


class AI():
    def __init__(self, env):
        self.env = env
        landform_0 = env.landform
        self.calculated_reward_matrix = calculate_reward_matrix(landform_0)
        self.calculated_flat_reward_matrix = get_flat_matrix(self.calculated_reward_matrix)
        self.calculated_transition_matrix = calculate_transition_matrix(landform_0)
        self.calculated_valid_actions_matrix = calculate_valid_actions_matrix(self.calculated_transition_matrix)
        self.calculated_lava_states_matrix = get_lava_states_matrix(landform_0)
        self.calculated_goal_states_matrix = get_goal_states_matrix(landform_0)

    def learn(self, steps, display=None):
        launch_qlearning(
                self.env,
                self.calculated_reward_matrix,
                self.calculated_transition_matrix,
                self.calculated_valid_actions_matrix,
                self.calculated_lava_states_matrix,
                self.calculated_goal_states_matrix,
                self.calculated_flat_reward_matrix
        )
