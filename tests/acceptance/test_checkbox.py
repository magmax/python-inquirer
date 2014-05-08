import unittest
import pexpect
from readchar import key


class ListTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/checkbox.py')
        self.sut.expect('History.*', timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \[\]}.*", timeout=1)

    def test_select_the_first(self):
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \['Computers'\]}.*", timeout=1)

    def test_select_two(self):
        self.sut.send(key.SPACE)
        self.sut.send(key.DOWN)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \['Computers', 'Books'\]}.*", timeout=1)

    def test_unselect(self):
        self.sut.send(key.SPACE)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \[\]}.*", timeout=1)

    def test_select_with_arrows(self):
        self.sut.send(key.RIGHT)
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \['Computers'\]}.*", timeout=1)

    def test_unselect_with_arrows(self):
        self.sut.send(key.SPACE)
        self.sut.send(key.LEFT)
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \[\]}.*", timeout=1)

    def test_select_last(self):
        for i in range(10):
            self.sut.send(key.DOWN)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': \['History'\]}.*", timeout=1)
