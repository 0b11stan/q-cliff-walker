import unittest
from environment import Environment, Map, Action
from ai import AI

class TestAI(unittest.TestCase):
    def test_choose_action(self):
        env = Environment([[Map.START, Map.GOAL]])
        ai = AI(env)
        action = ai.choose_action()
        self.assertTrue(action in Action.all())

    def test_compute_state(self):
        env = Environment([[Map.START, Map.GOAL]])
        env.step(Action.RIGHT)
        ai = AI(env)
        state = ai.get_state()
        self.assertEqual(1, state)

