class ExceptionBaseClass(Exception):
    def __init__(self, message: str):
        self.message = message


class QuestionMatchError(Exception):
    def __init__(self, pergunta: str, controle: int):
        self.message = f'Question "<{pergunta}>" already exists in control "<{controle}>"'


class BrokenFileError(ExceptionBaseClass):
    ...
