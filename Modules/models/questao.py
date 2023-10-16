from Modules.constants import *


class ModeloQuestao:
    def __init__(self, unidade: str, codigo: str, tempo: str, tipo: str, dificuldade: str, peso: str, pergunta: str,
                 alternativas: list[tuple[str, bool]], _id=None):
        self.unidade = unidade
        self.codigo = codigo
        self.tempo = tempo
        self.tipo = tipo
        self.dificuldade = dificuldade
        self.peso = peso
        self.pergunta = pergunta
        self.alternativas = alternativas
        self.id = _id

    def para_salvar(self):
        data = [self._informacao_padrao()]
        if self.tipo != D:
            data.extend(self._informacao_padrao(alternativa) for alternativa in self.alternativas)
        return data

    def _informacao_padrao(self, alternativa: tuple[str, bool] = None):
        infos = [
            None,
            self._verifica_tipo(),
            self.peso,
            self.tempo,
            None,
            self.pergunta,
            None,
            None,
            self.unidade,
            self.codigo,
            self.dificuldade,
        ]
        if alternativa is not None:
            infos[6] = alternativa[0]
            infos[7] = self._verifica_correta(alternativa[1])
        return infos

    def _verifica_correta(self, correta: bool) -> [str, None]:
        tipos = {
            ME: (CORRETA, None),
            MEN: (CORRETA, None),
            VF: (V, F),
            D: (None, None),
        }
        return tipos[self.tipo][int(correta)]

    def _verifica_tipo(self):
        tipos = {
            ME: 'me',
            MEN: 'men',
            VF: 'vf',
            D: 'd',
        }
        return tipos.get(self.tipo, self.tipo)

    def __str__(self):
        return f'Pergunta: {self.pergunta}\nID: {self.id}'

    def __repr__(self):
        return f'<ID: {self.id}>'

    def __bool__(self):
        return True
