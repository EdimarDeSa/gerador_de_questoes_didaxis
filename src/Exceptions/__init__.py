class ExceptionBaseClass(Exception):
    def __init__(self, message: str):
        self.message = message


class QuestionMatchError(Exception):
    def __init__(self, controle: int):
        self.message = f'A questão "<{controle}>" tem a mesma pergunta!'


class BrokenFileError(Exception):
    def __init__(self, message: str = None):
        self.message = message


class QuestionValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
