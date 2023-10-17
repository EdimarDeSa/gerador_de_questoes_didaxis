from pathlib import Path
import json
import pickle
import tempfile

import pandas as pd

from Modules.constants import *
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showwarning
from Modules.models.questao import ModeloQuestao


class Arquivos:
    def __init__(self):
        self.BASE = Path(__file__).resolve().parent.parent

        self._temp_dir = tempfile.gettempdir()

    @staticmethod
    def salva_json(path: Path, data: [dict, list]):
        with open(path, mode=W, encoding=ENCODER) as json_file:
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

    def caminho_para_salvar(self, titulo):
        caminho = asksaveasfilename(
            confirmoverwrite=ON, defaultextension=DEFAULT_EXTENSION, filetypes=FILETYPES, initialdir=self.BASE,
            title=titulo, initialfile='novo_banco'
        )
        return Path(caminho).resolve()

    @staticmethod
    def exportar(caminho: Path, lista_de_questoes: list[ModeloQuestao]):
        lista_questoes = []
        for questao in lista_de_questoes:
            lista_questoes.extend(questao.para_salvar())
        df_questoes = pd.DataFrame(lista_questoes, columns=COLUNAS_PADRAO, dtype='string')

        try:
            df_questoes.to_excel(caminho, engine='openpyxl', sheet_name='questoes', index=OFF)
        except PermissionError as err:
            showwarning(
                'PermissionError',
                'Não foi possível salvar o arquivo pois você não tem permissão.\n'
                'Verifique se o arquivo não está aberto antes de continuar.\n'
                f'Código: {err}'
            )
            return False
        except FileExistsError as err:
            showwarning(
                'FileExistsError',
                f'Código: {err}'
            )
            return False
        except Exception as err:
            showwarning(
                'Exception',
                f'Código: {err}'
            )
            return False

        df_questoes.truncate()

        del df_questoes
        return True
