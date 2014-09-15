class InquirerError(Exception):
    pass


class ValidationError(InquirerError):
    pass


class UnknownQuestionTypeError(InquirerError):
    pass


class Aborted(InquirerError):
    pass


class EndOfInput(InquirerError):
    def __init__(self, selection, *args, **kwargs):
        super(EndOfInput, self).__init__(*args, **kwargs)
        self.selection = selection
