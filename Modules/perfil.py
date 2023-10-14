from Modules.arquivos import Arquivos
from Modules.constants import *


__all__ = ['Perfil']


class Perfil:
    def __init__(self, arquivos: Arquivos):
        self.arquivos = arquivos

        self._PERFIL_FILE = self.arquivos.BASE / 'configs/perfil.json'
        self.CAMINHO_DICIONARIO_PESSOAL = self.arquivos.BASE / 'configs/dicionario_pessoal.json'
        self._verifica_dependencias()
        self._profile_dict = self.arquivos.abre_json(self._PERFIL_FILE)
        self.dicionario_pessoal = self.arquivos.abre_json(self.CAMINHO_DICIONARIO_PESSOAL)

    def salva_informacao_perfil(self, param, value):
        self._profile_dict[param] = value
        self.arquivos.salva_json(self._PERFIL_FILE, self._profile_dict)

    def _verifica_dependencias(self):
        if not self._PERFIL_FILE.exists():
            self.arquivos.salva_json(self._PERFIL_FILE, PERFIL)

        if not self.CAMINHO_DICIONARIO_PESSOAL.exists():
            self.arquivos.cria_dicionario_pessoal(self.CAMINHO_DICIONARIO_PESSOAL)

    @property
    def configuracao_unidade_padrao(self) -> str:
        return self._profile_dict['unidade_padrao']

    @property
    def apagar_enunciado(self) -> bool:
        return self._profile_dict['apagar_enunciado']

    @property
    def aparencia_do_sistema(self) -> str:
        return self._profile_dict['dark_mode']

    @property
    def escala_do_sistema(self) -> str:
        return self._profile_dict['escala_do_sistema']

    @property
    def cor_padrao(self) -> str:
        return self._profile_dict['cor_padrao']
