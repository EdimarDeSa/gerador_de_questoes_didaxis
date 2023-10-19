from ..constants import *
from .questao import ModeloQuestao


class ListaDeQuestoes:
    def __init__(self):
        self._dict_de_questoes: dict[int, ModeloQuestao] = {}
        self._control: int = 0
        self._intermediate_question: ModeloQuestao(None, None, None, None, None, None, None, None, None)

    def add_question(
            self, id: int = None, tipo: str = None, peso: str = None, tempo: str = None, controle: str = None,
            pergunta: str = None, categoria: str = None, subcategoria: str = None, dificuldade: str = None,
            alternativas: list[tuple[str, bool]] = None, serial_dict: dict = None
    ) -> int:
        if serial_dict is not None:
            new_question = ModeloQuestao(**serial_dict)
        else:
            new_question = ModeloQuestao(
                id=id, tipo=tipo, peso=peso, tempo=tempo, controle=controle, pergunta=pergunta, categoria=categoria,
                subcategoria=subcategoria, dificuldade=dificuldade, alternativas=alternativas
            )

        new_question.controle = self.__next_id()
        self._dict_de_questoes[new_question.controle] = new_question
        return new_question.controle

    def remove_question(self, *, question_id: int):
        if question_id in self._dict_de_questoes:
            del self._dict_de_questoes[question_id]
            return True
        return False

    def edit_question(
            self, question_id: int, unidade: str = None, codigo: str = None, tempo: str = None,
            tipo: str = None, dificuldade: str = None, peso: str = None, pergunta: str = None,
            alternativas: list[tuple[str, bool]] = None
    ) -> bool:
        if question_id not in self._dict_de_questoes: return False

        question = self._dict_de_questoes[question_id]
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

    def get_question(self, question_id: int):
        question = self._dict_de_questoes.get(question_id, None)
        return question.__dict__

    def __next_id(self) -> int:
        self._control += 1
        return self._control

    def serialize(self) -> list[dict]:
        return [question.__dict__ for question in self._dict_de_questoes.values()]
