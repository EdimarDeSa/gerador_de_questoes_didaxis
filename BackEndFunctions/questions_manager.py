from typing import Optional
from copy import deepcopy

from BackEndFunctions.DataClasses import QuestionDataClass
from BackEndFunctions.Errors import QuestionMatchError


class QuestionsManager:
    def __init__(self):
        self.__question_db: dict[int, QuestionDataClass] = {}

        self.__control: int = 0

        self._temp_question = QuestionDataClass()

    def create_new_question(self, tipo: str = None, peso: str = None, tempo: str = None, pergunta: str = None,
                            categoria: str = None, subcategoria: str = None, dificuldade: str = None,
                            alternativas: list[tuple[str, bool]] = None, serial_dict: dict = None) -> int:
        self._temp_question.pergunta = pergunta
        self._exists_pergunta()

        controle = self.__next_control()

        if serial_dict is not None:
            new_question = QuestionDataClass(controle=controle, **serial_dict)
        else:
            new_question = QuestionDataClass(
                tipo=tipo, peso=peso, tempo=tempo, pergunta=pergunta, categoria=categoria, controle=controle,
                subcategoria=subcategoria, alternativas=alternativas, dificuldade=dificuldade
            )
        self.__question_db[controle] = new_question
        return controle

    def remove_question(self, controle: int) -> bool:
        self._exists_controle(controle)
        if controle in self.__question_db:
            del self.__question_db[controle]
            return True

    def edit_question(
            self, controle: int, unidade: str = None, codigo: str = None, tempo: str = None,
            tipo: str = None, dificuldade: str = None, peso: str = None, pergunta: str = None,
            alternativas: list[tuple[str, bool]] = None
    ) -> bool:
        self._exists_controle(controle)

        question = self.__question_db[controle]
        if unidade is not None:
            question.categoria = unidade
        if codigo is not None:
            question.subcategoria = codigo
        if tempo is not None:
            question.tempo = tempo
        if tipo is not None:
            question.tipo = tipo
        if dificuldade is not None:
            question.dificuldade = dificuldade
        if peso is not None:
            question.peso = peso
        if pergunta is not None:
            question.pergunta = pergunta
        if alternativas is not None:
            question.alternativas = alternativas
        return True

    def get_question_data(self, controle: int) -> Optional[dict]:
        self._exists_controle(controle)
        question = self.__question_db.get(controle)
        if question is None: return None
        dict(self._temp_question).update(dict(question))
        return dict(self._temp_question).copy()

    def __next_control(self) -> int:
        self.__control += 1
        return self.__control

    def serialize(self) -> list[dict]:
        return [dict(question) for question in self.__question_db.values()]

    def _exists_pergunta(self):
        for question in self.__question_db.values():
            if question == self._temp_question:
                raise QuestionMatchError(question.pergunta, question.controle)

    def _exists_controle(self, controle):
        if controle not in self.__question_db.keys():
            raise KeyError('Unknown controle: %s' % controle)
