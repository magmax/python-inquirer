import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.Checkbox('interests',
                      message="What are you interested in?",
                      choices=[
                          ('Computers', 'c'),
                          ('Books', 'b'),
                          ('Science', 's'),
                          ('Nature', 'n'),
                          ('Fantasy', 'f'),
                          ('History', 'h'),
                      ],
                      default=['c', 'b']),
]

answers = inquirer.prompt(questions)

pprint(answers)
