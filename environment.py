from enum import Enum, unique
import matplotlib.pyplot as plt

def fill_row(length, row, land):
    while len(row) < length:
        row.append(Map.DANGER)
    row.insert(0, Map.DANGER)
    row.append(Map.DANGER)


def get_max_rows(landform):
    return len(landform)


def get_max_cols(landform):
    return max([len(row) for row in landform])

def get_state(coordinates, cols):
    X, Y = 0, 1
    return coordinates[X] + (coordinates[Y] * cols)

def plot_global_award(awards):
    awards_value = list(map(lambda x: x[1], awards))
    plt.plot(awards_value, '-k', linewidth=0.5)
    for index,award in enumerate(awards):
        if(award[0] == Map.GOAL.name):
            plt.plot(index, award[1], 'g^')
        elif(award[0] == Map.DANGER.name):
            plt.plot(index, award[1], 'rv')
    plt.ylabel('Score')
    plt.ylabel('Steps')
    plt.show()


@unique
class Map(Enum):
    LAND = 0
    START = 1
    GOAL = 2
    DANGER = 3

    def get_reward(self):
        if self == self.LAND:
            return -1
        elif self == self.START:
            return -1
        elif self == self.GOAL:
            return 0
        elif self == self.DANGER:
            return -100


@unique
class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def all():
        return [a for a in Action]


class Environment():
    def __init__(self, landform):
        self.position = None
        self.start_position = None
        self.goal_position = None
        self.reward_map = []
        self.landform = landform

        tmp_length = get_max_cols(landform)
        self._add_top_and_bottom_borders()

        for row_index, row in enumerate(self.landform):
            self.reward_map.append([])
            fill_row(tmp_length, row, Map.DANGER)
            for col_index, col in enumerate(row):
                self.reward_map[row_index].append(col.get_reward())
                self._register_common_positions(col, col_index, row_index)

        if self.start_position == None:
            exit("Starting land not found in landform.")
        elif self.goal_position == None:
            exit("A goal is expected in the provided landform.")

        self.ROWS = get_max_rows(self.landform)
        self.COLS = get_max_cols(self.landform)
        self.reset()


    def _register_common_positions(self, land, x, y):
        if land == Map.START:
            self.start_position = [x, y]
        elif land == Map.GOAL:
            self.goal_position = [x, y]

    def _add_top_and_bottom_borders(self):
        border = [Map.DANGER for _ in range(get_max_cols(self.landform))]
        self.landform.insert(0, border.copy())
        self.landform.append(border.copy())

    def step(self, action):
        X, Y = 0, 1
        if action == Action.UP:
            self.position[Y] -= 1
        elif action == Action.DOWN:
            self.position[Y] += 1
        elif action == Action.LEFT:
            self.position[X] -= 1
        elif action == Action.RIGHT:
            self.position[X] += 1
        done = False
        reward = self.reward_map[self.position[Y]][self.position[X]]
        win = self.position == self.goal_position
        loose = self.landform[self.position[Y]][self.position[X]] == Map.DANGER
        done = True if win or loose else False
        return (reward, done)

    def reset(self):
        self.position = self.start_position.copy()
