import json
import os
import os.path as path
from typing import Literal

from customtkinter import CTkFont

from Modules.constants import *
from Modules.arquivos import Arquivos


__all__ = ['Configuracoes']


class Perfil:
    def __init__(self, local: str):
        self.__PERFIL_FILE = path.join(local, 'perfil.json')
        self.__verifica_dependencias()
        self.__abre_arquivo()

    def __verifica_dependencias(self):
        if not path.exists(self.__PERFIL_FILE):
            with open(self.__PERFIL_FILE, mode='w', encoding=ENCODER) as json_file:
                json.dump(PERFIL, json_file, indent=2, ensure_ascii=False)

    def __abre_arquivo(self):
        with open(self.__PERFIL_FILE, mode='r', encoding=ENCODER) as json_file:
            self.__profile_dict: dict = json.load(json_file)

    def salva_informacao_perfil(self, param, value):
        with open(file=self.__PERFIL_FILE, mode='w', encoding=ENCODER) as json_file:
            self.__profile_dict[param] = value
            json.dump(self.__profile_dict, json_file, indent=2, sort_keys=True, ensure_ascii=False)

    @property
    def configuracao_unidade_padrao(self) -> str:
        return self.__profile_dict['unidade_padrao']

    @property
    def perfil_apagar_enunciado(self) -> bool:
        return self.__profile_dict['apagar_enunciado']

    @property
    def perfil_aparencia_do_sistema(self):
        return self.__profile_dict['dark_mode']

    @property
    def perfil_escala_do_sistema(self):
        return self.__profile_dict['escala_do_sistema']


class Configuracoes:
    def __init__(self, arquivos: Arquivos):
        self.arquivos = arquivos

        self._CONFIGS_FILE = self.arquivos.BASE / 'configs/configs.json'
        self._verifica_dependencias()
        self._configuracoes_dict = self.arquivos.abre_json(self._CONFIGS_FILE)

    def _verifica_dependencias(self):
        if not self._CONFIGS_FILE.exists():
            self.arquivos.salva_json(self._CONFIGS_FILE, CONFIGURACOES)

    def salva_informacao_configuracao(self, param, value):
        self._configuracoes_dict[param] = value
        self.arquivos.salva_json(self._CONFIGS_FILE, self._configuracoes_dict)

    @property
    def _fonte_titulo(self) -> CTkFont:
        font = CTkFont(
            family=self._configuracoes_dict['fonte'],
            size=self._configuracoes_dict['tamanho_titulo'],
            weight=self._configuracoes_dict['fonte_estilo'],
            slant='roman',
            underline=False,
            overstrike=False
        )
        return font

    @property
    def _fonte_texto(self) -> CTkFont:
        font = CTkFont(
            family=self._configuracoes_dict['fonte'],
            size=self._configuracoes_dict['tamanho_texto'],
            weight=self._configuracoes_dict['fonte_estilo'],
            slant='roman',
            underline=False,
            overstrike=False
        )
        return font

    @property
    def root_configs(self) -> dict:
        return {'background': self._configuracoes_dict['cor_da_borda']}

    @property
    def frame_configs(self) -> dict:
        return {'fg_color': self._configuracoes_dict['cor_de_fundo']}

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
        return {
            'background': self._configuracoes_dict['cor_de_fundo'],
            'activebackground': self._configuracoes_dict['cor_de_fundo']
        }

    @property
    def text_configs(self) -> dict:
        return {'undo': True, 'wrap': 'word', 'autoseparators': True, 'exportselection': True, 'maxundo': 5}

    @property
    def entry_configs(self) -> dict:
        return {'font': self._fonte_texto, 'exportselection': True}

    @property
    def scrollable_label_configs(self):
        return {'label_font': self._fonte_texto}

    @property
    def tipos(self) -> list:
        tipos: list = self._configuracoes_dict['tipos']
        tipos.sort()
        return tipos

    @property
    def unidades(self) -> list:
        unidades: list = self._configuracoes_dict['unidades']
        unidades.sort()
        return unidades

    @property
    def dificuldades(self) -> list:
        return self._configuracoes_dict['dificuldades']


class Dicionario:
    def __init__(self, local: str):
        self.__CAMINHO_DICIONARIO_PESSOAL = path.join(local, 'dicionario_pessoal.json')
        self.__verifica_dependencias()
        self.__abre_arquivo()

        self.__dicionario_pessoal: list

    def __verifica_dependencias(self):
        if not path.exists(self.__CAMINHO_DICIONARIO_PESSOAL):
            with open(self.__CAMINHO_DICIONARIO_PESSOAL, mode='w', encoding=ENCODER) as json_file:
                json.dump(CONFIGURACOES, json_file, indent=2, ensure_ascii=False)

    def __abre_arquivo(self):
        with open(self.__CAMINHO_DICIONARIO_PESSOAL, mode='r', encoding=ENCODER) as json_file:
            self.__dicionario_pessoal = json.load(json_file)

    @property
    def caminho_dicionario_pessoal(self):
        return self.__CAMINHO_DICIONARIO_PESSOAL

    def add_palavra(self, nova_palavra):
        self.__dicionario_pessoal.append(nova_palavra)
        with open(self.__CAMINHO_DICIONARIO_PESSOAL, mode='w', encoding=ENCODER) as json_file:
            json.dump(self.__dicionario_pessoal, json_file, indent=2, ensure_ascii=False, sort_keys=True)


class Configs(Configuracoes, Perfil):
    def __init__(self, diretorio_base=None):
        if diretorio_base is None:
            diretorio_base = self.__get_desktop_directory()
        self.__CONFIGS_DIR = path.join(diretorio_base, 'configs')
        self._verifica_dependencias()
        self.__DICIONARIO_FILE = path.join(self.__CONFIGS_DIR, 'dicionario_pessoal.json')
        self.dicionario_pessoal = Dicionario(self.__CONFIGS_DIR)

    @staticmethod
    def __get_desktop_directory():
        home_directory = os.path.expanduser("~")
        if os.name == 'posix':  # Unix-like systems (Linux, macOS, etc.)
            return os.path.join(home_directory, 'Desktop')
        elif os.name == 'nt':  # Windows
            return os.path.join(home_directory, 'Desktop')
        else:
            raise OSError("Unsupported operating system")

    def abre_configuracoes_e_perfil(self):
        Configuracoes.__init__(self, self.__CONFIGS_DIR)
        Perfil.__init__(self, self.__CONFIGS_DIR)

    def _verifica_dependencias(self):
        if not path.exists(self.__CONFIGS_DIR):
            os.mkdir(self.__CONFIGS_DIR)

    def salva_informacao(self, tipo: Literal['configs', 'perfil'], param: str, value: any):
        types = {
            'configs': self.salva_informacao_configuracao,
            'perfil': self.salva_informacao_perfil,
        }
        types[tipo](param, value)
