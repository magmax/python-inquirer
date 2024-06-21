import os
import sys
from pprint import pprint

import inquirer


sys.path.append(os.path.realpath("."))

questions = [
    inquirer.Path("path", message="Give me some any type of path"),
    inquirer.Path("directory", path_type=inquirer.Path.DIRECTORY, message="Give me directory"),
    inquirer.Path("file", path_type=inquirer.Path.FILE, message="Give me file"),
    inquirer.Path(
        "existing_file",
        path_type=inquirer.Path.FILE,
        exists=True,
        message="Give me existing file",
    ),
    inquirer.Path(
        "existing_dir",
        path_type=inquirer.Path.DIRECTORY,
        exists=True,
        message="Give me existing dir",
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
