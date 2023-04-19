import json
import os
import os.path as path
from typing import Literal

from . import CONFIGURACOES, PERFIL, DICIONARIO


class Configs:
    __configs = None
    __perfil = None

    def __init__(self, CONFIGS_DIR: str, CONFIGS_FILE: str, PERFIL_FILE: str, DICIONARIO_FILE: str):
        self.__CONFIGS_DIR = CONFIGS_DIR
        self.__CONFIGS_FILE = CONFIGS_FILE
        self.__PERFIL_FILE = PERFIL_FILE
        self.__DICIONARIO_FILE = DICIONARIO_FILE
        
        self.__verifica_dependencias()
        self.__abre_configs()

        self.root_configs: dict = self.__root_configs
        self.frame_configs: dict = self.__frame_configs
        self.label: dict = self.__label_configs
        self.list_configs: dict = self.__list_configs
        self.buttons_configs: dict = self.__buttons_configs
        self.bt_opcoes_configs: dict = self.__bt_opcoes_configs
        self.label_configs: dict = self.__label_configs
        self.text_configs: dict = self.__text_configs
        self.entry_configs: dict = self.__entry_configs

    def __verifica_dependencias(self):
        if not path.exists(self.__CONFIGS_DIR):
            os.mkdir(self.__CONFIGS_DIR)
        
        if not path.exists(self.__CONFIGS_FILE):
            with open(self.__CONFIGS_FILE, 'w') as json_file:
                json.dump(CONFIGURACOES, json_file, indent=2)
        else:
            with open(self.__CONFIGS_FILE, 'r+') as json_file:
                dicionario: dict = json.load(json_file)
                for key, value in CONFIGURACOES.items():
                    if key not in dicionario.keys():
                        self.salva_informacao('configs', key, value)
        
        if not path.exists(self.__PERFIL_FILE):
            with open(self.__PERFIL_FILE, 'w') as json_file:
                json.dump(PERFIL, json_file, indent=2)
        
        if not path.exists(self.__DICIONARIO_FILE):
            with open(self.__DICIONARIO_FILE, 'w') as json_file:
                json.dump(DICIONARIO, json_file, indent=2)

    def __abre_configs(self):
        with open(self.__CONFIGS_FILE) as json_file:
            self.__configs: dict = json.load(json_file)

        with open(self.__PERFIL_FILE) as json_file:
            self.__perfil: dict = json.load(json_file)

    def salva_informacao(self, type_: Literal['configs', 'perfil'], param: str, value: any):
        """Save the configuration in the json file

        Args:
            type_ (Literal[configs, perfil]): Select the configuration type
            param (str): Name of the parameter
            value (any): Value of the parameter
        """
        types = {
            'configs': {'caminho': self.__CONFIGS_FILE, 'dicionario': self.__configs},
            'perfil': {'caminho': self.__PERFIL_FILE, 'dicionario': self.__perfil}
        }
        caminho, dicionario = types[type_].values()
        with open(file=caminho, mode='r+', encoding='UTF-8') as json_file:
            dicionario[param] = value
            json.dump(dicionario, json_file, indent=2, sort_keys=True)

    @property
    def __root_configs(self) -> dict:
        return {'background': self.__configs['cor_da_borda']}

    @property
    def __frame_configs(self) -> dict:
        return {'background': self.__configs['cor_de_fundo']}

    @property
    def __label_configs(self) -> dict:
        return {
            'background': self.__configs['cor_de_fundo'],
            'font': (self.__configs['fonte'], self.__configs['tamanho_titulo'], self.__configs['fonte_estilo'])
        }

    @property
    def __list_configs(self) -> dict:
        return {
            'font': (self.__configs['fonte'], self.__configs['tamanho_texto'], self.__configs['fonte_estilo']),
            'exportselection': True,
            'state': 'readonly',
            'justify': 'left',
        }

    @property
    def __buttons_configs(self) -> dict:
        return {
            'relief': 'raised',
            'background': 'lightgray',
            'compound': 'center',
            'activebackground': self.__configs['cor_de_fundo'],
            'anchor': 'center',
            'underline': 0
        }

    @property
    def __bt_opcoes_configs(self) -> dict:
        return {
            'background': self.__configs['cor_de_fundo'],
            'activebackground': self.__configs['cor_de_fundo']
        }

    @property
    def __text_configs(self) -> dict:
        return dict(
            undo=True, wrap='word',
            autoseparators=True,
            exportselection=True,
            maxundo=5,
            tabstyle='tabular'
        )

    @property
    def __entry_configs(self) -> dict:
        return dict(
            font=(self.__configs['fonte'], self.__configs['tamanho_texto'], self.__configs['fonte_estilo']),
            exportselection=True
        )

    @property
    def tipos(self) -> list:
        return self.__configs['tipos']

    @property
    def unidades(self) -> list:
        unidades: list = self.__configs['unidades']
        unidades.sort()
        return unidades

    @property
    def dificuldades(self) -> list:
        return self.__configs['dificuldades']

    @property
    def versao(self) -> str:
        return self.__configs['Versão']

    @property
    def configuracao_unidade_padrao(self) -> str:
        return self.__perfil['unidade_padrao']

    @property
    def configuracao_apagar_enunciado(self) -> bool:
        return self.__perfil['apagar_enunciado']
