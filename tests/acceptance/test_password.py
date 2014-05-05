import unittest
import pexpect
from inquirer.getch import DOWN, UP, ENTER, BACKSPACE


class PasswordTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/password.py')

    def test_default_input(self):
        self.sut.expect("What's your password.*", timeout=1)
        self.sut.send('abcde')
        self.sut.send(ENTER)
        self.sut.expect("{'password': 'abcde'}", timeout=1)

    def test_backspace(self):
        self.sut.expect("What's your password.*", timeout=1)
        self.sut.send('abcde')
        self.sut.send(BACKSPACE)
        self.sut.send(ENTER)
        self.sut.expect("{'password': 'abcd'}", timeout=1)

    def test_backspace_limit(self):
        self.sut.expect("What's your password.*", timeout=1)
        self.sut.send('a')
        self.sut.send(BACKSPACE)
        self.sut.send(BACKSPACE)
        self.sut.send('b')
        self.sut.send(ENTER)
        self.sut.expect("{'password': 'b'}", timeout=1)
