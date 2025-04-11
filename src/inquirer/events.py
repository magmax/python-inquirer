from typing import Callable, Optional

import readchar


class Event:
    pass


class KeyPressed(Event):
    def __init__(self, value: str):
        self.value = value


class Repaint(Event):
    pass


class KeyEventGenerator:
    def __init__(self, key_generator: Optional[Callable[[], str]] = None):
        self._key_gen = key_generator or readchar.readkey

    def next(self) -> Event:
        return KeyPressed(self._key_gen())
