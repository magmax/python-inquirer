import readchar
import os

# Workaround for windows arrow keys
if os.name == 'nt':
    from msvcrt import getch
    def winreadkey():
        keypress = getch()
        if keypress == b'\xe0':
            keypress = getch()
        if keypress == b'H':
            return readchar.key.UP
        elif keypress == b'P':
            return readchar.key.DOWN
        elif keypress == b'K':
            return readchar.key.LEFT
        elif keypress == b'M':
            return readchar.key.RIGHT
        elif keypress == b'\r':
            return readchar.key.ENTER
        else:
            return keypress.__str__()
    readkey = winreadkey
else:
    readkey = readchar.readkey

class Event:
    pass


class KeyPressed(Event):
    def __init__(self, value):
        self.value = value


class Repaint(Event):
    pass


class KeyEventGenerator:
    def __init__(self, key_generator=None):
        self._key_gen = key_generator or readkey

    def next(self):
        return KeyPressed(self._key_gen())
