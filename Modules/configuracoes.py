import json
import os
import os.path as path
from typing import Literal

from customtkinter import CTkFont
import pandas as pd

from . import CONFIGURACOES, PERFIL, ENCODER


class Perfil(object):
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


class Configuracoes(object):
    def __init__(self, local: str):
        self.__CONFIGS_FILE = path.join(local, 'configs.json')
        self.__verifica_dependencias()
        self.__abre_arquivo()

        self.root_configs: dict = self.__root_configs
        self.frame_configs: dict = self.__frame_configs
        # self.label: dict = self.__label_configs
        self.list_configs: dict = self.__list_configs
        self.buttons_configs: dict = self.__buttons_configs
        self.bt_opcoes_configs: dict = self.__bt_opcoes_configs
        self.label_configs: dict = self.__label_configs
        self.scrollable_label_configs: dict = self.__scrollable_label_configs
        self.text_configs: dict = self.__text_configs
        self.entry_configs: dict = self.__entry_configs

    def __verifica_dependencias(self):
        if not path.exists(self.__CONFIGS_FILE):
            with open(self.__CONFIGS_FILE, mode='w', encoding=ENCODER) as json_file:
                json.dump(CONFIGURACOES, json_file, indent=2, ensure_ascii=False)

    def __abre_arquivo(self):
        with open(self.__CONFIGS_FILE, mode='r', encoding=ENCODER) as json_file:
            self.__configuracoes_dict: dict = json.load(json_file)

    def salva_informacao_configuracao(self, param, value):
        with open(file=self.__CONFIGS_FILE, mode='w', encoding=ENCODER) as json_file:
            self.__configuracoes_dict[param] = value
            json.dump(self.__configuracoes_dict, json_file, indent=2, sort_keys=True, ensure_ascii=False)

    @property
    def __fonte_titulo(self):
        return CTkFont(
            family=self.__configuracoes_dict['fonte'],
            size=self.__configuracoes_dict['tamanho_titulo'],
            weight=self.__configuracoes_dict['fonte_estilo'],
            slant='roman',
            underline=False,
            overstrike=False
        )

    @property
    def __fonte_texto(self):
        return CTkFont(
            family=self.__configuracoes_dict['fonte'],
            size=self.__configuracoes_dict['tamanho_texto'],
            weight=self.__configuracoes_dict['fonte_estilo'],
            slant='roman',
            underline=False,
            overstrike=False
        )

    @property
    def __root_configs(self) -> dict:
        return {'background': self.__configuracoes_dict['cor_da_borda']}

    @property
    def __frame_configs(self) -> dict:
        return {'fg_color': self.__configuracoes_dict['cor_de_fundo']}

    @property
    def __label_configs(self) -> dict:
        return {
            'font': self.__fonte_titulo
        }

    @property
    def __list_configs(self) -> dict:
        return {
            'font': self.__fonte_texto,
        }

    @property
    def __buttons_configs(self) -> dict:
        return {
            'font': self.__fonte_texto,
        }

    @property
    def __bt_opcoes_configs(self) -> dict:
        return {
            'background': self.__configuracoes_dict['cor_de_fundo'],
            'activebackground': self.__configuracoes_dict['cor_de_fundo']
        }

    @property
    def __text_configs(self) -> dict:
        return dict(
            undo=True, wrap='word',
            autoseparators=True,
            exportselection=True,
            maxundo=5,
        )

    @property
    def __entry_configs(self) -> dict:
        return dict(
            font=self.__fonte_texto,
            exportselection=True
        )

    @property
    def __scrollable_label_configs(self):
        return dict(
            label_font=self.__fonte_texto
        )

    @property
    def tipos(self) -> list:
        tipos: list = self.__configuracoes_dict['tipos']
        tipos.sort()
        return tipos

    @property
    def unidades(self) -> list:
        unidades: list = self.__configuracoes_dict['unidades']
        unidades.sort()
        return unidades

    @property
    def dificuldades(self) -> list:
        return self.__configuracoes_dict['dificuldades']


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
        self.__verifica_dependencias()
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

    def __verifica_dependencias(self):
        if not path.exists(self.__CONFIGS_DIR):
            os.mkdir(self.__CONFIGS_DIR)

    def salva_informacao(self, tipo: Literal['configs', 'perfil'], param: str, value: any):
        types = {
            'configs': self.salva_informacao_configuracao,
            'perfil': self.salva_informacao_perfil,
        }
        types[tipo](param, value)
