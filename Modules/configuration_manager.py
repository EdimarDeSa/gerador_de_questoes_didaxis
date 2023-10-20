from pathlib import Path
from typing import Literal

from customtkinter import CTkFont

from .arquivos import Arquivos
from .data_classes import Configuracoes, Perfil, PersonalDictionary
from .funcoes import FileSerializer
from .constants import WORD


class ConfigurationManager:
    def __init__(self, arquivos: Arquivos):
        self.arquivos = arquivos

        self.configs = Configuracoes()
        self._CONFIGS_FILE = self.arquivos.base_dir / 'configs/configs.json'
        self._check_customizations(self._CONFIGS_FILE, self.configs.__dict__)

        self.perfil = Perfil()
        self._PERFIL_FILE = self.arquivos.base_dir / 'configs/perfil.json'
        self._check_customizations(self._PERFIL_FILE, self.perfil.__dict__)

        self._dicionario_pessoal = PersonalDictionary()
        self.PERSONAL_DICT_FILE = self.arquivos.base_dir / 'configs/dicionario_pessoal.json'
        self._check_dictionary_customizations()

    @staticmethod
    def _check_customizations(path: Path, data_class: dict | list):
        if path.exists():
            data = FileSerializer.open_json(path)
            if data is None:
                ConfigurationManager._check_customizations(path, data_class)
                return
            data_class.update(data)
        else:
            FileSerializer.save_json(path, data_class)

    def _check_dictionary_customizations(self) -> None:
        if not self.PERSONAL_DICT_FILE.exists():
            self.arquivos.cria_dicionario_pessoal(self.PERSONAL_DICT_FILE)
            self._check_dictionary_customizations()
        else:
            words_list: list = FileSerializer.open_json(self.PERSONAL_DICT_FILE)
            self._dicionario_pessoal.dictionary = set(words_list)
        return None

    def save_new_config(self, key: str, value: any) -> bool:
        if key in self.configs.__dict__.keys():
            self.configs.atualiza_atributo(path=self._CONFIGS_FILE, key=key, value=value)
        elif key in self.perfil.__dict__.keys():
            self.perfil.atualiza_atributo(path=self._PERFIL_FILE, key=key, value=value)
        else:
            return False
        return True

    @property
    def _fonte_titulo(self) -> CTkFont:
        font = CTkFont(
            family=self.configs.fonte,
            size=self.configs.tamanho_titulo,
            weight=self.configs.fonte_estilo,
            slant='roman',
            underline=False,
            overstrike=False
        )
        return font

    @property
    def _fonte_texto(self) -> CTkFont:
        font = CTkFont(
            family=self.configs.fonte,
            size=self.configs.tamanho_texto,
            weight=self.configs.fonte_estilo,
            slant='roman',
            underline=False,
            overstrike=False
        )
        return font

    @property
    def label_titulos_configs(self) -> dict:
        return {'font': self._fonte_titulo}

    @property
    def list_configs(self) -> dict:
        return {'font': self._fonte_texto}

    @property
    def buttons_configs(self) -> dict:
        return {'font': self._fonte_texto}

    @property
    def bt_opcoes_configs(self) -> dict:
        return {'font': self._fonte_texto}

    @property
    def text_configs(self) -> dict:
        return {
            'undo': True,
            'wrap': WORD,
            'autoseparators': True,
            'exportselection': True,
            'maxundo': 5
        }

    @property
    def entry_configs(self) -> dict:
        return {
            'font': self._fonte_texto,
            'exportselection': True
        }

    @property
    def scrollable_label_configs(self):
        return {'label_font': self._fonte_texto}

    @property
    def tipos(self) -> list:
        tipos: list = self.configs.tipos
        tipos.sort()
        return tipos

    @property
    def unidades(self) -> list:
        unidades: list = self.configs.unidades
        unidades.sort()
        return unidades

    @property
    def dificuldades(self) -> list:
        dificuldades: list = self.configs.dificuldades
        dificuldades.sort()
        return dificuldades

    @property
    def unidade_padrao(self) -> str:
        return self.perfil.unidade_padrao

    @unidade_padrao.setter
    def unidade_padrao(self, value) -> None:
        self.perfil.atualiza_atributo(path=self._PERFIL_FILE, key='unidade_padrao', value=value)

    @property
    def apagar_enunciado(self) -> bool:
        return self.perfil.apagar_enunciado

    @apagar_enunciado.setter
    def apagar_enunciado(self, value) -> None:
        self.perfil.atualiza_atributo(path=self._PERFIL_FILE, key='apagar_enunciado', value=value)

    @property
    def aparencia_do_sistema(self) -> Literal['system', 'dark', 'light']:
        return self.perfil.aparencia_do_sistema

    @aparencia_do_sistema.setter
    def aparencia_do_sistema(self, value) -> None:
        self.perfil.atualiza_atributo(path=self._PERFIL_FILE, key='aparencia_do_sistema', value=value)

    @property
    def escala_do_sistema(self) -> str:
        return self.perfil.escala_do_sistema

    @escala_do_sistema.setter
    def escala_do_sistema(self, value) -> None:
        self.perfil.atualiza_atributo(path=self._PERFIL_FILE, key='escala_do_sistema', value=value)

    @property
    def cor_padrao(self) -> str:
        return self.perfil.cor_padrao

    @cor_padrao.setter
    def cor_padrao(self, value) -> None:
        self.perfil.atualiza_atributo(path=self._PERFIL_FILE, key='cor_padrao', value=value)
