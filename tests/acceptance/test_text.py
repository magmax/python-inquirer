import re
import sys
import unittest
import os

import pexpect
from readchar import key


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class TextTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/text.py")

    def set_name(self, name="foo"):
        self.sut.expect("What's", timeout=1)
        self.sut.sendline(name)

    def set_surname(self, surname="bar"):
        self.sut.expect("What's", timeout=1)
        self.sut.sendline(surname)

    def set_phone(self, phone="123456789"):
        self.sut.expect("What's", timeout=1)
        self.sut.sendline(phone)

    def test_default_input(self):
        self.set_name()
        self.set_surname()
        self.set_phone()
        self.sut.expect_list(
            [re.compile(b"'name': 'foo'"), re.compile(b"'surname': 'bar'"), re.compile(b"'phone': '123456789'")],
            timeout=1,
        )

    def test_invalid_phone(self):
        self.set_name()
        self.set_surname()
        self.set_phone("abcde")
        self.sut.expect("I don't like your phone number!", timeout=1)
        self.sut.sendline(5 * key.BACKSPACE + "12345")
        self.sut.expect_list(
            [re.compile(b"'name': 'foo'"), re.compile(b"'surname': 'bar'"), re.compile(b"'phone': '12345'")], timeout=1
        )


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class TextAutocompleteTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/text_autocomplete.py")

    def test_autocomplete(self):
        self.sut.send("random")
        self.sut.send(key.TAB)
        self.sut.send(key.ENTER)
        self.sut.expect("{'name': '" + os.getlogin() + "'}", timeout=1)
