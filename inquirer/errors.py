class InquirerError(Exception):
    pass


class ValidationError(InquirerError):
    pass


class UnknownQuestionTypeError(InquirerError):
    pass
