class ModeloQuestao:
    def __init__(self, unidade: str = None, codigo: str = None, tempo: str = None, tipo: str = None,
                 dificuldade: str = None, peso: str = None, pergunta: str = None,
                 alternativas: list[tuple[str, bool]] = None, _id: int = None, ):
        """Construct a new Question"""
        self.__unidade = unidade
        self.__codigo = codigo
        self.__tempo = tempo
        self.__tipo = tipo
        self.__dificuldade = dificuldade
        self.__peso = peso
        self.__pergunta = pergunta
        self.__alternativas = alternativas
        self.__id = _id

    @property
    def unidade(self) -> str:
        return self.__unidade

    @unidade.setter
    def unidade(self, value: str):
        self.__unidade = value

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, value: str):
        self.__codigo = value

    @property
    def tempo(self) -> str:
        return self.__tempo

    @tempo.setter
    def tempo(self, value: str):
        self.__tempo = value

    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, value: str):
        self.__tipo = value

    @property
    def dificuldade(self) -> str:
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, value: str):
        self.__dificuldade = value

    @property
    def peso(self) -> str:
        return self.__peso

    @peso.setter
    def peso(self, value: str):
        self.__peso = value

    @property
    def pergunta(self) -> str:
        return self.__pergunta

    @pergunta.setter
    def pergunta(self, value: str):
        self.__pergunta = value

    @property
    def alternativas(self) -> list[tuple[str, bool]]:
        return self.__alternativas

    @alternativas.setter
    def alternativas(self, value: list[tuple[str, bool]]):
        self.__alternativas = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not self.__id:
            self.__id = value
        else:
            raise AttributeError(f'ID já existente: {self.__id}')

    def para_salvar(self) -> list[list[str]]:
        data = []
        if self.tipo == 'Dissertativa':
            data.append(self.__informacao_padrao())
        else:
            for alternativa in self.alternativas:
                data.append(self.__informacao_padrao(alternativa))
        return data

    def __informacao_padrao(self, alternativa=None) -> list[str]:
        infos = [
            '',
            self.__verifica_tipo(),
            self.peso,
            self.tempo,
            '',
            self.pergunta,
            '',
            '',
            self.unidade,
            self.codigo,
            self.dificuldade
        ]
        if alternativa is not None:
            infos[6] = alternativa[0]
            infos[7] = self.__verifica_correta(alternativa[1])
        return infos

    def __verifica_correta(self, correta: bool):
        def verdadeiro_e_falso():
            if correta:
                return 'V'
            else:
                return 'F'

        def multipla_escolha():
            if correta:
                return 'CORRETA'
            else:
                return ''

        def dissertativa():
            pass

        tipos = {
            'Multipla escolha 1 correta': multipla_escolha,
            'Multipla escolha n corretas': multipla_escolha,
            'Verdadeiro ou falso': verdadeiro_e_falso,
            'Dissertativa': dissertativa,
        }
        return tipos[self.tipo]()

    def __verifica_tipo(self) -> str:
        tipos = {
            'Multipla escolha 1 correta': 'me',
            'Multipla escolha n corretas': 'men',
            'Verdadeiro ou falso': 'vf',
            'Dissertativa': 'd',
            'me': 'Multipla escolha 1 correta',
            'men': 'Multipla escolha n corretas',
            'vf': 'Verdadeiro ou falso',
            'd': 'Dissertativa',
        }
        return tipos[self.tipo]

    def __str__(self) -> str:
        return f'Pergunta: {self.__pergunta}\n' \
               f'ID: {self.__id}'

    def __repr__(self) -> str:
        return f'<ID: {self.__id}>'
