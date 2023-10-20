from Modules.data_classes import ModeloQuestao


class QuestionsManager:
    def __init__(self):
        self._dict_de_questoes: dict[int, ModeloQuestao] = {}
        self._control: int = 0
        self._intermediate_question: ModeloQuestao(None, None, None, None, None, None, None, None, None)

    def create_new_question(self, tipo: str = None, peso: str = None, tempo: str = None, pergunta: str = None,
                            categoria: str = None, subcategoria: str = None, dificuldade: str = None,
                            alternativas: list[tuple[str, bool]] = None, serial_dict: dict = None) -> int:
        if serial_dict is not None:
            new_question = ModeloQuestao(**serial_dict)
        else:
            new_question = ModeloQuestao(tipo=tipo, peso=peso, tempo=tempo, pergunta=pergunta, categoria=categoria,
                                         subcategoria=subcategoria, alternativas=alternativas, dificuldade=dificuldade)

        new_question.controle = self.__next_id()
        self._dict_de_questoes[new_question.controle] = new_question
        return new_question.controle

    def remove_question(self, controle: int):
        if controle in self._dict_de_questoes:
            del self._dict_de_questoes[controle]
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

    def get_question(self, controle: int):
        question = self._dict_de_questoes.get(controle, None)
        return question.__dict__.copy()

    def __next_id(self) -> int:
        self._control += 1
        return self._control

    def serialize(self) -> list[dict]:
        return [question.__dict__ for question in self._dict_de_questoes.values()]
