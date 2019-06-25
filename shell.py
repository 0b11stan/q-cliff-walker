import os

from environment import Map, Environment
from redteam.ai import AI as RED
from blueteam.ai import AI as BLUE


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
        self.position = [0, 0]

    def display(self, reward, action, done, title="## MAP ##"):
        os.system("clear")
        self.display_landform(reward, action, done, title)
        import time
        #time.sleep(0.2)

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
        if reward == 100: exit("win")

    def mainloop(self, blue, red):
        if blue:
            print ("## BLUE ##")
            BLUE(self.env).learn(100, self.display)
        if red:
            print ("## RED ##")
            RED(self.env).learn(100, self.display)
