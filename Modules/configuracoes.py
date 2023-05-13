import json
import os
import os.path as path
from typing import Literal

from Modules import CONFIGURACOES, PERFIL, DICIONARIO, ENCODER


class Perfil(object):
    def __init__(self, filename: str):
        self.__PERFIL_FILE = path.join(filename, 'perfil.json')
        self.__verifica_dependencias()
        self.__abre_arquivo()
        print(self.__profile_dict)

    def __verifica_dependencias(self):
        if not path.exists(self.__PERFIL_FILE):
            with open(self.__PERFIL_FILE, 'w') as json_file:
                json.dump(PERFIL, json_file, indent=2, ensure_ascii=False)

    def __abre_arquivo(self):
        with open(self.__PERFIL_FILE) as json_file:
            self.__profile_dict: dict = json.load(json_file)

    def salva_informacao_perfil(self, param, value):
        with open(file=self.__PERFIL_FILE, mode='w', encoding='utf-8') as json_file:
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
    def __init__(self, filename: str):
        self.__CONFIGS_FILE = path.join(filename, 'configs.json')
        self.__verifica_dependencias()
        self.__abre_arquivo()

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
        if not path.exists(self.__CONFIGS_FILE):
            with open(self.__CONFIGS_FILE, mode='w', encoding='utf-8') as json_file:
                json.dump(CONFIGURACOES, json_file, indent=2, ensure_ascii=False)

    def __abre_arquivo(self):
        with open(self.__CONFIGS_FILE, mode='r', encoding='utf-8') as json_file:
            self.__configuracoes_dict: dict = json.load(json_file)

    def salva_informacao_configuracao(self, param, value):
        with open(file=self.__CONFIGS_FILE, mode='w', encoding='utf-8') as json_file:
            self.__configuracoes_dict[param] = value
            json.dump(self.__configuracoes_dict, json_file, indent=2, sort_keys=True, ensure_ascii=False)

    @property
    def __root_configs(self) -> dict:
        return {'background': self.__configuracoes_dict['cor_da_borda']}

    @property
    def __frame_configs(self) -> dict:
        return {'fg_color': self.__configuracoes_dict['cor_de_fundo']}

    @property
    def __label_configs(self) -> dict:
        return {
            'font': (self.__configuracoes_dict['fonte'], self.__configuracoes_dict['tamanho_titulo'], self.__configuracoes_dict['fonte_estilo'])
        }

    @property
    def __list_configs(self) -> dict:
        return {
            'font': (self.__configuracoes_dict['fonte'], self.__configuracoes_dict['tamanho_texto'], self.__configuracoes_dict['fonte_estilo']),
            # 'exportselection': True,
            # 'state': 'readonly',
            # 'justify': 'left',
        }

    @property
    def __buttons_configs(self) -> dict:
        return {
            'font': (self.__configuracoes_dict['fonte'], self.__configuracoes_dict['tamanho_titulo']),

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
            # tabstyle='tabular'
        )

    @property
    def __entry_configs(self) -> dict:
        return dict(
            font=(self.__configuracoes_dict['fonte'], self.__configuracoes_dict['tamanho_texto'], self.__configuracoes_dict['fonte_estilo']),
            exportselection=True
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


class Configs(Configuracoes, Perfil):
    def __init__(self, diretorio_base: str):
        self.__CONFIGS_DIR = path.join(diretorio_base, 'configs')
        Configuracoes.__init__(self, self.__CONFIGS_DIR)
        self.__perfil = Perfil(self.__CONFIGS_DIR)
        self.__DICIONARIO_FILE = path.join(self.__CONFIGS_DIR, 'dicionario_pessoal.json')
        self.__verifica_dependencias()

    def __verifica_dependencias(self):
        if not path.exists(self.__CONFIGS_DIR):
            os.mkdir(self.__CONFIGS_DIR)
        
        if not path.exists(self.__DICIONARIO_FILE):
            with open(self.__DICIONARIO_FILE, 'w') as json_file:
                json.dump(DICIONARIO, json_file, indent=2)

    def salva_informacao(self, type_: Literal['configs', 'perfil'], param: str, value: any):
        types = {
            'configs': self.salva_informacao_configuracao,
            'perfil': self.salva_informacao_perfil,
        }
        types[type_](param, value)
