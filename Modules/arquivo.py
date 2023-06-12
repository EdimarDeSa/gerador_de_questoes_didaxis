from tkinter.filedialog import askopenfilename, asksaveasfilename
import os.path

import pandas as pd
from customtkinter import CTkFont, CTkImage
from PIL import Image

from . import DEFAULT_EXTENSION, FILETYPES, CABECALHO
from Modules.models.questao import ModeloQuestao


class Imagens:
    def __init__(self, diretorio_base=None):
        if diretorio_base is None:
            diretorio_base = self.__get_desktop_directory()
        self.__local = diretorio_base
        self.__caminho_imagens_padrao = os.path.join(self.__local, 'icons')

    @staticmethod
    def __get_desktop_directory():
        home_directory = os.path.expanduser("~")
        if os.name == 'posix':  # Unix-like systems (Linux, macOS, etc.)
            return os.path.join(home_directory, 'Desktop')
        elif os.name == 'nt':  # Windows
            return os.path.join(home_directory, 'Desktop')
        else:
            raise OSError("Unsupported operating system")

    def __imagem(self, nome_imagem: str) -> Image:
        caminho_imagem = os.path.join(self.__caminho_imagens_padrao, nome_imagem)
        return Image.open(caminho_imagem)

    def bt_configs_img(self) -> CTkImage:
        bt_configs_img_light_mode = self.__imagem('configuracoes_light_mode.png')
        bt_configs_img_dark_mode = self.__imagem('configuracoes_dark_mode.png')
        bt_configs_img = CTkImage(bt_configs_img_light_mode, bt_configs_img_dark_mode, (24, 24))
        return bt_configs_img

    def bt_deletar_questao_img(self) -> CTkImage:
        eraser_light_mode = self.__imagem('eraser_light_mode.png')
        eraser_dark_mode = self.__imagem('eraser_dark_mode.png')
        bt_deletar_questao = CTkImage(eraser_light_mode, eraser_dark_mode, (16, 16))
        return bt_deletar_questao

    def bt_editar_questao_img(self) -> CTkImage:
        edit_light_mode = self.__imagem('edit_light_mode.png')
        edit_dark_mode = self.__imagem('edit_dark_mode.png')
        bt_editar_questao = CTkImage(edit_light_mode, edit_dark_mode, (16, 16))
        return bt_editar_questao


