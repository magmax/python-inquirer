import os
import sys
import re
from pprint import pprint

import inquirer
from inquirer import errors

sys.path.append(os.path.realpath('.'))


def phone_validation(answers, current):
    if not re.match('\+?\d[\d ]+\d', current):
        raise errors.ValidationError('', reason='I don\'t like your phone number!')

    return True


questions = [
    inquirer.Text('name',
                  message="What's your name?"),
    inquirer.Text('surname',
                  message="What's your surname, {name}?"),
    inquirer.Text('phone',
                  message="What's your phone number",
                  validate=phone_validation,
                  )
]

answers = inquirer.prompt(questions)

pprint(answers)
