import json
import unittest

from blessed import Terminal

from inquirer import themes
from inquirer import errors


class ThemeTests(unittest.TestCase):
    def setUp(self):
        self.term = Terminal()
        self.theme_dict = {
            "Question": {"mark_color": "red", "brackets_color": "yellow"},
            "List": {"selection_color": "red", "selection_cursor": "->"},
        }
        self.theme_dict_wrong_field = {"Question": {"ark_color": "red"}}
        self.theme_dict_wrong_question = {"questionn": {"mark_color": "red"}}

    def test_load_from_dict(self):
        theme = themes.load_theme_from_dict(self.theme_dict)
        assert theme.Question.mark_color in ["red", "\x1b[31m"]
        assert theme.Question.brackets_color in ["yellow", "\x1b[33m"]
        assert theme.List.selection_color in ["red", "\x1b[31m"]
        assert theme.List.selection_cursor == "->"

    def test_load_from_json(self):
        theme = themes.load_theme_from_json(json.dumps(self.theme_dict))
        assert theme.Question.mark_color in ["red", "\x1b[31m"]
        assert theme.Question.brackets_color in ["yellow", "\x1b[33m"]
        assert theme.List.selection_color in ["red", "\x1b[31m"]
        assert theme.List.selection_cursor == "->"

    def test_invalid_question_field(self):
        with self.assertRaises(errors.ThemeError) as error:
            themes.load_theme_from_dict(self.theme_dict_wrong_field)
        assert "ark_color" in str(error.exception)

    def test_invalid_question(self):
        with self.assertRaises(errors.ThemeError) as error:
            themes.load_theme_from_dict(self.theme_dict_wrong_question)
        assert "questionn" in str(error.exception)
