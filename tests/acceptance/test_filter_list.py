import sys
import unittest

import pexpect
from readchar import key


class PublicParams:
    def __init__(self):
        self.choices_map = str.__dict__
        self.choices = sorted(self.choices_map.keys())


PRM = PublicParams()


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class FilterListTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py")
        self.choices = PRM.choices
        self.query = ""
        self.sut.expect(f"{self.choices[0]}.*", timeout=1)

    def _filter_choices(self, query="__"):
        self.query = query
        self.choices = list(filter(lambda x: query in str(x), PRM.choices))

    def _search(self, query="__"):
        self._filter_choices(query)
        self.sut.send(query)
        c = self.choices[0]
        self.sut.expect(f"{c}.*", timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        c = self.choices[0]
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_search_default_input(self):
        self._search()
        self.test_default_input()

    def test_change_selection(self):
        self.sut.send(key.DOWN)
        c = self.choices[1]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_search_change_selection(self):
        self._search()
        self.test_change_selection()

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        c = self.choices[0]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_search_out_of_bounds_up(self):
        self._search("is")
        self.test_out_of_bounds_up()

    def test_out_of_bounds_down(self):
        c = self.choices[-1]
        len_choices = len(self.choices)
        for i in range(len(self.choices) + 2):
            self.sut.send(key.DOWN)
            c = self.choices[min(i, len_choices - 1)]
            self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_search_out_of_bounds_down(self):
        self._search("s")
        self.test_out_of_bounds_down()

    def test_notfound_behaviour(self):
        query = "this_query_does_not_exist"
        self.sut.send(query)
        self.sut.expect(r"\s*$", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{query}'}}.*", timeout=1)

    def test_backspace(self):
        q = "__s"
        self._search(q)
        self._filter_choices(q[:-1])
        self.sut.send(key.BACKSPACE)
        c = self.choices[0]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_backspace_everything(self):
        self._search("__s")
        self.sut.send(key.BACKSPACE * len(self.query))
        self.choices = PRM.choices
        c = self.choices[0]
        self.sut.expect(f"{c}.*", timeout=1)

    def test_ctrl_w(self):
        self._search("__s")
        self.sut.send(key.CTRL_W)
        self.choices = PRM.choices
        c = self.choices[0]
        self.sut.expect(f"{c}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class FilterListCarouselTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py carousel")
        self.choices = PRM.choices
        self.sut.expect(f"{self.choices[0]}.*", timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        c = self.choices[-1]
        self.sut.expect(f"{c}.*", timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)

    def test_out_of_bounds_down(self):
        for i in range(len(self.choices)):
            self.sut.send(key.DOWN)
            # Not looking at what we expect along the way,
            # let the last "expect" check that we got the right result
            self.sut.expect(">.*", timeout=1)
        self.sut.send(key.ENTER)
        c = self.choices[0]
        self.sut.expect(f"{{'attribute': '{c}'}}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class CheckOtherTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py other carousel")
        self.choices = PRM.choices
        self.sut.expect(f"{PRM.choices[0]}", timeout=1)

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
        self.sut.expect(f"{{'attribute': '{self.choices[0]}'}}.*", timeout=1)


@unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
class FilterListTaggedTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn("python examples/filter_list.py tag")
        self.choices = PRM.choices
        self.choices_map = PRM.choices_map
        self.sut.expect(f"{self.choices[0]}.*", timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        c = self.choices[0]
        tag = str(self.choices_map[c])[:5]
        self.sut.expect(f"{{'attribute': '{tag}'}}.*", timeout=1)
