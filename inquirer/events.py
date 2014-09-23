import readchar


class Event(object):
    pass


class KeyPressed(Event):
    def __init__(self, value):
        self.value = value


class Repaint(Event):
    pass


class KeyEventGenerator(object):
    def __init__(self, key_generator=None):
        self._key_gen = readchar.readkey

    def next(self):
        return KeyPressed(self._key_gen())
