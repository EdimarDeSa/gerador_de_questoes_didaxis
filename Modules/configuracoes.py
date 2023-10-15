import json
import os
import os.path as path
from typing import Literal

from customtkinter import CTkFont

from Modules.constants import *
from Modules.arquivos import Arquivos


__all__ = ['Configuracoes']


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
