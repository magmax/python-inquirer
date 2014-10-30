import os
import sys
import re
import json
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

with open('examples/test_questions.json') as fd:
    questions_data = json.loads(fd.read())

questions = [inquirer.load_from_dict(q) for q in questions_data]

answers = inquirer.prompt(questions)

pprint(answers)
