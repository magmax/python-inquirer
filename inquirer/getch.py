# adapted from:
# http://stackoverflow.com/questions/510357/
#   python-read-a-single-character-from-the-user


import sys


try:
    import tty
    import termios
    unix = True
except ImportError:
    import msvcrt
    unix = False


UP = '\x1b\x5b\x41'
DOWN = '\x1b\x5b\x42'
LEFT = '\x1b\x5b\x44'
RIGHT = '\x1b\x5b\x43'
ENTER = '\x0d'
CTRL_C = '\x03'
BACKSPACE = '\x7f'
SPACE = '\x20'


def _getch_unix():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def _getch_windows():
    return msvcrt.getch()


getch = _getch_unix if unix else _getch_windows


def get_key():
    c1 = getch()
    if ord(c1) != 0x1b:
        return c1
    c2 = getch()
    if ord(c2) != 0x5b:
        return c1 + c2
    c3 = getch()
    return c1 + c2 + c3
