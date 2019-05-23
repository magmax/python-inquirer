class InquirerError(Exception):
    pass


class ValidationError(InquirerError):
    def __init__(self, value, reason=None, *args):
        super(ValidationError, self).__init__(*args)
        self.value = value
        self.reason = reason


class UnknownQuestionTypeError(InquirerError):
    pass


class Aborted(InquirerError):
    pass


class EndOfInput(InquirerError):
    def __init__(self, selection, *args):
        super(EndOfInput, self).__init__(*args)
        self.selection = selection


class ThemeError(AttributeError):
    pass
