import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def key_factory(*args):
    iterator = args.__iter__()

    def inner():
        return next(iterator)
    return inner


class BaseTestCase(object):
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

    def assertInStdout(self, message):
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertIn(message, stdout)

    def assertNotInStdout(self, message):
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertNotIn(message, stdout)
