import sys
import unittest
import pexpect
from readchar import key


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ShortcutsTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/shortcuts.py")

    def set_username(self, name="foo"):
        self.sut.expect("Enter your username", timeout=1)
        self.sut.sendline(name)

    def set_password(self, password="secret"):
        self.sut.expect("Please enter your password", timeout=1)
        self.sut.sendline(password)

    def set_checkbox(self):
        self.sut.expect("Please define your type of project", timeout=1)
        self.sut.send(key.ENTER)

    def set_list(self):
        self.sut.expect("Public or private?", timeout=1)
        self.sut.send(key.ENTER)

    def set_confirm(self):
        self.sut.expect("This will delete", timeout=1)
        self.sut.send("y")
        self.sut.send(key.ENTER)

    def test_shortcuts(self):
        self.set_username()
        self.set_password()
        self.set_checkbox()
        self.set_list()
        self.set_confirm()
