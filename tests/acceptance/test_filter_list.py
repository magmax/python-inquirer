import sys
import unittest

import inquirer
from inquirer.render.console.base import MAX_OPTIONS_DISPLAYED_AT_ONCE


import pexpect
from readchar import key


CHOICES = list(inquirer.__dict__.keys())
CHOICES.sort()


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ListTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py")
        self.sut.expect(CHOICES[3], timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        c = CHOICES[0]
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_change_selection(self):
        self.sut.send(key.DOWN)
        c = CHOICES[1]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        c = CHOICES[0]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_out_of_bounds_down(self):
        c = CHOICES[-1]
        for i in range(len(CHOICES)+2):
            self.sut.send(key.DOWN)
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ListCarouselTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py carousel")
        self.sut.expect(CHOICES[MAX_OPTIONS_DISPLAYED_AT_ONCE-1], timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        c = CHOICES[-1]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_out_of_bounds_down(self):
        for i in range(len(CHOICES)):
            self.sut.send(key.DOWN)
            # Not looking at what we expect along the way,
            # let the last "expect" check that we got the right result
            self.sut.expect(">.*", timeout=1)
        self.sut.send(key.ENTER)
        c = CHOICES[0]
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckOtherTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py other carousel")
        self.sut.expect(CHOICES[MAX_OPTIONS_DISPLAYED_AT_ONCE-1], timeout=1)
        #self.sut.expect(f"Standard.*", timeout=1)

    def test_other_input(self):
        self.sut.send(key.UP)
        self.sut.expect(r"\+ Other.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r": ", timeout=1)
        self.sut.send("Hello world")
        self.sut.expect(r"Hello world", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'attribute': 'Hello world'}.*", timeout=1)

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
        self.sut.expect("{'attribute': 'Hello world'}.*", timeout=1)

    def test_other_select_choice(self):
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{CHOICES[0]}'}}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class ListTaggedTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/list_tagged.py")
        self.sut.expect("Micro.*", timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'xxl'}.*", timeout=1)
