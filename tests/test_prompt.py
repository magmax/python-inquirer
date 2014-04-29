import unittest

from inquirer import prompt

class PromtTests(unittest.TestCase):
    def test_prompt_returns_a_hash(self):
        self.assertEquals({}, prompt([]))