class Arquivos:
    def __init__(self, diretorio_base=None):
        if diretorio_base is None:
            diretorio_base = self.__get_desktop_directory()
        self.contator_id = 0
        self.__dados_da_pergunta: [pd.DataFrame or None] = None
        self.__df_para_exportar = None
        self.__df_para_exportar_criado: bool = False
        self.__local = os.path.dirname(diretorio_base)

    @staticmethod
    def __get_desktop_directory():
        home_directory = os.path.expanduser("~")
        if os.name == 'posix':  # Unix-like systems (Linux, macOS, etc.)
            return os.path.join(home_directory, 'Desktop')
        elif os.name == 'nt':  # Windows
            return os.path.join(home_directory, 'Desktop')
        else:
            raise OSError("Unsupported operating system")

    def buscar_arquivo_para_abrir(self) -> str:
        arquivo = askopenfilename(defaultextension=DEFAULT_EXTENSION, filetypes=FILETYPES, title='Abrir',
                                  initialdir=self.__get_desktop_directory())
        return arquivo

    def caminho_salvar_para_salvar(self, titulo: str):
        caminho = asksaveasfilename(confirmoverwrite=True, defaultextension=DEFAULT_EXTENSION,
                                    filetypes=FILETYPES, initialdir=self.__get_desktop_directory(), title=titulo)
        return caminho

    def carrega_banco_de_dados(self, caminho):
        df_questoes = pd.read_excel(caminho, engine='openpyxl', dtype='string')
        df_questoes.fillna(value='', inplace=True)
        df_questoes.set_axis(self.__normatiza_cabecalho(df_questoes.columns), axis='columns')

        grouped = df_questoes.groupby('PERGUNTA', dropna=False)
        questoes = []
        for pergunta, dados in grouped:
            self.__dados_da_pergunta = dados
            questao = ModeloQuestao(_id=self.__atribui_id())
            questao.unidade = self.__get_unidade
            questao.codigo = self.__get_codigo
            questao.tempo = self.__get_tempo
            questao.tipo = self.__get_tipo
            questao.dificuldade = self.__get_dificuldade
            questao.peso = self.__get_peso
            questao.pergunta = pergunta
            questao.alternativas = self.__get_alternativas_com_resposta

            questoes.append(questao)

        return questoes

    @staticmethod
    def __converte_correta_para_booleanas(correta: str) -> bool:
        return correta.upper() == 'CORRETA' or correta.upper() == 'V'

    @staticmethod
    def __normatiza_cabecalho(colunas) -> list[str]:
        return [titulo.upper() for titulo in colunas]

    @property
    def __get_unidade(self) -> str:
        unidade: str = self.__dados_da_pergunta.get('CATEGORIA', '').tolist()[0]
        return unidade.capitalize()

    @property
    def __get_codigo(self) -> str:
        return self.__dados_da_pergunta.get('SUBCATEGORIA', '').tolist()[0]

    @property
    def __get_tempo(self) -> str:
        return self.__dados_da_pergunta.get('TEMPO', '').tolist()[0]

    @property
    def __get_tipo(self) -> str:
        tipos = {
            'me': 'Multipla escolha 1 correta',
            'men': 'Multipla escolha n corretas',
            'vf': 'Verdadeiro ou falso',
            'd': 'Dissertativa',
        }
        tipo = self.__dados_da_pergunta.get('TIPO', '').tolist()
        return tipos[tipo[0]]

    @property
    def __get_dificuldade(self) -> str:
        return self.__dados_da_pergunta.get('DIFICULDADE', '').tolist()[0]

    @property
    def __get_peso(self) -> str:
        return self.__dados_da_pergunta.get('PESO', '').tolist()[0]

    @property
    def __get_alternativas_com_resposta(self) -> list[tuple[str, bool]]:
        alternativas = self.__dados_da_pergunta.get('ALTERNATIVA', '')
        corretas = self.__dados_da_pergunta.get('CORRETA', '')
        corretas_convertidas_booleanas = [self.__converte_correta_para_booleanas(correta) for correta in corretas]
        alternativas_com_resposta = list(zip(alternativas, corretas_convertidas_booleanas))
        return alternativas_com_resposta

    @staticmethod
    def __verifica_tipo(tipo: str) -> str:
        tipos = {
            'Multipla escolha 1 correta': 'me',
            'Multipla escolha n corretas': 'men',
            'Verdadeiro ou falso': 'vf',
            'Dissertativa': 'd',
            'me': 'Multipla escolha 1 correta',
            'men': 'Multipla escolha n corretas',
            'vf': 'Verdadeiro ou falso',
            'd': 'Dissertativa',
        }
        return tipos[tipo]

    def __atribui_id(self):
        self.contator_id += 1
        return self.contator_id

    @staticmethod
    def __verifica_correta(correta: bool, tipo: str):
        def verdadeiro_e_falso():
            if correta:
                return 'V'
            else:
                return 'F'

        def multipla_escolha():
            if correta:
                return 'CORRETA'
            else:
                return ''

        def dissertativa():
            pass

        tipos = {
            'Multipla escolha 1 correta': multipla_escolha,
            'Multipla escolha n corretas': multipla_escolha,
            'Verdadeiro ou falso': verdadeiro_e_falso,
            'Dissertativa': dissertativa,
        }
        return tipos[tipo]()

    @staticmethod
    def exportar(caminho: str, questoes: list[ModeloQuestao]):
        data = []
        for questao in questoes:
            data.extend(questao.para_salvar())
        df = pd.DataFrame(data, columns=CABECALHO)
        try:
            df.to_excel(caminho, index=False)
            return True
        except PermissionError:
            return False


