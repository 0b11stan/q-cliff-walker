import os
import time
import matplotlib.pyplot as plt

from environment import Map, Environment
from redteam.ai import AI as RED
from blueteam.ai import AI as BLUE


class Shell():
    def __init__(self):
        self.landform = [
            [Map.LAND, Map.START, Map.LAND,   Map.DANGER],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.LAND],
            [Map.LAND, Map.DANGER,  Map.DANGER, Map.LAND],
            [Map.LAND, Map.DANGER,  Map.DANGER, Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.DANGER],
            [Map.GOAL, Map.LAND,  Map.LAND,   Map.DANGER]
        ]
        self.env = Environment(self.landform)
        self.position = [0, 0]
        self.step_reward = 0
        self.step_rewards = []

    def display(self, reward, action, done, title="## MAP ##"):
        os.system("clear")
        self.display_landform(reward, action, done, title)

        self.step_reward += reward
        if(reward == Map.GOAL.get_reward()):
            self.step_rewards.append([Map.GOAL.name, self.step_reward])
            self.step_reward = 0
        elif(reward == Map.DANGER.get_reward()):
            self.step_rewards.append([Map.DANGER.name, self.step_reward])
            self.step_reward = 0

        time.sleep(0.05)

    def display_landform(self, reward, action, done, title):
        col_num = (self.env.COLS * 2) - 1
        print(title)
        print("+{}+".format("-" * col_num))
        for y, row in enumerate(self.env.landform):
            to_display = ""
            for x, land in enumerate(row):
                if self.env.position[0] == x and self.env.position[1] == y:
                    to_display += "X"
                elif land == Map.LAND:
                    to_display += " "
                elif land == Map.DANGER:
                    to_display += "+"
                elif land == Map.GOAL:
                    to_display += "O"
                else:
                    to_display += "x"
                if x+1 != len(row):
                    to_display += " "
            print("|{}|".format(to_display))
        print("+{}+".format("-" * col_num))
        print("reward: {}".format(reward))
        print("action: {}".format(action.name))
        print("done: {}".format(done))

    def plot_global_reward(self):
        rewards_value = list(map(lambda x: x[1], self.step_rewards))
        plt.plot(rewards_value, '-k', linewidth=0.5)
        for index, reward in enumerate(self.step_rewards):
            if(reward[0] == Map.GOAL.name):
                plt.plot(index, reward[1], 'g^')
            elif(reward[0] == Map.DANGER.name):
                plt.plot(index, reward[1], 'rv')
        plt.ylabel('Score')
        plt.ylabel('Steps')
        plt.show()

    def mainloop(self, blue, red):
        if blue:
            print("## BLUE ##")
            BLUE(self.env).learn(100, self.display)
            self.plot_global_reward()
        elif red:
            print("## RED ##")
            RED(self.env).learn(100, self.display)
            self.plot_global_reward()
        else:
            exit("No team provided")
