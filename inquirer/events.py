import readchar


class Event(object):
    pass


class KeyPressed(Event):
    def __init__(self, value):
        self.value = value


class Repaint(Event):
    pass


class KeyEventGenerator(object):
    def next(self):
        return KeyPressed(readchar.readkey())
