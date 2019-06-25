import numpy as np
from enum import Enum
from environment import Action, get_state


class AI():
    def __init__(self, env, endeavours_bias=0.1, longterm_satisfaction_bias=0.9):
        self.endeavours_bias = endeavours_bias
        self.longterm_satisfaction_bias = longterm_satisfaction_bias
        self.env = env
        num_states = env.COLS * env.ROWS
        num_actions = len(Action.all())
        self.qvalues = np.zeros((num_states, num_actions))

    def learn(self, steps, display=None):
        for _ in range(steps):
            self.env.reset()
            done = False
            while not done:
                action = self.choose_action()
                previous_qvalues = self.qvalues[self.get_state()]
                reward, done = self.env.step(action)
                current_qvalues = self.qvalues[self.get_state()]
                previous_qvalues[action.value] = reward + \
                    (self.longterm_satisfaction_bias * np.max(current_qvalues))
                display(reward, action, done)

    def choose_action(self):
        if np.random.random() < self.endeavours_bias:
            return np.random.choice(Action.all())
        else:
            return Action.all()[np.argmax(self.qvalues[self.get_state()])]

    def get_state(self):
        return get_state(self.env.position, self.env.COLS)
