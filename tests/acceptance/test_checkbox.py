import sys
import unittest
from re import escape

import pexpect
from readchar import key

from inquirer.themes import Default as Theme


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/checkbox.py")
        self.sut.expect("History.*", timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books'\]}.*", timeout=1)  # noqa

    def test_select_the_third(self):
        self.sut.send(key.DOWN)
        self.sut.send(key.DOWN)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books', 'Science'\]}.*", timeout=1)  # noqa

    def test_select_one_more(self):
        self.sut.send(key.DOWN)
        self.sut.send(key.DOWN)
        self.sut.send(key.SPACE)
        self.sut.send(key.DOWN)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books', 'Science', 'Nature'\]}.*", timeout=1)  # noqa

    def test_unselect(self):
        self.sut.send(key.SPACE)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Books', 'Computers'\]}.*", timeout=1)  # noqa

    def test_select_with_arrows(self):
        self.sut.send(key.DOWN)
        self.sut.send(key.DOWN)
        self.sut.send(key.RIGHT)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books', 'Science'\]}.*", timeout=1)  # noqa

    def test_unselect_with_arrows(self):
        self.sut.send(key.DOWN)
        self.sut.send(key.LEFT)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers'\]}.*", timeout=1)  # noqa

    def test_select_last(self):
        for i in range(10):
            self.sut.send(key.DOWN)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books', 'History'\]}.*", timeout=1)  # noqa


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckCarouselTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/checkbox_carousel.py")
        self.sut.expect("Computers.*", timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        self.sut.expect("History.*", timeout=1)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books', 'History'\]}.*", timeout=1)  # noqa

    def test_out_of_bounds_down(self):
        for i in range(6):
            self.sut.send(key.DOWN)
            # Not looking at what we expect along the way,
            # let the last "expect" check that we got the right result
            self.sut.expect(">.*", timeout=1)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Books'\]}.*", timeout=1)  # noqa


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckOtherTest(unittest.TestCase):
    def setUp(self):
        self.theme = Theme()
        self.sut = pexpect.spawn("python examples/checkbox_other.py")
        self.sut.expect("Computers.*", timeout=1)

    def test_other_input(self):
        self.sut.send(key.UP)
        self.sut.expect(r"\+ Other.*", timeout=1)
        self.sut.send(key.SPACE)
        self.sut.expect(r": ", timeout=1)
        self.sut.send("Hello world")
        self.sut.expect(r"Hello world.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(rf"> {escape(self.theme.Checkbox.selected_icon)} Hello world[\s\S]*\+ Other.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books', 'Hello world'\]}", timeout=1)  # noqa

    def test_other_blank_input(self):
        self.sut.send(key.UP)
        self.sut.expect(r"\+ Other.*", timeout=1)
        self.sut.send(key.SPACE)
        self.sut.expect(r": ", timeout=1)
        self.sut.send(key.ENTER)  # blank input
        self.sut.expect(r"> \+ Other.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Computers', 'Books'\]}", timeout=1)  # noqa

    def test_other_select_choice(self):
        self.sut.send(key.SPACE)
        self.sut.expect(rf"{escape(self.theme.Checkbox.unselected_icon)} Computers.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(r"{'interests': \['Books'\]}", timeout=1)  # noqa


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckWithTaggedValuesTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/checkbox_tagged.py")
        self.sut.expect("History.*", timeout=1)

    def test_default_selection(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'interests': ", timeout=1)
