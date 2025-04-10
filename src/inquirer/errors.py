from typing import Any, Optional


class ValidationError(Exception):
    def __init__(self, value: Any, reason: Optional[str] = None, *args: Any):
        super().__init__(*args)
        self.value = value
        self.reason = reason


class UnknownQuestionTypeError(Exception):
    pass


class EndOfInput(Exception):
    def __init__(self, selection: Any, *args: Any):
        super().__init__(*args)
        self.selection = selection


class ThemeError(AttributeError):
    pass
