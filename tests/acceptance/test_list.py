import sys
import unittest

import pexpect
from readchar import key


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ListTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/list.py")
        self.sut.expect("Micro.*", timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)

    def test_change_selection(self):
        self.sut.send(key.DOWN)
        self.sut.expect("Micro.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Large'}.*", timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        self.sut.expect("Micro.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)

    def test_out_of_bounds_down(self):
        for i in range(10):
            self.sut.send(key.DOWN)
            self.sut.expect("Micro.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Micro'}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ListCarouselTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/list_carousel.py")
        self.sut.expect("Standard.*", timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        self.sut.expect("Standard.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Standard'}.*", timeout=1)

    def test_out_of_bounds_down(self):
        for i in range(3):
            self.sut.send(key.DOWN)
            # Not looking at what we expect along the way,
            # let the last "expect" check that we got the right result
            self.sut.expect(">.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckOtherTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/list_other.py")
        self.sut.expect("Standard.*", timeout=1)

    def test_other_input(self):
        self.sut.send(key.UP)
        self.sut.expect(r"\+ Other.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r": ", timeout=1)
        self.sut.send("Hello world")
        self.sut.expect(r"Hello world", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Hello world'}.*", timeout=1)

    def test_other_blank_input(self):
        self.sut.send(key.UP)
        self.sut.expect(r"\+ Other.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r": ", timeout=1)
        self.sut.send(key.ENTER)  # blank input
        self.sut.expect(r"\+ Other.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r": ", timeout=1)
        self.sut.send("Hello world")
        self.sut.expect(r"Hello world", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Hello world'}.*", timeout=1)

    def test_other_select_choice(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ListTaggedTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/list_tagged.py")
        self.sut.expect("Micro.*", timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'xxl'}.*", timeout=1)
