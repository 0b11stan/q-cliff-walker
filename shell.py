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
        self.episode_reward = 0
        self.episode_rewards = []
        self.step_tachometer = time.time()
        self.step_tachometers = []
        self.deaths = 0
        self.wins = 0

    def display(self, reward, action, done, title="## MAP ##"):
        os.system("clear")
        self.display_landform(reward, action, done, title)

        self.episode_reward += reward
        if(reward == Map.GOAL.get_reward()):
            self.episode_rewards.append([Map.GOAL.name, self.episode_reward])
            self.episode_reward = 0
            self.wins += 1
        elif(reward == Map.DANGER.get_reward()):
            self.episode_rewards.append([Map.DANGER.name, self.episode_reward])
            self.episode_reward = 0
            self.deaths += 1

        time.sleep(0.05)
        self.step_tachometers.append(time.time() - self.step_tachometer - 0.05)
        self.step_tachometer = time.time()

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

    def plot_global_reward(self, team):
        rewards_value = list(map(lambda x: x[1], self.episode_rewards))
        plt.subplot(2, 2, 1)
        plt.title(team)
        plt.plot(rewards_value, '-k', linewidth=0.5)
        for index, reward in enumerate(self.episode_rewards):
            if(reward[0] == Map.GOAL.name):
                plt.plot(index, reward[1], 'g^')
            elif(reward[0] == Map.DANGER.name):
                plt.plot(index, reward[1], 'rv')
        plt.ylabel('Score')
        plt.xlabel('Episodes')

    def plot_tachometers(self):
        plt.subplot(2, 2, 2)
        plt.plot(self.step_tachometers, '-k', linewidth=0.5)
        plt.ylabel('Execution Duration')
        plt.xlabel('Player Steps')

    def plot_kda(self):
        plt.subplot(2, 2, 3)
        bar = plt.barh(["Wins", "Deaths"], [self.wins, self.deaths])
        bar[0].set_color('g')
        bar[1].set_color('r')

    def show_plots(self, team):
        self.plot_global_reward(team)
        self.plot_tachometers()
        self.plot_kda()
        plt.show()

    def mainloop(self, blue, red):
        iterations = 100
        if blue:
            print("## BLUE ##")
            BLUE(self.env).learn(iterations, self.display)
            self.show_plots("BLUE")
        elif red:
            print("## RED ##")
            RED(self.env).learn(iterations, self.display)
            self.show_plots("RED")
        else:
            exit("No team provided")
