from typing import Optional

from icecream import ic

from .Constants import SUBCATEGORYLIST, TYPESLIST
from .DataClasses import QuestionDataClass
from .Errors import QuestionMatchError


class QuestionsManager:
    def __init__(self):
        self.__questions_db: dict[int, QuestionDataClass] = {}
        self.__lista_de_ids = list()

        self.__control: int = 0

        self._temp_question = QuestionDataClass()

    def create_new_question(self, **kwargs) -> int:
        """
        Cria uma nova questão.
                Args:
                    **kwargs (dict): Um dicionário com os parâmetros da questão. Deve conter os seguintes campos:
                        - 'id_': int, opcional
                        - 'tipo': str
                        - 'peso': str, opcional
                        - 'tempo': str, opcional
                        - 'pergunta': str
                        - 'categoria': str
                        - 'subcategoria': str, opcional
                        - 'dificuldade': str, opcional
                        - 'alternativas': list[tuple[str, bool]], opcional
                        - 'controle': int

                Returns:
                    int: O controle da nova questão criada.
        """
        internal_cntrl = self.__next_control()
        external_cntrl = kwargs.get('controle')

        kwargs['controle'] = internal_cntrl if not external_cntrl else external_cntrl

        self._temp_question.update(**kwargs)

        new_question = QuestionDataClass(**dict(self._temp_question))

        self.__questions_db[new_question.controle] = new_question
        if new_question.id_ is not None: self.__lista_de_ids.append(new_question.id_)

        return new_question.controle

    def remove_question(self, controle: int) -> None:
        self._exists_controle(controle)
        if controle in self.__questions_db:
            if self.__questions_db[controle].id_ in self.__lista_de_ids:
                self.__lista_de_ids.remove(self.__questions_db[controle].id_)
            del self.__questions_db[controle]

    def edit_question(self, **kwargs) -> None:
        controle = kwargs.get('controle')

        self._exists_controle(controle)

        question = self.__questions_db[controle]
        question.update(**kwargs)

    def get_question_data(self, controle: int) -> Optional[dict]:
        self._exists_controle(controle)

        question = self.__questions_db.get(controle)

        self._temp_question.update(**dict(question))
        return dict(self._temp_question)

    def __next_control(self) -> int:
        self.__control += 1
        return self.__control

    def serialize(self) -> list[dict]:
        return [dict(question) for question in self.__questions_db.values()]

    def _exists_pergunta(self):
        for question in self.__questions_db.values():
            if question == self._temp_question:
                return True
        return False

    def _exists_controle(self, controle):
        if controle not in self.__questions_db.keys():
            raise KeyError('Controle inexistente: %s' % controle)

    def __validate_question_data(self) -> None:
        if self._temp_question.id_ is not None:
            if any([self._temp_question.id_ < 0 or self._temp_question.id_ in self.__lista_de_ids]):
                raise ValueError(f'ID: "{self._temp_question.id_}" inválido ou já existente')

        if self._temp_question.tipo not in TYPESLIST:
            raise ValueError(f'Tipo: "{self._temp_question.tipo}" inválido')

        if not self._temp_question.peso.isdigit():
            raise ValueError(f'Peso: "{self._temp_question.peso}" inválido')

        if self._temp_question.controle in self.__questions_db:
            raise ValueError(f'Controle: "{self._temp_question.controle}" já existe')

        if self._exists_pergunta():
            raise QuestionMatchError(self._temp_question.controle)

        # if all([bool(x), _ for x in self._temp_question.alternativas]):
