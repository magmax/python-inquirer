import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def fake_key_generator():
    return sys.stdin.read(1)


class BaseTestCase(object):
    def base_setup(self):
        self._base_stdin = sys.stdin
        self._base_stdout = sys.stdout
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

    def set_input(self, stream):
        sys.stdin = StringIO(stream)
