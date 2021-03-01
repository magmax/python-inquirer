import inquirer
from inquirer.themes import GreenPassion

q = [
    inquirer.Text("name", message="Whats your name?", default="No one"),
    inquirer.List("jon", message="Does Jon Snow know?", choices=["yes", "no"], default="no"),
    inquirer.Checkbox(
        "kill_list", message="Who you want to kill?", choices=["Cersei", "Littlefinger", "The Mountain"]
    ),
]

inquirer.prompt(q, theme=GreenPassion())
