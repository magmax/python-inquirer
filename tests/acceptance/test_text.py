import re
import unittest
import pexpect


class TextTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/text.py')

    def set_name(self, name='foo'):
        self.sut.expect("What's your name.*", timeout=1)
        self.sut.sendline(name)

    def set_surname(self, surname='bar'):
        self.sut.expect("What's your surname.*", timeout=1)
        self.sut.sendline(surname)

    def set_phone(self, phone='123456789'):
        self.sut.expect("What's your phone.*", timeout=1)
        self.sut.sendline(phone)

    def test_default_input(self):
        self.set_name()
        self.set_surname()
        self.set_phone()
        self.sut.expect_list([re.compile(b"'name': 'foo'"),
                              re.compile(b"'surname': 'bar'"),
                              re.compile(b"'phone': '123456789'")],
                             timeout=1)

    def test_invalid_phone(self):
        self.set_name()
        self.set_surname()
        self.set_phone('abcde')
        self.sut.expect('Invalid value.*', timeout=1)
        self.sut.sendline('12345')
        self.sut.expect_list([re.compile(b"'name': 'foo'"),
                              re.compile(b"'surname': 'bar'"),
                              re.compile(b"'phone': '12345'")],
                             timeout=1)
