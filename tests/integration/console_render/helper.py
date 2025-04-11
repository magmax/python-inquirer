import sys


try:
    from StringIO import StringIO  # type: ignore
except ImportError:
    from io import StringIO

from inquirer import events


class Iterable:
    def __init__(self, *args: str):
        self.iterator = args.__iter__()

    def next(self):
        return events.KeyPressed(next(self.iterator))


def event_factory(*args: str):
    return Iterable(*args)


class BaseTestCase:
    def base_setup(self):
        self._base_stdin = sys.stdin
        self._base_stdout = sys.stdout
        sys.stdin = StringIO()
        sys.stdout = StringIO()

    def base_teardown(self):
        sys.stdin = self._base_stdin
        sys.stdout = self._base_stdout

    def printStdout(self):
        sys.stdout.seek(0)
        self._base_stdout.write(sys.stdout.read())

    def assertInStdout(self, message: str):
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertIn(message, stdout)

    def assertNotInStdout(self, message: str):
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertNotIn(message, stdout)
