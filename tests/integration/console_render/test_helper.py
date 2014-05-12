import sys
import unittest

from . import helper


class BaseTestCaseTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_stdin_mocking(self):
        self.set_input('foo')

        self.assertEqual('foo', sys.stdin.read())

    def test_assertOutputContains(self):
        print('foo')

        self.assertInStdout('foo')
