import os

from environment import Map, Environment
from redteam.ai import AI


class Shell():
    def __init__(self):
        self.landform = [
            [Map.LAND, Map.START, Map.LAND,   Map.DANGER],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND, Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND, Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.LAND],
            [Map.LAND, Map.LAND,  Map.LAND,   Map.DANGER],
            [Map.GOAL, Map.LAND,  Map.LAND,   Map.DANGER]
        ]
        self.env = Environment(self.landform)
        self.ai = AI(self.env)
        self.position = [0, 0]

    def display(self, reward, action):
        os.system("clear")
        self.display_landform(reward, action)
        import time
        time.sleep(0.2)

    def display_landform(self, reward, action):
        col_num = (self.env.COLS * 2) - 1
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

    def mainloop(self):
        self.ai.learn(100, self.display)
