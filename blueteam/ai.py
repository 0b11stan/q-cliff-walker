from environment import Action
from blueteam.bluemain import *


class AI():
    def __init__(self, env):
        self.env = env
        self.calculated_reward_matrix = calculate_reward_matrix(env.landform)
        self.calculated_transition_matrix = calculate_transition_matrix(env.landform)
        self.calculated_valid_actions_matrix = calculate_valid_actions_matrix(self.calculated_transition_matrix)
        self.calculated_lava_states_matrix = get_lava_states_matrix(env.landform)
        self.calculated_goal_states_matrix = get_goal_states_matrix(env.landform)

    def learn(self, episodes, display=None):
        launch_qlearning(
                self.env,
                episodes,
                display,
                self.calculated_reward_matrix,
                self.calculated_transition_matrix,
                self.calculated_valid_actions_matrix,
                self.calculated_lava_states_matrix,
                self.calculated_goal_states_matrix
        )
