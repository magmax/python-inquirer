import os
import sys
import re
import json
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

with open('examples/test_questions.json') as fd:
    questions = inquirer.load_from_json(fd.read())

answers = inquirer.prompt(questions)

pprint(answers)
