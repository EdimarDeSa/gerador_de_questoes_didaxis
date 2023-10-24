from pathlib import Path
from typing import Callable
from tkinter import WORD
from os import remove

from customtkinter import CTkFont, CENTER
from .Constants import CORRETA

from .DataClasses import ConfigurationDataClass, PerfilDataClass, PersonalDictionary


class ConfigurationManager:
    def __init__(self, base_dir: Path, read_json: Callable, save_json: Callable, create_personal_dict: Callable):
        self.read_json = read_json
        self.save_json = save_json
        self.create_personal_dict = create_personal_dict

        self.configs = ConfigurationDataClass()
        self._CONFIGS_FILE = base_dir / 'configs/configs.json'
        self._check_customizations(self._CONFIGS_FILE, self.configs.__dict__)

        self.perfil = PerfilDataClass()
        self._PERFIL_FILE = base_dir / 'configs/perfil.json'
        self._check_customizations(self._PERFIL_FILE, self.perfil.__dict__)

        self._personal_dict = PersonalDictionary()
        self.PERSONAL_DICT_FILE = base_dir / 'configs/dicionario_pessoal.json'
        self.PERSONAL_DICT_SOURCE = base_dir / 'configs/lista_de_paralvras.bin'
        self._check_dictionary_customizations()

    def _check_customizations(self, path: Path, data_class: dict | list) -> None:
        if path.exists():
            data = self.read_json(path)
            if data is None:
                remove(path)
                self._check_customizations(path, data_class)
                return None
            data_class.update(data)
        else:
            self.save_json(path, data_class)

    def _check_dictionary_customizations(self) -> None:
        if not self.PERSONAL_DICT_FILE.exists():
            self.create_personal_dict(self.PERSONAL_DICT_SOURCE, self.PERSONAL_DICT_FILE)
            self._check_dictionary_customizations()
        else:
            words_list: list = self.read_json(self.PERSONAL_DICT_FILE)
            self._personal_dict.dictionary = set(words_list)
        return None

    def save_new_config(self, key: str, value: any) -> None:
        if hasattr(self.configs, key):
            self.configs.atualiza_atributo(key, value)
            self.save_json(self._CONFIGS_FILE, dict(self.configs))
        elif hasattr(self.perfil, key):
            self.perfil.atualiza_atributo(key, value)
            self.save_json(self._PERFIL_FILE, dict(self.perfil))
        elif hasattr(self._personal_dict, key):
            self._personal_dict.atualiza_atributo(value)
            self.save_json(self.PERSONAL_DICT_FILE, self._personal_dict.to_list)
        else:
            raise KeyError(f"Invalid configuration key: {key}")

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
        return dict(font=self._fonte_titulo)

    @property
    def list_configs(self) -> dict:
        return dict(font=self._fonte_texto, dynamic_resizing=False, anchor=CENTER)

    @property
    def buttons_configs(self) -> dict:
        return dict(font=self._fonte_texto)

    @property
    def bt_opcoes_configs(self) -> dict:
        return dict(font=self._fonte_texto)

    @property
    def text_configs(self) -> dict:
        return dict(undo=True, wrap=WORD, autoseparators=True, exportselection=True, maxundo=5)

    @property
    def entry_configs(self) -> dict:
        return dict(font=self._fonte_texto, exportselection=True, width=180)

    @property
    def scrollable_label_configs(self):
        return dict(label_font=self._fonte_texto)

    @property
    def tipos(self) -> list:
        tipos: list = self.configs.tipos
        tipos.sort()
        return tipos

    @property
    def categorias(self) -> list:
        unidades: list = self.configs.unidades
        unidades.sort()
        return unidades

    @property
    def dificuldades(self) -> list:
        dificuldades: list = self.configs.dificuldades
        return dificuldades

    @property
    def unidade_padrao(self) -> str:
        return self.perfil.unidade_padrao

    @unidade_padrao.setter
    def unidade_padrao(self, value) -> None:
        self.save_new_config('unidade_padrao', value)

    @property
    def apagar_enunciado(self) -> bool:
        return self.perfil.apagar_enunciado

    @apagar_enunciado.setter
    def apagar_enunciado(self, value) -> None:
        self.save_new_config('apagar_enunciado', value)

    @property
    def exportar_automaticamente(self) -> bool:
        return self.perfil.exportar_automaticamente

    @exportar_automaticamente.setter
    def exportar_automaticamente(self, value) -> None:
        self.save_new_config('exportar_automaticamente', value)

    @property
    def aparencia_do_sistema(self) -> str:
        return self.perfil.aparencia_do_sistema

    @aparencia_do_sistema.setter
    def aparencia_do_sistema(self, value) -> None:
        self.save_new_config('aparencia_do_sistema', value)

    @property
    def escala_do_sistema(self) -> str:
        return self.perfil.escala_do_sistema

    @escala_do_sistema.setter
    def escala_do_sistema(self, value) -> None:
        self.save_new_config('var_escala_do_sistema', value)

    @property
    def cor_padrao(self) -> str:
        return self.perfil.cor_padrao

    @cor_padrao.setter
    def cor_padrao(self, value) -> None:
        self.save_new_config('var_cor_padrao', value)

    def add_palavra(self, palavra: str) -> None:
        self.save_new_config('dictionary', palavra)
