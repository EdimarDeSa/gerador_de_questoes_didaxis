from pathlib import Path
import json
import pickle
import tempfile

from Modules.constants import *


__all__ = ['Arquivos']


class Arquivos:
    def __init__(self):
        self.BASE = Path(__file__).resolve().parent.parent

        self.exportado = False

        self._temp_dir = tempfile.gettempdir()

    @staticmethod
    def salva_json(path: Path, data: [dict, list]):
        with open(path, mode='w', encoding=ENCODER) as json_file:
            json.dump(data, json_file, sort_keys=True)

    @staticmethod
    def abre_json(path: Path) -> dict:
        with open(path, encoding=ENCODER) as json_file:
            return json.load(json_file)

    @staticmethod
    def abre_bin(path: Path) -> str:
        with open(path, 'rb') as bin_file:
            list_palavras = pickle.load(bin_file)
        del bin_file
        return list_palavras

    def cria_dicionario_pessoal(self, path: Path):
        self.salva_json(path, self.abre_bin(self.BASE / './configs/lista_de_paralvras.bin').split())
