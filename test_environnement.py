import unittest
import environment
from environment import Environment, Map, Action


class TestEnvironnemnet(unittest.TestCase):
    def test_environnement_dimensions_computation(self):
        landform = [
            [Map.START, Map.LAND],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.LAND, Map.DANGER],
        ]
        env = Environment(landform)
        self.assertEqual(5, environment.get_max_rows(landform))
        self.assertEqual(5, environment.get_max_cols(landform))
        self.assertEqual(5, env.ROWS)
        self.assertEqual(5, env.COLS)

    def test_row_filling(self):
        landform = [
            [Map.START, Map.LAND],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.LAND, Map.DANGER],
        ]
        test = [Map.LAND]
        environment.fill_row(3, test, Map.DANGER)
        self.assertEqual(
            [Map.DANGER, Map.LAND, Map.DANGER, Map.DANGER, Map.DANGER],
            test
        )


    def test_environnment_landform_filling(self):
        landform = [
            [Map.START, Map.LAND],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.LAND],
        ]
        expected = [
            [Map.DANGER, Map.DANGER, Map.DANGER, Map.DANGER, Map.DANGER],
            [Map.DANGER, Map.START,  Map.LAND,   Map.DANGER, Map.DANGER],
            [Map.DANGER, Map.DANGER, Map.LAND,   Map.GOAL,   Map.DANGER],
            [Map.DANGER, Map.DANGER, Map.LAND,   Map.DANGER, Map.DANGER],
            [Map.DANGER, Map.DANGER, Map.DANGER, Map.DANGER, Map.DANGER]
        ]
        env = Environment(landform)
        self.assertEqual(expected, env.landform)

    def test_reward_map_building(self):
        landform = [
            [Map.START, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.LAND, Map.DANGER],
        ]
        expected = [
            [-100, -100, -100, -100, -100],
            [-100, -1,   -1,   -100, -100],
            [-100, -100, -1,   0,    -100],
            [-100, -100, -1,   -100, -100],
            [-100, -100, -100, -100, -100]
        ]
        env = Environment(landform)
        self.assertEqual(expected, env.reward_map)

    def test_starting_position_is_set(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.START, Map.DANGER],
        ]
        env = Environment(landform)
        self.assertEqual([2, 3], env.position)

    def test_steping_modify_the_position(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.START, Map.DANGER],
        ]
        env = Environment(landform)
        reward, done = env.step(Action.UP)
        self.assertEqual([2, 2], env.position)
        self.assertEqual(-1, reward)
        self.assertFalse(done)

    def test_steping_outside_of_bounds_is_like_danger_zone(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.START, Map.DANGER],
        ]
        env = Environment(landform)
        reward, done = env.step(Action.DOWN)
        self.assertEqual(Map.DANGER.get_reward(), reward)
        self.assertTrue(done)

    def test_steping_on_goal_land(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.START, Map.DANGER],
        ]
        env = Environment(landform)
        reward, done = env.step(Action.UP)
        reward, done = env.step(Action.RIGHT)
        self.assertEqual(Map.GOAL.get_reward(), reward)
        self.assertTrue(done)

    def test_landform_without_starting_point_creation(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.LAND, Map.DANGER],
        ]
        with self.assertRaises(SystemExit):
            env = Environment(landform)

    def test_landform_without_goal(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.LAND],
            [Map.DANGER, Map.START, Map.DANGER],
        ]
        with self.assertRaises(SystemExit):
            env = Environment(landform)

    def test_env_reset(self):
        landform = [
            [Map.LAND, Map.LAND, Map.DANGER],
            [Map.DANGER, Map.LAND, Map.GOAL],
            [Map.DANGER, Map.START, Map.DANGER],
        ]
        env = Environment(landform)
        env.step(Action.UP)
        env.step(Action.UP)
        env.reset()
        self.assertEqual([2, 3], env.position)

    def test_actions(self):
        actions = Action.all()
        self.assertEqual(4, len(actions))

